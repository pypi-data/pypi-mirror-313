# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/organization/v1/organization/organization_member_permission.proto
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
    'com/terraquantum/organization/v1/organization/organization_member_permission.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.common.v1.role import project_role_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_project__role__pb2
from com.terraquantum.common.v1.role import role_organization_resource_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_role__organization__resource__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nRcom/terraquantum/organization/v1/organization/organization_member_permission.proto\x12-com.terraquantum.organization.v1.organization\x1a\x32\x63om/terraquantum/common/v1/role/project_role.proto\x1a@com/terraquantum/common/v1/role/role_organization_resource.proto\"\xb2\x02\n!OrganizationMemberPermissionProto\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x34\n\x16organization_member_id\x18\x02 \x01(\tR\x14organizationMemberId\x12X\n\x0eprojects_roles\x18\x03 \x03(\x0b\x32\x31.com.terraquantum.common.v1.role.ProjectRoleProtoR\rprojectsRoles\x12m\n\x12organization_roles\x18\x04 \x03(\x0b\x32>.com.terraquantum.common.v1.role.OrganizationResourceRoleProtoR\x11organizationRolesB\x83\x03\n1com.com.terraquantum.organization.v1.organizationB!OrganizationMemberPermissionProtoP\x01ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\xa2\x02\x05\x43TOVO\xaa\x02-Com.Terraquantum.Organization.V1.Organization\xca\x02-Com\\Terraquantum\\Organization\\V1\\Organization\xe2\x02\x39\x43om\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\xea\x02\x31\x43om::Terraquantum::Organization::V1::Organizationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.organization.v1.organization.organization_member_permission_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n1com.com.terraquantum.organization.v1.organizationB!OrganizationMemberPermissionProtoP\001ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\242\002\005CTOVO\252\002-Com.Terraquantum.Organization.V1.Organization\312\002-Com\\Terraquantum\\Organization\\V1\\Organization\342\0029Com\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\352\0021Com::Terraquantum::Organization::V1::Organization'
  _globals['_ORGANIZATIONMEMBERPERMISSIONPROTO']._serialized_start=252
  _globals['_ORGANIZATIONMEMBERPERMISSIONPROTO']._serialized_end=558
# @@protoc_insertion_point(module_scope)
