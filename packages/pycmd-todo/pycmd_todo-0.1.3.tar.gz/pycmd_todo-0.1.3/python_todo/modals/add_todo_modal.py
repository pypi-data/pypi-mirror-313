"""Todo add modal module."""
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label

class AddTodoModal(ModalScreen[str]):
    """Add todo."""
    BINDINGS = [
            Binding('escape', 'cancel_add_todo', 'Cancel', show=False),
            ]
    CSS = """
    #dialog {
            padding: 0 1;
            width: 60;
            height: auto;
            border: thick $background 80%;
            background: $surface;
        }
    #add-todo-modal-input {
            margin: 1;
            border: none;
            border: solid #c0c90c;
            }
    #add-todo-modal-input:focus {
            border: none;
            border: solid #c0c90c;
            }
    #add-todo-modal-lbl {
            width: 100%;
            text-align: center;
            }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id='dialog'):
            yield Label('Add todo', id='add-todo-modal-lbl')
            yield Input(placeholder='New todo', id="add-todo-modal-input")

    def action_cancel_add_todo(self) -> None:
        """Cancel adding todo."""
        self.app.pop_screen()

    @on(Input.Submitted, '#add-todo-modal-input')
    def modal_add_todo(self) -> None:
        title = self.query_one('#add-todo-modal-input', Input).value
        self.dismiss(title)
