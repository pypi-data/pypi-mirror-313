"""Todo detail modal module."""
from typing import Optional
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from python_todo.models import TodoRead

class TodoDetailModal(ModalScreen):
    """Error message modal."""

    todo: reactive[Optional[TodoRead]] = reactive(None)

    BINDINGS = [
            Binding('escape', 'exit_modal', 'Quit modal', show=False),
            Binding('enter', 'exit_modal', 'Quit modal', show=False),
            Binding('q', 'exit_modal', 'Quit modal', show=False),
            ]
    CSS = """
    #error-dialog {
            padding: 0 1;
            width: auto;
            height: auto;
            border: thick $background 80%;
            background: $surface;
        }
    #detail-modal-header {
            width: 100%;
            margin-bottom: 1;
            text-align: center;
            }
    """
    def compose(self) -> ComposeResult:
        if self.todo:
            with Vertical(id='error-dialog'):
                yield Label('[b]Todo Detail[/b]', id="detail-modal-header")
                if self.app.user:
                    yield Label(f"Username:     {self.app.user.username}")
                yield Label(f"Title:        {self.todo.title.capitalize()}")
                status = 'Complete' if self.todo.done else 'Pending'
                yield Label(f"Status:       {status}")
                fmt = '%d-%m-%Y %H:%M'
                yield Label(f"Date:         {self.todo.create_date.strftime(fmt)}")

    def action_exit_modal(self) -> None:
        """Exit modal."""
        self.app.pop_screen()
