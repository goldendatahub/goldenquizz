from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, Title, Subtitle
from goldenquizz.ui import theme


def participant_final_page(engine):

    @ui.page("/participant/final")
    def participant_final():

        with mobile_layout():

            # -----------------------------
            # EN-TÊTE
            # -----------------------------
            with Card()():

                pid = str(app.storage.user.get("player_id"))
                name = app.storage.user.get("player_name", "Joueur")
                vip_id = str(engine.vip_id)
                is_vip = (pid == vip_id)

                Title("🏁 Fin de la partie")()
                Subtitle(f"Merci d’avoir joué, {name} !")()

                # ---------- Classement ----------
                if not is_vip:
                    leaderboard = engine.leaderboard()
                    ui.label("🏆 Classement général").classes(
                        "text-xl font-bold text-blue-700 mt-4 mb-2 text-center"
                    )
                    for entry in leaderboard:
                        ui.label(f"{entry['name']} — {entry['score']} pts").classes(
                            "text-gray-700 text-md text-center"
                        )

            # -----------------------------
            # FOOTER
            # -----------------------------
            ui.label("GoldenQuizz © 2025").classes(
                theme.TEXT_FOOTER + " mt-8 text-center"
            )
