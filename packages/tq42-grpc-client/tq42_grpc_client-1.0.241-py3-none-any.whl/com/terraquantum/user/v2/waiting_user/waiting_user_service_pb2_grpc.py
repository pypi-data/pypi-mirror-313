# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.terraquantum.user.v1.waiting_user import waiting_user_pb2 as com_dot_terraquantum_dot_user_dot_v1_dot_waiting__user_dot_waiting__user__pb2
from com.terraquantum.user.v2.waiting_user import add_waiting_user_request_pb2 as com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_add__waiting__user__request__pb2
from com.terraquantum.user.v2.waiting_user import join_waiting_list_request_pb2 as com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_join__waiting__list__request__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class WaitingUserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.JoinWaitingList = channel.unary_unary(
                '/com.terraquantum.user.v2.waiting_user.WaitingUserService/JoinWaitingList',
                request_serializer=com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_join__waiting__list__request__pb2.JoinWaitingListRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.AddWaitingUser = channel.unary_unary(
                '/com.terraquantum.user.v2.waiting_user.WaitingUserService/AddWaitingUser',
                request_serializer=com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_add__waiting__user__request__pb2.AddWaitingUserRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_user_dot_v1_dot_waiting__user_dot_waiting__user__pb2.WaitingUserProto.FromString,
                _registered_method=True)


class WaitingUserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def JoinWaitingList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddWaitingUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WaitingUserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'JoinWaitingList': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinWaitingList,
                    request_deserializer=com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_join__waiting__list__request__pb2.JoinWaitingListRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'AddWaitingUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddWaitingUser,
                    request_deserializer=com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_add__waiting__user__request__pb2.AddWaitingUserRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_user_dot_v1_dot_waiting__user_dot_waiting__user__pb2.WaitingUserProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.terraquantum.user.v2.waiting_user.WaitingUserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('com.terraquantum.user.v2.waiting_user.WaitingUserService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WaitingUserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def JoinWaitingList(request,
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
            '/com.terraquantum.user.v2.waiting_user.WaitingUserService/JoinWaitingList',
            com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_join__waiting__list__request__pb2.JoinWaitingListRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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
    def AddWaitingUser(request,
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
            '/com.terraquantum.user.v2.waiting_user.WaitingUserService/AddWaitingUser',
            com_dot_terraquantum_dot_user_dot_v2_dot_waiting__user_dot_add__waiting__user__request__pb2.AddWaitingUserRequest.SerializeToString,
            com_dot_terraquantum_dot_user_dot_v1_dot_waiting__user_dot_waiting__user__pb2.WaitingUserProto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
