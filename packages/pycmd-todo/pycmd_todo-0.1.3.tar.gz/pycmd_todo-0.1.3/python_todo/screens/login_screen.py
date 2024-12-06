"""Login screen module."""
from textual.app import ComposeResult
from textual.screen import Screen

from python_todo.components.login_form_component import LoginForm

class LoginScreen(Screen):
    """Login screen."""
    DEFAULT_CSS = """
    LoginScreen {
            align: center middle;
            }
    LoginForm {
            width: 40;
            height: 40;
            }
    """
    def compose(self) -> ComposeResult:
        yield LoginForm()
