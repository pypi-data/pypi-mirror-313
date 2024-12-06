from typing import Dict, Any

class Schema(Dict[str, type]):
    """Base class for input and output schemas."""
    def __init__(self, schema: Dict[str, type]):
        self._validate_schema(schema)
        super().__init__(schema)

    @staticmethod
    def _validate_schema(schema: Dict[str, type]) -> None:
        if not all(isinstance(v, type) for v in schema.values()):
            raise TypeError("Schema values must be types")

class InputSchema(Schema):
    """Input schema for a workflow."""

class OutputSchema(Schema):
    """Output schema for a workflow."""

class Input(Dict[str, Any]):
    """Input for a workflow."""

class Output(Dict[str, Any]):
    """Output for a workflow."""