import pandas as pd
import os
import glob
import re
import random
from datetime import datetime, timedelta
import platform
from typing import Optional, Any
def add_datetime(df: pd.DataFrame, start_time: datetime, min_increment: int, random_range: int) -> pd.DataFrame:
    current_time = start_time
    datetime_list = []

    for _ in df.index:
        datetime_list.append(current_time)
        increment = min_increment + random.randint(-random_range, random_range)
        current_time += timedelta(minutes=increment)

    df['datetime'] = datetime_list
    return df

def clean_string(s:str) -> str:
    str_parts = s.split(' ')
    str_output = []
    for st in str_parts:
        output = re.sub('[^A-Za-z]+', '', st).strip().lower()
        str_output.append(output)
    output = ' '.join(str_output)
    return output

def get_all_files(input_dir:str, extension:Optional[str]='.pdf') -> list[str]:
    pdf_paths = glob.glob(f"{input_dir}/*{extension}")
    return pdf_paths

def parse_file_list(lookup_str:str, file_paths:list[str]):
    found_paths = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_name_cleaned = clean_string(file_name)
        lookup_str_cleaned = clean_string(lookup_str)
        if lookup_str_cleaned in file_name_cleaned:
            found_paths.append(file_path)
    return found_paths


def get_operating_system() -> str:
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Darwin':
        return 'Mac'
    else:
        return 'Unknown'