"""Python code transform plugin module"""

from collections.abc import Sequence
from typing import Any

from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.parameter.code import PythonCode
from cmem_plugin_base.dataintegration.plugins import TransformPlugin

EXAMPLE_CODE = """result = str(inputs) """

documentation = """
This transform operator allows the execution of arbitrary Python source code inside of a
transformation 😈

The following variable is available in the scope of the code execution:

- `inputs` - a `Sequence` of `Sequence[str)`, which represents the data which is passed
   to the operator in the transformation. The inner sequence is the list of values
   from an input port while the outer sequence represents the list of ports.

In order to provide data for the next operator in the transformation, a `result`
variable of type `Sequence[str]` needs to be prepared.
"""


@Plugin(
    label="Python Code",
    plugin_id="cmem_plugin_python-transform",
    documentation=documentation,
    parameters=[
        PluginParameter(name="source_code", label="Source Code", default_value=EXAMPLE_CODE),
    ],
)
class PythonCodeTransformPlugin(TransformPlugin):
    """Python Code Transform Plugin"""

    def __init__(self, source_code: PythonCode):
        self.source_code = source_code

    def transform(self, inputs: Sequence[Sequence[str]]) -> Sequence[str]:
        """Transform a collection of values."""
        self.log.info("Start doing bad things with custom code.")
        scope: dict[str, Any] = {"inputs": inputs}
        exec(str(self.source_code), scope)  # nosec # noqa: S102
        result: Sequence[str] = scope["result"]
        return result
