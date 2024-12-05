from typing import List, Any, Dict, Optional

from checkov.common.graph.checks_infra.enums import Operators
from checkov.common.graph.checks_infra.solvers.base_solver import BaseSolver
from checkov.common.checks_infra.solvers.complex_solvers.base_complex_solver import BaseComplexSolver
from functools import reduce
from operator import and_


class AndSolver(BaseComplexSolver):
    operator = Operators.AND  # noqa: CCE003  # a static attribute

    def __init__(self, solvers: List[BaseSolver], resource_types: List[str]) -> None:
        super().__init__(solvers, resource_types)

    def _get_operation(self, *args: Any, **kwargs: Any) -> Any:
        return reduce(and_, args)

    def get_operation(self, vertex: Dict[str, Any]) -> Optional[bool]:
        has_unrendered_attribute = False
        for solver in self.solvers:
            operation = solver.get_operation(vertex)
            if operation is None:
                has_unrendered_attribute = True
            elif not operation:
                return False
        return None if has_unrendered_attribute else True
