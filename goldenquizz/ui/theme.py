# goldenquizz/ui/theme.py

PRIMARY_COLOR = "blue-600"
PRIMARY_COLOR_HOVER = "blue-700"

BACKGROUND_LIGHT = "bg-gray-50"
CARD_BG = "bg-white"

TEXT_TITLE = "text-3xl font-bold text-blue-600"
TEXT_SUBTITLE = "text-lg text-gray-600"
TEXT_FOOTER = "text-gray-400 text-sm"

CARD_CLASSES = "bg-white p-8 rounded-2xl shadow-xl"
INPUT_CLASSES = (
    "w-full text-lg p-3 border rounded-xl "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)
BUTTON_PRIMARY = (
    "w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold "
    "text-lg py-3 rounded-xl shadow-md transition"
)

# Layout helper
def page_container():
    return "min-h-screen w-full p-4 bg-gray-50 flex items-center justify-center"

# Carte avec fade-in
CARD_FADE_IN = (
    "transition duration-700 "
    "opacity-0 animate-fadeIn "
)

# Carte réponse correcte
CARD_GOOD = "bg-green-50 border-l-4 border-green-500"

# Carte réponse incorrecte
CARD_BAD = "bg-red-50 border-l-4 border-red-500"

GLOBAL_CSS = """
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
    animation: fadeIn 0.5s ease forwards;
}
"""
