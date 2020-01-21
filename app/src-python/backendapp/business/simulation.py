import os
import sys
import time
from pathlib import Path

from backendapp.external.twin_runtime import TwinRuntime
from backendapp.external.twin_runtime.log_level import LogLevel


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def get_log_path(twin_model_file):
    if not os.path.isfile(twin_model_file):
        raise RuntimeError('File does not exist: {}'.format(twin_model_file))
    return twin_model_file.replace('.twin', '.log')


def simulation_batch_csv(twin_model_file, input_file, runtime_log=None):

    # CUR_DIR = os.pathath.abspath(os.path.dirname(os.path.realpath(__file__)))
    # 
    # if not os.path.isabs(twin_model_file):
    #     twin_model_file = os.path.join(CUR_DIR, *twin_model_file.split(os.sep))

    if not os.path.isfile(twin_model_file):
        raise RuntimeError('File does not exist: {}'.format(twin_model_file))
    
    if not os.path.isfile(input_file):
        raise RuntimeError('File does not exist: {}'.format(twin_model_file))

    with open(input_file, 'r') as f:
        inputs = f.readlines()

    if not runtime_log:
        runtime_log = get_log_path(twin_model_file)

    # Load input and reference data
    twin_runtime = TwinRuntime(twin_model_file, runtime_log, log_level=LogLevel.TWIN_LOG_ALL)
    print('Model loaded!')
    twin_runtime.print_model_info(max_var_to_print=10)
    twin_runtime.twin_instantiate()
    print('Model instantiated!')
    twin_runtime.twin_set_inputs([float(v) for v in inputs[1].split(',')[1:]])

    twin_runtime.twin_initialize()
    print('Model initialized!')

    start = time.time()
    twin_runtime.twin_simulate_batch_mode_csv(input_file, 'runtime_output.csv')
    end = time.time()
    
    print('Simulation Finished! Time: {}s'.format(end - start))
    twin_runtime.twin_close()
    print('Model closed!')
