from nicegui import ui

def organizer_final_page(engine):

    @ui.page("/organizer/final")
    def organizer_final():
        if engine.state != "finished":
            ui.navigate.to(f"/organizer/{engine.state}")
            return

        leaderboard = engine.leaderboard()
        if not leaderboard:
            ui.label("Aucun joueur à afficher.")
            return

        winner = leaderboard[0]["name"]
        ui.label("🏆 Résultats finaux").classes("text-3xl font-bold mb-4 text-green-700")
        ui.label(f"🎉 Le grand vainqueur est : {winner} 🎉").classes("text-2xl text-purple-700 mb-6")

        ui.table(
            columns=[
                {"name": "name", "label": "Nom", "field": "name"},
                {"name": "score", "label": "Score", "field": "score"},
            ],
            rows=leaderboard,
        ).classes("w-full max-w-md mb-8")

        ui.button("🔄 Nouvelle partie", on_click=lambda: restart_game()).props("color=primary text-lg")

        def restart_game():
            engine.players.clear()
            engine.state = "lobby"
            engine.vip_id = None
            engine.current_q = None
            ui.navigate.to("/organizer/prep")
