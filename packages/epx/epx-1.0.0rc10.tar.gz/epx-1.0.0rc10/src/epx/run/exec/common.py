"""Structures used by all run execution strategies."""

from datetime import date, datetime
from pathlib import Path
from typing import Protocol, Optional, Union, Literal, List

from pydantic import BaseModel, Field, ConfigDict

from epx.random import random_seed
from epx.synthpop import SynthPop, SynthPopModel


class FREDArg(BaseModel):
    """A FRED command line argument/ value pair.

    Attributes
    ----------
    flag : str
        The command line flag to pass to FRED, e.g. ``-p``.
    value : str
        The value corresponding to the command line flag, e.g.
        ``my-model/main.fred``.
    """

    flag: str
    value: str


class RunRequest(BaseModel):
    """Configuration for an individual run to be executed.

    Attributes
    ----------
    working_dir : str
        Working directory that FRED should be called from. This ensures
        that e.g relative paths within the model code are resolved correctly.
    size : str
        Name of instance size to use for the run.
    fred_version : str
        Version of FRED to use for the run.
    population : SynthPopModel
        The specific locations within a synthetic population that should be
        used for the simulation.
    fred_args : list[FREDArg]
        Command line arguments to be passed to FRED.
    """

    model_config = ConfigDict(populate_by_name=True)

    job_name: str = Field(alias="jobName")
    working_dir: str = Field(alias="workingDir")
    size: str
    fred_version: str = Field(alias="fredVersion")
    population: Optional[SynthPopModel] = None
    fred_args: list[FREDArg] = Field(alias="fredArgs")


class RunError(BaseModel):
    """A run configuration error in FRED Cloud responses.

    Attributes
    ----------
    key : str
        The general category of the error reported by FRED Cloud API, e.g.
        ``size`` for errors related to instance size, or ``fredVersion`` if the
        specified FRED version is not recognized.
    error : str
        Detailed description of the error.
    """

    key: str
    error: str


class RunResponse(BaseModel):
    """Response object from the /runs endpoint for an individual run.

    Attributes
    ----------
    run_id : int
        Unique ID for the run.
    status : Literal["Submitted", "Failed"]
        Textual description of the status of the run.
    errors : list[RunError], optional
        List of any errors in the run configuration identified by the API
    run_request : _RunRequestPayload
        A copy of the originating request object that the response relates to.
    """

    model_config = ConfigDict(populate_by_name=True)

    run_id: int = Field(alias="runId")
    job_id: int = Field(alias="jobId")
    status: Literal["Submitted", "Failed"]
    errors: Optional[list[RunError]] = None
    run_request: RunRequest = Field(alias="runRequest")


