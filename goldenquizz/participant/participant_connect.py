from nicegui import ui, app
import uuid


def participant_connect_page(engine):

    @ui.page("/participant/connect")
    def connect():
        ui.label("🎮 Connexion au jeu").classes("text-2xl font-bold mb-4 text-blue-700")
        name_input = ui.input("Entre ton prénom").classes("w-64")

        def register_player():
            name = name_input.value.strip()
            if not name:
                ui.notify("Merci d’entrer ton prénom avant de valider.", type="warning")
                return

            # Crée un ID de session unique
            session_id = app.storage.user.get("player_id")
            if not session_id:
                session_id = str(uuid.uuid4())
                app.storage.user["player_id"] = session_id

            # Enregistre le joueur
            engine.register_player(session_id, name)
            app.storage.user["player_name"] = name

            ui.notify(f"Bienvenue {name} !", type="positive")
            ui.navigate.to("/participant/wait")

        ui.button("✅ Valider", on_click=register_player).props("color=primary mt-2")
