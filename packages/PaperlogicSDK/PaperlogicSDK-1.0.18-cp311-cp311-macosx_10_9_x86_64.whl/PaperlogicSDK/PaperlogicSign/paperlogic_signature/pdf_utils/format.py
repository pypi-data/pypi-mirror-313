from pytz import timezone
from datetime import datetime

__all__ = [
    'format_date'
]

def format_date():
    Tk = timezone('Asia/Tokyo')
    fmt = '%Y-%m-%d %H:%M:%S %z'
    # "%Y-%m-%d %H:%M:%S %z"
    loc_dt  = datetime.now()

    tk_dt = loc_dt.astimezone(Tk)
    str_time = tk_dt.strftime(fmt).replace('JST', '')
    timezone_offset = str_time[-5:]
    formatted_offset = timezone_offset[:3] + "'" + timezone_offset[3:] + "'"
    formatted_datetime_str = str_time.replace(timezone_offset, formatted_offset)
    return formatted_datetime_str