# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/organization/v1/organization/update_organization_request.proto
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
    'com/terraquantum/organization/v1/organization/update_organization_request.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nOcom/terraquantum/organization/v1/organization/update_organization_request.proto\x12-com.terraquantum.organization.v1.organization\x1a google/protobuf/field_mask.proto\"\xda\x01\n\x19UpdateOrganizationRequest\x12;\n\x0bupdate_mask\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\nupdateMask\x12\x1d\n\nrequest_id\x18\x02 \x01(\tR\trequestId\x12\x0e\n\x02id\x18\x03 \x01(\tR\x02id\x12\x12\n\x04name\x18\x04 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x05 \x01(\tR\x0b\x64\x65scription\x12\x1b\n\timage_url\x18\x06 \x01(\tR\x08imageUrlB\x80\x03\n1com.com.terraquantum.organization.v1.organizationB\x1eUpdateOrganizationRequestProtoP\x01ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\xa2\x02\x05\x43TOVO\xaa\x02-Com.Terraquantum.Organization.V1.Organization\xca\x02-Com\\Terraquantum\\Organization\\V1\\Organization\xe2\x02\x39\x43om\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\xea\x02\x31\x43om::Terraquantum::Organization::V1::Organizationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.organization.v1.organization.update_organization_request_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n1com.com.terraquantum.organization.v1.organizationB\036UpdateOrganizationRequestProtoP\001ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\242\002\005CTOVO\252\002-Com.Terraquantum.Organization.V1.Organization\312\002-Com\\Terraquantum\\Organization\\V1\\Organization\342\0029Com\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\352\0021Com::Terraquantum::Organization::V1::Organization'
  _globals['_UPDATEORGANIZATIONREQUEST']._serialized_start=165
  _globals['_UPDATEORGANIZATIONREQUEST']._serialized_end=383
# @@protoc_insertion_point(module_scope)
