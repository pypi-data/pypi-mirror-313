"""CLI tool for managing and deploying AO  applications."""

import os
import pty
import shutil
import subprocess
import time
from pathlib import Path
import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
import ell
import anthropic

from aob.prompts.generate_test import antrophic_generate_test_code, openai_generate_test_code
TOOL_VERSION = "0.0.1"
VERBOSE_MODE = False


ell.init(verbose=False)
client = anthropic.Anthropic()



def log_verbose(message: str):
    """Log a message if verbose mode is enabled."""
    if VERBOSE_MODE:
        console.print(f"[dim]{message}[/dim]")


app = typer.Typer(
    name="aob",
    help="AO Builder - Your AO Development Assistant\n\nThis tool helps you:\n1. Create new AO applications\n2. Test existing AO applications\n3. Deploy processes to the AO network\n4. Generate code using AI assistance",
    add_completion=False,
)
console = Console()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Handle the main entry point for the CLI."""
    global VERBOSE_MODE
    VERBOSE_MODE = verbose


def get_repo_path() -> Path:
    """Get the path to the AO application repository in current directory."""
    return Path.cwd() / "ao-counter"


@app.command(name="version")
def version():
    """Display the current version of AOB CLI."""
    console.print(f"AOB CLI version {TOOL_VERSION}")


@app.command(name="init")
def init(
    path: str = typer.Option(
        None,
        "--path",
        "-p",
        help="Custom installation path (defaults to current directory)",
    ),
    sqlite: bool = typer.Option(
    False,
    "--sqlite",
    help="Initialize with SQLite template ",
    ),
):
    """Initialize a new AO App """
    
     # Prompt for project name
    project_name = typer.prompt("Enter your project name").strip()
    
    # Validate project name
    if not project_name:
        show_error_panel("Project name cannot be empty")
    if not project_name.replace("-", "").replace("_", "").isalnum():
        show_error_panel("Project name can only contain letters, numbers, hyphens and underscores")

    if path:
        base_dir = Path(path)
    else:
        base_dir = Path.cwd()
    
    target_dir = base_dir / project_name

    repo_url = (
        "https://github.com/usedispatch/sqlite-template.git"
        if sqlite
        else "https://github.com/usedispatch/ao-counter"
    )
    log_verbose(f"Target directory: {target_dir}")

    # if path:
    #     try:
    #         # Create directory if it doesn't exist
    #         os.makedirs(path, exist_ok=True)
    #         # Change to that directory
    #         os.chdir(path)
    #         target_dir = Path.cwd()
    #     except OSError as e:
    #         show_error_panel("Failed to create or access target directory", str(e))
    # else:
    #     target_dir = Path.cwd()
    # log_verbose(f"Target directory: {target_dir}")
    # Show installation header with path info
    console.print("\n[bold blue]AO Project Installation[/bold blue]")
    console.print("└─ [dim]Repository:[/dim] [cyan]{}[/cyan]".format(repo_url))
    console.print(
        "└─ [dim]Installing to:[/dim] [green]{}[/green]\n".format(target_dir.absolute())
    )
    try:
        # Check existing installation
        if target_dir.exists():
            if any(target_dir.iterdir()):
                show_error_panel(
                    "Directory not empty",
                    f"The target directory '{target_dir.absolute()}' already exists and is not empty."
                )
                raise typer.Exit(1)
        else:
            target_dir.mkdir(parents=True)

        progress_columns = [
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ]

        with Progress(*progress_columns, expand=True) as progress:
            # Clone repository into a temporary directory
            clone_task = progress.add_task("Cloning repository...", total=100)
            temp_dir = target_dir / "temp_ao_counter"
            process = subprocess.Popen(
                ["git", "clone", repo_url, str(temp_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            while process.poll() is None:
                progress.update(clone_task, advance=1)
                time.sleep(0.1)

            progress.update(clone_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "git clone", error
                )

            # Move contents from temp directory to target directory
            for item in temp_dir.iterdir():
                shutil.move(str(item), str(target_dir))

            # Remove the temporary directory
            shutil.rmtree(temp_dir)

            # Root yarn install
            root_install_task = progress.add_task(
                "Installing dependencies...", total=100
            )

            os.chdir(target_dir)
            process = subprocess.Popen(
                ["yarn", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            while process.poll() is None:
                progress.update(root_install_task, advance=1)
                time.sleep(0.1)

            progress.update(root_install_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", error
                )

            # App yarn install
            app_install_task = progress.add_task(
                "Installing app dependencies...", total=100
            )

            os.chdir(target_dir / "app")
            process = subprocess.Popen(
                ["yarn", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            while process.poll() is None:
                progress.update(app_install_task, advance=1)
                time.sleep(0.1)

            progress.update(app_install_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", error
                )
            
            git_dir = target_dir / ".git"
            if git_dir.exists():
                
                log_verbose(f"Removing .git directory: {git_dir}")
                shutil.rmtree(git_dir)

            success_message = (
                "[green bold]✓ AO SQLite template installed successfully!\n\n"
                if sqlite
                else "[green bold]✓ AO Starter app installed successfully!\n\n"
            )

        # Show success message
        show_success_panel(
            success_message +
            "[white]Getting Started:[/white]\n"
            "1. Run [cyan]aob dev[/cyan] to start the frontend dev server\n"
            "2. Run [cyan]aob deploy process[/cyan] to deploy the process\n"
            "3. Run [cyan]aob test process[/cyan] to run the process tests\n"
            "4. Run [cyan]aob generate test[/cyan] to generate new tests",
            "Installation Complete",
        )
    except subprocess.CalledProcessError as e:
        show_error_panel("Failed to clone repository", e.stderr)
    except Exception as e:
        show_error_panel("An error occurred", str(e))


@app.command(name="deploy")
def deploy(
    component: str = typer.Argument(..., help="Component to deploy (process/frontend)"),
    wallet: str = typer.Option(None, "--wallet", "-w", help="Path to wallet file for deployment")
):
    """Deploy AO application components (process or frontend)."""
    if component not in ["process", "frontend"]:
        show_error_panel("Invalid component. Must be either 'process' or 'frontend'")

    if not os.path.exists(wallet):
        show_error_panel(
            f"Wallet file not found: {wallet}\n"
            "Please provide a valid wallet path using --wallet option"
        )

    

    
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO application."
        )
    try:
        if component == "process":
            try:
                with open(wallet, 'r') as f:
                    wallet_content = f.read()
                os.environ['WALLET_JSON'] = wallet_content
                log_verbose(f"Wallet loaded from: {wallet}")
            except Exception as e:
                show_error_panel("Failed to read wallet file", str(e))
            console.print("\n[bold blue]Deploying AO Application Process[/bold blue]")
            command = "deploy:process"
            success_message = "Process deployed successfully!"
            process, master = run_command_with_pty(f"yarn {command}")
        else:
            console.print("\n[bold blue]Deploying AO Application Frontend[/bold blue]")
            build_command = "yarn build"
            console.print("[yellow]Building frontend...[/yellow]")
            build_process = subprocess.run(build_command, shell=True, capture_output=True, text=True)
            if build_process.returncode != 0:
                raise subprocess.CalledProcessError(build_process.returncode, build_command, build_process.stderr)
            
            if not wallet:
                show_error_panel(
                    "Wallet path is required for frontend deployment.\n"
                    "Usage: aob deploy frontend --wallet <path-to-wallet>"
                )

            deploy_command = f"arkb deploy ./dist --wallet {wallet}"
            console.print("[yellow]Deploying to Arweave...[/yellow]")
            process, master = run_command_with_pty(deploy_command)
            try:
                while True:
                    try:
                        # Read from master fd
                        data = os.read(master, 1024).decode()
                        if data:
                            print(data, end="", flush=True)
                        # Check if confirmation is required
                        if "upload (Y/n)" in data:
                            # Write 'y' and newline to the process
                            os.write(master, b'y\n')
                    except OSError:
                        break
            finally:
                os.close(master)
                process.terminate()
            success_message = "Frontend deployed successfully to Arweave!"

        

        try:
            while True:
                try:
                    # Read from master fd and display output in real-time
                    data = os.read(master, 1024).decode()
                    if data:
                        print(data, end="", flush=True)
                except OSError:
                    break

        finally:
            # Cleanup
            os.close(master)
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, f"Deployment failed"
                )

        # Show success message if we get here
        show_success_panel(success_message, "Deployment Complete")

    except subprocess.CalledProcessError:
        show_error_panel("Deployment failed")
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="test")
def test(component: str = typer.Argument(..., help="Component to test (process)")):
    """Run tests for AO application components (process)."""
    if component != "process":
        show_error_panel(
            "Invalid component. Currently only 'process' testing is supported"
        )

    
    
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO application."
        )

    try:
        console.print("\n[bold blue]Running AO Application Process Tests[/bold blue]")
        test_dir = Path.cwd() / "test"
        node_modules = test_dir / "node_modules"

        if not node_modules.exists():
            console.print("\n[yellow]Installing test dependencies...[/yellow]")
            os.chdir(test_dir)

            # Run yarn install in test directory
            process = subprocess.run(
                ["yarn", "install"], capture_output=True, text=True
            )

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", process.stderr
                )

            # Change back to project root
            os.chdir(test_dir.parent)
            console.print("[green]✓ Test dependencies installed[/green]\n")

        # Create a pseudo-terminal
        process, master = run_command_with_pty("yarn test:process")

        try:
            while True:
                try:
                    # Read from master fd and display output in real-time
                    data = os.read(master, 1024).decode()
                    if not data:  # Process has completed
                        break
                    print(data, end="", flush=True)
                except OSError:  # Read error means process likely completed
                    break

        finally:
            # Cleanup
            os.close(master)
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            if process.returncode and process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn process:test"
                )

        # Show success message if we get here
        show_success_panel("Process tests completed successfully!", "Tests Complete")

    except subprocess.CalledProcessError:
        show_error_panel("Tests failed")
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="dev")
def dev(
    component: str = typer.Argument(
        "frontend",
        help="Component to run in development mode (currently only supports 'frontend')",
    )
):
    """Start the AO application development server for the specified component."""
    # Validate component
    if component.lower() != "frontend":
        show_error_panel(
            "Currently only the 'frontend' component is supported for development mode.\n"
            "Usage: aob dev frontend"
        )
        return

    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO application project."
        )
        return

    try:
        console.print(
            f"\n[bold blue]Starting AO application {component.title()} Development Server[/bold blue]"
        )

        # Create a pseudo-terminal
        process, master = run_command_with_pty("yarn dev:frontend")

        try:
            while True:
                try:
                    # Read from master fd
                    data = os.read(master, 1024).decode()
                    if data:
                        # Print directly to preserve formatting
                        print(data, end="", flush=True)
                except OSError:
                    break
        except KeyboardInterrupt:
            # show_error_panel("Development server stopped by user")
            print("\n")
            pass

        finally:
            # Cleanup
            os.close(master)
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log_verbose("Development server timed out")
                process.kill()

    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="build")
def build(
    component: str = typer.Argument(..., help="Component to build (process/frontend)")
):
    """Build AO application components (process or frontend)."""
    if component not in ["process", "frontend"]:
        console.print(
            Panel.fit(
                "[red]Invalid component. Must be either 'process' or 'frontend'",
                title="❌ Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO application project."
        )

    try:
        if component == "process":
            # Process deployment logic
            console.print("\n[bold blue]Building AO application Process[/bold blue]")
            command = "build:process"
            success_message = "Process built successfully!"
        else:
            # Frontend deployment logic
            console.print("\n[bold blue]Building AO application Frontend[/bold blue]")
            command = "build:frontend"
            success_message = "Frontend built successfully!"

        with console.status(f"[bold blue]Running {command}...", spinner="dots"):
            # Run the deployment command
            process = subprocess.run(["yarn", command], capture_output=True, text=True)

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, f"yarn {command}", process.stderr
                )
        # Show success message
        show_success_panel(success_message, "Build Complete")

    except subprocess.CalledProcessError as e:
        show_error_panel("Build failed", e.stderr)
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")




@app.command(name="generate")
def generate(
    component: str = typer.Argument(..., help="Component to generate (test)"),
     model: str = typer.Option("auto", "--model", "-m", help="Model to use for generation ('anthropic' or 'openai', defaults to auto)")
):
    """Generate code for AO application components (test)."""
    if component != "test":
        show_error_panel(
            "Invalid component. Currently only 'test' generation is supported"
        )

    
    is_sqlite = is_sqlite_template()
    
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO application."
        )

    try:
            # Determine which API key is available
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if model == "auto":
            if anthropic_key:
                selected_model = "anthropic"
            elif openai_key:
                selected_model = "openai"
            else:
                show_error_panel(
                    "No API keys found. Please set either ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable."
                )
        else:
            selected_model = model
            if selected_model == "anthropic" and not anthropic_key:
                show_error_panel("ANTHROPIC_API_KEY environment variable not set")
            elif selected_model == "openai" and not openai_key:
                show_error_panel("OPENAI_API_KEY environment variable not set")

        console.print(f"\n[bold blue]Generating Tests using {selected_model.upper()}[/bold blue]")
        
        # Read Lua code from output.lua
        lua_code = read_lua_code()
        if not lua_code:
            show_error_panel("No Lua code found in output.lua")
            
        # Read existing test code
        existing_tests = read_existing_tests()
        if not existing_tests:
            show_error_panel("No existing test code found in test/src/index.ts")
    
    
        # prompt_response = antrophic_generate_test_code(lua_code, existing_tests)
        if selected_model == "anthropic":
            prompt_response = antrophic_generate_test_code(lua_code, existing_tests,is_sqlite)
        else:
            prompt_response = openai_generate_test_code(lua_code, existing_tests,is_sqlite)

        # try:
        #     analysis_start = prompt_response.find("<code_analysis>")
        #     analysis_end = prompt_response.find("</code_analysis>") 
        #     if analysis_start != -1 and analysis_end != -1:
        #         analysis = prompt_response[analysis_start + len("<code_analysis>"):analysis_end].strip()
        #         # Display analysis in CLI
        #         console.print("\n[bold blue]Code Analysis[/bold blue]")
        #         console.print(Panel.fit(analysis, border_style="blue"))
        # except Exception as e:
        #     show_error_panel(f"An error occurred in code analysis: {str(e)}")


        try:
            generated_tests_start = prompt_response.find("<new_tests>")
            generated_tests_end = prompt_response.find("</new_tests>")
            if generated_tests_start != -1 and generated_tests_end != -1:
                generated_tests = prompt_response[generated_tests_start + len("<new_tests>"):generated_tests_end].strip()
                # console.print(f"\n[bold blue]Generated Tests[/bold blue]")
                # console.print(Panel.fit(generated_tests, border_style="blue"))
                if generated_tests == "None":
                    show_error_panel("No new tests generated")
                else:
                    write_test_code(generated_tests)
                    console.print("[green]✓ Tests written to test/src/index.ts[/green]")
        except Exception as e:
            show_error_panel(f"An error occurred in generated tests: {str(e)}")
        
        
        # Generate system prompt
        # prompt = generate_system_prompt(lua_code, existing_tests)
        
        # # Call LLM to generate tests
        # with console.status("[bold blue]Generating tests...", spinner="dots"):
        #     generated_tests = generate_test_code(prompt, model)
            
        # if not generated_tests:
        #     show_error_panel("Failed to generate tests")
            
        # # Write generated tests
        # write_test_code(generated_tests)
        
        # Show success message
        show_success_panel(
            "[green bold]✓ Tests generated successfully!\n\n"
            "[white]Next steps:[/white]\n"
            "1. Review the generated tests in [cyan]test/src/index.ts[/cyan]\n"
            "2. Run [cyan]aob test process[/cyan] to execute the tests",
            "Test Generation Complete"
        )

    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


def write_test_code(generated_tests: str):
    """Write generated tests to test/src/index.ts."""
    test_file = Path.cwd() / "test" / "src" / "index.ts"
    
    # Read existing content
    with open(test_file, "r") as f:
        content = f.read()
    
    # Find the last closing brace of the describe block
    last_brace_index = content.rindex("});")
    
    # Insert new tests before the closing brace
    new_content = (
        content[:last_brace_index] + 
        "\n  " + 
        generated_tests.replace("\n", "\n  ") + 
        "\n" +
        content[last_brace_index:]
    )
    
    # Write back to file
    with open(test_file, "w") as f:
        f.write(new_content)
    
def read_lua_code() -> str:
    """Read and parse Lua code from output.lua."""
    try:
        lua_file = Path.cwd() / "process" / "build" / "output.lua"
        if not lua_file.exists():
            return None
            
        with open(lua_file, "r") as f:
            content = f.read()
            
        # TODO: Add logic to extract only handlers and functions
        return content
        
    except Exception as e:
        log_verbose(f"Error reading Lua code: {str(e)}")
        return None
    
def read_existing_tests() -> str:
    """Read existing test code from test/src/index.ts."""
    try:
        test_file = Path.cwd() / "test" / "src" / "index.ts"
        if not test_file.exists():
            return ""
            
        with open(test_file, "r") as f:
            return f.read()
            
    except Exception as e:
        log_verbose(f"Error reading existing tests: {str(e)}")
        return ""
    

def show_success_panel(message: str, title: str = "Complete"):
    """Display a success panel with consistent formatting."""
    console.print(
        Panel.fit(
            f"[green bold]✓ {message}",
            title=title,
            border_style="green",
        )
    )


def show_error_panel(message: str, error_details: str = None):
    """Display an error panel with consistent formatting."""
    log_verbose(f"Error occurred: {error_details or message}")
    error_text = f"[red]{message}"
    if error_details:
        error_text += f"\nError: {error_details}"

    console.print(
        Panel.fit(
            error_text,
            title="❌ Error",
            border_style="red",
        )
    )
    raise typer.Exit(1)


def run_command_with_pty(command: str) -> subprocess.Popen:
    """Run a command with pseudo-terminal support."""
    master, slave = pty.openpty()
    process = subprocess.Popen(
        command,
        shell=True,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        text=True,
        preexec_fn=os.setsid,
        env={**os.environ, "FORCE_COLOR": "1"},
    )
    os.close(slave)
    return process, master

def is_sqlite_template() -> bool:
    """Check if the current project uses the SQLite template."""
    try:
        package_json = Path.cwd() / "package.json"
        
        with open(package_json) as f:
            data = json.loads(f.read())
            deploy_script = data.get('scripts', {}).get('deploy:process', '')
            return deploy_script == 'lua process/scripts/replace.lua && aoform apply -f processes.yaml'
    except (FileNotFoundError, json.JSONDecodeError):
        return False


if __name__ == "__main__":
    app()



# # Work with Claude 3.5 Sonnet on your repo
# export ANTHROPIC_API_KEY=your-key-goes-here

# # Work with GPT-4o on your repo
# export OPENAI_API_KEY=your-key-goes-here