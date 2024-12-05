# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nucliadb_protos import nodereader_pb2 as nucliadb__protos_dot_nodereader__pb2
from nucliadb_protos import noderesources_pb2 as nucliadb__protos_dot_noderesources__pb2


class NodeReaderStub(object):
    """Implemented at nucliadb_object_storage

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetShard = channel.unary_unary(
                '/nodereader.NodeReader/GetShard',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.GetShardRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_noderesources__pb2.Shard.FromString,
                )
        self.DocumentIds = channel.unary_unary(
                '/nodereader.NodeReader/DocumentIds',
                request_serializer=nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
                )
        self.ParagraphIds = channel.unary_unary(
                '/nodereader.NodeReader/ParagraphIds',
                request_serializer=nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
                )
        self.VectorIds = channel.unary_unary(
                '/nodereader.NodeReader/VectorIds',
                request_serializer=nucliadb__protos_dot_noderesources__pb2.VectorSetID.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
                )
        self.RelationIds = channel.unary_unary(
                '/nodereader.NodeReader/RelationIds',
                request_serializer=nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
                )
        self.RelationEdges = channel.unary_unary(
                '/nodereader.NodeReader/RelationEdges',
                request_serializer=nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.EdgeList.FromString,
                )
        self.Search = channel.unary_unary(
                '/nodereader.NodeReader/Search',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.SearchRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.SearchResponse.FromString,
                )
        self.Suggest = channel.unary_unary(
                '/nodereader.NodeReader/Suggest',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.SuggestRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.SuggestResponse.FromString,
                )
        self.Paragraphs = channel.unary_stream(
                '/nodereader.NodeReader/Paragraphs',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.StreamRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.ParagraphItem.FromString,
                )
        self.Documents = channel.unary_stream(
                '/nodereader.NodeReader/Documents',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.StreamRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.DocumentItem.FromString,
                )
        self.GetShardFiles = channel.unary_unary(
                '/nodereader.NodeReader/GetShardFiles',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.GetShardFilesRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.ShardFileList.FromString,
                )
        self.DownloadShardFile = channel.unary_stream(
                '/nodereader.NodeReader/DownloadShardFile',
                request_serializer=nucliadb__protos_dot_nodereader__pb2.DownloadShardFileRequest.SerializeToString,
                response_deserializer=nucliadb__protos_dot_nodereader__pb2.ShardFileChunk.FromString,
                )


class NodeReaderServicer(object):
    """Implemented at nucliadb_object_storage

    """

    def GetShard(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DocumentIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ParagraphIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RelationIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RelationEdges(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Search(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Suggest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Paragraphs(self, request, context):
        """Streams
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Documents(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetShardFiles(self, request, context):
        """Shard Download
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadShardFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeReaderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetShard': grpc.unary_unary_rpc_method_handler(
                    servicer.GetShard,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.GetShardRequest.FromString,
                    response_serializer=nucliadb__protos_dot_noderesources__pb2.Shard.SerializeToString,
            ),
            'DocumentIds': grpc.unary_unary_rpc_method_handler(
                    servicer.DocumentIds,
                    request_deserializer=nucliadb__protos_dot_noderesources__pb2.ShardId.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.SerializeToString,
            ),
            'ParagraphIds': grpc.unary_unary_rpc_method_handler(
                    servicer.ParagraphIds,
                    request_deserializer=nucliadb__protos_dot_noderesources__pb2.ShardId.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.SerializeToString,
            ),
            'VectorIds': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorIds,
                    request_deserializer=nucliadb__protos_dot_noderesources__pb2.VectorSetID.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.SerializeToString,
            ),
            'RelationIds': grpc.unary_unary_rpc_method_handler(
                    servicer.RelationIds,
                    request_deserializer=nucliadb__protos_dot_noderesources__pb2.ShardId.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.IdCollection.SerializeToString,
            ),
            'RelationEdges': grpc.unary_unary_rpc_method_handler(
                    servicer.RelationEdges,
                    request_deserializer=nucliadb__protos_dot_noderesources__pb2.ShardId.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.EdgeList.SerializeToString,
            ),
            'Search': grpc.unary_unary_rpc_method_handler(
                    servicer.Search,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.SearchRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.SearchResponse.SerializeToString,
            ),
            'Suggest': grpc.unary_unary_rpc_method_handler(
                    servicer.Suggest,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.SuggestRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.SuggestResponse.SerializeToString,
            ),
            'Paragraphs': grpc.unary_stream_rpc_method_handler(
                    servicer.Paragraphs,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.StreamRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.ParagraphItem.SerializeToString,
            ),
            'Documents': grpc.unary_stream_rpc_method_handler(
                    servicer.Documents,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.StreamRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.DocumentItem.SerializeToString,
            ),
            'GetShardFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetShardFiles,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.GetShardFilesRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.ShardFileList.SerializeToString,
            ),
            'DownloadShardFile': grpc.unary_stream_rpc_method_handler(
                    servicer.DownloadShardFile,
                    request_deserializer=nucliadb__protos_dot_nodereader__pb2.DownloadShardFileRequest.FromString,
                    response_serializer=nucliadb__protos_dot_nodereader__pb2.ShardFileChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nodereader.NodeReader', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NodeReader(object):
    """Implemented at nucliadb_object_storage

    """

    @staticmethod
    def GetShard(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/GetShard',
            nucliadb__protos_dot_nodereader__pb2.GetShardRequest.SerializeToString,
            nucliadb__protos_dot_noderesources__pb2.Shard.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DocumentIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/DocumentIds',
            nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ParagraphIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/ParagraphIds',
            nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/VectorIds',
            nucliadb__protos_dot_noderesources__pb2.VectorSetID.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RelationIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/RelationIds',
            nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.IdCollection.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RelationEdges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/RelationEdges',
            nucliadb__protos_dot_noderesources__pb2.ShardId.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.EdgeList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Search(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/Search',
            nucliadb__protos_dot_nodereader__pb2.SearchRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.SearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Suggest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/Suggest',
            nucliadb__protos_dot_nodereader__pb2.SuggestRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.SuggestResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Paragraphs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/nodereader.NodeReader/Paragraphs',
            nucliadb__protos_dot_nodereader__pb2.StreamRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.ParagraphItem.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Documents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/nodereader.NodeReader/Documents',
            nucliadb__protos_dot_nodereader__pb2.StreamRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.DocumentItem.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetShardFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nodereader.NodeReader/GetShardFiles',
            nucliadb__protos_dot_nodereader__pb2.GetShardFilesRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.ShardFileList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DownloadShardFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/nodereader.NodeReader/DownloadShardFile',
            nucliadb__protos_dot_nodereader__pb2.DownloadShardFileRequest.SerializeToString,
            nucliadb__protos_dot_nodereader__pb2.ShardFileChunk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
