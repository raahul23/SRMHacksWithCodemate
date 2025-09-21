import os
import psutil
import google.generativeai as genai
import random
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

console = Console()

API_KEY = "AIzaSyCrKqWsYuyveE1OFmCP4pS4keAvd3anjXk"  # replace with your Gemini API key
genai.configure(api_key=API_KEY)

# ---------------- Gamification ----------------
xp_points = 0
level = 1
XP_THRESHOLD = 50  # XP needed to level up


def add_xp(points=10):
    """Add XP and handle leveling up."""
    global xp_points, level
    xp_points += points
    if xp_points >= XP_THRESHOLD * level:
        level += 1
        console.print(f"\n🌟 [bold green]Congratulations![/bold green] You reached Level {level}!\n")
    show_xp_bar()


def show_xp_bar():
    """Display XP progress bar."""
    with Progress(transient=True) as progress:
        task = progress.add_task(f"🎮 XP: {xp_points}/{XP_THRESHOLD * level} (Level {level})",
                                 total=XP_THRESHOLD * level)
        progress.update(task, completed=min(xp_points, XP_THRESHOLD * level))


# ---------------- Autocomplete ----------------
COMMANDS = ["pwd", "ls", "cd", "mkdir", "rm", "cpu", "mem", "ps",
            "ai", "fortune", "cat", "help", "exit"]
command_completer = WordCompleter(COMMANDS, ignore_case=True)


def get_input(cwd):
    """Prompt input with autocomplete."""
    return prompt(f"[{cwd}] > ", completer=command_completer)


# ---------------- AI Translator ----------------
def translate_to_command(natural_language_query):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt_text = f"""
        You are a helpful assistant that translates natural language queries from a user
        into executable commands for a custom Python terminal.

        The available commands are: ls, cd, pwd, mkdir, rm, cpu, mem, ps, fortune, cat, help.

        - Only respond with the command(s).
        - If multiple commands are needed, separate them with a newline character (\\n).
        - Do not add any explanation or commentary.
        - If the user's request cannot be fulfilled, respond with 'ERROR: Cannot fulfill request'.

        User query: "{natural_language_query}"
        Response:
        """
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        return f"ERROR: AI model failed - {e}"


# ---------------- Command Executor ----------------
def execute_command(user_input):
    parts = user_input.split()
    if not parts:
        return

    command = parts[0]
    args = parts[1:]

    # --- AI Command ---
    if command == 'ai':
        query = " ".join(args)
        if not query:
            console.print("[bold red]ai:[/bold red] Please provide a query. e.g., ai \"create a folder called test\"")
            return
        with console.status(f"🤖 Thinking about your request: '{query}'...", spinner="dots"):
            ai_commands = translate_to_command(query)
        if ai_commands.startswith("ERROR:"):
            console.print(f"[bold red]AI Error:[/bold red] {ai_commands}")
            return
        console.print(f"🤖 [bold green]Executing Commands:[/bold green]\n---\n{ai_commands}\n---")
        for cmd in ai_commands.split('\n'):
            if cmd.strip():
                execute_command(cmd.strip())
        return

    # --- Help Command ---
    if command == 'help':
        console.print("""
[bold cyan]Available Commands:[/bold cyan]
📁 ls          → List files
🏠 cd <path>   → Change directory
📍 pwd         → Print working directory
📂 mkdir <dir> → Create directory
❌ rm <file>   → Remove file/folder
🖥️ cpu         → Show CPU usage
💾 mem         → Show memory usage
⚙️ ps          → Show processes
🧠 ai "<query>"→ AI natural language command
🍀 fortune     → Get a random fun/motivational quote
📜 cat <file>  → Show file contents
❓ help        → Show this help menu
🚪 exit        → Exit terminal
        """)
        return

    # --- Fortune Command ---
    if command == 'fortune':
        quotes = [
            "Keep pushing, you're closer than you think!",
            "Debugging is twice as hard as writing the code in the first place.",
            "The best error message is the one that never shows up.",
            "Stay curious, stay foolish. 🚀",
            "Code is like humor. When you have to explain it, it’s bad."
        ]
        console.print(f"🍀 {random.choice(quotes)}")
        add_xp(5)
        return

    # --- File and Directory Commands ---
    if command == 'pwd':
        console.print(os.getcwd())
        add_xp()
    elif command == 'ls':
        path = args[0] if args else '.'
        try:
            for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                    console.print(f"[bold blue]📁 {entry}/[/bold blue]")
                else:
                    console.print(f"📄 {entry}")
            add_xp()
        except FileNotFoundError:
            console.print(f"[bold red]ls:[/bold red] cannot access '{path}': No such file or directory")
    elif command == 'cd':
        path = args[0] if args else os.path.expanduser('~')
        try:
            os.chdir(path)
            add_xp()
        except FileNotFoundError:
            console.print(f"[bold red]cd:[/bold red] no such file or directory: {path}")
    elif command == 'mkdir':
        if not args:
            console.print("[bold red]mkdir:[/bold red] missing operand")
        else:
            try:
                os.makedirs(args[0], exist_ok=True)
                add_xp()
            except Exception as e:
                console.print(f"[bold red]mkdir:[/bold red] cannot create directory '{args[0]}': {e}")
    elif command == 'rm':
        if not args:
            console.print("[bold red]rm:[/bold red] missing operand")
        else:
            path = args[0]
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    console.print(f"Removed file: '{path}'")
                elif os.path.isdir(path):
                    os.rmdir(path)
                    console.print(f"Removed empty directory: '{path}'")
                else:
                    console.print(f"[bold red]rm:[/bold red] cannot remove '{path}': No such file or directory")
                add_xp()
            except OSError as e:
                console.print(f"[bold red]rm:[/bold red] cannot remove '{path}': {e.strerror}")

    # --- System Monitoring Commands ---
    elif command == 'cpu':
        console.print(f"CPU Usage: [bold green]{psutil.cpu_percent(interval=1)}%[/bold green]")
        add_xp()
    elif command == 'mem':
        memory = psutil.virtual_memory()
        console.print(f"Total Memory: {memory.total / (1024**3):.2f} GB")
        console.print(f"Used Memory: [bold yellow]{memory.used / (1024**3):.2f} GB ({memory.percent}%)[/bold yellow]")
        add_xp()
    elif command == 'ps':
        table = Table(title="Running Processes")
        table.add_column("PID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("CPU %", justify="right", style="green")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                table.add_row(str(proc.info['pid']), proc.info['name'], f"{proc.info['cpu_percent']:.1f}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        console.print(table)
        add_xp()

    # --- Cat Command ---
    elif command == 'cat':
        if not args:
            console.print("[bold red]cat:[/bold red] missing file operand")
        else:
            try:
                with open(args[0], 'r') as f:
                    console.print(f.read())
                add_xp()
            except Exception as e:
                console.print(f"[bold red]cat:[/bold red] cannot read file '{args[0]}': {e}")

    else:
        console.print(f"[bold red]Error:[/bold red] Command '{command}' not found.")


# ---------------- Main Loop ----------------
def main():
    console.print("[bold green]Welcome to the AI-Powered Gamified Terminal![/bold green] 🚀")
    console.print("Type 'help' to see available commands.\n")
    while True:
        user_input = get_input(os.getcwd())
        if user_input.lower() == 'exit':
            console.print("👋 Goodbye, Hacker!")
            break
        execute_command(user_input)


if __name__ == "__main__":
    main()
