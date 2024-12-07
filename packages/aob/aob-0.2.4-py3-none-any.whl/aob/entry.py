from rich.console import Console
from rich.panel import Panel

def show_welcome_message():
    """Display welcome message when package is installed."""
    console = Console()
    console.print("\n[bold blue]Welcome to AOB CLI![/bold blue]")
    console.print(
        "\n[bold]AO Builder - Your AO Development Assistant[/bold]\n\n"
        "This tool helps you:\n"
        "1. Create new AO applications\n"
        "2. Deploy processes to the AO network\n"
        "3. Generate tests for your AO applications using AI assistance\n"
    )
    console.print("\n[yellow]Would you like to create a new AO application?[/yellow]")
    console.print(
        "\nTo get started:\n"
        "1. Create an empty directory: [cyan]mkdir my-ao-app && cd my-ao-app[/cyan]\n"
        "2. Initialize your app: [cyan]aob init[/cyan]\n"
        "\nOr run [cyan]aob --help[/cyan] to see all available commands"
    )


if __name__ == "__main__":
    show_welcome_message()