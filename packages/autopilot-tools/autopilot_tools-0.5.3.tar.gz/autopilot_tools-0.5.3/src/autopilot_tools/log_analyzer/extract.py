#!/usr/bin/env python3
"""
Set of functions to extract usefull data from .ulg logs.
"""
import csv
import subprocess
import os
from .color_logging import log_info, log_err


def convert_relative_path_to_absolute(path):
    if len(path) == 0:
        path = ""
    elif path[0] == '/':
        pass  # is already absolute
    else:
        path = f"{os.getcwd()}/{path}"
    return path


def ulog2csv(output_path, log_path):
    """
    Process bash command: ulog2csv
    """
    output_path = convert_relative_path_to_absolute(output_path)
    bash_command_log_to_csv = f"ulog2csv -o {output_path} {log_path}"
    log_info(bash_command_log_to_csv)
    process = subprocess.Popen(bash_command_log_to_csv.split(),
                               stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    _, _ = process.communicate()


def ulog_params(ulog_full_path):
    """
    Process bash command: ulog_params
    """
    bash_command_extract_params = f"ulog_params {ulog_full_path}"
    process = subprocess.Popen(bash_command_extract_params.split(), stdout=subprocess.PIPE)
    params_raw, _ = process.communicate()
    params_raw = params_raw.decode("utf-8")
    params_raw = params_raw.split('\n')
    return params_raw


def read_csv_file(csv_file_path):
    """
    Open and read given file
    csv_file_path - relative or absolute
    """
    path = convert_relative_path_to_absolute(csv_file_path)
    csvfile = open(path, newline='', encoding="utf8")
    reader = csv.reader(csvfile, delimiter=',')
    return reader


def parse_ulog_if_it_is_not_parsed_and_read_csv_file(log_path, output_path, msg):
    """
    log_path    String of relative or absolute path to log file.
                Example: data_set/fw/log_172_2022-1-14-18-07-00.ulg
    output_path String of relative or absolute path to output folder.
                Example: data_set/fw/output
    msg         String of uorb topic name.
                Example: vehicle_local_position_0
    return      reader on success, otherwise None
    """
    splited_log_path = log_path.split("/", 10)
    log_name = splited_log_path[-1]
    log_name_without_extension = os.path.splitext(log_name)[0]
    csv_file_path = f"{output_path}/{log_name_without_extension}_{msg}.csv"

    reader = None

    try:
        reader = read_csv_file(csv_file_path)
    except FileNotFoundError:
        print("")
        log_info(f"Can't find the corresponded {csv_file_path} file for {msg} message..")
        log_info("Trying to convert it...")

        try:
            ulog2csv(output_path, log_path)
        except FileNotFoundError as err:
            log_err(f"Can't convert ulg to csv. {err}")
            return None
        file_str = f"The log file {log_path}"
        folder_str = f"the folder {output_path}"
        log_info(f"{file_str} has been successfully converter into {folder_str} as .csv files.")

        try:
            reader = read_csv_file(csv_file_path)
        except FileNotFoundError as err:
            log_err(f"Can't find {csv_file_path} file: {err}")
            return None
    return reader


def extract_args(log_path, output_path, msg, msg_fields):
    """
    log_path    String of relative or absolute path to log file.
                Example: data_set/fw/log_172_2022-1-14-18-07-00.ulg
    output_path String of relative or absolute path to output folder.
                Example: data_set/fw/output
    msg         String of uorb topic name.
                Example: vehicle_local_position_0
    msg_fields  Tuple of message fields name.
                Example: ('timestamp', 'z')
    return      List of parsed data
    """
    msg_fields_amount = len(msg_fields)
    parsed_data = list([] for _ in range(msg_fields_amount))

    # Check args
    if log_path[-4:] != ".ulg":
        log_err(f"extract_args: wrong log_path. {log_path}. The format should be .ulg!")
        return parsed_data

    # 1. try to open desired .csv file. It it is not exist yet, convert .ulg to .csv
    csv_fd = parse_ulog_if_it_is_not_parsed_and_read_csv_file(log_path, output_path, msg)
    if csv_fd is None:
        return parsed_data

    # 2. parse all specified msg_fields related to this msg
    data_idx = list(None for _ in range(msg_fields_amount))

    row = next(csv_fd)
    for field_idx in range(msg_fields_amount):
        msg_field = msg_fields[field_idx]
        try:
            data_idx[field_idx] = row.index(msg_field)
        except ValueError:
            log_err(f"{field_idx}/{msg_fields_amount}. csv file has {row}, but not {msg_field}.")
            break

    for row_with_values in csv_fd:
        for idx in range(msg_fields_amount):
            data = data_idx[idx]
            new_data = float(row_with_values[data])
            parsed_data[idx].append(new_data)
    return parsed_data


def extract_params(log_path):
    """
    log_path    String with log path.
                Example: data_set/fw/log_79_2021-12-5-06-22-20.ulg
    """
    params_raw = ulog_params(log_path)
    params_parsed = {}
    for param in params_raw:
        parsed = param.split(',')
        try:
            params_parsed[parsed[0]] = parsed[1]
        except IndexError:
            continue
    return params_parsed
