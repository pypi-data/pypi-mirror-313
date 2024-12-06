from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


from wrap_technote.utils import *
from wrap_technote.gwutils import *
from wrap_technote.charts import *
from wrap_technote.fileio import *
from wrap_technote.reporting import *
from wrap_technote.salinity import *
from wrap_technote.waterlevels import *
from wrap_technote.rainfall import *

from wrap_technote import scripts


from pathlib import Path

import warnings

warnings.filterwarnings(
    "ignore",
    module="wrap_technote.reporting",
    # lineno=800
)
