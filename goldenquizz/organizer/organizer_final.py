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

        # Tri du classement final (score desc)
        leaderboard_sorted = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

        winner = leaderboard_sorted[0]["name"]

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

                container = ui.column().classes("w-full gap-4")

                position = 1
                for entry in leaderboard_sorted:
                    name = entry["name"]
                    score = entry["score"]

                    with container:
                        # même style que organizer_results
                        with ui.row().classes(
                            "items-center justify-between bg-white border "
                            "border-gray-300 rounded-xl shadow-sm p-4 w-full "
                        ):
                            ui.label(f"#{position} — {name}").classes(
                                "text-lg font-bold text-gray-800"
                            )
                            ui.label(f"{score} pts").classes(
                                "text-lg font-semibold text-blue-700"
                            )

                    position += 1

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
