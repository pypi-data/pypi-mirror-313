# Don't touch! This is a keystring substituted in GitHub workflows!
__version__ = "1.0.0-rc.10"
###################################################################

from epx.job import Job, ModelConfig, ModelConfigSweep, JobResults
from epx.run import Run, RunParameters
from epx.synthpop import SynthPop

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
