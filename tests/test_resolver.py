"""Unit tests for agent-git-conflict-semantic-resolver."""
import unittest
from agent_git_conflict_semantic_resolver.resolver import GitSemanticResolver

class TestSemanticResolver(unittest.TestCase):
    def test_independent_features_merged(self):
        base = "def base_fn(): pass"
        ours = "def base_fn(): pass" + chr(10) + "def fn_a(): return 'a'"
        theirs = "def base_fn(): pass" + chr(10) + "def fn_b(): return 'b'"
        res = GitSemanticResolver.merge_independent_functions(base, ours, theirs)
        self.assertTrue(res.resolved)
        self.assertIn("fn_a", res.merged_code)
        self.assertIn("fn_b", res.merged_code)

    def test_conflicting_implementations(self):
        base = "def target(): return 1"
        ours = "def target(): return 2"
        theirs = "def target(): return 3"
        res = GitSemanticResolver.merge_independent_functions(base, ours, theirs)
        self.assertFalse(res.resolved)
        self.assertIn("Conflicting", res.conflict_reasons[0])

if __name__ == "__main__":
    unittest.main()
