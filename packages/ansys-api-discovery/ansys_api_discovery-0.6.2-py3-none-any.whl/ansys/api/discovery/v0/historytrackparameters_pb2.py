# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/discovery/v0/historytrackparameters.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ansys.api.dbu.v0 import dbumodels_pb2 as ansys_dot_api_dot_dbu_dot_v0_dot_dbumodels__pb2
from ansys.api.discovery.v0 import discoverymodels_pb2 as ansys_dot_api_dot_discovery_dot_v0_dot_discoverymodels__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3ansys/api/discovery/v0/historytrackparameters.proto\x12-ansys.api.discovery.v0.historytrackparameters\x1a ansys/api/dbu/v0/dbumodels.proto\x1a,ansys/api/discovery/v0/discoverymodels.proto\x1a\x1bgoogle/protobuf/empty.proto\"a\n\x0eGetAllResponse\x12O\n\x18history_track_parameters\x18\x01 \x03(\x0b\x32-.ansys.api.discovery.v0.HistoryTrackParameter\"_\n\rUpdateRequest\x12N\n\x17history_track_parameter\x18\x01 \x01(\x0b\x32-.ansys.api.discovery.v0.HistoryTrackParameter\" \n\x0eReplayResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"l\n\x1aGetRecordingStatusResponse\x12N\n\x06status\x18\x01 \x01(\x0e\x32>.ansys.api.discovery.v0.historytrackparameters.RecordingStatus\"k\n\x19SetRecordingStatusRequest\x12N\n\x06status\x18\x01 \x01(\x0e\x32>.ansys.api.discovery.v0.historytrackparameters.RecordingStatus*\"\n\x0fRecordingStatus\x12\x07\n\x03OFF\x10\x00\x12\x06\n\x02ON\x10\x01\x32\x9c\x05\n\x16HistoryTrackParameters\x12X\n\x03Get\x12\".ansys.api.dbu.v0.EntityIdentifier\x1a-.ansys.api.discovery.v0.HistoryTrackParameter\x12_\n\x06GetAll\x12\x16.google.protobuf.Empty\x1a=.ansys.api.discovery.v0.historytrackparameters.GetAllResponse\x12u\n\x06Update\x12<.ansys.api.discovery.v0.historytrackparameters.UpdateRequest\x1a-.ansys.api.discovery.v0.HistoryTrackParameter\x12_\n\x06Replay\x12\x16.google.protobuf.Empty\x1a=.ansys.api.discovery.v0.historytrackparameters.ReplayResponse\x12w\n\x12GetRecordingStatus\x12\x16.google.protobuf.Empty\x1aI.ansys.api.discovery.v0.historytrackparameters.GetRecordingStatusResponse\x12v\n\x12SetRecordingStatus\x12H.ansys.api.discovery.v0.historytrackparameters.SetRecordingStatusRequest\x1a\x16.google.protobuf.EmptyB0\xaa\x02-Ansys.Api.Discovery.V0.HistoryTrackParametersb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.discovery.v0.historytrackparameters_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002-Ansys.Api.Discovery.V0.HistoryTrackParameters'
  _RECORDINGSTATUS._serialized_start=660
  _RECORDINGSTATUS._serialized_end=694
  _GETALLRESPONSE._serialized_start=211
  _GETALLRESPONSE._serialized_end=308
  _UPDATEREQUEST._serialized_start=310
  _UPDATEREQUEST._serialized_end=405
  _REPLAYRESPONSE._serialized_start=407
  _REPLAYRESPONSE._serialized_end=439
  _GETRECORDINGSTATUSRESPONSE._serialized_start=441
  _GETRECORDINGSTATUSRESPONSE._serialized_end=549
  _SETRECORDINGSTATUSREQUEST._serialized_start=551
  _SETRECORDINGSTATUSREQUEST._serialized_end=658
  _HISTORYTRACKPARAMETERS._serialized_start=697
  _HISTORYTRACKPARAMETERS._serialized_end=1365
# @@protoc_insertion_point(module_scope)
