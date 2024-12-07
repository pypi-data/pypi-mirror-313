from _typeshed import Incomplete
from gitnote.commitgen.generator import commit_generator as commit_generator
from gitnote.config.settings import load_token as load_token, save_token as save_token
from gitnote.gittools.tools import display_diff as display_diff, ensure_git_repository as ensure_git_repository, get_git_diff as get_git_diff
from gitnote.utils import validate_token as validate_token
from typing import Annotated

app: Incomplete
console: Incomplete

def generate() -> None: ...
def diff() -> None: ...
def set_token(token: Annotated[str, None] = ''): ...
def main() -> None: ...
