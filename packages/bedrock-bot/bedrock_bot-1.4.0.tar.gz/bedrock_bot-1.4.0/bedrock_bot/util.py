from rich.console import Console
from rich.markdown import Markdown

console = Console()


def formatted_print(text: str) -> None:
    console.print(Markdown(text, code_theme="material"))
