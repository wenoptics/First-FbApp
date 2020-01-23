python -m grpc_tools.protoc \
 -I./app/src/statics/protos \
  --python_out=./app/src-python/backendapp/protodef \
  --grpc_python_out=./app/src-python/backendapp/protodef \
   app/src/statics/protos/twindemo.proto

"Protobuf generation OK. Press ANY key to exit..."

read
pause
