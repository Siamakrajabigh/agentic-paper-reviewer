from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AgentResult:
    output: Any
    logs: Dict[str, Any]
