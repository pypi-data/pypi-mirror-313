
'Utilities for converting and operating on JIT and torch types.'
from __future__ import annotations
import enum
from typing import Dict, Literal, Optional, Union
import torch
ScalarName = Literal[('Byte', 'Char', 'Double', 'Float', 'Half', 'Int', 'Long', 'Short', 'Bool', 'ComplexHalf', 'ComplexFloat', 'ComplexDouble', 'QInt8', 'QUInt8', 'QInt32', 'BFloat16', 'Float8E5M2', 'Float8E4M3FN', 'Float8E5M2FNUZ', 'Float8E4M3FNUZ', 'Undefined')]
TorchName = Literal[('bool', 'uint8_t', 'int8_t', 'double', 'float', 'half', 'int', 'int64_t', 'int16_t', 'complex32', 'complex64', 'complex128', 'qint8', 'quint8', 'qint32', 'bfloat16', 'float8_e5m2', 'float8_e4m3fn', 'float8_e5m2fnuz', 'float8_e4m3fnuz')]

class JitScalarType(enum.IntEnum):
    'Scalar types defined in torch.\n\n    Use ``JitScalarType`` to convert from torch and JIT scalar types to ONNX scalar types.\n\n    Examples:\n        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_ONNX)\n        >>> # xdoctest: +IGNORE_WANT("win32 has different output")\n        >>> JitScalarType.from_value(torch.ones(1, 2)).onnx_type()\n        TensorProtoDataType.FLOAT\n\n        >>> JitScalarType.from_value(torch_c_value_with_type_float).onnx_type()\n        TensorProtoDataType.FLOAT\n\n        >>> JitScalarType.from_dtype(torch.get_default_dtype).onnx_type()\n        TensorProtoDataType.FLOAT\n\n    '
    UINT8 = 0
    INT8 = enum.auto()
    INT16 = enum.auto()
    INT = enum.auto()
    INT64 = enum.auto()
    HALF = enum.auto()
    FLOAT = enum.auto()
    DOUBLE = enum.auto()
    COMPLEX32 = enum.auto()
    COMPLEX64 = enum.auto()
    COMPLEX128 = enum.auto()
    BOOL = enum.auto()
    QINT8 = enum.auto()
    QUINT8 = enum.auto()
    QINT32 = enum.auto()
    BFLOAT16 = enum.auto()
    FLOAT8E5M2 = 23
    FLOAT8E4M3FN = enum.auto()
    FLOAT8E5M2FNUZ = enum.auto()
    FLOAT8E4M3FNUZ = enum.auto()
    UNDEFINED = enum.auto()

    @classmethod
    def _from_name(cls, name: Union[(ScalarName, TorchName, Optional[str])]) -> JitScalarType:
        'Convert a JIT scalar type or torch type name to ScalarType.\n\n        Note: DO NOT USE this API when `name` comes from a `torch._C.Value.type()` calls.\n            A "RuntimeError: INTERNAL ASSERT FAILED at "../aten/src/ATen/core/jit_type_base.h" can\n            be raised in several scenarios where shape info is not present.\n            Instead use `from_value` API which is safer.\n\n        Args:\n            name: JIT scalar type name (Byte) or torch type name (uint8_t).\n\n        Returns:\n            JitScalarType\n\n        Raises:\n           OnnxExporterError: if name is not a valid scalar type name or if it is None.\n        '
        if (name is None):
            raise ValueError('Scalar type name cannot be None')
        if valid_scalar_name(name):
            return _SCALAR_NAME_TO_TYPE[name]
        if valid_torch_name(name):
            return _TORCH_NAME_TO_SCALAR_TYPE[name]
        raise ValueError(f"Unknown torch or scalar type: '{name}'")

    @classmethod
    def from_dtype(cls, dtype: Optional[torch.dtype]) -> JitScalarType:
        'Convert a torch dtype to JitScalarType.\n\n        Note: DO NOT USE this API when `dtype` comes from a `torch._C.Value.type()` calls.\n            A "RuntimeError: INTERNAL ASSERT FAILED at "../aten/src/ATen/core/jit_type_base.h" can\n            be raised in several scenarios where shape info is not present.\n            Instead use `from_value` API which is safer.\n\n        Args:\n            dtype: A torch.dtype to create a JitScalarType from\n\n        Returns:\n            JitScalarType\n\n        Raises:\n            OnnxExporterError: if dtype is not a valid torch.dtype or if it is None.\n        '
        if (dtype not in _DTYPE_TO_SCALAR_TYPE):
            raise ValueError(f'Unknown dtype: {dtype}')
        return _DTYPE_TO_SCALAR_TYPE[dtype]

    @classmethod
    def from_value(cls, value: Union[(None, torch._C.Value, torch.Tensor)], default=None) -> JitScalarType:
        "Create a JitScalarType from an value's scalar type.\n\n        Args:\n            value: An object to fetch scalar type from.\n            default: The JitScalarType to return if a valid scalar cannot be fetched from value\n\n        Returns:\n            JitScalarType.\n\n        Raises:\n            OnnxExporterError: if value does not have a valid scalar type and default is None.\n            SymbolicValueError: when value.type()'s info are empty and default is None\n        "
        if ((not isinstance(value, (torch._C.Value, torch.Tensor))) or (isinstance(value, torch._C.Value) and value.node().mustBeNone())):
            if (default is None):
                raise ValueError('value must be either torch._C.Value or torch.Tensor objects.')
            elif (not isinstance(default, JitScalarType)):
                raise ValueError('default value must be a JitScalarType object.')
            return default
        if isinstance(value, torch.Tensor):
            return cls.from_dtype(value.dtype)
        if isinstance(value.type(), torch.ListType):
            try:
                return cls.from_dtype(value.type().getElementType().dtype())
            except RuntimeError:
                return cls._from_name(str(value.type().getElementType()))
        if isinstance(value.type(), torch._C.OptionalType):
            if (value.type().getElementType().dtype() is None):
                if isinstance(default, JitScalarType):
                    return default
                raise ValueError('default value must be a JitScalarType object.')
            return cls.from_dtype(value.type().getElementType().dtype())
        scalar_type = None
        if ((value.node().kind() != 'prim::Constant') or (not isinstance(value.type(), torch._C.NoneType))):
            scalar_type = value.type().scalarType()
        if (scalar_type is not None):
            return cls._from_name(scalar_type)
        if (default is not None):
            return default
        raise ValueError(f"Cannot determine scalar type for this '{type(value.type())}' instance and a default value was not provided.", value)

    def scalar_name(self) -> ScalarName:
        'Convert a JitScalarType to a JIT scalar type name.'
        return _SCALAR_TYPE_TO_NAME[self]

    def torch_name(self) -> TorchName:
        'Convert a JitScalarType to a torch type name.'
        return _SCALAR_TYPE_TO_TORCH_NAME[self]

    def dtype(self) -> torch.dtype:
        'Convert a JitScalarType to a torch dtype.'
        return _SCALAR_TYPE_TO_DTYPE[self]

