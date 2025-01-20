# shortcuts/__init__.py

from .main import on_press, shortcuts, confirm_key, controller
from .database import engine, Base, get_db
from .crud import create_shortcut, get_shortcut, get_shortcuts, update_shortcut, delete_shortcut

__all__ = [
    "on_press",
    "shortcuts",
    "confirm_key",
    "controller",
    "engine",
    "Base",
    "get_db",
    "create_shortcut",
    "get_shortcut",
    "get_shortcuts",
    "update_shortcut",
    "delete_shortcut",
]