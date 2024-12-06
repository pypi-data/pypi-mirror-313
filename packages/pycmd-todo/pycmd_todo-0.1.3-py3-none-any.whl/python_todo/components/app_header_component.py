"""App header component module."""
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Horizontal

from python_todo.models import TodoStat

class TotalTodo(Widget):
    """Total todos."""
    value: reactive[int] = reactive(0)

    def render(self) -> str:
        return f"Total: [b]{self.value}[/b]"

class CompletedTodo(Widget):
    """Completed todos."""
    value: reactive[int] = reactive(0)

    def render(self) -> str:
        return f"Completed: [b]{self.value}[/b]"

class PendingTodo(Widget):
    """Pending todos."""
    value: reactive[int] = reactive(0)

    def render(self) -> str:
        return f"Pending: [b]{self.value}[/b]"

class UsernameDisplay(Widget):
    """Username display."""

    value: reactive[str] = reactive('')

    def render(self) -> str:
        return f"Username: [b]{self.value}[/b]"

class AppHeader(Static):
    DEFAULT_CSS = """
    AppHeader {
            height: 3;
            dock: top;
            background: black;
            }
    .app-header-label {
            width: auto;
            height: auto;
            padding: 1;
            }
    """
    def compose(self) -> ComposeResult:
        if self.app.user:
            with Horizontal():
                yield TotalTodo(classes='app-header-label')
                yield CompletedTodo(classes='app-header-label')
                yield PendingTodo(classes='app-header-label')
                display = UsernameDisplay(classes='app-header-label')
                display.value = self.app.user.username
                yield display
