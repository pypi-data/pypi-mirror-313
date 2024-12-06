"""Change password modal module."""
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from python_todo.components.error_message import ErrorMessage
from python_todo.models import PasswordChange

class ChangePassword(ModalScreen[PasswordChange]):
    """Add todo."""
    BINDINGS = [
            Binding('escape', 'cancel_change_password', 'Cancel', show=False),
            ]
    CSS = """
    #dialog {
            padding: 0 1;
            width: 60;
            height: auto;
            border: thick $background 80%;
            background: $surface;
        }
    .change-password-input {
            margin: 1;
            border: none;
            border: solid #c0c90c;
            }
    .change-password-input:focus {
            border: none;
            border: solid #c0c90c;
            }
    #change-password-header {
            width: 100%;
            text-align: center;
            }
    #change-password-button-container {
            height: auto;
            }
    #change-password-button-container > Button {
            width: 50%;
            margin: 1;
            }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id='dialog'):
            yield Label('[b]Change password[/b]', id='change-password-header')
            yield Input(placeholder='Current password',
                        classes='change-password-input',
                        id='current-password-input',
                        password=True)
            yield Input(placeholder='New password',
                        classes='change-password-input',
                        id='new-password-input',
                        password=True)
            yield Input(placeholder='Confirm password',
                        classes='change-password-input',
                        id='confirm-password-input',
                        password=True)
            with Horizontal(id='change-password-button-container'):
                yield Button(label='Save', id='change-password-save-button')
                yield Button(label='Cancel', id='change-password-cancel-button')
            yield ErrorMessage(id="password-do-not-match")


    def action_cancel_change_password(self) -> None:
        """Cancel adding todo."""
        self.app.pop_screen()

    @on(Input.Submitted, '#current-password-input')
    def focus_new_password(self) -> None:
        self.focus_next()

    @on(Input.Submitted, '#new-password-input')
    def focus_confirm_password(self) -> None:
        self.focus_next()

    @on(Input.Submitted, '#confirm-password-input')
    def submit_payload(self) -> None:
        self.save_and_exit()

    @on(Button.Pressed, '#change-password-save-button')
    def call_save_and_exit(self) -> None:
        self.save_and_exit()

    @on(Button.Pressed, '#change-password-cancel-button')
    async def cancel_and_exit(self) -> None:
        await self.run_action('cancel_change_password')

    def save_and_exit(self) -> None:
        """Save and exit."""
        current_password = self.query_one('#current-password-input', Input).value
        new_password = self.query_one('#new-password-input', Input).value
        confirm_password = self.query_one('#confirm-password-input', Input).value

        if new_password != confirm_password:
            msg = 'Passwords do not match.'
            self.query_one('#password-do-not-match', ErrorMessage).msg = msg
        else:
            payload = PasswordChange(
                    current_password=current_password,
                    new_password=new_password
                    )
            self.dismiss(payload)
