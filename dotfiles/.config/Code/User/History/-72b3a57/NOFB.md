# 🩺 careLog — CLI Health Journal

`careLog` is a simple, command-line health journaling tool built in Python to help you track symptoms, habits, medicines, and more — all from your terminal.

Whether you're logging daily wellness notes or building patterns in your health history, `careLog` keeps it organized — with optional tags, filtering, editing, and exporting.

---

## ✨ Features

- 📥 Log health entries with optional `--tag`
- 📖 View your full health history
- 🔍 Filter by keyword, tag, or both
- ✏️ Edit entries interactively
- 🗑️ Delete specific entries safely
- 📤 Export logs to `.txt` or `.json`
- 📊 View meaningful statistics (top words, tags, active days)
- 🧠 Fully offline & works on Linux/Mac/Windows


## 🧰 Installation - or linux (making it feel like a CLI tool)

To make `carelog` available as a system command follow these steps:


### ✅ 1. Add a Shebang (already done)
Ensure the first line of the file is:

#!/usr/bin/env python3


### ✅ 2. Make it Executable
From inside the project folder:

chmod +x carelog.py


### ✅ 3. Rename the Script
Remove the .py and make it feel more like a native tool:

mv carelog.py carelog