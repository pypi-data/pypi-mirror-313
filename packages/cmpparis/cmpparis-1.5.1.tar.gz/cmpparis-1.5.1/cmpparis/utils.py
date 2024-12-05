####################################################
# utils.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################
from datetime import datetime
import re
import unicodedata

###### Data manipulation ######

# Date functions
def format_date(date, input_format, output_format):
    return datetime.strptime(date, input_format).strftime(output_format)

def get_current_datetime_formatted(format):
    return datetime.now().strftime(format)

# String functions
def lstrip(value):
    return value.lstrip()

def remove_diacritics(value):
    nfkd_form = unicodedata.normalize('NFKD', value)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def replace(value, pattern, replacement):
    return re.sub(pattern, replacement, value)

def replace_ampersand(value):
    return value.replace('&', '+')

def replace_comma(value):
    return value.replace(',', '.')

def replace_endash(value):
    return value.replace('–', '-')

def replace_emdash(value):
    return value.replace('—', '-')

def rstrip(value):
    return value.rstrip()

def tofloat(value):
    return float(value)

def toint(value):
    return int(value)

def upper(value):
    return value.upper()

###### Data checking ######

def check_email(value):
    return False if re.fullmatch("^[\w\-\.]+@([\w\-]+\.)+[\w]{2,4}$", value) == None else True

def check_empty_value(value):
    return False if len(value) == 0 or value == None else True

def check_encoding(value):
    try:
        value.encode('utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True