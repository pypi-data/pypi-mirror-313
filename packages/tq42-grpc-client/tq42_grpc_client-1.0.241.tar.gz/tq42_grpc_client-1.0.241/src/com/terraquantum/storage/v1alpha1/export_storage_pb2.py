# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/storage/v1alpha1/export_storage.proto
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
    'com/terraquantum/storage/v1alpha1/export_storage.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6com/terraquantum/storage/v1alpha1/export_storage.proto\x12!com.terraquantum.storage.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\"?\n\x14\x45xportStorageRequest\x12\'\n\nstorage_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tstorageId\"8\n\x15\x45xportStorageResponse\x12\x1f\n\x0bsigned_urls\x18\x01 \x03(\tR\nsignedUrlsB\xb9\x02\n%com.com.terraquantum.storage.v1alpha1B\x12\x45xportStorageProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\xa2\x02\x03\x43TS\xaa\x02!Com.Terraquantum.Storage.V1alpha1\xca\x02!Com\\Terraquantum\\Storage\\V1alpha1\xe2\x02-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::Storage::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.storage.v1alpha1.export_storage_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.storage.v1alpha1B\022ExportStorageProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\242\002\003CTS\252\002!Com.Terraquantum.Storage.V1alpha1\312\002!Com\\Terraquantum\\Storage\\V1alpha1\342\002-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::Storage::V1alpha1'
  _globals['_EXPORTSTORAGEREQUEST'].fields_by_name['storage_id']._loaded_options = None
  _globals['_EXPORTSTORAGEREQUEST'].fields_by_name['storage_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_EXPORTSTORAGEREQUEST']._serialized_start=122
  _globals['_EXPORTSTORAGEREQUEST']._serialized_end=185
  _globals['_EXPORTSTORAGERESPONSE']._serialized_start=187
  _globals['_EXPORTSTORAGERESPONSE']._serialized_end=243
# @@protoc_insertion_point(module_scope)
