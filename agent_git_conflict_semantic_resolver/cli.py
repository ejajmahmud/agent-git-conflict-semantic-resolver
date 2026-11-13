"""CLI for agent-git-conflict-semantic-resolver."""
import sys
import argparse
from .resolver import GitSemanticResolver

def main():
    parser = argparse.ArgumentParser(description="Agent Git Conflict Semantic Resolver CLI")
    parser.add_argument("--demo", action="store_true", help="Run semantic AST merge demo")
    args = parser.parse_args()

    if args.demo:
        base = "def common(): pass"
        ours = "def common(): pass" + chr(10) + "def feature_a(): return 1"
        theirs = "def common(): pass" + chr(10) + "def feature_b(): return 2"
        res = GitSemanticResolver.merge_independent_functions(base, ours, theirs)
        print(f"[+] Merge resolved: {res.resolved}")
        print(f"[+] Merged code:
{res.merged_code}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
