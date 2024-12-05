# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/terraquantum/invitation/v1/invitation/invitation_service.proto
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
    'com/terraquantum/invitation/v1/invitation/invitation_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.invitation.v1.invitation import generate_new_invitation_token_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_generate__new__invitation__token__request__pb2
from com.terraquantum.invitation.v1.invitation import get_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import get_valid_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__valid__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import invitation_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2
from com.terraquantum.invitation.v1.invitation import invitation_token_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__token__pb2
from com.terraquantum.invitation.v1.invitation import resend_organization_member_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_resend__organization__member__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import cancel_organization_member_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_cancel__organization__member__invitation__request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nBcom/terraquantum/invitation/v1/invitation/invitation_service.proto\x12)com.terraquantum.invitation.v1.invitation\x1aUcom/terraquantum/invitation/v1/invitation/generate_new_invitation_token_request.proto\x1a\x46\x63om/terraquantum/invitation/v1/invitation/get_invitation_request.proto\x1aLcom/terraquantum/invitation/v1/invitation/get_valid_invitation_request.proto\x1a:com/terraquantum/invitation/v1/invitation/invitation.proto\x1a@com/terraquantum/invitation/v1/invitation/invitation_token.proto\x1a]com/terraquantum/invitation/v1/invitation/resend_organization_member_invitation_request.proto\x1a]com/terraquantum/invitation/v1/invitation/cancel_organization_member_invitation_request.proto2\xdb\x06\n\x11InvitationService\x12\xab\x01\n\x1aGenerateNewInvitationToken\x12L.com.terraquantum.invitation.v1.invitation.GenerateNewInvitationTokenRequest\x1a?.com.terraquantum.invitation.v1.invitation.InvitationTokenProto\x12\x8c\x01\n\rGetInvitation\x12?.com.terraquantum.invitation.v1.invitation.GetInvitationRequest\x1a:.com.terraquantum.invitation.v1.invitation.InvitationProto\x12\x96\x01\n\x12GetValidInvitation\x12\x44.com.terraquantum.invitation.v1.invitation.GetValidInvitationRequest\x1a:.com.terraquantum.invitation.v1.invitation.InvitationProto\x12\xb6\x01\n\"ResendOrganizationMemberInvitation\x12T.com.terraquantum.invitation.v1.invitation.ResendOrganizationMemberInvitationRequest\x1a:.com.terraquantum.invitation.v1.invitation.InvitationProto\x12\xb6\x01\n\"CancelOrganizationMemberInvitation\x12T.com.terraquantum.invitation.v1.invitation.CancelOrganizationMemberInvitationRequest\x1a:.com.terraquantum.invitation.v1.invitation.InvitationProtoB\xe0\x02\n-com.com.terraquantum.invitation.v1.invitationB\x16InvitationServiceProtoP\x01ZMterraquantum.swiss/tq42_grpc_client/com/terraquantum/invitation/v1/invitation\xa2\x02\x05\x43TIVI\xaa\x02)Com.Terraquantum.Invitation.V1.Invitation\xca\x02)Com\\Terraquantum\\Invitation\\V1\\Invitation\xe2\x02\x35\x43om\\Terraquantum\\Invitation\\V1\\Invitation\\GPBMetadata\xea\x02-Com::Terraquantum::Invitation::V1::Invitationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.invitation.v1.invitation.invitation_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n-com.com.terraquantum.invitation.v1.invitationB\026InvitationServiceProtoP\001ZMterraquantum.swiss/tq42_grpc_client/com/terraquantum/invitation/v1/invitation\242\002\005CTIVI\252\002)Com.Terraquantum.Invitation.V1.Invitation\312\002)Com\\Terraquantum\\Invitation\\V1\\Invitation\342\0025Com\\Terraquantum\\Invitation\\V1\\Invitation\\GPBMetadata\352\002-Com::Terraquantum::Invitation::V1::Invitation'
  _globals['_INVITATIONSERVICE']._serialized_start=667
  _globals['_INVITATIONSERVICE']._serialized_end=1526
# @@protoc_insertion_point(module_scope)
