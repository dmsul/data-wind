import os
import socket

from os import path


PROJECT_NAME = 'data-wind'

# Check which machine we're on
HOST = socket.gethostname()
if HOST in ('sullivan-10d', 'DESKTOP-HOME'):
    data_root = "D:\\data"
else:
    data_root = r'\\Sullivan-10d\\'

DATA_PATH = os.path.join(data_root, PROJECT_NAME)
SRC_PATH = path.join(DATA_PATH, 'src')


def data_path(*args):
    return os.path.join(DATA_PATH, *args)


def src_path(*args):
    return os.path.join(SRC_PATH, *args)
