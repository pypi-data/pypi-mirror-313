# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import unittest

from typing import Any

from tests.utils import testutils
import tests.protos as protos

from azure_functions_worker.handle_event import (Status,
                                                 worker_init_request,
                                                 functions_metadata_request,
                                                 function_load_request,
                                                 function_environment_reload_request)


class WorkerRequest:
    def __init__(self, name: str, request: Any, properties: dict):
        self.name = name
        self.request = request
        self.properties = properties


class InnerRequest:
    def __init__(self, name: Any):
        self.worker_init_request = name
        self.function_load_request = name
        self.function_environment_reload_request = name


class InnerInnerRequest:
    def __init__(self, name: Any):
        self.capabilities = name
        self.function_app_directory = "C:\\Users\\victoriahall\\Documents\\repos\\azure-functions-python-worker-313\\tests\\unit_tests\\default_template"
        self.function_id = 1
        self.metadata = Metadata(name="default_template")
        self.environment_variables = {}


class Metadata:
    def __init__(self, name: Any):
        self.name = name
        self.directory = 'C:\\Users\\victoriahall\\Documents\\repos\\basic-http-v1\\HttpTrigger1'
        self.script_file = 'C:\\Users\\victoriahall\\Documents\\repos\\basic-http-v1\\HttpTrigger1\\__init__.py'
        self.entry_point = ""
        self.bindings = {'req': Binding("httpTrigger"), '$return': Binding("http", 1)}
        self.environment_variables = {}


class Binding:
    def __init__(self, type, direction=""):
        self.type = type
        self.direction = direction


class TestObjects(unittest.TestCase):
    def test_stringify_enum(self):
        pass

    def test_status(self):
        pass

    def test_worker_response(self):
        pass


class TestHandleEvent(testutils.AsyncTestCase):
    async def test_worker_init_request(self):
        worker_request = WorkerRequest(name='worker_init_request',
                                       request=InnerRequest(InnerInnerRequest('hello')),
                                       properties={'host': '123',
                                                   'protos': protos})
        result = await worker_init_request(worker_request)
        self.assertEqual(result.name, "worker_init_request")
        self.assertEqual(result.status, Status.SUCCESS)
        self.assertEqual(result.result.get('capabilities'), {'RawHttpBodyBytes': 'true', 'RpcHttpBodyOnly': 'true', 'RpcHttpTriggerMetadataRemoved': 'true', 'SharedMemoryDataTransfer': 'true', 'TypedDataCollection': 'true', 'WorkerStatus': 'true'})
        self.assertEqual(result.exception, None)

    def test_worker_init_request_with_streaming(self):
        pass

    def test_worker_init_request_with_exception(self):
        pass

    async def test_functions_metadata_request(self):
        worker_request = WorkerRequest(name='functions_metadata_request',
                                       request=InnerRequest(InnerInnerRequest('hello')),
                                       properties={})
        result = await functions_metadata_request(worker_request)
        self.assertEqual(result.name, "functions_metadata_request")
        self.assertEqual(result.status, Status.SUCCESS)
        self.assertEqual(result.result, None)
        self.assertEqual(result.exception, None)

    def test_functions_metadata_request_with_exception(self):
        pass

    async def test_functions_load_request(self):
        worker_request = WorkerRequest(name='functions_load_request',
                                       request=InnerRequest(InnerInnerRequest('hello')),
                                       properties={'protos': protos})
        init_result = await worker_init_request(worker_request)
        result = await function_load_request(worker_request)
        self.assertEqual(result.name, "functions_load_request")
        self.assertEqual(result.status, Status.SUCCESS)
        self.assertEqual(result.result, {"function_id": 1})
        self.assertEqual(result.exception, None)

    def test_invocation_request_sync(self):
        pass

    def test_invocation_request_async(self):
        pass

    def test_invocation_request_with_exception(self):
        pass

    async def test_function_environment_reload_request(self):
        worker_request = WorkerRequest(name='function_environment_reload_request',
                                       request=InnerRequest(InnerInnerRequest('hello')),
                                       properties={'host': '123',
                                                   'protos': protos})
        result = await function_environment_reload_request(worker_request)
        self.assertEqual(result.name, "function_environment_reload_request")
        self.assertEqual(result.status, Status.SUCCESS)
        self.assertEqual(result.result.get('capabilities'), {})
        self.assertEqual(result.exception, None)

    def test_function_environment_reload_request_with_streaming(self):
        pass

    def test_function_environment_reload_request_with_exception(self):
        pass

    def test_load_function_metadata(self):
        pass

    def test_index_functions(self):
        pass
