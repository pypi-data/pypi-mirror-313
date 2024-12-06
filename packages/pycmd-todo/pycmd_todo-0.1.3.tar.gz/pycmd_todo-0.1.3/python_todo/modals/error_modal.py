"""Todo error modal module."""
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

class ErrorModal(ModalScreen):
    """Error message modal."""
    BINDINGS = [
            Binding('escape', 'exit_modal', 'Quit modal', show=False),
            Binding('enter', 'exit_modal', 'Quit modal', show=False),
            Binding('q', 'exit_modal', 'Quit modal', show=False),
            ]
    CSS = """
    #error-dialog {
            padding: 0 1;
            width: 60;
            color: red;
            height: auto;
            border: thick $background 80%;
            background: $surface;
            align: center middle;
        }
    #error-modal-button {
            width: auto;
            margin: 1;
            }
    #todo-error-modal-label {
            width: 100%;
            text-align: center;
            }
    """
    def compose(self) -> ComposeResult:
        msg = self.app.error_message or 'Unknown Error'
        with Vertical(id='error-dialog'):
            yield Label(msg, id='todo-error-modal-label')
            yield Center(Button(label='Ok', id='error-modal-button'))

    def action_exit_modal(self) -> None:
        """Exit modal."""
        self.app.pop_screen()

    @on(Button.Pressed, '#error-modal-button')
    async def quit_error_modal(self) -> None:
        """Exit modal."""
        await self.run_action('exit_modal')
