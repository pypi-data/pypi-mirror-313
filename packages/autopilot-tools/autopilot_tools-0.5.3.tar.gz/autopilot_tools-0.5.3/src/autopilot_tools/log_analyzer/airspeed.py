#!/usr/bin/env python3
import matplotlib.pyplot as plt

from .extract import extract_args
from .device_id_parser import parse_device_id
from .utils import log_name_from_full_path


def airspeed(log_path, output_path, output_report_path):
    log_name = log_name_from_full_path(log_path)
    # 1. Extract data
    expected_data_list = [
        ("differential_pressure_0", "device_id", "differential_pressure_pa"),
        ("differential_pressure_1", "device_id", "differential_pressure_pa"),
    ]
    extracted_data = []
    for idx, expected_data in enumerate(expected_data_list):
        data = extract_args(log_path=f"{log_path}/{log_name}.ulg",
                            output_path=output_path,
                            msg=expected_data[0],
                            msg_fields=expected_data[1:])
        if data is None or len(data) == 0:
            print("err", idx)
        extracted_data.append(data)

    # 2. Parse data
    parsed_data_list = []

    device_id = int(extracted_data[0][0][0])
    parsed_data_list.append(parse_device_id(device_id, verbose=True))

    device_id = int(extracted_data[1][0][0])
    parsed_data_list.append(parse_device_id(device_id, verbose=True))

    label = "diff_pressure"
    plt.cla()
    plt.plot(extracted_data[0][1], label="node_id=" + str(parsed_data_list[0]["address"]))
    plt.plot(extracted_data[1][1], label="node_id=" + str(parsed_data_list[1]["address"]))
    plt.legend()
    plt.title(log_name)
    plt.ylabel("Differential pressure, Pa")
    plt.grid()
    plt.savefig(f'{output_report_path}/{label}.png')
