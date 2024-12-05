"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import ansys.api.discovery.v0.monitors_pb2
import grpc

class MonitorsStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    CreateMonitor: grpc.UnaryUnaryMultiCallable[
        ansys.api.discovery.v0.monitors_pb2.CreateMonitorRequest,
        ansys.api.discovery.v0.monitors_pb2.MonitorCreationResponse] = ...
    """Creates a new monitor"""


class MonitorsServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def CreateMonitor(self,
        request: ansys.api.discovery.v0.monitors_pb2.CreateMonitorRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.discovery.v0.monitors_pb2.MonitorCreationResponse:
        """Creates a new monitor"""
        pass


def add_MonitorsServicer_to_server(servicer: MonitorsServicer, server: grpc.Server) -> None: ...
