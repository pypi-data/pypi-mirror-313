#!/usr/bin/env python3
import matplotlib.pyplot as plt
from .extract import extract_args
from .uorb_topics import ActuatorOutputs

MINIMAL_DURATION_SEC = 5.0


def get_desired_time_limit(state_timestamps, states):
    first_work_timestamp = state_timestamps[-1]
    for idx, state in enumerate(states):
        if state == 2:
            first_work_timestamp = state_timestamps[idx]
            break
    last_work_timestamp = state_timestamps[0]

    for idx, state in reversed(list(enumerate(states))):
        if state == 2:
            last_work_timestamp = state_timestamps[idx]
            break

    if last_work_timestamp < first_work_timestamp:
        print(f'Wrong timestamp. From {first_work_timestamp} to {last_work_timestamp}')
        return None, None

    return first_work_timestamp, last_work_timestamp


def get_most_useful_time_limit(state_timestamps, states):
    longest_repeating_counter = 0
    longest_repeating_last_idx = 0
    repeating_counter = 0
    for idx, state in enumerate(states):
        if state == 2:
            repeating_counter += 1
            if repeating_counter > longest_repeating_counter:
                longest_repeating_counter = repeating_counter
                longest_repeating_last_idx = idx
        else:
            repeating_counter = 0

    first_work_timestamp = state_timestamps[longest_repeating_last_idx - longest_repeating_counter]
    last_work_timestamp = state_timestamps[longest_repeating_last_idx]

    duration_sec = (last_work_timestamp - first_work_timestamp) * 1e-6
    if duration_sec < MINIMAL_DURATION_SEC:
        print(f'Wrong timestamp. From {first_work_timestamp} to {last_work_timestamp}.')
        return None, None
    return first_work_timestamp, last_work_timestamp


def clamp_dataset(timestamps, data, first_work_timestamp, last_work_timestamp):
    first_rpm_idx = len(timestamps) - 1
    for idx, timestamp in enumerate(timestamps):
        if timestamp > first_work_timestamp:
            first_rpm_idx = idx
            break
    last_rpm_idx = len(timestamps) - 1

    for idx, timestamp in reversed(list(enumerate(timestamps))):
        if timestamps[idx] < last_work_timestamp:
            last_rpm_idx = idx
            break
    timestamps = timestamps[first_rpm_idx: last_rpm_idx]
    data = data[first_rpm_idx: last_rpm_idx]
    return timestamps, data


def fit_func(x, b, c):
    return b * x ** 2 + c * x


def ice(in_log_path, out_path, out_report_path):
    if in_log_path is None or len(in_log_path) == 0:
        return

    log_path_splitted = in_log_path.split('/')
    log_name = f"{log_path_splitted[-2]}/{log_path_splitted[-1]}"[0:-4]

    # 1. Extract data
    data = extract_args(log_path=in_log_path,
                        output_path=out_path,
                        msg="internal_combustion_engine_status_0",
                        msg_fields=("timestamp", "engine_speed_rpm", "spark_plug_usage", "state"))
    ice_tss = data[0]
    ice_rpms = data[1]
    states = data[3]

    if ice_tss is None:
        return

    cmd = ActuatorOutputs()
    data = extract_args(log_path=in_log_path,
                        output_path=out_path,
                        msg=cmd.msg,
                        msg_fields=cmd.args)
    cmd.append_data(data)

    cmd_value = cmd.values["output[7]"]
    if len(ice_rpms) == 0 or len(cmd_value) == 0 or len(states) == 0:
        print(f"Initial sizes 0: rpm={len(ice_rpms)}, cmds={len(cmd_value)}, states={len(states)}")
        return

    plt.cla()
    plt.title(log_name)
    plt.plot(ice_tss, ice_rpms, label="rpm")
    plt.plot(cmd.values["timestamp"], cmd_value, label="cmd")
    plt.legend()
    plt.grid()
    plt.savefig(f'{out_report_path}/ice.png')
