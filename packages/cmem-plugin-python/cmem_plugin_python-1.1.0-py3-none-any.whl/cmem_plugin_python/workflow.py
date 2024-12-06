"""Python code workflow plugin module"""

from collections.abc import Sequence
from types import SimpleNamespace
from typing import Any

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Icon, Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import Entities
from cmem_plugin_base.dataintegration.parameter.code import PythonCode
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin

docu_links = SimpleNamespace()
docu_links.entities = (
    "https://documentation.eccenca.com/latest/develop/python-plugins/development/#entities"
)
docu_links.context = (
    "https://documentation.eccenca.com/23.3/develop/python-plugins/development/#context-objects"
)

examples_init = SimpleNamespace()
examples_init.no_input_ports = """# no input ports (empty list)
# e.g. if you fetch data from the web
from cmem_plugin_base.dataintegration import ports
input_ports = ports.FixedNumberOfInputs([])"""
examples_init.single_input_flexible = """# A single port with flexible schema
# e.g. to process everything that comes in
from cmem_plugin_base.dataintegration import ports
input_ports = ports.FixedNumberOfInputs(
    [ports.FlexibleSchemaPort()]
)"""
examples_init.single_input_fixed = """# A single port with a fixed schema
# e.g. to fetch data from a dataset
from cmem_plugin_base.dataintegration import ports, entity
my_schema = entity.EntitySchema(
    type_uri="urn:x-example:output",
    paths=[
        entity.EntityPath("name"),
        entity.EntityPath("description")
    ]
)
input_ports = ports.FixedNumberOfInputs(
    [ports.FixedSchemaPort(schema=my_schema)]
)"""
examples_init.no_output = """# no output port
# e.g. if you post data to the web
output_port = None"""
examples_init.fixed_output = """# An output port with a fixed schema
from cmem_plugin_base.dataintegration import ports, entity
my_schema = entity.EntitySchema(
    type_uri="urn:x-example:output",
    paths=[
        entity.EntityPath("name"),
        entity.EntityPath("description")
    ]
)
output_port = ports.FixedSchemaPort(schema=my_schema)"""

examples_execute = SimpleNamespace()
examples_execute.take_first = """# take the entities from the first input port
# and copy it to the output port
try:
    result = inputs[0]
except IndexError:
    raise ValueError("Please connect a task to the first input port.")
"""
examples_execute.randoms = """# Create 1000 random strings and output them with a custom schema
from uuid import uuid4
from secrets import token_hex
from cmem_plugin_base.dataintegration import entity
my_schema = entity.EntitySchema(
    type_uri="urn:x-example:random",
    paths=[entity.EntityPath("random")]
)
entities = []
for _ in range(1000):
    entity_uri = "urn:uuid:" + str(uuid4())
    values = [[token_hex(10)]]
    entities.append(
        entity.Entity(uri=entity_uri, values=values)
    )
result = entity.Entities(entities=entities, schema=my_schema)
"""

cmem = "Corporate Memory"
documentation = f"""
This workflow task allows the execution of arbitrary Python source code as a workflow task 😈

The "configuration" is split into two code fields: initialization and execution.

## <a id="parameter_doc_init_code">Initialization</a>

The initialization code is executed on task creation and task update.
It is optional and can be used to configure the input and output ports of the task as well as to
prepare data for the execution phase.
Note that the execution scope of this code is empty.
All used objects need to be imported first.

### Specify input ports

To specify input ports, you have to define the variable `input_ports`.
Here are some valid examples.
If you do not specify any input ports, the default
behavior is a flexible number of flexible schema input ports.

``` python
{examples_init.no_input_ports}
```

``` python
{examples_init.single_input_flexible}
```

``` python
{examples_init.single_input_fixed}
```

### Specify the output port

To specify the output port, you have to define the variable `output_port`.
Here are some valid examples.
If you do not specify the output port, the default behavior is a flexible schema output port.

``` python
{examples_init.no_output}
```

``` python
{examples_init.fixed_output}
```

### Additional Data

In addition to input and output port specifications, you can provide additional data for
the task execution phase by manipulating the `data` dictionary.

``` python
data["my_schema"] = my_schema  # in case you used a schema example above
data["output"] = ":-)"
```

## <a id="parameter_doc_execute_code">Execution</a>

The execution code is interpreted in the context of an executed workflow.
The following variables are available in the scope of the code execution:

- `inputs` - a `Sequence` of `Entities`, which represents the data which will be passed to
   the to task in the workflow. Have a look at [the entities documentation]({docu_links.entities})
   for more information.
- `context` - an `ExecutionContext` object, which holds information about the system,
   the user the current task, and more. Have a look at
   [the context object documentation]({docu_links.context}) for more information.
- `data` - a `dict` of arbitrary data, which was optionally added by the initialization code.

To provide data for the next workflow task in the workflow, a `result`
variable of type `Entities` needs to be prepared.

Here are some valid examples:

``` python
{examples_execute.take_first}
```

``` python
{examples_execute.randoms}
```

### Using {cmem} APIs

To access {cmem} APIs, initialize the authentication environment with the following code:

``` python
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access
setup_cmempy_user_access(context.user)
```

This ensures that all {cmem} API requests, made with `cmempy` are authenticated using
the current user session.
"""


@Plugin(
    label="Python Code",
    icon=Icon(file_name="python_icon.svg", package=__package__),
    plugin_id="cmem_plugin_python-workflow",
    description="Run arbitrary Python code as a workflow task.",
    documentation=documentation,
    parameters=[
        PluginParameter(
            name="init_code",
            label="Python source code for the initialization phase.",
            default_value="",
        ),
        PluginParameter(
            name="execute_code",
            label="Python source code for the execution phase",
            default_value="",
        ),
    ],
)
class PythonCodeWorkflowPlugin(WorkflowPlugin):
    """Python Code Workflow Plugin"""

    init_code: str
    execute_code: str
    data: dict

    def __init__(self, init_code: PythonCode, execute_code: PythonCode):
        self.init_code = str(init_code)
        self.execute_code = str(execute_code)
        self.data = {}
        scope: dict[str, Any] = {"data": self.data}
        exec(str(self.init_code), scope)  # nosec  # noqa: S102
        if "input_ports" in scope:
            self.input_ports = scope["input_ports"]
        if "output_port" in scope:
            self.output_port = scope["output_port"]
        self.data = scope.get("data", {})

    def execute(self, inputs: Sequence[Entities], context: ExecutionContext) -> Entities | None:
        """Start the plugin in workflow context."""
        self.log.info("Start doing bad things with custom code.")
        scope: dict[str, Any] = {"inputs": inputs, "context": context, "data": self.data}
        exec(str(self.execute_code), scope)  # nosec  # noqa: S102
        return scope.get("result")
