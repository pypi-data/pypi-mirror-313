# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.terraquantum.invitation.v1.invitation import cancel_organization_member_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_cancel__organization__member__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import generate_new_invitation_token_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_generate__new__invitation__token__request__pb2
from com.terraquantum.invitation.v1.invitation import get_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import get_valid_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__valid__invitation__request__pb2
from com.terraquantum.invitation.v1.invitation import invitation_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2
from com.terraquantum.invitation.v1.invitation import invitation_token_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__token__pb2
from com.terraquantum.invitation.v1.invitation import resend_organization_member_invitation_request_pb2 as com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_resend__organization__member__invitation__request__pb2


class InvitationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GenerateNewInvitationToken = channel.unary_unary(
                '/com.terraquantum.invitation.v1.invitation.InvitationService/GenerateNewInvitationToken',
                request_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_generate__new__invitation__token__request__pb2.GenerateNewInvitationTokenRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__token__pb2.InvitationTokenProto.FromString,
                _registered_method=True)
        self.GetInvitation = channel.unary_unary(
                '/com.terraquantum.invitation.v1.invitation.InvitationService/GetInvitation',
                request_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__invitation__request__pb2.GetInvitationRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
                _registered_method=True)
        self.GetValidInvitation = channel.unary_unary(
                '/com.terraquantum.invitation.v1.invitation.InvitationService/GetValidInvitation',
                request_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__valid__invitation__request__pb2.GetValidInvitationRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
                _registered_method=True)
        self.ResendOrganizationMemberInvitation = channel.unary_unary(
                '/com.terraquantum.invitation.v1.invitation.InvitationService/ResendOrganizationMemberInvitation',
                request_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_resend__organization__member__invitation__request__pb2.ResendOrganizationMemberInvitationRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
                _registered_method=True)
        self.CancelOrganizationMemberInvitation = channel.unary_unary(
                '/com.terraquantum.invitation.v1.invitation.InvitationService/CancelOrganizationMemberInvitation',
                request_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_cancel__organization__member__invitation__request__pb2.CancelOrganizationMemberInvitationRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
                _registered_method=True)


class InvitationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GenerateNewInvitationToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInvitation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValidInvitation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResendOrganizationMemberInvitation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelOrganizationMemberInvitation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InvitationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GenerateNewInvitationToken': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateNewInvitationToken,
                    request_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_generate__new__invitation__token__request__pb2.GenerateNewInvitationTokenRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__token__pb2.InvitationTokenProto.SerializeToString,
            ),
            'GetInvitation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInvitation,
                    request_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__invitation__request__pb2.GetInvitationRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.SerializeToString,
            ),
            'GetValidInvitation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValidInvitation,
                    request_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__valid__invitation__request__pb2.GetValidInvitationRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.SerializeToString,
            ),
            'ResendOrganizationMemberInvitation': grpc.unary_unary_rpc_method_handler(
                    servicer.ResendOrganizationMemberInvitation,
                    request_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_resend__organization__member__invitation__request__pb2.ResendOrganizationMemberInvitationRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.SerializeToString,
            ),
            'CancelOrganizationMemberInvitation': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelOrganizationMemberInvitation,
                    request_deserializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_cancel__organization__member__invitation__request__pb2.CancelOrganizationMemberInvitationRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.terraquantum.invitation.v1.invitation.InvitationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('com.terraquantum.invitation.v1.invitation.InvitationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class InvitationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GenerateNewInvitationToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.terraquantum.invitation.v1.invitation.InvitationService/GenerateNewInvitationToken',
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_generate__new__invitation__token__request__pb2.GenerateNewInvitationTokenRequest.SerializeToString,
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__token__pb2.InvitationTokenProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetInvitation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.terraquantum.invitation.v1.invitation.InvitationService/GetInvitation',
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__invitation__request__pb2.GetInvitationRequest.SerializeToString,
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetValidInvitation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.terraquantum.invitation.v1.invitation.InvitationService/GetValidInvitation',
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_get__valid__invitation__request__pb2.GetValidInvitationRequest.SerializeToString,
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ResendOrganizationMemberInvitation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.terraquantum.invitation.v1.invitation.InvitationService/ResendOrganizationMemberInvitation',
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_resend__organization__member__invitation__request__pb2.ResendOrganizationMemberInvitationRequest.SerializeToString,
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CancelOrganizationMemberInvitation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.terraquantum.invitation.v1.invitation.InvitationService/CancelOrganizationMemberInvitation',
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_cancel__organization__member__invitation__request__pb2.CancelOrganizationMemberInvitationRequest.SerializeToString,
            com_dot_terraquantum_dot_invitation_dot_v1_dot_invitation_dot_invitation__pb2.InvitationProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
