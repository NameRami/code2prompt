from pathlib import Path
import argparse

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".pdf", ".zip", ".tar", ".gz", ".7z",
    ".exe", ".dll", ".so",
    ".mp3", ".mp4", ".mov", ".avi",
}

SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
}

def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)

def should_skip_file(path: Path, max_size: int) -> bool:
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    try:
        if path.stat().st_size > max_size:
            return True
    except Exception:
        return True
    return False

def iter_files(root: Path, include_hidden: bool, max_size: int):
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not include_hidden and is_hidden(path):
            continue
        if should_skip_file(path, max_size):
            continue
        yield path

def read_text_file(path: Path, max_chars: int) -> str | None:
    try:
        content = path.read_text(encoding="utf-8")
        if max_chars and len(content) > max_chars:
            return content[:max_chars] + "\n\n...[truncated]..."
        return content
    except UnicodeDecodeError:
        return None
    except Exception as e:
        return f"[Error reading file: {e}]"

def build_tree(files, root: Path):
    return [f"- {path.relative_to(root)}" for path in files]

def main():
    parser = argparse.ArgumentParser(description="Export repo to prompt-friendly markdown.")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--output", default="code2prompt.md", help="Output file")
    parser.add_argument("--max-chars", type=int, default=20000)
    parser.add_argument("--max-file-size", type=int, default=200000)
    parser.add_argument("--include-hidden", action="store_true")
    parser.add_argument("--no-tree", action="store_true")

    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = sorted(iter_files(root, args.include_hidden, args.max_file_size))

    lines = ["# Project Export\n"]

    if not args.no_tree:
        lines.append("## File Tree\n")
        lines.extend(build_tree(files, root))
        lines.append("")

    lines.append("## Files\n")

    for path in files:
        rel = path.relative_to(root)
        content = read_text_file(path, args.max_chars)

        lines.append(f"\n### {rel}\n")

        if content is None:
            lines.append("[Skipped: non-text file]\n")
            continue

        lang = path.suffix.lstrip(".") or "text"

        lines.append(f"```{lang}")
        lines.append(content)
        lines.append("```")

    Path(args.output).write_text("\n".join(lines), encoding="utf-8")

    print(f"\n✅ Exported {len(files)} files to {args.output}")

if __name__ == "__main__":
    main()