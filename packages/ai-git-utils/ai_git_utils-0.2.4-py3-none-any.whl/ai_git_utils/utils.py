import os
import tempfile
import subprocess
from rich.syntax import Syntax
from rich.console import Console

console = Console()

def beautify_diff(diff_output: str) -> None:
    syntax = Syntax(diff_output, "diff", line_numbers=True, word_wrap=True, indent_guides=False, theme="monokai")
    console.print(syntax)

def edit_commit_message(initial_message: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".tmp", delete=False) as tf:
        tf.write(initial_message)
        tf.flush()
        tf_name = tf.name

    editor = os.environ.get('EDITOR', 'vim')
    subprocess.call([editor, tf_name])

    with open(tf_name, 'r') as tf:
        edited_message = tf.read().strip()

    os.unlink(tf_name)
    return edited_message
