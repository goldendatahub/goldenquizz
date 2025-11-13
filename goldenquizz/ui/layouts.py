from nicegui import ui
from . import theme

def mobile_layout():
    """Layout centré pour les pages participant"""
    return ui.column().classes("min-h-screen w-full p-4 bg-gray-50 flex items-center justify-center")


def desktop_layout():
    """Layout large pour les pages organisateur (projecteur)"""
    return ui.column().classes(
        "min-h-screen w-full p-8 bg-gray-50 items-start justify-start"
    )