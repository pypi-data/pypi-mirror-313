# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/organization/v1/organization/organization_member_permission_request.proto
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
    'com/terraquantum/organization/v1/organization/organization_member_permission_request.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.common.v1.role import project_role_request_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_project__role__request__pb2
from com.terraquantum.common.v1.role import role_organization_resource_request_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_role__organization__resource__request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nZcom/terraquantum/organization/v1/organization/organization_member_permission_request.proto\x12-com.terraquantum.organization.v1.organization\x1a:com/terraquantum/common/v1/role/project_role_request.proto\x1aHcom/terraquantum/common/v1/role/role_organization_resource_request.proto\"\xf2\x01\n#OrganizationMemberPermissionRequest\x12Z\n\x0eprojects_roles\x18\x01 \x03(\x0b\x32\x33.com.terraquantum.common.v1.role.ProjectRoleRequestR\rprojectsRoles\x12o\n\x12organization_roles\x18\x02 \x03(\x0b\x32@.com.terraquantum.common.v1.role.OrganizationResourceRoleRequestR\x11organizationRolesB\x8a\x03\n1com.com.terraquantum.organization.v1.organizationB(OrganizationMemberPermissionRequestProtoP\x01ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\xa2\x02\x05\x43TOVO\xaa\x02-Com.Terraquantum.Organization.V1.Organization\xca\x02-Com\\Terraquantum\\Organization\\V1\\Organization\xe2\x02\x39\x43om\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\xea\x02\x31\x43om::Terraquantum::Organization::V1::Organizationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.organization.v1.organization.organization_member_permission_request_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n1com.com.terraquantum.organization.v1.organizationB(OrganizationMemberPermissionRequestProtoP\001ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\242\002\005CTOVO\252\002-Com.Terraquantum.Organization.V1.Organization\312\002-Com\\Terraquantum\\Organization\\V1\\Organization\342\0029Com\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\352\0021Com::Terraquantum::Organization::V1::Organization'
  _globals['_ORGANIZATIONMEMBERPERMISSIONREQUEST']._serialized_start=276
  _globals['_ORGANIZATIONMEMBERPERMISSIONREQUEST']._serialized_end=518
# @@protoc_insertion_point(module_scope)
