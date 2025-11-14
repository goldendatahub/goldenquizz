from nicegui import ui
from goldenquizz.ui.layouts import organizer_layout, organizer_header
from goldenquizz.ui.components import OrganizerTitle, OrganizerCard, OrganizerButton


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

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():
                OrganizerTitle("🏆 Résultats finaux")()
                ui.label("Fin de partie").classes("text-md text-gray-500 italic")

            # ---------------- WINNER ----------------
            with OrganizerCard()():
                ui.label(f"🎉 Le grand vainqueur est : {winner} 🎉").classes(
                    "text-3xl font-extrabold text-purple-700 mb-6 text-center"
                )

            # ---------------- LEADERBOARD ----------------
            with OrganizerCard()():
                ui.label("🏅 Classement final").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                ui.table(
                    columns=[
                        {"name": "name", "label": "Nom", "field": "name"},
                        {"name": "score", "label": "Score", "field": "score"},
                    ],
                    rows=leaderboard,
                ).classes(
                    "w-full max-w-xl border border-gray-200 rounded-xl shadow-sm "
                    "hover:shadow-md transition"
                )

            # ---------------- RESTART BUTTON ----------------
            with OrganizerCard()():

                def restart_game():
                    engine.players.clear()
                    engine.state = "lobby"
                    engine.vip_id = None
                    engine.current_q = None
                    ui.navigate.to("/organizer/prep")

                OrganizerButton("🔄 Nouvelle partie", restart_game)().classes(
                    "mt-4 bg-green-600 hover:bg-green-700"
                )
