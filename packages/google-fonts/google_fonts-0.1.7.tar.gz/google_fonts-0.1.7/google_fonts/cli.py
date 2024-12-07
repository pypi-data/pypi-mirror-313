import os
import platform
from typing import List

import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from google_fonts.font.list import list_fonts
from .font.install import install_fonts, install_all_fonts

app = typer.Typer()
console = Console()
env_file_path = os.path.expanduser("~/.config/google-fonts/.env")
load_dotenv(env_file_path)


@app.command(name="install", help="Install specified fonts.")
def install_fonts_cli(names: List[str] = typer.Argument(None, help="Names of the fonts to process."),
                      install_all: bool = typer.Option(False, "--all", help="Install all available fonts."),
                      force: bool = typer.Option(False, "--force/--no-force",
                                                 help="Force installation of fonts. Using name in https://github.com/google/fonts/tree/main/ofl/"),
                      github_token: str = typer.Option(None, "--token", help="GitHub Access Token for authentication."),
                      ):
    if github_token is not None:
        os.environ["ACCESS_TOKEN"] = github_token
    if install_all:
        print("Installing all available fonts...")
        install_all_fonts()
        return
    if force:
        print("Forcing installation of fonts...")
        install_fonts(names, force=force)
        return

    install_fonts(names)
    if platform.system() == "Linux":
        os.system("fc-cache -fv")


@app.command(name="list",
             help="List all available fonts. See https://github.com/google/fonts/tree/main/ofl and https://fonts.google.com/")
def list_fonts_cli(
        name: str = typer.Argument(None, help="Name of the font to list."),
        github_token: str = typer.Option(None, "--token", help="GitHub Access Token for authentication.")
):
    if github_token is not None:
        os.environ["ACCESS_TOKEN"] = github_token
    list_fonts(search_content=name)


@app.command(name="config", help="Configure GitHub Access Token.")
def config(
        github_token: str = typer.Option("", "--token", help="GitHub Access Token for authentication.")
):
    # 确保目录存在
    os.makedirs(os.path.expanduser("~/.config/google-fonts"), exist_ok=True)

    if github_token:
        # 保存 token 到 .env 文件
        set_key(os.path.expanduser("~/.config/google-fonts/.env"), "ACCESS_TOKEN", github_token)
        console.print(f"GitHub Access Token saved to .config/google-fonts/.env", style="green")
    else:
        # 如果没有提供 Token，读取并显示现有的 Token
        token = os.getenv("ACCESS_TOKEN", "")
        if token:
            console.print(f"Current GitHub Access Token: {token}", style="yellow")
        else:
            console.print("No GitHub Access Token found.", style="red")


@app.command(name="author", help="This package is written by desonglll. See my github on github.com/desonglll.")
def author():
    print("This package is written by desonglll.")
    print("See my github on github.com/desonglll.")
    pass


if __name__ == "__main__":
    app()
