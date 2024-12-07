"""Implementation for running FRED jobs using the Platform IDE.

The cloud execution strategy is implemented by the ``RunExecuteCloudStrategy``
class defined here. This class conforms to the ``RunExecuteStrategy``
interface.
"""

from datetime import date
import logging
from pathlib import Path
from typing import Optional, Union, List

import requests

from pydantic import BaseModel, ConfigDict, Field

from epx.synthpop import SynthPopModel, SynthPop
from epx.run.exec.common import (
    RunExecuteStrategy,
    RunParameters,
    RunExecuteMultipleStrategy,
    RunResponse,
    RunRequest,
    FREDArg,
)
from epx.run.exec.compat import fred_major_version
from epx.run.exec.cloud.auth import platform_api_headers
from epx.config import read_auth_config


logger = logging.getLogger(__name__)


class _RunRequestPayload(BaseModel):
    """The complete run request object passed to FRED Cloud.

    Attributes
    ----------
    run_requests : list[RunRequest]
        Collection of individual run request configurations.
    """

    model_config = ConfigDict(populate_by_name=True)

    run_requests: list[RunRequest] = Field(alias="runRequests")


class _RunResponseBody(BaseModel):
    """Response object for a batch of submitted runs from the /runs endpoint.

    Attributes
    ----------
    run_responses : list[RunResponse]
        Collection of responses for individual runs in the originating
        request.
    """

    model_config = ConfigDict(populate_by_name=True)

    run_responses: list[RunResponse] = Field(alias="runResponses")


class ForbiddenResponse(BaseModel):
    """Response object for a 403 Forbidden response from the SRS."""

    description: str


class NotFoundResponse(BaseModel):
    """Response object for a 404 NotFound response from the SRS."""

    description: str


class BadRequestResponse(BaseModel):
    """Response object for a 400 BadRequest response from the SRS."""

    description: str


class RunExecuteCloudStrategy(RunExecuteStrategy):
    """Strategy for submitting an individual run to execute on FRED Cloud.

    Encapsulates logic for forming a request that is compatible with the FRED
    Cloud API /run endpoint based on user input, submitting that request
    to FRED Cloud, and converting any errors reported by FRED Cloud into Python
    exceptions.

    Parameters
    ----------
    job_name : str
        Name of the job to associate this run to on FRED Cloud.
    params : RunParameters
        Parameters to be passed to FRED configuring the run.
    output_dir : Path
        Directory in the user's environment to write run results to.
    size : str
        Name of instance size to use for the run.
    fred_version : str
        Version of FRED to use for the run.

    Attributes
    ----------
    job_name : str
        Name of the job to associate this run to on FRED Cloud.
    params : RunParameters
        Parameters to be passed to FRED configuring the run.
    output_dir : Path
        Directory in the user's environment to write run results to.
    size : str
        Name of instance size to use for the run.
    fred_version : str
        Version of FRED to use for the run.
    """

    def __init__(
        self,
        job_name: Union[str, None],
        params: RunParameters,
        output_dir: Path,
        size: str,
        fred_version: str,
    ):
        self.job_name = job_name
        self.params = params
        self.output_dir = output_dir
        self.size = size
        self.fred_version = fred_version

    def execute(self) -> RunResponse:
        """Submit a run to FRED Cloud.

        Raises
        ------
        UnauthorizedUserError
            If the user does not have sufficient privileges to perform the
            specified action on FRED Cloud.
        RuntimeError
            If a FRED Cloud server error occurs.
        IndexError
            If the FRED Cloud response unexpectedly implies the submission of
            multiple runs.
        RunConfigError
            If FRED Cloud reports an issue with the user's request.
        """
        endpoint_url = f"{read_auth_config('api-url')}/runs"

        # Post request for a run to be executed to FRED Cloud API
        payload = self._request_payload().model_dump_json(by_alias=True)
        logger.debug(f"RunExecuteCloudStrategy - Request payload: {payload}")
        response = requests.post(
            endpoint_url,
            headers=platform_api_headers(),
            data=payload,
        )

        # Check HTTP response status code and raise exceptions as appropriate
        if not response.ok:
            if response.status_code == requests.codes.forbidden:
                raise UnauthorizedUserError(
                    ForbiddenResponse.model_validate_json(response.text).description
                )
            if response.status_code == requests.codes.bad_request:
                raise ValidationError(
                    BadRequestResponse.model_validate_json(response.text).description
                )
            else:
                raise RuntimeError(f"FRED Cloud error code: {response.status_code}")
        response_payload = response.text
        logger.debug(f"RunExecuteCloudStrategy - Response payload: {response_payload}")
        response_body = _RunResponseBody.model_validate_json(response_payload)

        # Confirm response contains response data for exactly one run request
        if (response_length := len(response_body.run_responses)) != 1:
            raise IndexError(
                "Exactly 1 run request expected to be associated with response "
                f"but found {response_length}"
            )

        # Check for any run configuration errors reported in the response and
        # raise exceptions as appropriate
        errors = response_body.run_responses[0].errors
        if errors is not None:
            for error in errors:
                raise RunConfigError(error.key, error.error)

        return response_body.run_responses[0]

    def _request_payload(self) -> _RunRequestPayload:
        return _RunRequestPayload(
            run_requests=[
                RunRequest(
                    job_name=self.job_name,
                    working_dir=str(Path.cwd()),
                    size=self.size,
                    fred_version=self.fred_version,
                    population=(
                        SynthPopModel(
                            version=self.params.synth_pop.name,
                            locations=self.params.synth_pop.locations,
                        )
                        if self.params.synth_pop is not None
                        else None
                    ),
                    fred_args=(
                        _FREDArgsBuilder(self.fred_version)
                        .program(self.params.program)
                        .output_dir(self.output_dir.expanduser().resolve())
                        .overrides(self.params.model_params)
                        .seed(self.params.seed)
                        .start_date(self.params.start_date)
                        .end_date(self.params.end_date)
                        .locations(self.params.synth_pop)
                        .build()
                    ),
                )
            ]
        )


