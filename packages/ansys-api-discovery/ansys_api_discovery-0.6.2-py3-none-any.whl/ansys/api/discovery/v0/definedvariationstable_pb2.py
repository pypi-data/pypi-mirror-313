# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/discovery/v0/definedvariationstable.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3ansys/api/discovery/v0/definedvariationstable.proto\x12-ansys.api.discovery.v0.definedvariationstable\x1a ansys/api/dbu/v0/dbumodels.proto\x1a,ansys/api/discovery/v0/discoverymodels.proto\x1a\x1bgoogle/protobuf/empty.proto\"Y\n\x18GetAllVariationsResponse\x12=\n\x12\x64\x65\x66ined_variations\x18\x01 \x03(\x0b\x32!.ansys.api.discovery.v0.Variation\"K\n\x14GetAllInputsResponse\x12\x33\n\x06inputs\x18\x01 \x03(\x0b\x32#.ansys.api.discovery.v0.InputColumn\"N\n\x15GetAllOutputsResponse\x12\x35\n\x07outputs\x18\x01 \x03(\x0b\x32$.ansys.api.discovery.v0.OutputColumn\"Y\n\x1bGetInputForVariationRequest\x12\x19\n\x11variation_moniker\x18\x01 \x01(\t\x12\x1f\n\x17input_parameter_moniker\x18\x02 \x01(\t\"\x80\x01\n\x14SetInputValueRequest\x12\x19\n\x11variation_moniker\x18\x01 \x01(\t\x12M\n\x1d\x64\x65\x66ined_variation_table_input\x18\x02 \x01(\x0b\x32&.ansys.api.discovery.v0.InputParameter\"[\n\x1cGetOutputForVariationRequest\x12\x19\n\x11variation_moniker\x18\x01 \x01(\t\x12 \n\x18output_parameter_moniker\x18\x02 \x01(\t\"8\n\x15GetInputColumnRequest\x12\x1f\n\x17input_parameter_moniker\x18\x01 \x01(\t\"M\n\x16GetInputColumnResponse\x12\x33\n\x06\x63olumn\x18\x01 \x01(\x0b\x32#.ansys.api.discovery.v0.InputColumn\":\n\x16GetOutputColumnRequest\x12 \n\x18output_parameter_moniker\x18\x01 \x01(\t\"O\n\x17GetOutputColumnResponse\x12\x34\n\x06\x63olumn\x18\x01 \x01(\x0b\x32$.ansys.api.discovery.v0.OutputColumn\"G\n\x17SetStarredStatusRequest\x12\x1b\n\x13variations_monikers\x18\x01 \x03(\t\x12\x0f\n\x07starred\x18\x02 \x01(\x08\"I\n\x1bGetCurrentVariationResponse\x12\x19\n\x11variation_moniker\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"1\n\x0eUpdateResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\'\n\x11IsSolvingResponse\x12\x12\n\nis_solving\x18\x01 \x01(\x08\x32\xda\x0f\n\x16\x44\x65\x66inedVariationsTable\x12U\n\x0cGetVariation\x12\".ansys.api.dbu.v0.EntityIdentifier\x1a!.ansys.api.discovery.v0.Variation\x12s\n\x10GetAllVariations\x12\x16.google.protobuf.Empty\x1aG.ansys.api.discovery.v0.definedvariationstable.GetAllVariationsResponse\x12k\n\x0cGetAllInputs\x12\x16.google.protobuf.Empty\x1a\x43.ansys.api.discovery.v0.definedvariationstable.GetAllInputsResponse\x12m\n\rGetAllOutputs\x12\x16.google.protobuf.Empty\x1a\x44.ansys.api.discovery.v0.definedvariationstable.GetAllOutputsResponse\x12\x8a\x01\n\x14GetInputForVariation\x12J.ansys.api.discovery.v0.definedvariationstable.GetInputForVariationRequest\x1a&.ansys.api.discovery.v0.InputParameter\x12|\n\rSetInputValue\x12\x43.ansys.api.discovery.v0.definedvariationstable.SetInputValueRequest\x1a&.ansys.api.discovery.v0.InputParameter\x12L\n\x0f\x43reateVariation\x12\x16.google.protobuf.Empty\x1a!.ansys.api.discovery.v0.Variation\x12\x8d\x01\n\x15GetOutputForVariation\x12K.ansys.api.discovery.v0.definedvariationstable.GetOutputForVariationRequest\x1a\'.ansys.api.discovery.v0.OutputParameter\x12\x9d\x01\n\x0eGetInputColumn\x12\x44.ansys.api.discovery.v0.definedvariationstable.GetInputColumnRequest\x1a\x45.ansys.api.discovery.v0.definedvariationstable.GetInputColumnResponse\x12\xa0\x01\n\x0fGetOutputColumn\x12\x45.ansys.api.discovery.v0.definedvariationstable.GetOutputColumnRequest\x1a\x46.ansys.api.discovery.v0.definedvariationstable.GetOutputColumnResponse\x12y\n\x13GetCurrentVariation\x12\x16.google.protobuf.Empty\x1aJ.ansys.api.discovery.v0.definedvariationstable.GetCurrentVariationResponse\x12\x62\n\x13SetCurrentVariation\x12\".ansys.api.dbu.v0.EntityIdentifier\x1a\'.ansys.api.discovery.v0.MessageResponse\x12r\n\x10SetStarredStatus\x12\x46.ansys.api.discovery.v0.definedvariationstable.SetStarredStatusRequest\x1a\x16.google.protobuf.Empty\x12\x66\n\rUpdateCurrent\x12\x16.google.protobuf.Empty\x1a=.ansys.api.discovery.v0.definedvariationstable.UpdateResponse\x12\x66\n\rUpdateStarred\x12\x16.google.protobuf.Empty\x1a=.ansys.api.discovery.v0.definedvariationstable.UpdateResponse\x12\x62\n\tUpdateAll\x12\x16.google.protobuf.Empty\x1a=.ansys.api.discovery.v0.definedvariationstable.UpdateResponse\x12\x65\n\tIsSolving\x12\x16.google.protobuf.Empty\x1a@.ansys.api.discovery.v0.definedvariationstable.IsSolvingResponseB0\xaa\x02-Ansys.Api.Discovery.V0.DefinedVariationsTableb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.discovery.v0.definedvariationstable_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002-Ansys.Api.Discovery.V0.DefinedVariationsTable'
  _GETALLVARIATIONSRESPONSE._serialized_start=211
  _GETALLVARIATIONSRESPONSE._serialized_end=300
  _GETALLINPUTSRESPONSE._serialized_start=302
  _GETALLINPUTSRESPONSE._serialized_end=377
  _GETALLOUTPUTSRESPONSE._serialized_start=379
  _GETALLOUTPUTSRESPONSE._serialized_end=457
  _GETINPUTFORVARIATIONREQUEST._serialized_start=459
  _GETINPUTFORVARIATIONREQUEST._serialized_end=548
  _SETINPUTVALUEREQUEST._serialized_start=551
  _SETINPUTVALUEREQUEST._serialized_end=679
  _GETOUTPUTFORVARIATIONREQUEST._serialized_start=681
  _GETOUTPUTFORVARIATIONREQUEST._serialized_end=772
  _GETINPUTCOLUMNREQUEST._serialized_start=774
  _GETINPUTCOLUMNREQUEST._serialized_end=830
  _GETINPUTCOLUMNRESPONSE._serialized_start=832
  _GETINPUTCOLUMNRESPONSE._serialized_end=909
  _GETOUTPUTCOLUMNREQUEST._serialized_start=911
  _GETOUTPUTCOLUMNREQUEST._serialized_end=969
  _GETOUTPUTCOLUMNRESPONSE._serialized_start=971
  _GETOUTPUTCOLUMNRESPONSE._serialized_end=1050
  _SETSTARREDSTATUSREQUEST._serialized_start=1052
  _SETSTARREDSTATUSREQUEST._serialized_end=1123
  _GETCURRENTVARIATIONRESPONSE._serialized_start=1125
  _GETCURRENTVARIATIONRESPONSE._serialized_end=1198
  _UPDATERESPONSE._serialized_start=1200
  _UPDATERESPONSE._serialized_end=1249
  _ISSOLVINGRESPONSE._serialized_start=1251
  _ISSOLVINGRESPONSE._serialized_end=1290
  _DEFINEDVARIATIONSTABLE._serialized_start=1293
  _DEFINEDVARIATIONSTABLE._serialized_end=3303
# @@protoc_insertion_point(module_scope)
