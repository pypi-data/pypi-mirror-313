"""Todo list items container component."""
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import Label, ListItem, ListView

from python_todo.components.todo_item_component import TodoItem
from python_todo.modals.todo_detail_modal import TodoDetailModal
from python_todo.models import TodoRead

class TodoList(ListView):
    """Todo list container widget."""
    BORDER_TITLE = "List"
    DEFAULT_CSS = """
    TodoList {
            border: solid #c0c90c;
            background: black;
            }
    """
    BINDINGS: list[BindingType] = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding(
            "down", "cursor_down", "Cursor Down", show=False
        ),
        Binding(
            "j", "cursor_down", "Cursor Down", show=False
        ),
    ]
    def compose(self) -> ComposeResult:
        for i in self.children:
            yield i

    async def on_mount(self) -> None:
        self.app.get_stats()
        for todo in self.app.todos:
            self.add(todo)

    def add(self, todo: TodoRead) -> None:
        """Add todo."""
        index = len(self) # start from 1
        self.append(TodoItem(Label(
            f"[{index + 1}]  [b]{todo.title.capitalize()}[/b]",
                                   id=f"todo-item-{index}")))

    def update_list(self) -> None:
        self.clear()
        for todo in self.app.todos:
            self.add(todo)

    def complete_todo(self) -> None:
        """Complete todo."""

        if (self.index is not None) and (self.index < len(self)):
            todo = self.app.todos.pop(self.index)
            self.update_list()
            self.app.complete_db_todo(todo)
            # for todo in self.app.todos:
            #     self.add(todo)
    def view_todo(self) -> None:
        """Complete todo."""
        if (self.index is not None) and (self.index < len(self)):
            todo = self.app.todos[self.index]
            modal = TodoDetailModal()
            modal.todo = todo
            self.app.push_screen(modal)

    def delete_todo(self) -> None:
        """Delete todo."""
        if (self.index is not None) and (self.index < len(self)):
            todo = self.app.todos.pop(self.index)
            self.update_list()
            self.app.delete_db_todo(todo)
