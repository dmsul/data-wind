import os
import socket

from os import path

# Check which machine we're on
HOST = socket.gethostname()
if HOST == 'sullivan-10d':
    data_root = "D:\\data"
elif HOST == 'DESKTOP-HOME':
    data_root = "D:\\data"
elif HOST == 'nepf-7d':
    data_root = "M:\\EPA_AirPollution\\"
elif HOST == 'lu-10d':
    data_root = "C:\\Users\\lu\\Desktop\\Research_lu\\"
else:
    data_root = r'\\Sullivan-10d\\'

DATA_PATH = os.path.join(data_root, 'winddata')
SRC_PATH = path.join(DATA_PATH, 'src')

def data_path(*args):
    return os.path.join(DATA_PATH, *args)


def src_path(*args):
    return os.path.join(SRC_PATH, *args)
