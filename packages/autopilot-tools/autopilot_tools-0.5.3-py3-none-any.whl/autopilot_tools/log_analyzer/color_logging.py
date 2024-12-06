#!/usr/bin/env python3
from enum import Enum


class Colors(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_info(log_str):
    print(f"INFO: {log_str}")


def log_warn(log_str):
    print(f"{Colors.WARNING.value}WARN: {log_str}{Colors.ENDC.value}")


def log_err(log_str):
    print(f"{Colors.FAIL.value}ERR: {log_str}{Colors.ENDC.value}")


def log_green(log_str):
    print(f"{Colors.OKGREEN.value}{log_str}{Colors.ENDC.value}")


def log_cyan(log_str):
    print(f"{Colors.OKCYAN.value}{log_str}{Colors.ENDC.value}")
