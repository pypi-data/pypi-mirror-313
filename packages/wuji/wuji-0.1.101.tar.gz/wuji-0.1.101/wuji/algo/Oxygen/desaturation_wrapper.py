import ctypes
import numpy as np
import pandas as pd
import os

# Load the shared library
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, 'desaturation.so')
lib = ctypes.CDLL(lib_path)


# Define the return structure from the C function
class DesaturationResult(ctypes.Structure):
    _fields_ = [
        ("onset", ctypes.POINTER(ctypes.c_int)),
        ("duration", ctypes.POINTER(ctypes.c_int)),
        ("level", ctypes.POINTER(ctypes.c_float)),  # Adjusted for float
        ("size", ctypes.c_int)
    ]


# Specify argument and return types
lib.detect_oxygen_desaturation.argtypes = [
    ctypes.POINTER(ctypes.c_float),  # spo2_arr now expects floats
    ctypes.c_int,  # arr_size
    ctypes.c_int,  # duration_max
    ctypes.c_float  # spo2_des_min_thre also as float
]
lib.detect_oxygen_desaturation.restype = DesaturationResult
lib.free_memory.argtypes = [ctypes.c_void_p]


def detect_oxygen_desaturation(spo2_arr, duration_max=120, spo2_des_min_thre=3):
    spo2_data = spo2_arr.astype(np.float32)  # Ensure the data is in float32 format
    spo2_data_ptr = spo2_data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))  # Pointer to float
    arr_size = len(spo2_data)
    # Call the C function
    result = lib.detect_oxygen_desaturation(spo2_data_ptr, arr_size, duration_max, spo2_des_min_thre)

    # Convert results from C to Python
    onset_array = np.ctypeslib.as_array(result.onset, (result.size,)).copy()
    duration_array = np.ctypeslib.as_array(result.duration, (result.size,)).copy()
    level_array = np.ctypeslib.as_array(result.level, (result.size,)).copy()  # Correctly handle as float

    # Free allocated memory in C
    lib.free_memory(result.onset)
    lib.free_memory(result.duration)
    lib.free_memory(result.level)

    return pd.DataFrame({
        'Type': 'OD',
        'Start': onset_array,
        'Duration': duration_array,
        'OD_level': level_array
    })

