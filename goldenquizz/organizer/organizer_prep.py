from nicegui import ui
from goldenquizz.ui.layouts import organizer_layout, organizer_header, organizer_section
from goldenquizz.ui.components import OrganizerTitle, OrganizerCard, OrganizerButton


def organizer_prep_page(engine):

    @ui.page("/organizer/prep")
    def organizer_prep():
        if engine.state != "lobby":
            ui.navigate.to(f"/organizer/{engine.state}")
            return

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():
                OrganizerTitle("🛠️ Préparation de la partie")()
                ui.label("Mode organisateur").classes("text-md text-gray-500 italic")

            # ---------------- JOUEURS ----------------
            with OrganizerCard()():
                ui.label("📋 Joueurs connectés").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                players_container = ui.row().classes(
                    "w-full flex-wrap gap-4 mt-4"
                )


            # ---------------- VIP ----------------
            with OrganizerCard()():

                ui.label("👑 Sélection du VIP").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                vip_selector = ui.select(
                    options={},
                    label="Choisir le VIP",
                ).classes("w-72 text-lg")

                def define_vip():
                    pid = vip_selector.value
                    if not pid:
                        ui.notify("Veuillez sélectionner un joueur.", type="warning")
                        return
                    engine.set_vip(pid)
                    ui.notify(f"{engine.players[pid]['name']} est maintenant le VIP 👑")

                OrganizerButton("Valider le VIP", define_vip)().classes("mt-4")

            # ---------------- START ----------------
            with OrganizerCard()():

                ui.label("🎬 Démarrer la partie").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                def start_game():
                    if not engine.vip_id:
                        ui.notify("Veuillez définir le VIP avant de démarrer.", type="warning")
                        return
                    engine.open_question(0)
                    ui.navigate.to("/organizer/question")

                OrganizerButton("▶️ Lancer la partie", start_game)().classes("mt-4")

            # ---------------- REFRESH ----------------
            def refresh():
                players_container.clear()
                for pid, p in engine.players.items():
                    is_vip = p.get("is_vip")

                    with players_container:
                        with ui.column().classes(
                            "p-4 bg-blue-50 rounded-xl shadow-md items-center w-40 border "
                            "border-blue-200 animate-fadeIn"
                        ):
                            ui.label(p["name"]).classes(
                                "text-lg font-bold text-blue-800 text-center"
                            )

                            if is_vip:
                                ui.label("👑 VIP").classes(
                                    "text-yellow-600 font-semibold mt-1"
                                )


                vip_selector.options = {
                    pid: p["name"] for pid, p in engine.players.items()
                }
                vip_selector.update()

            ui.timer(1.0, refresh)
