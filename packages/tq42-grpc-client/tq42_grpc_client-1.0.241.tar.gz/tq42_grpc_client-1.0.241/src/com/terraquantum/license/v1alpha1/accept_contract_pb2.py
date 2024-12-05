# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/license/v1alpha1/accept_contract.proto
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
    'com/terraquantum/license/v1alpha1/accept_contract.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from com.terraquantum.license.v1alpha1 import contract_pb2 as com_dot_terraquantum_dot_license_dot_v1alpha1_dot_contract__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7com/terraquantum/license/v1alpha1/accept_contract.proto\x12!com.terraquantum.license.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x30\x63om/terraquantum/license/v1alpha1/contract.proto\"\xc2\x02\n\x17\x43ontractAcceptanceProto\x12\x1d\n\x05\x65mail\x18\x01 \x01(\tB\x07\xbaH\x04r\x02`\x01R\x05\x65mail\x12\'\n\nlicense_id\x18\x02 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tlicenseId\x12,\n\x03url\x18\x03 \x01(\tB\x1a\xbaH\x17r\x15\x32\x13^(http://|https://)R\x03url\x12\x1a\n\x04\x65tag\x18\x04 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x04\x65tag\x12R\n\x04type\x18\x05 \x01(\x0e\x32\x34.com.terraquantum.license.v1alpha1.ContractTypeProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04type\x12\x41\n\ncreated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x06\xbaH\x03\xc8\x01\x01R\tcreatedAt\"\xc2\x01\n\x15\x41\x63\x63\x65ptContractRequest\x12\'\n\nlicense_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tlicenseId\x12,\n\x03url\x18\x02 \x01(\tB\x1a\xbaH\x17r\x15\x32\x13^(http://|https://)R\x03url\x12R\n\x04type\x18\x03 \x01(\x0e\x32\x34.com.terraquantum.license.v1alpha1.ContractTypeProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04typeB\xba\x02\n%com.com.terraquantum.license.v1alpha1B\x13\x41\x63\x63\x65ptContractProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/license/v1alpha1;licensev1alpha1\xa2\x02\x03\x43TL\xaa\x02!Com.Terraquantum.License.V1alpha1\xca\x02!Com\\Terraquantum\\License\\V1alpha1\xe2\x02-Com\\Terraquantum\\License\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::License::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.license.v1alpha1.accept_contract_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.license.v1alpha1B\023AcceptContractProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/license/v1alpha1;licensev1alpha1\242\002\003CTL\252\002!Com.Terraquantum.License.V1alpha1\312\002!Com\\Terraquantum\\License\\V1alpha1\342\002-Com\\Terraquantum\\License\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::License::V1alpha1'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['email']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['email']._serialized_options = b'\272H\004r\002`\001'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['license_id']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['license_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['url']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['url']._serialized_options = b'\272H\027r\0252\023^(http://|https://)'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['etag']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['etag']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['type']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['created_at']._loaded_options = None
  _globals['_CONTRACTACCEPTANCEPROTO'].fields_by_name['created_at']._serialized_options = b'\272H\003\310\001\001'
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['license_id']._loaded_options = None
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['license_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['url']._loaded_options = None
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['url']._serialized_options = b'\272H\027r\0252\023^(http://|https://)'
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['type']._loaded_options = None
  _globals['_ACCEPTCONTRACTREQUEST'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CONTRACTACCEPTANCEPROTO']._serialized_start=207
  _globals['_CONTRACTACCEPTANCEPROTO']._serialized_end=529
  _globals['_ACCEPTCONTRACTREQUEST']._serialized_start=532
  _globals['_ACCEPTCONTRACTREQUEST']._serialized_end=726
# @@protoc_insertion_point(module_scope)
