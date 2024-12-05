# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/discovery/v0/monitors.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ansys.api.discovery.v0 import discoverymodels_pb2 as ansys_dot_api_dot_discovery_dot_v0_dot_discoverymodels__pb2
from ansys.api.discovery.v0 import results_pb2 as ansys_dot_api_dot_discovery_dot_v0_dot_results__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%ansys/api/discovery/v0/monitors.proto\x12\x1f\x61nsys.api.discovery.v0.monitors\x1a,ansys/api/discovery/v0/discoverymodels.proto\x1a$ansys/api/discovery/v0/results.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x9e\x01\n\x14\x43reateMonitorRequest\x12\x41\n\rcreation_data\x18\x01 \x01(\x0b\x32*.ansys.api.discovery.v0.ScopedCreationData\x12\x43\n\x07monitor\x18\x02 \x01(\x0b\x32\x32.ansys.api.discovery.v0.monitors.MonitorProperties\"\xa2\x01\n\x17MonitorCreationResponse\x12\x42\n\x10monitor_response\x18\x01 \x01(\x0b\x32(.ansys.api.discovery.v0.CreationResponse\x12\x43\n\x07monitor\x18\x02 \x01(\x0b\x32\x32.ansys.api.discovery.v0.monitors.MonitorDefinition\"\xa7\x02\n\x11MonitorProperties\x12G\n\x0fresult_variable\x18\x01 \x01(\x0e\x32..ansys.api.discovery.v0.results.ResultVariable\x12G\n\x0fresult_function\x18\x02 \x01(\x0e\x32..ansys.api.discovery.v0.results.ResultFunction\x12N\n\x10result_component\x18\x03 \x01(\x0e\x32/.ansys.api.discovery.v0.results.ResultComponentH\x00\x88\x01\x01\x12\x1b\n\x13locations_secondary\x18\x04 \x03(\tB\x13\n\x11_result_component\"\x86\x01\n\x11MonitorDefinition\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x11\n\tlocations\x18\x03 \x03(\t\x12\x43\n\x07monitor\x18\x04 \x01(\x0b\x32\x32.ansys.api.discovery.v0.monitors.MonitorProperties2\x8d\x01\n\x08Monitors\x12\x80\x01\n\rCreateMonitor\x12\x35.ansys.api.discovery.v0.monitors.CreateMonitorRequest\x1a\x38.ansys.api.discovery.v0.monitors.MonitorCreationResponseB\"\xaa\x02\x1f\x41nsys.Api.Discovery.V0.Monitorsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.discovery.v0.monitors_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\037Ansys.Api.Discovery.V0.Monitors'
  _CREATEMONITORREQUEST._serialized_start=188
  _CREATEMONITORREQUEST._serialized_end=346
  _MONITORCREATIONRESPONSE._serialized_start=349
  _MONITORCREATIONRESPONSE._serialized_end=511
  _MONITORPROPERTIES._serialized_start=514
  _MONITORPROPERTIES._serialized_end=809
  _MONITORDEFINITION._serialized_start=812
  _MONITORDEFINITION._serialized_end=946
  _MONITORS._serialized_start=949
  _MONITORS._serialized_end=1090
# @@protoc_insertion_point(module_scope)
