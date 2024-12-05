"""Main todo app layout module."""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import HorizontalScroll

from python_todo.components.app_header_component import AppHeader
from python_todo.components.app_footer_component import AppFooter
from python_todo.components.todo_list_component import TodoList

class TodoScreen(Screen):
    def compose(self) -> ComposeResult:
        yield AppHeader(id="AppHeader")
        yield AppFooter()
        with HorizontalScroll():
            yield TodoList(id='todo-list')

    async def on_mount(self) -> None:
        self.query_one(TodoList).focus()
