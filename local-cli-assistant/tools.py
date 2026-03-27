"""
Safe helper tools for local inspection.
Version 1 keeps all tools read-only.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import ast
import operator as op

from config import READ_FILE_CHAR_LIMIT, LIST_FILES_LIMIT, GREP_MATCH_LIMIT


def list_files(path: str = ".") -> str:
    """
    List files under the provided path, capped for safety/readability.
    """
    root = Path(path).expanduser().resolve()

    if not root.exists():
        return f"Path does not exist: {root}"

    results: list[str] = []
    for item in root.rglob("*"):
        if len(results) >= LIST_FILES_LIMIT:
            results.append("... output truncated ...")
            break
        results.append(str(item.relative_to(root)))

    return "\n".join(results) if results else "(no files found)"


def read_file(path: str) -> str:
    """
    Read a text file with a size cap.
    """
    file_path = Path(path).expanduser().resolve()

    if not file_path.exists():
        return f"File does not exist: {file_path}"

    if not file_path.is_file():
        return f"Not a file: {file_path}"

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"Unable to read as UTF-8 text: {file_path}"

    if len(text) > READ_FILE_CHAR_LIMIT:
        return text[:READ_FILE_CHAR_LIMIT] + "\n\n... output truncated ..."
    return text


def grep_text(pattern: str, path: str = ".") -> str:
    """
    Search recursively for a text pattern using grep.
    """
    try:
        result = subprocess.run(
            ["grep", "-RIn", pattern, path],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        return f"grep failed: {exc}"

    output = result.stdout.strip() or result.stderr.strip() or "(no matches)"
    lines = output.splitlines()

    if len(lines) > GREP_MATCH_LIMIT:
        lines = lines[:GREP_MATCH_LIMIT] + ["... output truncated ..."]

    return "\n".join(lines)


def git_status(path: str = ".") -> str:
    """
    Return git status --short for a repository.
    """
    try:
        result = subprocess.run(
            ["git", "-C", path, "status", "--short"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        return f"git status failed: {exc}"

    return result.stdout.strip() or result.stderr.strip() or "(clean working tree)"


def git_diff_staged(path: str = ".") -> str:
    """
    Return staged git diff.
    """
    try:
        result = subprocess.run(
            ["git", "-C", path, "diff", "--staged"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        return f"git diff --staged failed: {exc}"

    return result.stdout.strip() or result.stderr.strip() or "(no staged changes)"


def git_diff_unstaged(path: str = ".") -> str:
    """
    Return unstaged git diff.
    """
    try:
        result = subprocess.run(
            ["git", "-C", path, "diff"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:
        return f"git diff failed: {exc}"

    return result.stdout.strip() or result.stderr.strip() or "(no unstaged changes)"


_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Unsupported expression")


def calculate(expression: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval_node(parsed.body)
        return str(result)
    except Exception as exc:
        return f"Calculation error: {exc}"