def valid_scalar_name(scalar_name: Union[(ScalarName, str)]) -> bool:
    'Return whether the given scalar name is a valid JIT scalar type name.'
    return (scalar_name in _SCALAR_NAME_TO_TYPE)

def valid_torch_name(torch_name: Union[(TorchName, str)]) -> bool:
    'Return whether the given torch name is a valid torch type name.'
    return (torch_name in _TORCH_NAME_TO_SCALAR_TYPE)
_SCALAR_TYPE_TO_NAME: Dict[(JitScalarType, ScalarName)] = {JitScalarType.BOOL: 'Bool', JitScalarType.UINT8: 'Byte', JitScalarType.INT8: 'Char', JitScalarType.INT16: 'Short', JitScalarType.INT: 'Int', JitScalarType.INT64: 'Long', JitScalarType.HALF: 'Half', JitScalarType.FLOAT: 'Float', JitScalarType.DOUBLE: 'Double', JitScalarType.COMPLEX32: 'ComplexHalf', JitScalarType.COMPLEX64: 'ComplexFloat', JitScalarType.COMPLEX128: 'ComplexDouble', JitScalarType.QINT8: 'QInt8', JitScalarType.QUINT8: 'QUInt8', JitScalarType.QINT32: 'QInt32', JitScalarType.BFLOAT16: 'BFloat16', JitScalarType.FLOAT8E5M2: 'Float8E5M2', JitScalarType.FLOAT8E4M3FN: 'Float8E4M3FN', JitScalarType.FLOAT8E5M2FNUZ: 'Float8E5M2FNUZ', JitScalarType.FLOAT8E4M3FNUZ: 'Float8E4M3FNUZ', JitScalarType.UNDEFINED: 'Undefined'}
_SCALAR_NAME_TO_TYPE: Dict[(ScalarName, JitScalarType)] = {v: k for (k, v) in _SCALAR_TYPE_TO_NAME.items()}
_SCALAR_TYPE_TO_TORCH_NAME: Dict[(JitScalarType, TorchName)] = {JitScalarType.BOOL: 'bool', JitScalarType.UINT8: 'uint8_t', JitScalarType.INT8: 'int8_t', JitScalarType.INT16: 'int16_t', JitScalarType.INT: 'int', JitScalarType.INT64: 'int64_t', JitScalarType.HALF: 'half', JitScalarType.FLOAT: 'float', JitScalarType.DOUBLE: 'double', JitScalarType.COMPLEX32: 'complex32', JitScalarType.COMPLEX64: 'complex64', JitScalarType.COMPLEX128: 'complex128', JitScalarType.QINT8: 'qint8', JitScalarType.QUINT8: 'quint8', JitScalarType.QINT32: 'qint32', JitScalarType.BFLOAT16: 'bfloat16', JitScalarType.FLOAT8E5M2: 'float8_e5m2', JitScalarType.FLOAT8E4M3FN: 'float8_e4m3fn', JitScalarType.FLOAT8E5M2FNUZ: 'float8_e5m2fnuz', JitScalarType.FLOAT8E4M3FNUZ: 'float8_e4m3fnuz'}
_TORCH_NAME_TO_SCALAR_TYPE: Dict[(TorchName, JitScalarType)] = {v: k for (k, v) in _SCALAR_TYPE_TO_TORCH_NAME.items()}
_SCALAR_TYPE_TO_DTYPE = {v: getattr(torch, k) for (v, k) in _SCALAR_TYPE_TO_TORCH_NAME.items() if hasattr(torch, k)}
_DTYPE_TO_SCALAR_TYPE = {v: k for (k, v) in _SCALAR_TYPE_TO_DTYPE.items()}
