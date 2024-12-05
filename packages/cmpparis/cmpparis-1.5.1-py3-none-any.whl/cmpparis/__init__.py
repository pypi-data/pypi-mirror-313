####################################################
# __init__.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################

from .document_db_manager import DocumentDBManager
from .file import File
from .ftp import FTP
from .parameters_utils import get_parameter
from .quable_api import QuableAPI
from .s3 import S3
from .ses_utils import *
from .sm_utils import *
from .utils import *

__all__ = [
    "DocumentDBManager",
    "File",
    "FTP",
    "QuableAPI",
    "S3",
    "get_secret",
    "send_email",
    "send_email_to_support",
    "get_parameter",
    "format_date",
    "get_current_datetime_formatted",
    "lstrip",
    "remove_diacritics",
    "replace",
    "replace_ampersand",
    "replace_comma",
    "replace_endash",
    "replace_emdash",
    "rstrip",
    "toint",
    "upper",
    "check_email",
    "check_empty_value",
    "check_encoding"
]