class RunParameters:
    """Parameters to configure a run.

    Notes
    -----
    In a future version of the client, we plan to support ``program`` being
    specified with type ``Union[Path, list[Path], str, list[str]]``. This will
    make it possible for users to avoid specifying a single entrypoint file
    and instead provide an ordered list of ``.fred`` model files to include.

    Parameters
    ----------
    program : Union[Path, str]
        FRED entrypoint filename.
    synth_pop : SynthPop
        Synthetic population to use for the run.
    start_date : Union[date, str], optional
        Simulation start date. If a ``str`` is given, should be in ISO 8601
        format, i.e. ``YYYY-MM-DD``.
    end_date : Union[date, str], optional
        Simulation end date. If a ``str`` is given, should be in ISO 8601
        format, i.e. ``YYYY-MM-DD``.
    model_params : dict[str, Union[float, str]], optional
        Dictionary where the keys are model variable names and the values are
        the corresponding numeric or string values.
    seed : int, optional
        Random number seed for the run. If ``None``, a random seed will be
        generated.
    compile_only : bool, optional
        If ``True``, compile the FRED model, but do not run it. Defaults to
        ``False``.

    Attributes
    ----------
    program : Path
        FRED entrypoint filename.
    synth_pop : SynthPop
        Synthetic population to use for the run.
    start_date : date
        Simulation start date.
    end_date : date
        Simulation end date.
    model_params : dict[str, Union[float, str]], optional
        Dictionary where the keys are model variable names and the values are
        the corresponding numeric or string values.
    seed : int
        Random number seed for the run.
    compile_only : bool
        If ``True``, compile the FRED model, but do not run it. Defaults to
        ``False``.
    """

    def __init__(
        self,
        program: Union[Path, str],
        synth_pop: Optional[SynthPop] = None,
        start_date: Optional[Union[date, str]] = None,
        end_date: Optional[Union[date, str]] = None,
        model_params: Optional[dict[str, Union[float, str]]] = None,
        seed: Optional[int] = None,
        compile_only: bool = False,
    ):
        self.program = Path(program)
        self.synth_pop = synth_pop
        self.start_date = self._normalize_date(start_date) if start_date else None
        self.end_date = self._normalize_date(end_date) if end_date else None
        self.model_params = model_params
        self.seed: int = seed if seed is not None else random_seed()
        self.compile_only = compile_only

    @staticmethod
    def _normalize_date(d: Union[date, str]) -> date:
        if isinstance(d, date):
            return d
        elif isinstance(d, str):
            return datetime.strptime(d, r"%Y-%m-%d").date()
        else:
            raise TypeError(f"Date format not recognized: {d}")

    def __repr__(self) -> str:
        return (
            f"RunParameters("
            f"program={self.program}, "
            f"synth_pop={self.synth_pop}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date}, "
            f"model_params={self.model_params}, "
            f"seed={self.seed}, "
            f"compile_only={self.compile_only}"
            f")"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, RunParameters):
            return False
        if (
            (self.program == other.program)
            and (self.synth_pop == other.synth_pop)
            and (self.start_date == other.start_date)
            and (self.end_date == other.end_date)
            and (self.model_params == other.model_params)
            and (self.seed == other.seed)
            and (self.compile_only == other.compile_only)
        ):
            return True
        return False


class RunParametersModel(BaseModel):
    """Data model facilitating JSON serialization of ``RunParameters`` objects.

    The reason for having both a Pydantic model (this class) and a vanilla
    Python class (``RunParameters``) is that Pydantic models' constructors
    require arguments to be passed as keywords, and their method signatures
    (i.e. those exposed by the builtin ``help`` function) do not explicitly show
    required arguments and types. ``RunParameters`` is part of the public API,
    and these limitations would make Pydantic models awkward for users to
    interact with.
    """

    program: Union[Path, str]
    synth_pop: Optional[SynthPopModel] = None
    start_date: Optional[Union[date, str]]
    end_date: Optional[Union[date, str]]
    sim_model_params: Optional[dict[str, Union[float, str]]] = None
    seed: Optional[int] = None
    compile_only: bool = False

    @staticmethod
    def from_run_parameters(run_parameters: RunParameters) -> "RunParametersModel":
        return RunParametersModel(
            program=run_parameters.program,
            synth_pop=(
                SynthPopModel.from_synth_pop(run_parameters.synth_pop)
                if run_parameters.synth_pop
                else None
            ),
            start_date=run_parameters.start_date,
            end_date=run_parameters.end_date,
            sim_model_params=run_parameters.model_params,
            seed=run_parameters.seed,
            compile_only=run_parameters.compile_only,
        )

    def as_run_parameters(self) -> RunParameters:
        return RunParameters(
            program=self.program,
            synth_pop=self.synth_pop.as_synth_pop() if self.synth_pop else None,
            start_date=self.start_date,
            end_date=self.end_date,
            model_params=self.sim_model_params,
            seed=self.seed,
            compile_only=self.compile_only,
        )


class RunExecuteStrategy(Protocol):
    def execute(self) -> RunResponse: ...


class RunExecuteMultipleStrategy(Protocol):
    def execute_all(self) -> List[RunResponse]: ...
