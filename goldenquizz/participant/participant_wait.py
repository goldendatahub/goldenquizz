from nicegui import ui, app


def participant_wait_page(engine):

    @ui.page("/participant/wait")
    def wait():
        name = app.storage.user.get("player_name", "Inconnu")
        ui.label(f"👋 Bonjour {name}").classes("text-xl font-semibold mb-2")
        ui.label("⏳ En attente du démarrage du jeu...").classes("text-lg mb-4")

        table = ui.table(columns=[{"name": "name", "label": "Joueurs connectés", "field": "name"}], rows=[])

        def refresh():
            table.rows = [{"name": p["name"] + (" 👑" if p.get("is_vip") else "")} for p in engine.players.values()]

            # Si la partie a démarré → redirection
            if engine.state == "running":
                ui.navigate.to("/participant/question")

        ui.timer(2, refresh)