class RunExecuteMultipleCloudStrategy(RunExecuteMultipleStrategy):
    """Strategy for submitting multiple runs to execute on FRED Cloud.

    Encapsulates logic for forming a request that is compatible with the FRED
    Cloud API /run endpoint based on user input, submitting that request
    to FRED Cloud, and converting any errors reported by FRED Cloud into Python
    exceptions.
    """

    def __init__(
        self,
        runs,
    ):
        self.runs = runs

    def execute_all(self) -> List[RunResponse]:
        """Submit multiple runs to FRED Cloud.

        Raises
        ------
        UnauthorizedUserError
            If the user does not have sufficient privileges to perform the
            specified action on FRED Cloud.
        RuntimeError
            If a FRED Cloud server error occurs.
        IndexError
            If the FRED Cloud response unexpectedly implies the submission of
            multiple runs.
        RunConfigError
            If FRED Cloud reports an issue with the user's request.
        """
        endpoint_url = f"{read_auth_config('api-url')}/runs"
        # Post request for a run to be executed to FRED Cloud API
        payload = self._request_payload_runs(self.runs).model_dump_json(by_alias=True)
        logger.debug(f"RunExecuteMultipleCloudStrategy - Request payload: {payload}")
        response = requests.post(
            endpoint_url,
            headers=platform_api_headers(),
            data=payload,
        )

        # Check HTTP response status code and raise exceptions as appropriate
        if not response.ok:
            logger.error(
                f"Run Request {payload} FAILED: {response.status_code} - "
                f"{response.text}"
            )
            if response.status_code == requests.codes.forbidden:
                raise UnauthorizedUserError(
                    ForbiddenResponse.model_validate_json(response.text).description
                )
            if response.status_code == requests.codes.bad_request:
                raise ValidationError(
                    BadRequestResponse.model_validate_json(response.text).description
                )
            else:
                raise RuntimeError(f"FRED Cloud error code: {response.status_code}")
        response_payload = response.text
        logger.debug(
            f"RunExecuteMultipleCloudStrategy - Response payload: {response_payload}"
        )
        response_body = _RunResponseBody.model_validate_json(response_payload)
        response_length = len(response_body.run_responses)

        # Confirm response contains response data for exactly one run request
        if response_length == 0:
            raise IndexError(
                "No responses received. Expected at least one response for run requests"
            )
        # Check for any run configuration errors reported in the response and
        # raise exceptions as appropriate
        for run_response in response_body.run_responses:
            errors = run_response.errors
            if errors is not None:
                for error in errors:
                    raise RunConfigError(error.key, error.error)
        return response_body.run_responses

    def _request_payload_runs(self, runs) -> _RunRequestPayload:
        return _RunRequestPayload(
            run_requests=[
                RunRequest(
                    job_name=run.job_name,
                    working_dir=str(Path.cwd()),
                    size=run.size,
                    fred_version=run.fred_version,
                    population=(
                        SynthPopModel(
                            version=run.params.synth_pop.name,
                            locations=run.params.synth_pop.locations,
                        )
                        if run.params.synth_pop is not None
                        else None
                    ),
                    fred_args=(
                        _FREDArgsBuilder(run.fred_version)
                        .program(run.params.program)
                        .output_dir(run.output_dir.expanduser().resolve())
                        .overrides(run.params.model_params)
                        .seed(run.params.seed)
                        .start_date(run.params.start_date)
                        .end_date(run.params.end_date)
                        .locations(run.params.synth_pop)
                        .build()
                    ),
                )
                for run in runs
            ]
        )


