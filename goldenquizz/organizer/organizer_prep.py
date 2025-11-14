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

                        # ---------------- QUESTIONS YAML (pliable) ----------------
            with OrganizerCard()():

                ui.label("📝 Liste des questions (YAML)").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                # Zone repliable
                with ui.expansion("Afficher / masquer la configuration YAML").classes(
                    "w-full text-lg"
                ) as yaml_expansion:

                    # Pré-remplir le YAML depuis engine.config
                    import yaml
                    yaml_text = ui.textarea(
                        label="Configuration YAML",
                        value=yaml.safe_dump(engine.config, sort_keys=False, allow_unicode=True),
                    ).classes("w-full h-80 text-base font-mono bg-gray-50 p-3 rounded-xl")

                    def apply_yaml_update():
                        try:
                            # 1) Vérifier YAML valide
                            new_config = yaml.safe_load(yaml_text.value)

                            if not isinstance(new_config, dict):
                                raise ValueError("Le YAML doit contenir un objet racine (dict).")

                            # 2) Validation stricte
                            if "questions" not in new_config:
                                raise ValueError("Clé 'questions' manquante.")
                            if not isinstance(new_config["questions"], list):
                                raise ValueError("'questions' doit être une liste.")

                            for q in new_config["questions"]:
                                if "text" not in q:
                                    raise ValueError("Chaque question doit contenir 'text'.")
                                if "options" not in q:
                                    raise ValueError("Chaque question doit contenir 'options'.")
                                if not isinstance(q["options"], list):
                                    raise ValueError("'options' doit être une liste.")
                                if "points" in q and not isinstance(q["points"], int):
                                    raise ValueError("'points' doit être un entier.")
                                if "duration" in q and not isinstance(q["duration"], int):
                                    raise ValueError("'duration' doit être un entier.")

                            # 3) Overwrite mémoire
                            engine.config = new_config
                            engine.questions = new_config["questions"]

                            # 4) Reset moteur
                            engine.players.clear()
                            engine.vip_id = None
                            engine.current_q = None
                            engine.answers.clear()
                            engine.state = "lobby"

                            ui.notify("✔ Configuration mise à jour et jeu réinitialisé.", type="positive")

                        except Exception as e:
                            ui.notify(f"Erreur YAML : {e}", type="negative")

                    ui.button(
                        "💾 Mettre à jour les questions",
                        on_click=apply_yaml_update
                    ).classes(
                        "mt-4 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-xl"
                    )

            
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
