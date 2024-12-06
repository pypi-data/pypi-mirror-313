from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class CompilerParameters(ABC):
    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        return {}


class SolcParameters(CompilerParameters):
    def __init__(self, optimizer_on: bool, optimizer_runs: Optional[int], via_ir: bool):
        self.optimizer_on = optimizer_on
        self.optimizer_runs = optimizer_runs
        self.via_ir = via_ir
        CompilerParameters.__init__(self)

    def as_dict(self) -> Dict[str, Any]:
        as_dict = CompilerParameters.as_dict(self)
        as_dict.update({"optimizerOn": self.optimizer_on, "optimizerRuns": self.optimizer_runs, "viaIR": self.via_ir,
                        "type": "SolcParameters"})
        return as_dict
