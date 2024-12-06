#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from .extract import extract_args
from .utils import log_name_from_full_path
from .uorb_topics import EscStatus


def esc_status(in_log_path, out_path, out_report_path):
    if in_log_path is None or len(in_log_path) == 0:
        return

    log_name = log_name_from_full_path(in_log_path)

    # 1. Extract data
    data = extract_args(log_path=in_log_path,
                        output_path=out_path,
                        msg="esc_status_0",
                        msg_fields=("timestamp",
                                    "esc[0].esc_rpm",
                                    "esc[1].esc_rpm",
                                    "esc[2].esc_rpm",
                                    "esc[4].esc_rpm",
                                    "esc[0].esc_voltage",
                                    "esc[1].esc_voltage",
                                    "esc[2].esc_voltage",
                                    "esc[3].esc_voltage"))
    tss = np.array(data[0], dtype=np.int32)
    tss = np.divide(tss, 1e5)
    tss -= tss[0]
    tss = np.array(tss, dtype=np.int32)

    if tss is None:
        return

    esc_status_topic = EscStatus()
    esc_status_topic.append_data(data)

    plt.cla()
    plt.title(log_name)
    plt.plot(tss, esc_status_topic.values["esc[0].esc_rpm"], label="rpm 0")
    plt.plot(tss, esc_status_topic.values["esc[1].esc_rpm"], label="rpm 1")
    plt.plot(tss, esc_status_topic.values["esc[2].esc_rpm"], label="rpm 2")
    plt.plot(tss, esc_status_topic.values["esc[3].esc_rpm"], label="rpm 3")
    # plt.plot(tss, esc_status_topic.values["esc[0].esc_voltage"], label="voltage 0")
    # plt.plot(tss, esc_status_topic.values["esc[1].esc_voltage"], label="voltage 1")
    # plt.plot(tss, esc_status_topic.values["esc[2].esc_voltage"], label="voltage 2")
    # plt.plot(tss, esc_status_topic.values["esc[3].esc_voltage"], label="voltage 3")
    plt.legend()
    plt.grid()
    plt.savefig(f'{out_report_path}/esc_status.png')
