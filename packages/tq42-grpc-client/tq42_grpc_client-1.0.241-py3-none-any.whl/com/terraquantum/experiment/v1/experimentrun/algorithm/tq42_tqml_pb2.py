# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/tq42_tqml.proto
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
    'com/terraquantum/experiment/v1/experimentrun/algorithm/tq42_tqml.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_shared__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import generic_algo_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_generic__algo__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFcom/terraquantum/experiment/v1/experimentrun/algorithm/tq42_tqml.proto\x12\x36\x63om.terraquantum.experiment.v1.experimentrun.algorithm\x1a\x43\x63om/terraquantum/experiment/v1/experimentrun/algorithm/shared.proto\x1aIcom/terraquantum/experiment/v1/experimentrun/algorithm/generic_algo.proto\x1a\x1b\x62uf/validate/validate.proto\"v\n\x0fTQmlInputsProto\x12\x63\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x04\x64\x61ta\"\x7f\n\x10TQmlOutputsProto\x12k\n\x08solution\x18\x01 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x08solution\"\xec\x01\n\x11TQmlMetadataProto\x12v\n\nparameters\x18\x01 \x01(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.GenericParametersProtoB\x06\xbaH\x03\xc8\x01\x01R\nparameters\x12_\n\x06inputs\x18\x02 \x01(\x0b\x32G.com.terraquantum.experiment.v1.experimentrun.algorithm.TQmlInputsProtoR\x06inputs\"\xe2\x01\n\x10TQmlOutcomeProto\x12j\n\x06result\x18\x01 \x01(\x0b\x32J.com.terraquantum.experiment.v1.experimentrun.algorithm.GenericResultProtoB\x06\xbaH\x03\xc8\x01\x01R\x06result\x12\x62\n\x07outputs\x18\x02 \x01(\x0b\x32H.com.terraquantum.experiment.v1.experimentrun.algorithm.TQmlOutputsProtoR\x07outputsB\xa7\x03\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\rTq42TqmlProtoP\x01ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\xa2\x02\x06\x43TEVEA\xaa\x02\x36\x43om.Terraquantum.Experiment.V1.Experimentrun.Algorithm\xca\x02\x36\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\xe2\x02\x42\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\xea\x02;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithmb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.tq42_tqml_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\rTq42TqmlProtoP\001ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\242\002\006CTEVEA\252\0026Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm\312\0026Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\342\002BCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\352\002;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithm'
  _globals['_TQMLMETADATAPROTO'].fields_by_name['parameters']._loaded_options = None
  _globals['_TQMLMETADATAPROTO'].fields_by_name['parameters']._serialized_options = b'\272H\003\310\001\001'
  _globals['_TQMLOUTCOMEPROTO'].fields_by_name['result']._loaded_options = None
  _globals['_TQMLOUTCOMEPROTO'].fields_by_name['result']._serialized_options = b'\272H\003\310\001\001'
  _globals['_TQMLINPUTSPROTO']._serialized_start=303
  _globals['_TQMLINPUTSPROTO']._serialized_end=421
  _globals['_TQMLOUTPUTSPROTO']._serialized_start=423
  _globals['_TQMLOUTPUTSPROTO']._serialized_end=550
  _globals['_TQMLMETADATAPROTO']._serialized_start=553
  _globals['_TQMLMETADATAPROTO']._serialized_end=789
  _globals['_TQMLOUTCOMEPROTO']._serialized_start=792
  _globals['_TQMLOUTCOMEPROTO']._serialized_end=1018
# @@protoc_insertion_point(module_scope)
