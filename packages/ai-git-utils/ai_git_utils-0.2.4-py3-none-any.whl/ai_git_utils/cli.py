import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from datetime import datetime
from .config_manager import (
    add_model_to_config,
    remove_model_from_config,
    set_active_model_in_config,
    get_active_model,
    load_config
)
from .git_operations import get_git_diff, commit_changes
from .ai_model import get_model
from .utils import beautify_diff, edit_commit_message
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError
from .git_operations import get_commit_diff
from . import __version__


app = typer.Typer()
model_app = typer.Typer()
diff_app = typer.Typer()
console = Console()
parser = StrOutputParser()

system_prompt = '''
Craft clear and concise commit messages following the Conventional Commits standard format for git. When presented with a git diff summary, your task is to convert it into a useful commit message and add a brief description of the changes made, ensuring that lines are not longer than 74 characters. 
Your commit message should describe the nature and purpose of the changes in a comprehensive, informative, and concise manner. The commit message should follow the format: <type>(<scope>): <subject>, starting the <subject> with an emoji from the list provided below that appropriately describes the content, and an optional body for more detailed changes or multiple changes listed briefly in bullet points. Keep the content concise and to the point.
emoji-list:
```
- ✨ New feature
- 🐛 Fix bug
- 📚 Documentation update
- 🚀 Deploy stuff
- 💄 UI/style update
- 🎨 Improve structure/format of the code
- 🔧 Configuration modification
- 🔥 Delete code/file
- 🚑 Critical fix
- ➕ Add dependency
- ⚡️ Performance improvement
- ♻️ Refactor code
- 👷 Add or update CI build system
```

example:
```
fix(cli): 🐛 segmentation fault in inference

- fix segmentation fault in inference
```

Answer all my questions in {language}.
'''

@model_app.command("add")
def add_model(
    name: str = typer.Option(..., prompt=True),
    model: str = typer.Option(..., prompt=True),
    base_url: str = typer.Option(..., prompt=True),
    temperature: float = typer.Option(..., prompt=True),
    api_key: str = typer.Option(..., prompt=True)
):
    """添加新的模型配置"""
    model_config = {
        "model": model,
        "base_url": base_url,
        "temperature": temperature,
        "api_key": api_key
    }
    add_model_to_config(name, model_config)
    typer.echo(f"模型 '{name}' 已添加并激活。")

@model_app.command("remove")
def remove_model(name: str = typer.Option(..., prompt=True)):
    """删除指定的模型配置"""
    remove_model_from_config(name)
    typer.echo(f"模型 '{name}' 已删除。")

@model_app.command("active")
def activate_model(name: str = typer.Option(..., prompt=True)):
    """激活指定的模型配置"""
    set_active_model_in_config(name)
    typer.echo(f"模型 '{name}' 已激活。")

@model_app.command("list")
def list_models():
    """列出所有可用的模型配置"""
    config = load_config()
    active_model = config["active_model"]

    table = Table(title="可用模型配置")
    table.add_column("模型名称", style="cyan")
    table.add_column("状态", style="magenta")

    for name in config["models"]:
        status = "激活" if name == active_model else ""
        table.add_row(name, status)

    console.print(table)

@model_app.command("show")
def show_config():
    """显示当前的模型配置"""
    config = load_config()
    active_model = config["active_model"]

    if not config["models"]:
        typer.echo("当前没有保存的模型配置。请运行 'aigit model add' 命令添加模型。")
        return

    table = Table(title=f"当前激活的模型配置: {active_model}")
    table.add_column("配置项", style="cyan", no_wrap=True)
    table.add_column("值", style="magenta")

    active_config = config["models"].get(active_model, {})
    for key, value in active_config.items():
        if key == 'api_key' and value:
            value = value[:4] + '*' * (len(value) - 4)
        table.add_row(key, str(value))

    console.print(table)


