"""
Contains internal utilities
"""

import platform
import os
import ctypes
import argparse
import random

SKYRAMP_YAML_VERSION = "v1"

def _generate_hex_string(length):
    hex_digits = "0123456789abcdef"
    return "".join(random.choice(hex_digits) for _ in range(length))

def _get_c_library():
    system = platform.system().lower()
    machine = platform.machine().lower()

    lib_dir = os.path.join(os.path.dirname(__file__), "lib")
    lib_file = ""

    if system == "darwin":
        if machine in ["amd64", "x86_64"]:
            lib_file = "dev-darwin-amd64.dylib"
        elif machine == "arm64":
            lib_file = "dev-darwin-arm64.dylib"
    elif system == "linux":
        if machine in ["amd64", "x86_64"]:
            lib_file = "dev-linux-amd64.so"
        elif machine == "ia32":
            lib_file = "dev-linux-386.so"
    elif system == "win32":
        lib_file = "dev-windows-amd64.dll"

    if lib_file == "":
        raise Exception(
            f"unsupported system and architecture. System: {system}, Architecture: {machine}"
        )

    lib_path = os.path.join(lib_dir, lib_file)

    return ctypes.cdll.LoadLibrary(lib_path)

def _call_function(func, argtypes, restype, args, return_output=False):
    func.argtypes = argtypes
    func.restype = restype

    output = func(*args)
    if not output:
        return None

    output_bytes = ctypes.string_at(output)
    output = output_bytes.decode()

    if return_output:
        return output

    # If output is not expected, the result output is parsed as an exception
    if len(output) > 0:
        raise Exception(output)

    return None

def add_unique_items(target_list, source_list):
    """
    Add unique items from the source_list to the target_list.

    Args:
        target_list (list): The list where unique items will be added.
        source_list (list): The list containing items to be added to the target_list.
    """
    for item in source_list:
        if item not in target_list:
            target_list.append(item)

def _convert_nested_list_to_dict(target_list):
    flattened = [item for row in target_list for item in row]
    ret = {}
    for pair in flattened:
        try:
            fields = pair.split('=')
            key = fields[0]
            value = fields[1]
            ret[key] = value
        except IndexError:
            print(f"failed to parse { pair }")
            continue
    return ret


def parse_mocker_args():
    """
    parse command line arguments for Skyramp generated mock files
    """
    parser = argparse.ArgumentParser(description="Skyramp generated mock file")

    # worker in non-k8s env
    parser.add_argument('--address', help='Skyramp worker address', dest="address",
                        default=None)
    # worker in k8s env
    parser.add_argument('--kubeconfig', help='Path to k8s config', dest="kubeconfig",
                        default=None)
    parser.add_argument("--kube-context", help='k8s config context', dest="kubecontext",
                        default=None)
    parser.add_argument("--cluster-name", help="cluster name registered with Skyramp",
                        dest="cluster_name", default=None)
    parser.add_argument("--namespace", help="Skyramp worker's namespace", dest="namespace",
                        default=None)

    # any additional args
    parser.add_argument('--extra-vars', help='Extra variables',
                        dest='extra_vars', nargs='+', action='append', default=None)

    args = parser.parse_args()

    new_args = {}
    for key, value in args.__dict__.items():
        if value is not None:
            new_args[key] = value

    return new_args


def parse_args():
    """
    parse command line arguments for Skyramp generated test files
    """
    parser = argparse.ArgumentParser(description="Skyramp generated test file")

    # generic worker releated
    parser.add_argument(
        "--deploy-worker",
        help="Deploy Skyramp worker",
        dest="deploy_worker",
        default=False,
        type=bool,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--worker-image",
        help="Skyramp worker image",
        dest="worker_image",
        default="public.ecr.aws/j1n2c2p2/rampup/worker:latest",
    )

    # worker in non-k8s env
    parser.add_argument('--address', help='Skyramp worker address', dest="address",
                        default=None)
    parser.add_argument(
        "--docker-network",
        help="Docker network for deploying Skyramp worker",
        dest="docker_network",
        default=None,
    )
    parser.add_argument( "--docker-service-alias",
        #pylint: disable=line-too-long
        help="Docker service alias used for deploying worker in the same docker network as the service under test",
        dest="docker_service_alias",default="",
    )
    # worker in k8s env
    parser.add_argument('--kubeconfig', help='Path to k8s config', dest="kubeconfig",
                        default=None)
    parser.add_argument("--kube-context", help='k8s config context', dest="kubecontext",
                        default=None)
    parser.add_argument("--cluster-name", help="cluster name registered with Skyramp",
                        dest="cluster_name", default=None)
    parser.add_argument("--namespace", help="Skyramp worker's namespace", dest="namespace",
                        default=None)

    parser.add_argument('--override-code-path', help='Skyramp override assert code path',
                        dest='override_code_path', default=None)
    parser.add_argument('--endpoint-address', help='Endpoint addreess override',
                        dest='endpoint_address', default=None)
    parser.add_argument('--skip-verify', help='Skip CA verification',
                        dest='skip_verify', default=None)
    parser.add_argument('--global-vars', help='Global variables',
                        dest='global_vars', nargs='+', action='append', default=None)
    parser.add_argument('--blobs', help='Blob overrides',
                        dest='blobs', nargs='+', action='append', default=None)
    parser.add_argument('--synchronous', help='execute in synchronous mode', type=bool,
                        dest='synchronous', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--test-name', help='Test name override',
                        dest='override_test_name', default=None)

    # load test related
    parser.add_argument('--duration', help='Duration for load test', type=str,
                        dest='duration', default=None)
    parser.add_argument('--at-once', help='Number of threads for load test', type=int,
                        dest='at_once', default=None)
    parser.add_argument('--count', help='Number of repeat for load test', type=int,
                        dest='count', default=None)
    parser.add_argument('--rampup-interval', help='Ramp up interval for load test', type=str,
                        dest='rampup_interval', default=None)
    parser.add_argument('--rampup-duration', help='Ramp up duration for load test', type=str,
                        dest='rampup_duration', default=None)
    parser.add_argument('--target-rps', help='Target RPS for load test', type=int,
                        dest='target_rps', default=None)
    parser.add_argument('--stop-on-failure', help='Stop on failure for load test', type=bool,
                        dest='stop_on_failure', default=False)

    # any additional args
    parser.add_argument('--extra-vars', help='Extra variables',
                        dest='extra_vars', nargs='+', action='append', default=None)
    parser.add_argument('--labels', help='Labels for test scenarios',
                        dest='override_labels', nargs='+', action='append', default=None)

    args = parser.parse_args()

    if args.global_vars is not None:
        args.global_vars = _convert_nested_list_to_dict(args.global_vars)
    if args.blobs is not None:
        args.blobs = _convert_nested_list_to_dict(args.blobs)
    if args.extra_vars is not None:
        args.extra_vars = _convert_nested_list_to_dict(args.extra_vars)
    if args.override_labels is not None:
        args.override_labels = _convert_nested_list_to_dict(args.override_labels)

    new_args = {}
    for key, value in args.__dict__.items():
        if value is not None:
            new_args[key] = value

    return new_args

_library = _get_c_library()

if _library is None:
    raise Exception("failed to load Skyramp C library")
