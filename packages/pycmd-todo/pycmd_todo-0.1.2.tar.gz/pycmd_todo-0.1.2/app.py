#!/bin/env python
"""Todo app main module."""
from typing import Optional
from textual import on
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.widgets import ListView
from textual.binding import Binding
from python_todo.components.app_header_component import CompletedTodo
from python_todo.components.app_header_component import PendingTodo
from python_todo.components.app_header_component import TotalTodo
from python_todo.components.app_header_component import UsernameDisplay
from python_todo.components.login_form_component import LoginForm
from python_todo.components.error_message import ErrorMessage

from sqlalchemy import func, select, update, delete
from sqlalchemy.exc import IntegrityError
from python_todo.components.todo_list_component import TodoList
from python_todo.db import Todo, TodoUser, get_db
from python_todo.modals.change_password_modal import ChangePassword
from python_todo.modals.change_username_modal import ChangeUsername
from python_todo.modals.error_modal import ErrorModal
from python_todo.security import verify_password, get_password_hash
from python_todo.models import PasswordChange, TodoCreate, TodoRead, TodoStat, TodoUserRead
from python_todo.screens.main_screen import TodoScreen
from python_todo.screens.login_screen import LoginScreen
from python_todo.modals.add_todo_modal import AddTodoModal

class TodoApp(App):
    """A Textual todo app."""

    MODES = {
            'login': LoginScreen,
            'home': TodoScreen,
            }
    user: reactive[Optional[TodoUserRead]] = reactive(None)
    todos: reactive[list[TodoRead]] = reactive([], layout=True, always_update=True)
    todos_stat: reactive[TodoStat | None] = reactive(TodoStat(), always_update=True)
    error_message: str | None = None

    CSS = """
    Screen {
            align: center middle;
            color: #c0c90c;
            }"""

    BINDINGS = [
            Binding("a", "add_todo", "Add", key_display='a'),
            Binding("c", "completed_todo", "Completed", key_display='c'),
            Binding("d", "delete_todo", "Delete", key_display='d'),
            Binding("v", "todo_detail", "View", key_display='v'),
            Binding('u', 'change_username', 'Change username', key_display='u'),
            Binding('p', 'change_password', 'Change password', key_display='p'),
            Binding("l", "todo_logout", "Logout", key_display="l"),
            Binding("q", "quit", "Quit", key_display="q"),
            ]


    async def on_mount(self) -> None:
        self.switch_mode('login')

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_completed_todo(self) -> None:
        """Mark todo as completed."""
        lst = self.query_one('#todo-list', ListView)
        lst.complete_todo()

    def action_delete_todo(self) -> None:
        """Delete todo."""
        lst = self.query_one('#todo-list', ListView)
        lst.delete_todo()

    def action_todo_detail(self) -> None:
        """View todo detail."""
        lst = self.query_one('#todo-list', ListView)
        lst.view_todo()

    def action_add_todo(self) -> None:
        """Add todo."""
        def get_todo_title(title: str) -> None:
            if title:
                title.strip().lower()
                if self.user:
                    try:
                        todo = TodoCreate(user_id=self.user.id, title=title)
                        todo_db = Todo(**todo.model_dump())
                        session = get_db()
                        session.add(todo_db)
                        session.commit()
                        session.refresh(todo_db)
                        self.todos = self.todos[:] + [
                                TodoRead(**todo_db.__dict__)
                                ]
                        self.get_stats()
                    except IntegrityError:
                        self.push_screen(ErrorModal())
                        return
        self.push_screen(AddTodoModal(), get_todo_title)

    def action_change_username(self) -> None:
        """Change username."""

        def new_username(username: str) -> None:
            if username and self.user:
                username = username.strip().lower()
                try:
                    session = get_db()
                    stmt = update(TodoUser).where(
                            TodoUser.id == self.user.id
                            ).values(username=username)
                    result = session.execute(stmt)
                    session.commit()
                    user = self.get_user_by_username(username)
                    self.user = user
                except IntegrityError:
                    self.error_message = 'Username exists.'
                    self.push_screen(ErrorModal())

        self.push_screen(ChangeUsername(), new_username)

    def action_change_password(self) -> None:
        """Change password."""

        def new_password(payload: PasswordChange) -> None:
            """Set new password"""
            if self.user:
                stmt = select(TodoUser).where(TodoUser.id == self.user.id)
                session = get_db()
                db_user = session.execute(stmt).scalar_one_or_none()
                session.commit()
                if db_user is None:
                    self.error_message = 'User not found.'
                    self.push_screen(ErrorModal())
                    return

                valid_password = verify_password(
                        payload.current_password,
                        db_user.password_hash
                        )
                if not valid_password:
                    self.error_message = 'Invalid current password.'
                    self.push_screen(ErrorModal())
                    return
                password_hash = get_password_hash(payload.new_password)
                stmt = update(TodoUser).where(TodoUser.id == db_user.id).values(
                        password_hash=password_hash
                        )
                session.execute(stmt)
                session.commit()

        self.push_screen(ChangePassword(), new_password)

    def watch_todos(self, old_value, new_value) -> None:
        """Refresh list."""
        try:
            lst = self.query_one('#todo-list', TodoList)
            lst.update_list()
        except NoMatches:
            pass

    def watch_user(self, old_value: TodoUserRead, new_value: TodoUserRead) -> None:
        """Refresh user."""
        try:
            if new_value:
                self.query_one(UsernameDisplay).value = new_value.username
        except NoMatches:
            pass

    def watch_todos_stat(self, old_value: TodoStat, new_value: TodoStat) -> None:
        """Refresh stats."""
        try:
            self.query_one(TotalTodo).value = new_value.total
            self.query_one(CompletedTodo).value = new_value.completed
            self.query_one(PendingTodo).value = new_value.pending
        except NoMatches:
            pass

    def get_user_by_username(self, username: str) -> TodoUserRead:
        """Fetch user by username."""
        session = get_db()
        stmt = select(TodoUser).where(TodoUser.username == username)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        return TodoUserRead(**user.__dict__)

    def get_stats(self) -> None:
        """Fetch stats."""
        if self.user:
            total_stmt = select(func.count()).select_from(Todo).where(
                    Todo.user_id == self.user.id
                    )
            pending_stmt = select(func.count()).select_from(Todo).where(
                    Todo.done == False,
                    Todo.user_id == self.user.id
                    )
            session = get_db()
            total = session.execute(total_stmt).scalar() or 0
            pending = session.execute(pending_stmt).scalar() or 0
            session.commit()
            completed = total - pending

            self.todos_stat = TodoStat(
                    total=total,
                    pending=pending,
                    completed=completed
                    )
            print(self.todos_stat)

    def get_db_todos(self) -> None:
        """Fetch todos."""
        if self.user:
            self.get_stats()
            stmt= select(Todo).where(Todo.done == False, Todo.user_id == self.user.id)
            session = get_db()
            result = session.execute(stmt)
            todo_list = result.scalars().all()
            self.todos = [TodoRead(**i.__dict__) for i in todo_list]

    def complete_db_todo(self, todo: TodoRead) -> None:
        """Mark todo completed."""
        stmt = select(Todo).where(Todo.id == todo.id)
        session = get_db()
        result = session.execute(stmt)
        item = result.scalar_one_or_none()
        if item is None:
            self.error_message = 'Todo not found.'
            self.push_screen(ErrorModal())
            return
        stmt = update(Todo).where(Todo.id == todo.id).values(done=True)
        result = session.execute(stmt)
        session.commit()
        self.get_stats()

    def delete_db_todo(self, todo: TodoRead) -> None:
        """Delete todo."""
        stmt = select(Todo).where(Todo.id == todo.id)
        session = get_db()
        result = session.execute(stmt)
        todo = result.scalar_one_or_none()
        if todo is None:
            self.error_message = 'Todo not found.'
            self.push_screen(ErrorModal())
            return
        session.execute(delete(Todo).where(Todo.id == todo.id))
        session.commit()
        self.get_stats()


    @on(LoginForm.LoginMessage)
    def login(self, message:LoginForm.LoginMessage) -> None:
        """Login."""
        username = message.crendials.username
        password = message.crendials.password

        stmt = select(TodoUser).where(TodoUser.username == username)
        session = get_db()
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        msg = 'Invalid username or password.'

        if user is None:
            self.query_one('#login-error', ErrorMessage).msg = msg
            return

        valid_password = verify_password(password, user.password_hash)
        if not valid_password:
            self.query_one('#login-error', ErrorMessage).msg = msg
            return

        self.user = TodoUserRead(**user.__dict__)
        self.get_db_todos()
        self.switch_mode('home')

    def action_todo_logout(self) -> None:
        """Logout."""
        self.switch_mode('login')

def init():
    """Init db for the first time."""

    session = get_db()
    stmt = select(func.count()).select_from(TodoUser)
    result = session.execute(stmt)
    count = result.scalar() or 0 # None becomes 0
    if count < 1:
        print('Initializing database...')
        admin = TodoUser(username='aad', password_hash=get_password_hash('admin'))
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print('Default username=aad and password = admin')

def main():
    init()
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
