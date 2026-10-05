import sys
import os

# Ensure the backend root is on the path so `src.*` imports resolve
# regardless of the working directory the script is launched from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.orchestrator import full_review
from src.tools.explanation_tool import explain_code
from src.tools.find_bug_tool import find_bug
from src.tools.test_tool import generate_tests

from src.db.init_db import init_db
from src.utils.github_loader import get_code_from_github_file

from rich.console import Console  # main output manager, supports colors, borders etc
from rich.panel import Panel       # boxes around text
from rich.syntax import Syntax     # syntax highlighting for code

console = Console()

# Maps CLI mode number → human-readable panel title
PANEL_TITLES = {
    "1": "Beginner Explanation",
    "2": "Interview Analysis",
    "3": "Test Case Generation",
    "4": "Bug Report",
    "5": "Full Review",
}


def main():

    console.print("[bold cyan]Code Analyser[/bold cyan]")

    while True:

        # MODE INPUT
        mode = input(
            "\nEnter mode\n"
            " 1. Beginner friendly\n"
            " 2. Interview style\n"
            " 3. Test Case Generation\n"
            " 4. Find Bug\n"
            " 5. Full Review\n"
            " 6. Exit\n"
            "Choose mode : "
        ).strip()

        if mode == "6":
            return

        # CHOICE INPUT
        choice = input(
            "\nEnter input style\n"
            " 1. Paste code\n"
            " 2. File Input\n"
            " 3. Github URL\n"
            " 4. Exit\n"
            "Choose : "
        ).strip()

        if choice == "4":
            return

        # CHOICE - 1  Paste / write code
        if choice == "1":
            language = input("Enter source code language (or 'exit' to quit) : ").strip()
            if language.lower() in ("quit", "exit"):
                return

            lines = []
            print("Enter code (type 'end' on a new line to finish) :")

            while True:
                line = input()
                if line.lower() == "end":
                    break
                lines.append(line)

            code = "\n".join(lines)

        # CHOICE - 2  File input
        elif choice == "2":
            path = input("Enter input file path : ").strip()

            if path.lower() in ("quit", "exit"):
                return

            try:
                with open(path, "r") as f:
                    code = f.read()
            except FileNotFoundError:
                console.print("[red]Invalid File Path[/red]")
                continue

            language = input("Enter language of the file : ").strip()

        # CHOICE - 3  Github URL
        elif choice == "3":
            github_url = input("Enter github URL of the file for source code : ").strip()
            try:
                code = get_code_from_github_file(github_url)
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
                continue

            language = input("Enter language of the file : ").strip()

        else:
            console.print("[red]Invalid Input[/red]")
            continue

        console.print("\n[yellow]Generating analysis...[/yellow]\n")

        syntax = Syntax(code, language, theme="monokai", line_numbers=True)

        # Print the input code in a panel
        console.print(Panel(syntax, title="Input Code"))

        # Run the selected mode
        with console.status("[bold green]Analyzing code..."):
            if mode == "5":
                result = full_review(code, language)
            elif mode == "4":
                result = find_bug(code, language, mode)
            elif mode == "3":
                result = generate_tests(code, language, mode)
            else:
                result = explain_code(code, language, mode)

        panel_title = PANEL_TITLES.get(mode, "Analysis Result")

        console.print(
            Panel(
                result,
                title=panel_title,
                border_style="green",
            )
        )


if __name__ == "__main__":
    init_db()
    main()
