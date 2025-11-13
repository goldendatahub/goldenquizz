from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, Title, Subtitle
from goldenquizz.ui import theme


def participant_wait_page(engine):

    
    @ui.page("/participant/wait")
    def wait():

        name = app.storage.user.get("player_name", "Inconnu")

        with mobile_layout():

            with Card()():

                # Titre utilisateur
                Title(f"👋 Bonjour {name}")()

                Subtitle("⏳ En attente du démarrage du jeu...")()

                # Animation sur le texte d'attente
                ui.label("Patiente un instant…") \
                    .classes("text-gray-500 text-md mb-6 animate-pulse text-center")

                # Tableau des joueurs connectés
                table = ui.table(
                    columns=[
                        {
                            "name": "name",
                            "label": "Joueurs connectés",
                            "field": "name",
                        }
                    ],
                    rows=[],
                ).classes(
                    "rounded-xl shadow-inner bg-gray-100 w-full"
                )

                # Fonction de mise à jour
                def refresh():
                    table.rows = [
                        {"name": p["name"] + (" 👑" if p.get("is_vip") else "")}
                        for p in engine.players.values()
                    ]

                    # Si la partie commence ⇒ navigation
                    if engine.state == "running":
                        ui.navigate.to("/participant/question")

                ui.timer(2, refresh)

                # Footer discret
                ui.label("GoldenQuizz © 2025") \
                    .classes(theme.TEXT_FOOTER + " mt-6")
    
