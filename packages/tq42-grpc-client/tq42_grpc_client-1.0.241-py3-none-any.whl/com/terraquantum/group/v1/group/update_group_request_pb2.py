# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/group/v1/group/update_group_request.proto
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
    'com/terraquantum/group/v1/group/update_group_request.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from com.terraquantum.common.v1.role import project_role_request_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_project__role__request__pb2
from com.terraquantum.common.v1.role import role_organization_resource_request_pb2 as com_dot_terraquantum_dot_common_dot_v1_dot_role_dot_role__organization__resource__request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:com/terraquantum/group/v1/group/update_group_request.proto\x12\x1f\x63om.terraquantum.group.v1.group\x1a google/protobuf/field_mask.proto\x1a:com/terraquantum/common/v1/role/project_role_request.proto\x1aHcom/terraquantum/common/v1/role/role_organization_resource_request.proto\"\xb9\x01\n\x12UpdateGroupRequest\x12G\n\x05group\x18\x01 \x01(\x0b\x32\x31.com.terraquantum.group.v1.group.UpdateGroupProtoR\x05group\x12;\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\nupdateMask\x12\x1d\n\nrequest_id\x18\x03 \x01(\tR\trequestId\"\xdb\x02\n\x10UpdateGroupProto\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x36\n\x17organization_member_ids\x18\x04 \x03(\tR\x15organizationMemberIds\x12X\n\rproject_roles\x18\x05 \x03(\x0b\x32\x33.com.terraquantum.common.v1.role.ProjectRoleRequestR\x0cprojectRoles\x12o\n\x12organization_roles\x18\x06 \x03(\x0b\x32@.com.terraquantum.common.v1.role.OrganizationResourceRoleRequestR\x11organizationRolesB\xa5\x02\n#com.com.terraquantum.group.v1.groupB\x17UpdateGroupRequestProtoP\x01ZCterraquantum.swiss/tq42_grpc_client/com/terraquantum/group/v1/group\xa2\x02\x05\x43TGVG\xaa\x02\x1f\x43om.Terraquantum.Group.V1.Group\xca\x02\x1f\x43om\\Terraquantum\\Group\\V1\\Group\xe2\x02+Com\\Terraquantum\\Group\\V1\\Group\\GPBMetadata\xea\x02#Com::Terraquantum::Group::V1::Groupb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.group.v1.group.update_group_request_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n#com.com.terraquantum.group.v1.groupB\027UpdateGroupRequestProtoP\001ZCterraquantum.swiss/tq42_grpc_client/com/terraquantum/group/v1/group\242\002\005CTGVG\252\002\037Com.Terraquantum.Group.V1.Group\312\002\037Com\\Terraquantum\\Group\\V1\\Group\342\002+Com\\Terraquantum\\Group\\V1\\Group\\GPBMetadata\352\002#Com::Terraquantum::Group::V1::Group'
  _globals['_UPDATEGROUPREQUEST']._serialized_start=264
  _globals['_UPDATEGROUPREQUEST']._serialized_end=449
  _globals['_UPDATEGROUPPROTO']._serialized_start=452
  _globals['_UPDATEGROUPPROTO']._serialized_end=799
# @@protoc_insertion_point(module_scope)
