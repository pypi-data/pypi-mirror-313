# Build and Install


Create a new conda environment with `conda create -n intrepid python=3.10`

Activate environment with

```
conda activate intrepid
```

Install `poetry` with `pip install poetry` and all requirements `pip install -r requirements.txt`

Build Python Intrepid SDK

```Bash
poetry build
poetry install
```
And check that all has been installed correctly

```
python examples/ex0.py
```

This should print

```
Hello from Intrepid SDK
```


<!-- `python3 -m websockets ws://localhost:9999/` -->



# Example for showcasing Python bindings

## Create Python Node

A Python node is created from dashboard and rendered according to the Python function signature that is attached.

A Python SDK allows to
1. read from the output of a node and
2. write to the input of a node.

Rendering a node means defining inputs and outputs complete with types (only primitive types supported).

```Python
from intrepid import Intrepid, Qos


# Callback function to execute when inputs are ready
def my_callback_function(in1: int, in2:int) -> (float, bool):
    # Add code here
    time.sleep(0.2)
    return 1. * (in1 + in2), True


# Create QoS policy for function node
# Create QoS policy for function node
qos = Qos(reliability="BestEffort", durability="TransientLocal")
qos.set_history("KeepLast")
qos.set_deadline(100)  # Deadline expressed in milliseconds



# Create my node
mynode = Node("my_type")
mynode.add_input("flow", DataType.FLOW)
mynode.add_input("in1", DataType.INTEGER)
mynode.add_input("in2", DataType.INTEGER)
mynode.add_output("flow", DataType.FLOW)
mynode.add_output("out1", DataType.FLOAT)
mynode.add_output("is_float", DataType.BOOLEAN)


# Write to Graph
node_handler = Intrepid(node_id="node_type/node_id")
node_handler.register_node(mynode)

# Attach Qos policy to this node
node_handler.create_qos(qos)

# Register callback with node input. Callback and node inputs must have the same signature (same number/name/type)
node_handler.register_callback(my_callback_function)

# Start server and node execution
node_handler.start()
```

`node_id`, `input_id`, `output_id` are in the property section of the sidebar of the relative nodes.



## Create Node

A node in the Intrepid platform is a fundamental building block that represents a logical function, package, or module capable of performing computation on inputs and making results available on outputs. In the context of visual programming tools provided by Intrepid, a node is a block that users can drag and drop in the editor and connect with other nodes to create workflows or pipelines.

From a developer’s perspective, a node can be thought of as a container for custom logic implemented in Python, Rust, C/C++. Users who want to implement their own custom logic can create a node using Python, add their desired functionality, and publish it to the Intrepid graph. Once published, these custom nodes can be seamlessly integrated into the visual programming environment, allowing users to connect them with other nodes just like any other built-in node.

In summary, a node in Intrepid serves as a modular unit for encapsulating computational logic, enabling users to create custom functionalities and extend the capabilities of the platform’s visual programming tools.

An example node with 3 inputs and 3 outputs is provided below

```Python
# Create my node
mynode = Node("my_type")
mynode.add_input("flow", DataType.FLOW)
mynode.add_input("in1", DataType.INTEGER)
mynode.add_input("in2", DataType.INTEGER)
mynode.add_output("flow", DataType.FLOW)
mynode.add_output("out1", DataType.FLOAT)
mynode.add_output("is_float", DataType.BOOLEAN)
```


## Register Node

Once a node has been created with its desired logic implemented, it must be registered with the Intrepid engine to become operational within the platform’s ecosystem. Registration involves associating the node with the Intrepid engine, enabling it to be recognized and utilized by other components of the system.

After registration, the user needs to attach a callback function to the node. This callback function defines the specific actions or computations the node will perform when inputs are received. The callback function typically takes input data, processes it, and generates output data accordingly.

Once the callback function is attached, the node is ready to start executing its logic. Starting the node initiates its operation within the Intrepid environment, allowing it to actively process inputs, execute the defined logic, and produce output data as per its functionality.

Below is an example demonstrating the process of registering, attaching a callback, and starting a node in Python using the Python SDK:


```Python
# Write to Graph
node_handler = Intrepid(node_id="node_type/node_id")
node_handler.register_node(mynode)

# Attach Qos policy to this node
node_handler.create_qos(qos)
```
​
## Register Callback and Start Node

```Python
# Register callback with node input. Callback and node inputs must have the same signature (same number/name/type)
node_handler.register_callback(my_callback_function)

# Start server and node execution
node_handler.start()
```

This should show node info and status

```Bash
Created node  node/sdk/ex1
Attached QoS policy to node
Callback registered to node
Listening on host 127.0.0.1:9999

```

Node `node/sdk/ex1` is running a websocket server at `127.0.0.1:9999`



## Start Intrepid Runtime Core

Execute the Intrepid runtime (`intrepid-agent`) with arguments
`run-node` <node_name>
`--load ws://<host>:<port>` where the node is running
`-i input1`
`-i input2`


```Bash
./intrepid-agent run-node node/sdk/ex1 --load ws://127.0.0.1:9999 -i 1 -i 2
```

This should show

```Bash
2024-10-08T14:18:42.078Z INFO  [exec_graph_connector::plugins] remote plugin initialized: ws://127.0.0.1:9999
2024-10-08T14:18:42.104Z INFO  [exec_graph_connector::plugins] remote plugin initialized: ws://127.0.0.1:9999
2024-10-08T14:18:42.607Z INFO  [exec_graph_connector::agent_task] 3.0

```

The node is running and computing the callback function, and returning `3.0`

## Publish custom node

In order to be viewed from the dashboard and connected to the rest of the graph, a node must be published.
An authentication token is necessary to publish a node to a user library. Such token can be retrieved from dashboard at https://labs.intrepid.ai from the `Project` section on the left sidebar.


```Bash
./intrepid-agent publish node/sdk/ex1 --load ws://127.0.0.1:9999 https://labs.intrepid.ai/projects/34/r3Gvmurb5cYdrzMJVLFGotpm

```

If node is published correctly, this will be printed to stdout

```Bash
intrepid.ai/projects/34/Uy66ce2RCqqOniGLBuNGcaUu
2024-10-08T15:15:28.790Z INFO  [exec_graph_connector::plugins] remote plugin initialized: ws://127.0.0.1:9999
2024-10-08T15:15:28.795Z INFO  [exec_graph_connector::http] -> https://labs.intrepid.ai/api/nodes/sdk
2024-10-08T15:15:28.833Z INFO  [exec_graph_connector::http] <- 201, length: 43
```