class _FREDArgsBuilder:
    """Builder for list of arguments to pass to FRED via SRS.

    Handles correct argument naming for different FRED versions.

    Parameters
    ----------
    fred_version : str
        FRED version for the run.
    """

    def __init__(self, fred_version: str):
        self.fred_version = fred_version
        self._args: list[FREDArg] = []

    def build(self) -> list[FREDArg]:
        return self._args

    def program(self, program: Union[Path, str]) -> "_FREDArgsBuilder":
        self._args.append(FREDArg(flag="-p", value=str(program)))
        return self

    def output_dir(self, output_dir: Path) -> "_FREDArgsBuilder":
        """Add the output directory argument to the FRED command line.

        Parameters
        ----------
        output_dir : Path
            Absolute path to the output directory.

        Returns
        -------
        _FREDArgsBuilder
            Current state of a partially built FRED command line.
        """
        if not output_dir.is_absolute():
            raise ValueError("output_dir must be an absolute path.")
        self._args.append(FREDArg(flag="-d", value=str(output_dir)))
        return self

    def overrides(
        self, model_params: Optional[dict[str, Union[float, str]]]
    ) -> "_FREDArgsBuilder":
        if model_params is not None:
            self._args.extend(
                [FREDArg(flag="-o", value=f"{k}={v}") for k, v in model_params.items()]
            )
        return self

    def seed(self, seed: int) -> "_FREDArgsBuilder":
        if fred_major_version(self.fred_version) < 11:
            # Use run number as an pseudo-seed
            self._args.append(FREDArg(flag="-r", value=str(seed)))
        else:
            self._args.append(FREDArg(flag="-s", value=str(seed)))
        return self

    def start_date(self, start_date: Optional[date]) -> "_FREDArgsBuilder":
        if start_date is not None:
            self._args.append(
                FREDArg(
                    flag="--start-date",
                    value=start_date.strftime(r"%Y-%m-%d"),
                )
            )
        return self

    def end_date(self, end_date: Optional[date]) -> "_FREDArgsBuilder":
        if end_date is not None:
            self._args.append(
                FREDArg(
                    flag="--end-date",
                    value=end_date.strftime(r"%Y-%m-%d"),
                )
            )
        return self

    def locations(self, synth_pop: Optional[SynthPop]) -> "_FREDArgsBuilder":
        if (
            synth_pop is not None
            and synth_pop.locations is not None
            and fred_major_version(self.fred_version) >= 11
        ):
            # FRED 10 does not support --locations flag
            for location in synth_pop.locations:
                self._args.append(FREDArg(flag="-l", value=location))
        return self


class ValidationError(Exception):
    """Error indicating the model configuration is invalid.

    Parameters
    ----------
    description : str
        Detailed description of the error as reported by SRS.

    Attributes
    ----------
    message : str
        Message describing the error.
    """

    def __init__(self, description: str):
        super().__init__(f"Model configuration error: {description}")


class UnauthorizedUserError(Exception):
    """Error indicating the user is not authorized to perform requested action.

    This can be thrown in the following circumstances:
        * User is not found in the Platform system
        * User does not have a subscription
        * User does not have sufficient compute credits

    Parameters
    ----------
    description : str
        Detailed description of the error as reported by SRS.

    Attributes
    ----------
    message : str
        Message describing the error.
    """

    def __init__(self, description: str):
        super().__init__(f"Authorization error: {description}")


class NotFoundError(Exception):
    """Custom exception for not found errors.

    Parameters
    ----------
    description : str
        Detailed description of the error as reported by SRS.
    """

    def __init__(self, description: str):
        super().__init__(f"NotFound error: {description}")


class RunConfigError(Exception):
    """Error indicating there was a run configuration error.

    This is thrown when FRED Cloud API has reported an issue with the user's
    request.

    Parameters
    ----------
    key : str
        The general category of the error reported by FRED Cloud API, e.g.
        ``size`` for errors related to instance size, or ``fredVersion`` if the
        specified FRED version is not recognized.
    desc : str
        Detailed description of the error.

    Attributes
    ----------
    key : str
        The general category of the error reported by FRED Cloud API, e.g.
        ``size`` for errors related to instance size, or ``fredVersion`` if the
        specified FRED version is not recognized.
    desc : str
        Detailed description of the error.
    message : str
        Summary message describing the error.
    """

    def __init__(self, key: str, desc: str):
        self.key = key
        self.desc = desc
        super().__init__(f"{self.key} error: {self.desc}")
