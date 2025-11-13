from nicegui import ui
from . import theme


def Title(text: str):
    """Titre stylé (retardé)"""
    def _title():
        return ui.label(text).classes(theme.TEXT_TITLE)
    return _title


def Subtitle(text: str):
    """Sous-titre stylé (retardé)"""
    def _subtitle():
        return ui.label(text).classes(theme.TEXT_SUBTITLE)
    return _subtitle


def Card():
    """Container card (utilisation : with Card()(): ...)"""
    def _card():
        return ui.card().classes(theme.CARD_CLASSES)
    return _card


def PrimaryButton(label: str, on_click=None):
    """Bouton stylé principal (retardé)"""
    def _button():
        return ui.button(label, on_click=on_click).classes(theme.BUTTON_PRIMARY)
    return _button


def TextInput(label: str, placeholder=None):
    """Champ texte stylé (retardé)"""
    def _input():
        return ui.input(label=label, placeholder=placeholder).classes(theme.INPUT_CLASSES)
    return _input


def QuestionCard(
    number: int,
    question_text: str,
    vip_text: str,
    me_text: str | None,
    ok: bool | None,
    points: int | None,
    correct_stats: str,
    is_vip: bool,
):
    """Affichage d'une carte récapitulative (version mobile-friendly, retardée)"""

    base_color = "bg-purple-50" if is_vip else "bg-blue-50"

    # ⚠️ Très important : NE PAS créer la carte ici
    # On retourne une fonction que la page appellera elle-même.

    def _render():
        card = ui.card().classes(
            f"rounded-xl shadow-md p-4 mb-4 w-full {base_color} {theme.CARD_FADE_IN}"
        )

        with card:

            ui.label(f"Question {number}").classes("text-lg font-bold text-gray-800")
            ui.label(question_text).classes("text-md text-gray-700 mt-2")
            ui.label(f"👑 VIP: {vip_text}").classes("text-md text-blue-600 mt-2")

            if not is_vip and me_text:
                ui.label(f"📝 Toi: {me_text}").classes("text-md text-gray-600 mt-1")

            if ok is not None:
                status = "✅ Correct!" if ok else "❌ Incorrect"
                status_class = "text-green-600" if ok else "text-red-600"
                ui.label(status).classes(f"text-md {status_class} mt-2")

            if points is not None:
                ui.label(f"📊 +{points} points").classes("text-md text-amber-600 mt-1")

            ui.label(f"📈 {correct_stats} ont trouvé").classes("text-sm text-gray-500 mt-2")

        return card

    return _render
