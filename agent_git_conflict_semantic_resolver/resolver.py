"""3-way AST semantic git merge resolver."""
import ast
from typing import Dict, List, Optional, Tuple, Any

class MergeOutcome:
    def __init__(self, resolved: bool, merged_code: str, conflict_reasons: List[str]):
        self.resolved = resolved
        self.merged_code = merged_code
        self.conflict_reasons = conflict_reasons

class GitSemanticResolver:
    """Resolves independent top-level function additions using AST node unification."""

    @staticmethod
    def merge_independent_functions(base_code: str, ours_code: str, theirs_code: str) -> MergeOutcome:
        try:
            tree_base = ast.parse(base_code)
            tree_ours = ast.parse(ours_code)
            tree_theirs = ast.parse(theirs_code)
        except Exception as e:
            return MergeOutcome(False, "", [f"AST parse error: {e}"])

        def get_func_dict(tree: ast.AST) -> Dict[str, ast.FunctionDef]:
            return {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

        base_funcs = get_func_dict(tree_base)
        ours_funcs = get_func_dict(tree_ours)
        theirs_funcs = get_func_dict(tree_theirs)

        merged_body: List[ast.stmt] = []
        conflicts = []

        all_names = list(base_funcs.keys())
        for n in ours_funcs:
            if n not in all_names:
                all_names.append(n)
        for n in theirs_funcs:
            if n not in all_names:
                all_names.append(n)

        for name in all_names:
            in_base = name in base_funcs
            in_ours = name in ours_funcs
            in_theirs = name in theirs_funcs

            if in_ours and in_theirs:
                # Compare AST dumps
                if ast.dump(ours_funcs[name]) == ast.dump(theirs_funcs[name]):
                    merged_body.append(ours_funcs[name])
                else:
                    conflicts.append(f"Conflicting modifications to function '{name}'")
            elif in_ours and not in_theirs:
                if not in_base:
                    merged_body.append(ours_funcs[name])
            elif in_theirs and not in_ours:
                if not in_base:
                    merged_body.append(theirs_funcs[name])

        if conflicts:
            return MergeOutcome(False, "", conflicts)

        merged_module = ast.Module(body=merged_body, type_ignores=[])
        ast.fix_missing_locations(merged_module)
        return MergeOutcome(True, ast.unparse(merged_module), [])
