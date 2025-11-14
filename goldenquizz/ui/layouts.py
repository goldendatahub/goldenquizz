from nicegui import ui
from contextlib import contextmanager
from . import theme

def mobile_layout():
    return ui.column().classes(
        "min-h-screen w-full p-4 bg-gray-50 flex items-center justify-center"
    )

@contextmanager
def organizer_layout():
    with ui.column().classes(
        "min-h-screen w-full bg-gray-100 flex justify-start items-start py-10 px-6"
    ):
        with ui.column().classes(
            "w-full max-w-6xl bg-white rounded-2xl shadow-2xl p-12 gap-10 animate-fadeIn"
        ) as container:
            yield container

@contextmanager
def organizer_header():
    with ui.row().classes(
        "w-full items-center justify-between border-b pb-4 mb-6"
    ):
        yield

@contextmanager
def organizer_section(title: str, dark: bool = False):
    if dark:
        base = "w-full bg-slate-700 border border-slate-600 shadow-xl p-6 rounded-xl"
        title_class = "text-2xl font-bold text-amber-400 mb-4"
    else:
        base = "w-full bg-white border border-gray-200 shadow-md p-6 rounded-xl"
        title_class = "text-2xl font-bold text-blue-700 mb-4"

    with ui.column().classes(base):
        ui.label(title).classes(title_class)
        yield
