"""Change username modal module."""
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button

class ChangeUsername(ModalScreen[str]):
    """Add todo."""
    BINDINGS = [
            Binding('escape', 'cancel_change_username', 'Cancel', show=False),
            ]
    CSS = """
    #dialog {
            padding: 0 1;
            width: 60;
            height: auto;
            border: thick $background 80%;
            background: $surface;
        }
    #change-username-modal-input {
            margin: 1;
            border: none;
            border: solid #c0c90c;
            }
    #change-username-modal-input:focus {
            border: none;
            border: solid #c0c90c;
            }
    #change-username-header {
            width: 100%;
            text-align: center;
            }
    #change-username-button-container {
            height: auto;
            }
    #current-username-label {
            margin: 1 2;
            }
    #change-username-button-container > Button {
            width: 50%;
            margin: 1;
            }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id='dialog'):
            yield Label('[b]Change Username[/b]', id='change-username-header')
            yield Label(f'Current username: [b]{self.app.user.username}[/b]',
                        id='current-username-label')
            yield Input(placeholder='New username', id="change-username-modal-input")
            with Horizontal(id='change-username-button-container'):
                yield Button(label='Save', id='change-username-save-button')
                yield Button(label='Cancel', id='change-username-cancel-button')

    def action_cancel_change_username(self) -> None:
        """Cancel adding todo."""
        self.cancel_and_exit()

    @on(Input.Submitted, '#change-username-modal-input')
    def modal_add_todo(self) -> None:
        self.save_and_exit()

    @on(Button.Pressed, '#change-username-save-button')
    def save_username(self) -> None:
        """Save and exit."""
        self.save_and_exit()
    @on(Button.Pressed, '#change-username-cancel-button')
    def cancel_change_username(self) -> None:
        """Cancel and exit."""
        self.cancel_and_exit()

    def cancel_and_exit(self) -> None:
        """Cancel and exit."""
        self.app.pop_screen()

    def save_and_exit(self) -> None:
        username = self.query_one('#change-username-modal-input', Input).value
        self.dismiss(username)
