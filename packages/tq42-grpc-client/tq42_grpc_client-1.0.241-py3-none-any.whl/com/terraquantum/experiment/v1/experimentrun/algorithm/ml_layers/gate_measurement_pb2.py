# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_measurement.proto
# Protobuf Python Version: 5.28.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    2,
    '',
    'com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_measurement.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from com.terraquantum import default_value_pb2 as com_dot_terraquantum_dot_default__value__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nWcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_measurement.proto\x12@com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers\x1a\x1b\x62uf/validate/validate.proto\x1a$com/terraquantum/default_value.proto\x1aMcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/shared.proto\"\xae\x01\n\x0fMeasurementGate\x12$\n\x04wire\x18\x01 \x01(\x05\x42\x10\xbaH\x06\x1a\x04\x18\x19(\x00\x82\xa6\x1d\x03\x1a\x01\x00R\x04wire\x12u\n\x05pauli\x18\x02 \x01(\x0e\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.MeasureProtoB\x0f\xbaH\x05\x82\x01\x02\x10\x01\x82\xa6\x1d\x03z\x01\x01R\x05pauliB\xe8\x03\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\x14GateMeasurementProtoP\x01Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\xa2\x02\x07\x43TEVEAM\xaa\x02?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\xca\x02?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\xe2\x02KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\xea\x02\x45\x43om::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayersb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate_measurement_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\024GateMeasurementProtoP\001Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\242\002\007CTEVEAM\252\002?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\312\002?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\342\002KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\352\002ECom::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayers'
  _globals['_MEASUREMENTGATE'].fields_by_name['wire']._loaded_options = None
  _globals['_MEASUREMENTGATE'].fields_by_name['wire']._serialized_options = b'\272H\006\032\004\030\031(\000\202\246\035\003\032\001\000'
  _globals['_MEASUREMENTGATE'].fields_by_name['pauli']._loaded_options = None
  _globals['_MEASUREMENTGATE'].fields_by_name['pauli']._serialized_options = b'\272H\005\202\001\002\020\001\202\246\035\003z\001\001'
  _globals['_MEASUREMENTGATE']._serialized_start=304
  _globals['_MEASUREMENTGATE']._serialized_end=478
# @@protoc_insertion_point(module_scope)
