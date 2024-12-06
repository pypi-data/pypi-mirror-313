from .os_specific import OsSpecific
from .svc import svc
from .utils import Utils

# --------------------
if svc.utils is None:
    OsSpecific.init()
    svc.utils = Utils()
