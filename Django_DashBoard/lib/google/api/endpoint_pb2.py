# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/endpoint.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x19google/api/endpoint.proto\x12\ngoogle.api"Q\n\x08\x45ndpoint\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x07\x61liases\x18\x02 \x03(\tB\x02\x18\x01\x12\x0e\n\x06target\x18\x65 \x01(\t\x12\x12\n\nallow_cors\x18\x05 \x01(\x08\x42o\n\x0e\x63om.google.apiB\rEndpointProtoP\x01ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\xa2\x02\x04GAPIb\x06proto3'
)


_ENDPOINT = DESCRIPTOR.message_types_by_name["Endpoint"]
Endpoint = _reflection.GeneratedProtocolMessageType(
    "Endpoint",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENDPOINT,
        "__module__": "google.api.endpoint_pb2"
        # @@protoc_insertion_point(class_scope:google.api.Endpoint)
    },
)
_sym_db.RegisterMessage(Endpoint)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\016com.google.apiB\rEndpointProtoP\001ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\242\002\004GAPI"
    _ENDPOINT.fields_by_name["aliases"]._options = None
    _ENDPOINT.fields_by_name["aliases"]._serialized_options = b"\030\001"
    _ENDPOINT._serialized_start = 41
    _ENDPOINT._serialized_end = 122
# @@protoc_insertion_point(module_scope)