@app.command()
def commit(
        staged: bool = typer.Option(False, "--staged", "-s", help="显示暂存的更改"),
        file_path: Optional[str] = typer.Option(None, "--file", "-f", help="指定文件路径"),
        language: str = typer.Option("English", "--lang", "-l", help="设置语言（English/Chinese）"),

):
    """
    使用 AI 智能生成代码更改信息
    """
    active_config = get_active_model()
    if not active_config:
        typer.echo("错误：未找到激活的模型配置。请先运行 'aigit model add' 或 'aigit model active' 命令。")
        raise typer.Exit(code=1)
    try:
        repo = Repo('.')
        diff_output = get_git_diff(repo, staged, file_path)

        if not diff_output:
            typer.echo("没有检测到更改。")
        else:
            message_content = '''
git diff summary:
{diff_summary}
'''

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", message_content),
            ])

            messages = prompt.invoke({"language": language, 'diff_summary': diff_output})

            model = get_model()

            result = model.invoke(messages)
            initial_commit_message = parser.invoke(result)
            initial_commit_message = initial_commit_message.strip('```')
            initial_commit_message = initial_commit_message.strip()

            typer.echo("AI 生成的提交信息：")
            typer.echo(initial_commit_message)
            typer.echo("\n请编辑提交信息，保存并关闭编辑器以继续。")

            edited_message = edit_commit_message(initial_commit_message)

            typer.echo("编辑后的提交信息：")
            typer.echo(edited_message)

            if typer.confirm("确认提交这些更改？"):
                commit_changes(repo, edited_message)
                typer.echo("更改已成功提交！")
            else:
                typer.echo("提交已取消。")

    except InvalidGitRepositoryError:
        typer.echo("错误：当前目录不是有效的Git仓库。", err=True)
    except GitCommandError as e:
        typer.echo(f"Git命令执行错误：{str(e)}", err=True)


@diff_app.command("current")
def diff(
        staged: bool = typer.Option(False, "--staged", "-s", help="显示暂存的更改"),
        file_path: Optional[str] = typer.Option(None, "--file", "-f", help="指定文件路径"),
):
    """
    查看代码更改
    """
    try:
        repo = Repo('.')
        diff_output = get_git_diff(repo, staged, file_path)

        if not diff_output:
            typer.echo("没有检测到更改。")
        else:
            beautify_diff(diff_output)

    except InvalidGitRepositoryError:
        typer.echo("错误：当前目录不是有效的Git仓库。", err=True)
    except GitCommandError as e:
        typer.echo(f"Git命令执行错误：{str(e)}", err=True)

@app.command()
def log(
        limit: int = typer.Option(10, "--limit", "-n", help="显示的提交数量"),
        since: str = typer.Option(None, "--since", "-s", help="显示指定日期之后的提交，格式：YYYY-MM-DD"),
        until: str = typer.Option(None, "--until", "-u", help="显示指定日期之前的提交，格式：YYYY-MM-DD"),
):
    """美观地显示git log"""
    try:
        repo = Repo('.')
        commits = repo.iter_commits()

        if since:
            since_date = datetime.strptime(since, "%Y-%m-%d")
            commits = filter(lambda c: c.committed_datetime > since_date, commits)

        if until:
            until_date = datetime.strptime(until, "%Y-%m-%d")
            commits = filter(lambda c: c.committed_datetime < until_date, commits)

        table = Table(title="Git Log")
        table.add_column("提交哈希", style="cyan", no_wrap=True)
        table.add_column("作者", style="magenta")
        table.add_column("日期", style="green")
        table.add_column("提交信息", style="yellow")

        for _commit in list(commits)[:limit]:
            table.add_row(
                _commit.hexsha[:7],
                _commit.author.name,
                _commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                _commit.message.split('\n')[0]
            )

        console.print(table)

    except InvalidGitRepositoryError:
        typer.echo("错误：当前目录不是有效的Git仓库。", err=True)
    except GitCommandError as e:
        typer.echo(f"Git命令执行错误：{str(e)}", err=True)


@diff_app.command("commit")
def commit_diff(commit_hash: str = typer.Argument(..., help="指定的commit哈希值")):
    """显示指定commit的diff"""
    try:
        repo = Repo('.')
        diff_output = get_commit_diff(repo, commit_hash)
        beautify_diff(diff_output)
    except InvalidGitRepositoryError:
        typer.echo("错误：当前目录不是有效的Git仓库。", err=True)
    except GitCommandError as e:
        typer.echo(f"Git命令执行错误：{str(e)}", err=True)


@app.command()
def version():
    """显示当前软件版本"""
    typer.echo(f"AI Git Utils V{__version__}")

app.add_typer(model_app, name="model", help="管理AI模型")
app.add_typer(diff_app, name="diff", help="查看代码更改")
