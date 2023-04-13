# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http: //www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
import numpy as np
from mindquantum._math import dtype

__dtype__ = [
    'float32',
    'float64',
    'complex64',
    'complex128',
]

float32 = dtype.float32
float64 = dtype.float64
complex64 = dtype.complex64
complex128 = dtype.complex128
mq_number_type = [float32, float64, complex64, complex128]
mq_real_number_type = [float32, float64]
mq_complex_number_type = [complex64, complex128]

str_dtype_map = {
    str(float32): float32,
    str(float64): float64,
    str(complex64): complex64,
    str(complex128): complex128,
}


def to_mq_type(dtype):
    """Convert type to mindquantum type."""
    type_mapper = {
        float32: float32,
        float64: float64,
        complex128: complex128,
        complex64: complex64,
        float: float64,
        complex: complex128,
        np.double: float64,
        np.float32: float32,
        np.float64: float64,
        np.complex64: complex64,
        np.complex128: complex128,
    }
    try:
        import mindspore as ms
        type_mapper[ms.float32] = float32
        type_mapper[ms.float64] = float64
        type_mapper[ms.complex64] = complex64
        type_mapper[ms.complex128] = complex128
    except:
        pass
    if dtype not in type_mapper:
        raise TypeError(f"type error: {dtype}, now we support {list(type_mapper.keys())}")
    return type_mapper[dtype]


def to_real_type(dtype):
    """Covert type to real type."""
    dtype = to_mq_type(dtype)
    return {
        float32: float32,
        float64: float64,
        complex128: float64,
        complex64: float32,
    }[dtype]

def to_complex_type(dtype):
    """Convert type to complex type."""
    dtype = to_mq_type(dtype)
    return {
        float32: float32,
        float64: float64,
        float64: complex128,
        float32: complex64,
    }[dtype]
