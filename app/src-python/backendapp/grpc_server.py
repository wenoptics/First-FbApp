from concurrent import futures
import logging

import grpc

from backendapp.business.simulation import simulation_batch_csv, get_log_path, check_file_exists
from backendapp.protodef import twindemo_pb2_grpc, twindemo_pb2


class TwinServicer(twindemo_pb2_grpc.TwinServicer):
    def CheckFileTwin(self, request, context):
        return twindemo_pb2.CheckFileResult(is_success=check_file_exists(request.file_path))

    def CheckFileInputCSV(self, request, context):
        return twindemo_pb2.CheckFileResult(is_success=check_file_exists(request.file_path))

    def SimulateBatchCSV(self, request: twindemo_pb2.SimulationInput, context):
        log_file = None
        is_success = True
        msg = None
        
        try:
            log_file = get_log_path(request.model_file_path)
            simulation_batch_csv(request.model_file_path, request.input_file_path)
        except Exception as e:
            is_success = False
            msg = str(e)
        finally:
            log = open(log_file).read() if log_file else None
            return twindemo_pb2.SimulationResponse(is_success=is_success, log=log, message=msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    twindemo_pb2_grpc.add_TwinServicer_to_server(TwinServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('grpc server started')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
