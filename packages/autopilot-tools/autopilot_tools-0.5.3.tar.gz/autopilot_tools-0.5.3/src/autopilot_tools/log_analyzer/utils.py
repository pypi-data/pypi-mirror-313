#!/usr/bin/env python3
import sys
import os
from glob import glob
from .color_logging import log_info, log_warn


def get_log_names(path, verbose=False):
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.ulg'))]
    result.sort()
    if verbose:
        log_info("List of log pathes:")
        for log_idx, log_res in enumerate(result):
            log_info(f"{log_idx}. {log_res}")
        print("")

    return result


def extract_date_from_date_string(date_string):
    """Example: `2021.12.31`"""
    try:
        splitted_date = date_string.split(".")
        year = int(splitted_date[0])
        month = int(splitted_date[1])
        day = int(splitted_date[2])
        month_num = (year - 2021) * 12 + month
        day_num = month_num * 31 + day
    except ValueError as err:
        log_warn(f"Can't extract the date from the log {err}.")
        sys.exit()
    return month_num, day_num


def extract_date_from_log_path(path):
    """assume that every month has 31 days to simplify the model"""
    date_string = path.split("/")[-2]
    return extract_date_from_date_string(date_string)


# def log_name_from_full_path(log_path):
#     splited_log_path = log_path.split("/", 10)
#     log_name = splited_log_path[-1]
#     log_name_without_extension = os.path.splitext(log_name)[0]
#     return log_name_without_extension

def log_name_from_full_path(log_path):
    log_path_splitted = log_path.split('/')
    log_name = f"{log_path_splitted[-2]}/{log_path_splitted[-1]}"[0:-4]
    return log_name
