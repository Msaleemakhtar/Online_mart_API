# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x10usermicroservice\x1a\x1fgoogle/protobuf/timestamp.proto\"1\n\x05Token\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\t\"_\n\x08GptToken\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\t\x12\x12\n\nexpires_in\x18\x03 \x01(\x05\x12\x15\n\rrefresh_token\x18\x04 \x01(\t\"\x1d\n\tTokenData\x12\x10\n\x08username\x18\x01 \x01(\t\"V\n\x08UserRead\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tfull_name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\x04 \x01(\x08\"\xd7\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\x05 \x01(\x08\x12\x17\n\x0fhashed_password\x18\x06 \x01(\t\x12.\n\nupdated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"l\n\x0cUserRegister\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tfull_name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\x04 \x01(\x08\x12\x10\n\x08password\x18\x05 \x01(\t\"{\n\x08UserInDb\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\x05 \x01(\x08\x12\x17\n\x0fhashed_password\x18\x06 \x01(\t\"d\n\nUserOutput\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\x05 \x01(\x08\"\x90\x01\n\rLoginResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\t\x12*\n\x04user\x18\x03 \x01(\x0b\x32\x1c.usermicroservice.UserOutput\x12\x12\n\nexpires_in\x18\x04 \x01(\x05\x12\x15\n\rrefresh_token\x18\x05 \x01(\t\"i\n\rUserOperation\x12\x32\n\toperation\x18\x01 \x01(\x0e\x32\x1f.usermicroservice.OperationType\x12$\n\x04user\x18\x02 \x01(\x0b\x32\x16.usermicroservice.User*3\n\rOperationType\x12\n\n\x06\x43REATE\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OPERATIONTYPE._serialized_start=1141
  _OPERATIONTYPE._serialized_end=1192
  _TOKEN._serialized_start=65
  _TOKEN._serialized_end=114
  _GPTTOKEN._serialized_start=116
  _GPTTOKEN._serialized_end=211
  _TOKENDATA._serialized_start=213
  _TOKENDATA._serialized_end=242
  _USERREAD._serialized_start=244
  _USERREAD._serialized_end=330
  _USER._serialized_start=333
  _USER._serialized_end=548
  _USERREGISTER._serialized_start=550
  _USERREGISTER._serialized_end=658
  _USERINDB._serialized_start=660
  _USERINDB._serialized_end=783
  _USEROUTPUT._serialized_start=785
  _USEROUTPUT._serialized_end=885
  _LOGINRESPONSE._serialized_start=888
  _LOGINRESPONSE._serialized_end=1032
  _USEROPERATION._serialized_start=1034
  _USEROPERATION._serialized_end=1139
# @@protoc_insertion_point(module_scope)
