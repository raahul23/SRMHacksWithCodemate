# 🤖 AI-Powered Gamified Python Terminal

A custom terminal built in Python for the **CodeMate Hackathon 2025** 🚀.  
It mimics a Linux shell, supports system monitoring, file operations, and includes an **AI-powered natural language interface** with a fun gamification twist.

---

## ✨ Features
- 🧠 **AI Commands**: Natural language → terminal commands (powered by Gemini API).
- 📁 **File Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`.
- ⚙️ **System Monitoring**: `cpu`, `mem`, `ps`.
- 🎮 **Gamification**: Earn XP for every command, level up with a progress bar.
- 🍀 **Fun Commands**: `fortune` for random quotes.
- 📜 **File Preview**: `cat <file>` to view contents.
- ❓ **Help Menu**: Colorful command list with emojis.

---

## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/python-terminal.git
   cd python-terminal
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Add your Gemini API key in main.py:

python
Copy code
API_KEY = "YOUR_API_KEY"
▶️ Usage
Run the terminal:

bash
Copy code
python main.py
Example Commands
bash
Copy code
pwd
ls
mkdir demo
cd demo
fortune
ai make a new folder called test and enter it
cpu
mem
ps
cat main.py
help
exit
📽️ Demo Video
🎥 Watch the Demo

📌 Hackathon Submission
This project was developed for the CodeMate Hackathon 2025.
Submission includes:

✅ Source code (this repo)

✅ Video demo

✅ GitHub repository link

✅ Hosted submission on CodeMate platform

👨‍💻 Author
Raahul U
B.Tech CSE(AI & ML) | SRM Institute of Science and Technology

yaml
Copy code

---

⚡ Next step: create a `requirements.txt` with this content:

```txt
psutil
rich
google-generativeai
prompt_toolkit
