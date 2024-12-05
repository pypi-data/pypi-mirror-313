from onnx import onnx_ml_pb2 as _onnx_ml_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapProto(_message.Message):
    __slots__ = ["key_type", "keys", "name", "string_keys", "values"]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING_KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key_type: int
    keys: _containers.RepeatedScalarFieldContainer[int]
    name: str
    string_keys: _containers.RepeatedScalarFieldContainer[bytes]
    values: SequenceProto
    def __init__(self, name: _Optional[str] = ..., key_type: _Optional[int] = ..., keys: _Optional[_Iterable[int]] = ..., string_keys: _Optional[_Iterable[bytes]] = ..., values: _Optional[_Union[SequenceProto, _Mapping]] = ...) -> None: ...

class OptionalProto(_message.Message):
    __slots__ = ["elem_type", "map_value", "name", "optional_value", "sequence_value", "sparse_tensor_value", "tensor_value"]
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ELEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP: OptionalProto.DataType
    MAP_VALUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL: OptionalProto.DataType
    OPTIONAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE: OptionalProto.DataType
    SEQUENCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    SPARSE_TENSOR: OptionalProto.DataType
    SPARSE_TENSOR_VALUE_FIELD_NUMBER: _ClassVar[int]
    TENSOR: OptionalProto.DataType
    TENSOR_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNDEFINED: OptionalProto.DataType
    elem_type: int
    map_value: MapProto
    name: str
    optional_value: OptionalProto
    sequence_value: SequenceProto
    sparse_tensor_value: _onnx_ml_pb2.SparseTensorProto
    tensor_value: _onnx_ml_pb2.TensorProto
    def __init__(self, name: _Optional[str] = ..., elem_type: _Optional[int] = ..., tensor_value: _Optional[_Union[_onnx_ml_pb2.TensorProto, _Mapping]] = ..., sparse_tensor_value: _Optional[_Union[_onnx_ml_pb2.SparseTensorProto, _Mapping]] = ..., sequence_value: _Optional[_Union[SequenceProto, _Mapping]] = ..., map_value: _Optional[_Union[MapProto, _Mapping]] = ..., optional_value: _Optional[_Union[OptionalProto, _Mapping]] = ...) -> None: ...

class SequenceProto(_message.Message):
    __slots__ = ["elem_type", "map_values", "name", "optional_values", "sequence_values", "sparse_tensor_values", "tensor_values"]
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ELEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP: SequenceProto.DataType
    MAP_VALUES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL: SequenceProto.DataType
    OPTIONAL_VALUES_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE: SequenceProto.DataType
    SEQUENCE_VALUES_FIELD_NUMBER: _ClassVar[int]
    SPARSE_TENSOR: SequenceProto.DataType
    SPARSE_TENSOR_VALUES_FIELD_NUMBER: _ClassVar[int]
    TENSOR: SequenceProto.DataType
    TENSOR_VALUES_FIELD_NUMBER: _ClassVar[int]
    UNDEFINED: SequenceProto.DataType
    elem_type: int
    map_values: _containers.RepeatedCompositeFieldContainer[MapProto]
    name: str
    optional_values: _containers.RepeatedCompositeFieldContainer[OptionalProto]
    sequence_values: _containers.RepeatedCompositeFieldContainer[SequenceProto]
    sparse_tensor_values: _containers.RepeatedCompositeFieldContainer[_onnx_ml_pb2.SparseTensorProto]
    tensor_values: _containers.RepeatedCompositeFieldContainer[_onnx_ml_pb2.TensorProto]
    def __init__(self, name: _Optional[str] = ..., elem_type: _Optional[int] = ..., tensor_values: _Optional[_Iterable[_Union[_onnx_ml_pb2.TensorProto, _Mapping]]] = ..., sparse_tensor_values: _Optional[_Iterable[_Union[_onnx_ml_pb2.SparseTensorProto, _Mapping]]] = ..., sequence_values: _Optional[_Iterable[_Union[SequenceProto, _Mapping]]] = ..., map_values: _Optional[_Iterable[_Union[MapProto, _Mapping]]] = ..., optional_values: _Optional[_Iterable[_Union[OptionalProto, _Mapping]]] = ...) -> None: ...
