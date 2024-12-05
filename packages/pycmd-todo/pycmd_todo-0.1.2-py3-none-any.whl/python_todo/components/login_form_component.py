"""Login form component module."""
from pydantic import BaseModel
from textual import on
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Static

from python_todo.components.error_message import ErrorMessage



class Form(Vertical):
    # BORDER_TITLE = 'Login'
    DEFAULT_CSS = """
    Form {
            align: center middle;
            height: 50%;
            }
    .login-input {
            margin: 1;
            border: none;
            background: black;
            padding: 1;
            }
    .login-input:focus {
            border: none;
            }
    #login-btn {
            width: 100%;
            margin: 1;
            }
    #login-lbl {
            text-align: center;
            width: 1fr;
            }
    """
    def compose(self) -> ComposeResult:

        yield Label('Login', id='login-lbl')
        yield Input(placeholder='Username',
                    classes='login-input',
                    id="login-username")
        yield Input(placeholder='Password',
                        classes='login-input',
                        id='login-password',
                        password=True)
        yield Button(label='Login', id='login-btn')
        yield ErrorMessage(id='login-error')

class LoginPayload(BaseModel):
    username: str
    password: str

class LoginForm(Static):
    """Todo app login form."""
    DEFAULT_CSS = """
    LoginForm {
            align: center middle;
            }
    """
    def compose(self) -> ComposeResult:
        yield  Form()

    class LoginMessage(Message):
        """Login message."""
        def __init__(self, credentials: LoginPayload) -> None:
            self.crendials = credentials
            super().__init__()

    @on(Input.Submitted, '#login-username')
    async def focus_password(self) -> None:
        await self.run_action('focus_next')

    @on(Input.Submitted, '#login-password')
    async def submit(self) -> None:
        self.post_message(self.get_credentials())

    @on(Button.Pressed, '#login-btn')
    async def login_btn_pressed(self) -> None:
        self.post_message(self.get_credentials())

    def get_credentials(self) -> LoginMessage:
        """Get credentials."""
        username = self.query_one('#login-username', Input).value
        password = self.query_one('#login-password', Input).value

        return self.LoginMessage(
                LoginPayload(
                username=username,
                password=password
                ))
