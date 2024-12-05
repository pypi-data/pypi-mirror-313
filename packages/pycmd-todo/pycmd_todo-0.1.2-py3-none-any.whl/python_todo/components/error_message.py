"""Error message widget module."""
from textual.reactive import reactive
from textual.widget import Widget

class ErrorMessage(Widget):
    """Log errors"""
    DEFAULT_CSS = """
    ErrorMessage {
            text-align: center;
            height: auto;
            margin: 1;
            color: red;
            }"""
    msg = reactive('')

    def render(self):
        return f"{self.msg}"
