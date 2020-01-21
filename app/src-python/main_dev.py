import sys
from pathlib import Path
SOURCE = Path(__file__).parent / 'backendapp'
sys.path.append(str(SOURCE / 'external'))
sys.path.append(str(SOURCE / 'protodef'))

from backendapp import grpc_server

grpc_server.serve()

