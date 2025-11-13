from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, Title, Subtitle, TextInput, PrimaryButton
import uuid


def participant_connect_page(engine):

    @ui.page('/participant/connect')
    def connect():
        with mobile_layout():
            with Card()():
                Title("🎮 Connexion au jeu")()
                Subtitle("Entre ton prénom pour rejoindre la partie")()

                name_input = TextInput("Ton prénom", "Ex: Lucas")()

                def register_player():
                    name = name_input.value.strip()
                    if not name:
                        ui.notify("Veuillez entrer un prénom.", type="warning")
                        return

                    session_id = app.storage.user.get("player_id")

                    # 🔧 AUTO-GÉNÉRATION DE LA SESSION SI ABSENTE
                    if not session_id:
                        session_id = str(uuid.uuid4())
                        app.storage.user["player_id"] = session_id

                    # on enregistre toujours le nom
                    app.storage.user["player_name"] = name

                    # enregistre le joueur dans l'engine
                    engine.register_player(session_id, name)

                    ui.notify(f"Bienvenue {name} !", type="positive")
                    ui.navigate.to("/participant/wait")

                PrimaryButton("Rejoindre le jeu", register_player)()

                ui.label("GoldenQuizz © 2025").classes("text-gray-400 text-sm mt-6")
