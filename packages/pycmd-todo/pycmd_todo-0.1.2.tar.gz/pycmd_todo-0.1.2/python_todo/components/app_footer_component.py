"""App footer component module."""
from textual.widgets import Footer

class AppFooter(Footer):
    DEFAULT_CSS = """
    AppFooter {
            height: 1;
            dock: bottom;
            color: #c0c90c;
            background: $surface;
            }
    AppFooter > .footer--highlight {
        background: $accent-darken-1;
    }

    AppFooter > .footer--highlight-key {
        background: $secondary;
        text-style: bold;
    }

    AppFooter > .footer--key {
        text-style: bold;
        background: black;
    }
    """
