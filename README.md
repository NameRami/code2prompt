# code2prompt

> Turn any codebase into clean, prompt-ready context in seconds.

Stop wasting time opening files and copy-pasting code into ChatGPT or Claude.
`code2prompt` exports your entire project into a structured Markdown format optimized for LLM prompts.

---

## ✨ Features

* 📦 Export full repositories into a single file
* 🧠 Prompt-friendly Markdown formatting
* 🌳 Includes project file tree
* 🚫 Skips binaries automatically
* 📏 Limits file size to avoid huge prompts
* ⚡ Fast and dependency-free

---

## 🚀 Usage

```bash
python code2prompt.py
```

Or specify options:

```bash
python code2prompt.py --root . --output project.md
```

---

## ⚙️ Options

| Flag               | Description                       |
| ------------------ | --------------------------------- |
| `--root`           | Root directory (default: current) |
| `--output`         | Output file                       |
| `--max-chars`      | Max characters per file           |
| `--max-file-size`  | Skip large files                  |
| `--include-hidden` | Include hidden files              |
| `--no-tree`        | Skip file tree                    |

---

## 📄 Example Output

````text
# Project Export

## File Tree
- main.py
- utils.py

## Files

### main.py
```py
print("hello")
````

```

---

## ⚠️ Security Note

Review output before sharing.  
Do not expose:
- API keys
- `.env` files
- secrets

---

## 📜 License

MIT
```
