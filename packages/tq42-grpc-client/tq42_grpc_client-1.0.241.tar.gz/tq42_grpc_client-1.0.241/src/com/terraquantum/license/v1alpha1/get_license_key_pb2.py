# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/license/v1alpha1/get_license_key.proto
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
    'com/terraquantum/license/v1alpha1/get_license_key.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7com/terraquantum/license/v1alpha1/get_license_key.proto\x12!com.terraquantum.license.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\"?\n\x14GetLicenseKeyRequest\x12\'\n\nlicense_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tlicenseId\"1\n\x15GetLicenseKeyResponse\x12\x18\n\x03key\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x03keyB\xb9\x02\n%com.com.terraquantum.license.v1alpha1B\x12GetLicenseKeyProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/license/v1alpha1;licensev1alpha1\xa2\x02\x03\x43TL\xaa\x02!Com.Terraquantum.License.V1alpha1\xca\x02!Com\\Terraquantum\\License\\V1alpha1\xe2\x02-Com\\Terraquantum\\License\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::License::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.license.v1alpha1.get_license_key_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.license.v1alpha1B\022GetLicenseKeyProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/license/v1alpha1;licensev1alpha1\242\002\003CTL\252\002!Com.Terraquantum.License.V1alpha1\312\002!Com\\Terraquantum\\License\\V1alpha1\342\002-Com\\Terraquantum\\License\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::License::V1alpha1'
  _globals['_GETLICENSEKEYREQUEST'].fields_by_name['license_id']._loaded_options = None
  _globals['_GETLICENSEKEYREQUEST'].fields_by_name['license_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_GETLICENSEKEYRESPONSE'].fields_by_name['key']._loaded_options = None
  _globals['_GETLICENSEKEYRESPONSE'].fields_by_name['key']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETLICENSEKEYREQUEST']._serialized_start=123
  _globals['_GETLICENSEKEYREQUEST']._serialized_end=186
  _globals['_GETLICENSEKEYRESPONSE']._serialized_start=188
  _globals['_GETLICENSEKEYRESPONSE']._serialized_end=237
# @@protoc_insertion_point(module_scope)
