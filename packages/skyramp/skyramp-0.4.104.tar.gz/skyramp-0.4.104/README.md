# Skyramp
Skyramp is a pip module that provides utility functions for leveraging [Skyramp CLI](https://skyramp.dev/docs/reference/cli-commands/) commands. It offers functionalities to create and apply mock configurations for gRPC and REST APIs, as well as testing and asserting scenarios in various test environments. The package provides classes such as GrpcEndpoint, RestEndpoint, Scenario, and Client to facilitate these tasks.

## Installation
To install Skyramp, simply run the following command in your terminal:
```bash
pip install skyramp
```

## Usage
Once you've installed Skyramp, you can import it into your project like this:
```python
import skyramp
```

## Client
The Client class is the primary entry point to interact with the skyramp package. It allows you to apply configurations, start test scenarios, and deploy or delete workers. First, set up the Client with a Kubernetes cluster.

**Example: Provision Local Cluster with Skyramp**
```python
skyramp_client = skyramp.Client()
skyramp_client.apply_local()
```
Once you have a Client instance configured with a Kubernetes cluster, you can deploy the Skyramp Worker in-cluster to apply mocks and run tests.

**Example: Deploy Skyramp Worker**

### Deploy default worker image
```python
skyramp_client.deploy_skyramp_worker("test-worker")
```
### Deploy your custom worker image with added python packages (optional)
You can use additional python modules with mocker/tester and build your own extended "workerImage".  
[Building custom Worker Image](https://skyramp.dev/docs/docker/get-started/install-worker/#building-the-worker-image-with-python-modules)
```python
skyramp_client.deploy_skyramp_worker("test-worker", workerImage, True)
```

### RestEndpoint
The RestEndpoint class represents a REST API endpoint and provides methods to configure mock responses and apply them using the Client.

**Example: Create REST Mock Configuration**
```python
rest_endpoint = skyramp.RestEndpoint("artists", "", 50050, "api/openapi/artists.yaml")
rest_endpoint.mock_method_from_file("artists-GET", "files/rest-values.yaml")
skyramp_client.mocker_apply("test-worker", "", rest_endpoint)
```

### GrpcEndpoint
The GrpcEndpoint class represents a gRPC API endpoint and provides methods to configure mock responses and apply them using the Client.

**Example: Create gRPC Mock Configuration**
```python

def handler(req):
    return SkyrampValue(
        value={"message": req.value.name + "temp"}
    )       

grpc_endpoint = skyramp.GrpcEndpoint("helloworld", "Greeter", 50051, "../../../examples/pb/helloworld.proto")
mock_object = {
    "responseValue": {
        "name": "HelloReply",
        "blob": "{\n  \"message\": \"Hello!\"\n}"
    }
}
grpc_endpoint.mock_method("SayHello", mock_object)
skyramp_client.mocker_apply("test-worker", "", grpc_endpoint)
```

### Scenario
The Scenario class allows you to define test scenarios by specifying a sequence of API requests and assertions. Once a Scenario is created, you can start it using the Client instance.

**Example: Test Assert Scenario (REST)**
```python
scenario = skyramp.Scenario("rest-test")
step_name = scenario.add_request(endpoint=rest_endpoint, method_name="artists-GET")
scenario.add_assert_equal(f"{step_name}.res.message", "Hello!")
skyramp_client.tester_start("test-worker", "", scenario)
```

**Example: GRPC test assert with request chaining*

Sample dynamic handler for tester as external python script.
```
# filename scripts/request_handler.py

i = 0
def handler():
   """
   Sample dynamic handler that retreives a "name" variable from a test scenario
   and provides a json output, as the value of variable with a nummeric value.
   """
    global i
    i += 1
    return SkyrampValue(
        value= { "name": vars.name + str(i)}
    )
```

Protobuf API
```
// filename pb/helloworld.proto
syntax = "proto3";

option go_package = "google.golang.org/grpc/examples/helloworld/helloworld";
option java_multiple_files = true;
option java_package = "io.grpc.examples.helloworld";
option java_outer_classname = "HelloWorldProto";

package helloworld;

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

Chaining Mocker/Tester
```
# filename chaining.py
#!/usr/bin/env python
import os, skyramp

skyramp_client = skyramp.Client()

# Define a dynamic mock handler
def handler(req):
   """
   Sample mock handler that appends the litteral "mock" to the 
   received json field "name". 
   """
   return SkyrampValue(
     value={"message": req.value.name + "mock"}
   )

def test_chaining():
    """ Chaining test"""
    namespace = "chaining-test      "

    try:
        # create a local k8s cluster
        skyramp_client.apply_local()
        skyramp_client.deploy_skyramp_worker(namespace)

        # Mocker

        # generate grpc endpoint from protobuf file
        grpc_endpoint = skyramp.GrpcEndpoint(name='helloworld', service='Greeter', port=50050, pb_file='pb/helloworld.proto')

        response = skyramp.ResponseValue(
            name="response",
            python_function=handler,
            endpoint_descriptor=grpc_endpoint,
            method_name="SayHello")

        # Mocker apply
        skyramp_client.mocker_apply_v1(namespace, "", [response])


        # Tester with dynamic request with global variables. 

        # define variable name
        request_var = {
            "name": "name"
        }

        request1 = skyramp.Request(
            name="request1",
            endpoint_descriptor=grpc_endpoint,
            method_name="SayHello",
            python_path="scripts/request_handler.py",
            vars_ = request_var,
        )
        #

        # Tester with request chaining

        scenario = skyramp.Scenario("scenario1")
        step1 = scenario.add_request_v1(request=request1)
        step1_value = step1.get_response_value("message")
        scenario.add_assert_v1(assert_step=skyramp.Assert(step1_value, "name1mock"))
        # Expected response from the dynamic mock handler is "name1mock"

        step2 = scenario.add_request_v1(request=request1)
        step2_value = step2.get_response_value("message")

        # Overide the variable "name" with output from previous step "name1mock"
        step2.set_value({"name": step1_value})

        # The dynamic mock handler returns the "name" field with appended "mock" literal
        scenario.add_assert_v1(assert_step=skyramp.Assert(step2_value, "name1mock1mock"))
        step3 = scenario.add_request_v1(request=request1)
        step3_value = step3.get_response_value("message")

        # Overide the variable "name" with output from previous step "name1mock1mock"
        step3.set_value({"name": step2_value})
        # Overide the variable "name" with output from previous step "name1mock1mock1mock"
        scenario.add_assert_v1(assert_step=skyramp.Assert(step3_value, "name1mock1mock1mock"))
    
        skyramp_client.tester_start_v1(scenario, None, namespace, "", "test-chaining", True)
        skyramp_client.delete_skyramp_worker(namespace)
        skyramp_client.remove_local()

    except Exception as e:
        print(f"An error occurred: {e}")
        assert False, f"Test failed with error: {e}"
    print("Test succeeded.")

if __name__== "__main__":
   test_chaining() 
```