# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/user/v1/user/user_profile.proto
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
    'com/terraquantum/user/v1/user/user_profile.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.user.v1.waiting_user import waiting_user_pb2 as com_dot_terraquantum_dot_user_dot_v1_dot_waiting__user_dot_waiting__user__pb2
from com.terraquantum.javalibs.logging.v1 import logging_extensions_pb2 as com_dot_terraquantum_dot_javalibs_dot_logging_dot_v1_dot_logging__extensions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0com/terraquantum/user/v1/user/user_profile.proto\x12\x1d\x63om.terraquantum.user.v1.user\x1a\x38\x63om/terraquantum/user/v1/waiting_user/waiting_user.proto\x1a=com/terraquantum/javalibs/logging/v1/logging_extensions.proto\"\xe5\x03\n\x10UserProfileProto\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x34\n\nfirst_name\x18\x02 \x01(\tB\x15\x88\xb5\x18\x01\x90\xb5\x18\x01\x98\xb5\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01R\tfirstName\x12\x36\n\x0bmiddle_name\x18\x03 \x01(\tB\x15\x88\xb5\x18\x01\x90\xb5\x18\x01\x98\xb5\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01R\nmiddleName\x12\x32\n\tlast_name\x18\x04 \x01(\tB\x15\x88\xb5\x18\x01\x90\xb5\x18\x01\x98\xb5\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01R\x08lastName\x12\x18\n\x07\x63ompany\x18\x05 \x01(\tR\x07\x63ompany\x12H\n\x04role\x18\x06 \x01(\x0e\x32\x34.com.terraquantum.user.v1.waiting_user.UserRoleProtoR\x04role\x12s\n\x18primary_area_of_interest\x18\x07 \x01(\x0e\x32:.com.terraquantum.user.v1.waiting_user.AreaOfInterestProtoR\x15primaryAreaOfInterest\x12\x18\n\x07picture\x18\x08 \x01(\tR\x07picture\x12,\n\x12newsletter_sign_up\x18\t \x01(\x08R\x10newsletterSignUpB\x92\x02\n!com.com.terraquantum.user.v1.userB\x10UserProfileProtoP\x01ZAterraquantum.swiss/tq42_grpc_client/com/terraquantum/user/v1/user\xa2\x02\x05\x43TUVU\xaa\x02\x1d\x43om.Terraquantum.User.V1.User\xca\x02\x1d\x43om\\Terraquantum\\User\\V1\\User\xe2\x02)Com\\Terraquantum\\User\\V1\\User\\GPBMetadata\xea\x02!Com::Terraquantum::User::V1::Userb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.user.v1.user.user_profile_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.com.terraquantum.user.v1.userB\020UserProfileProtoP\001ZAterraquantum.swiss/tq42_grpc_client/com/terraquantum/user/v1/user\242\002\005CTUVU\252\002\035Com.Terraquantum.User.V1.User\312\002\035Com\\Terraquantum\\User\\V1\\User\342\002)Com\\Terraquantum\\User\\V1\\User\\GPBMetadata\352\002!Com::Terraquantum::User::V1::User'
  _globals['_USERPROFILEPROTO'].fields_by_name['first_name']._loaded_options = None
  _globals['_USERPROFILEPROTO'].fields_by_name['first_name']._serialized_options = b'\210\265\030\001\220\265\030\001\230\265\030\377\377\377\377\377\377\377\377\377\001'
  _globals['_USERPROFILEPROTO'].fields_by_name['middle_name']._loaded_options = None
  _globals['_USERPROFILEPROTO'].fields_by_name['middle_name']._serialized_options = b'\210\265\030\001\220\265\030\001\230\265\030\377\377\377\377\377\377\377\377\377\001'
  _globals['_USERPROFILEPROTO'].fields_by_name['last_name']._loaded_options = None
  _globals['_USERPROFILEPROTO'].fields_by_name['last_name']._serialized_options = b'\210\265\030\001\220\265\030\001\230\265\030\377\377\377\377\377\377\377\377\377\001'
  _globals['_USERPROFILEPROTO']._serialized_start=205
  _globals['_USERPROFILEPROTO']._serialized_end=690
# @@protoc_insertion_point(module_scope)
