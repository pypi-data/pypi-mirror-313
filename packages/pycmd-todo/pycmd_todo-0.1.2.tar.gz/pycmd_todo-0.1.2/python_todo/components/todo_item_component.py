"""Todo item component module."""
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal
from textual.widgets import Checkbox, Label, ListItem

from python_todo.models import TodoRead

class TodoItem(ListItem):
    """Todo item widget."""
    DEFAULT_CSS = """
    TodoItem {
        color: #c0c90c;
        height: auto;
        margin: 1 4;
        background: black;
        overflow: hidden hidden;
    }
    TodoItem > Widget :hover {
        background: $boost;
    }
    TodoList > TodoItem.--highlight {
        background: $accent 50%;
    }
    TodoList:focus > TodoItem.--highlight {
        background: $surface;
    }
    TodoItem > Widget {
        height: auto;
    }
    """
