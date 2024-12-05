# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.terraquantum.organization.v1.organization import create_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_create__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import get_organization_member_by_id_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__id__request__pb2
from com.terraquantum.organization.v1.organization import get_organization_member_by_organization_id_and_user_id_without_permissions_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__organization__id__and__user__id__without__permissions__request__pb2
from com.terraquantum.organization.v1.organization import inactivate_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_inactivate__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import list_organization_members_by_organization_id_and_organization_members_ids_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__and__organization__members__ids__request__pb2
from com.terraquantum.organization.v1.organization import list_organization_members_by_organization_id_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__request__pb2
from com.terraquantum.organization.v1.organization import organization_member_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2
from com.terraquantum.organization.v1.organization import reactivate_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_reactivate__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import update_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_update__organization__member__request__pb2


class OrganizationMemberServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateOrganizationMember = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/CreateOrganizationMember',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_create__organization__member__request__pb2.CreateOrganizationMemberRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.ReactivateOrganizationMember = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ReactivateOrganizationMember',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_reactivate__organization__member__request__pb2.ReactivateOrganizationMemberRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.InactivateOrganizationMember = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/InactivateOrganizationMember',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_inactivate__organization__member__request__pb2.InactivateOrganizationMemberRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.UpdateOrganizationMember = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/UpdateOrganizationMember',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_update__organization__member__request__pb2.UpdateOrganizationMemberRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.GetOrganizationMemberById = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/GetOrganizationMemberById',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__id__request__pb2.GetOrganizationMemberByIdRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__organization__id__and__user__id__without__permissions__request__pb2.GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissionsRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
                _registered_method=True)
        self.ListOrganizationMembers = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ListOrganizationMembers',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__request__pb2.ListOrganizationMembersByOrganizationIdRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.FromString,
                _registered_method=True)
        self.ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds = channel.unary_unary(
                '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds',
                request_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__and__organization__members__ids__request__pb2.ListOrganizationMembersByOrganizationIdAndOrganizationMembersIdsRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.FromString,
                _registered_method=True)


class OrganizationMemberServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateOrganizationMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReactivateOrganizationMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InactivateOrganizationMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateOrganizationMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationMemberById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOrganizationMembers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrganizationMemberServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateOrganizationMember': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateOrganizationMember,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_create__organization__member__request__pb2.CreateOrganizationMemberRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'ReactivateOrganizationMember': grpc.unary_unary_rpc_method_handler(
                    servicer.ReactivateOrganizationMember,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_reactivate__organization__member__request__pb2.ReactivateOrganizationMemberRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'InactivateOrganizationMember': grpc.unary_unary_rpc_method_handler(
                    servicer.InactivateOrganizationMember,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_inactivate__organization__member__request__pb2.InactivateOrganizationMemberRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'UpdateOrganizationMember': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateOrganizationMember,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_update__organization__member__request__pb2.UpdateOrganizationMemberRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'GetOrganizationMemberById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationMemberById,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__id__request__pb2.GetOrganizationMemberByIdRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__organization__id__and__user__id__without__permissions__request__pb2.GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissionsRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.SerializeToString,
            ),
            'ListOrganizationMembers': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOrganizationMembers,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__request__pb2.ListOrganizationMembersByOrganizationIdRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.SerializeToString,
            ),
            'ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds,
                    request_deserializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__and__organization__members__ids__request__pb2.ListOrganizationMembersByOrganizationIdAndOrganizationMembersIdsRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.terraquantum.organization.v1.organization.OrganizationMemberService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('com.terraquantum.organization.v1.organization.OrganizationMemberService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class OrganizationMemberService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateOrganizationMember(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/CreateOrganizationMember',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_create__organization__member__request__pb2.CreateOrganizationMemberRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def ReactivateOrganizationMember(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ReactivateOrganizationMember',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_reactivate__organization__member__request__pb2.ReactivateOrganizationMemberRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def InactivateOrganizationMember(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/InactivateOrganizationMember',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_inactivate__organization__member__request__pb2.InactivateOrganizationMemberRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def UpdateOrganizationMember(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/UpdateOrganizationMember',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_update__organization__member__request__pb2.UpdateOrganizationMemberRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def GetOrganizationMemberById(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/GetOrganizationMemberById',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__id__request__pb2.GetOrganizationMemberByIdRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissions',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__organization__id__and__user__id__without__permissions__request__pb2.GetOrganizationMemberByOrganizationIdAndUserIdWithoutPermissionsRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.OrganizationMemberProto.FromString,
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
    def ListOrganizationMembers(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ListOrganizationMembers',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__request__pb2.ListOrganizationMembersByOrganizationIdRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.FromString,
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
    def ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds(request,
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
            '/com.terraquantum.organization.v1.organization.OrganizationMemberService/ListOrganizationMembersByOrganizationIdAndOrganizationMembersIds',
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__and__organization__members__ids__request__pb2.ListOrganizationMembersByOrganizationIdAndOrganizationMembersIdsRequest.SerializeToString,
            com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2.ListOrganizationMembersResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
