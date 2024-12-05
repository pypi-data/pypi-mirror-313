from pydantic import constr

import enum

class UserType(str, enum.Enum):
    admin = "admin"
    scope_admin  = "scope_admin"
    standard_user = "standard_user"
    superuser = "superuser"

class FileType(str, enum.Enum):
    HDF5 = "HDF5"
    HDF5_NETCDF = "HDF5_NETCDF"
    HDF5_CACHE = "HDF5_CACHE"
    NDARRAY = "NDARRAY"
    JSON = "JSON"
    TEXT = "TEXT"
    UNKNOWN = "UNKNOWN"

class FileStatusRem(str, enum.Enum):
    announced = "announced"
    pending = "pending" # means in the process of uploading.
    secured = "secured" # upload completed.

# TODO move this to a better location!
class FileStatusLocal(str, enum.Enum):
    writing = "writing" # file is being written currenly.
    complete = "complete" # file is written and ready for upload.
    unavailable = "unavailable" # File is not created or deleted.

class UploadConcat(str, enum.Enum):
    partial = "partial"
    final = "final"

class UserLogStatus(str, enum.Enum):
    pending = "pending"
    secured = "secured"

class SoftwareType(str, enum.Enum):
    etiket = "etiket"
    dataQruiser = "dataQruiser"
    qdrive = "qdrive"

class ObjectStoreType(enum.Enum):
    TUD = "TUD"
    AWS = "AWS"
    AZURE = "AZURE"
    SWIFT = "SWIFT"

class S3ScopeTransferStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class S3FileTransferStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


namestr     = constr(min_length=1, max_length=100)
usernamestr = constr(min_length=4, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
metastr     = constr(min_length=1, max_length=255)
filestr     = constr(min_length=2, max_length=255)
datasetstr  = constr(min_length=2, max_length=255)
collectionstr = constr(min_length=2, max_length=255)
uidstr      = constr(min_length=5, max_length=80)
scopestr    = constr(min_length=4, max_length=100,  pattern=r"^[a-zA-Z0-9_ ]+$")
passwordstr = constr(min_length=6, max_length=20)