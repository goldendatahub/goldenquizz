from nicegui import ui
from goldenquizz.ui.layouts import organizer_layout, organizer_header
from goldenquizz.ui.components import OrganizerTitle, OrganizerCard, OrganizerButton


def organizer_question_page(engine):

    @ui.page("/organizer/question")
    def organizer_question():

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():

                q = engine.get_current_question()
                points = q.get("points", 0)

                # Ligne d'en-tête : numéro + points
                with ui.row().classes("items-baseline gap-4"):
                    OrganizerTitle(f"🎯 Question {engine.current_q + 1}")()
                    ui.label(f"{points} pts").classes(
                        "text-xl font-bold text-green-700"
                    )

                ui.label("Mode organisateur").classes(
                    "text-md text-gray-500 italic"
                )



            # ---------------- QUESTION + ANSWERS ----------------
            with OrganizerCard()():

                # Question (toujours tout en haut)
                question_label = ui.label("").classes(
                    "text-2xl font-semibold text-blue-800 mb-4"
                )

                # 🔥 Conteneur image juste sous la question
                image_container = ui.column().classes(
                    "w-full items-center mb-6"
                )

                # Conteneur des réponses sous l’image
                answers_container = ui.column().classes(
                    "mt-2 gap-3 w-full"
                )

                # Bouton de clôture TOUT EN BAS
                def close_question():
                    result = engine.close_question()
                    if not result:
                        ui.notify("⚠️ Aucune question active à clôturer.", type="warning")
                        return

                    ui.notify("🔒 Question clôturée, calcul des scores...", type="info")
                    ui.timer(1.0, lambda: ui.navigate.to("/organizer/results"), once=True)

                OrganizerButton("Clôturer la question", close_question)().classes(
                    "mt-6 bg-red-600 hover:bg-red-700"
                )

                # Mémorisation pour éviter redraw inutile
                last_q_index = {'value': None}

                # Fonction d’affichage
                def show_current_question():
                    q = engine.get_current_question()
                    if not q:
                        question_label.set_text("⏳ Aucune question active.")
                        answers_container.clear()
                        image_container.clear()
                        return

                    if last_q_index['value'] == engine.current_q:
                        return
                    last_q_index['value'] = engine.current_q

                    # Reset contenu visuel (sans casser l’ordre)
                    answers_container.clear()
                    image_container.clear()

                    # 1) QUESTION
                    question_label.set_text(q.get("text", "❓ Question"))

                    # 2) IMAGE (si présente et autorisée)
                    image_url = q.get("image")
                    allowed_ext = (".jpg", ".jpeg", ".png", ".gif", ".webp")

                    if isinstance(image_url, str) and image_url.lower().endswith(allowed_ext):
                        with image_container:
                            ui.image(image_url).classes(
                                "max-h-64 object-contain rounded-xl shadow-md border"
                            ).style("max-width: 100%;")

                    # 3) RÉPONSES
                    answers = (
                        q.get("answers")
                        or q.get("options")
                        or q.get("reponses")
                        or q.get("choices")
                        or []
                    )

                    if not answers:
                        with answers_container:
                            ui.label("⚠️ Aucune réponse configurée.").classes("text-red-600 mt-2")
                        return

                    with answers_container:
                        for i, answer in enumerate(answers, start=1):
                            ui.button(
                                f"{i}. {answer}",
                                on_click=None,
                            ).classes(
                                "w-full max-w-2xl py-4 px-4 rounded-xl text-xl font-bold "
                                "bg-blue-600 text-white shadow-lg border border-blue-800 "
                                "opacity-50"
                            ).disable()


                # Premier affichage
                show_current_question()

                # Refresh question
                ui.timer(2, show_current_question)


            # --------------------------------------------------------------
            # SECTION : joueurs ayant répondu & n'ayant pas répondu
            # --------------------------------------------------------------

            with OrganizerCard()():
                ui.label("🟢 Participants ayant répondu").classes(
                    "text-2xl font-bold text-green-700 mb-4"
                )
                answered_container = ui.row().classes("w-full flex-wrap gap-4")

            with OrganizerCard()():
                ui.label("🟠 En attente de réponse").classes(
                    "text-2xl font-bold text-amber-700 mb-4"
                )
                pending_container = ui.row().classes("w-full flex-wrap gap-4")

            # ----- REFRESH PARTICIPANTS -----
            def refresh_participants():
                raw_answers = engine.answers.get(engine.current_q, {})

                answered_container.clear()
                pending_container.clear()

                for pid, p in engine.players.items():
                    name = p["name"]
                    is_vip = p.get("is_vip")

                    if str(pid) in raw_answers:   # joueur a répondu
                        with answered_container:
                            with ui.column().classes(
                                "p-4 bg-green-50 rounded-xl shadow-md items-center w-40 "
                                "border border-green-200 animate-fadeIn"
                            ):
                                ui.label(name).classes(
                                    "text-lg font-bold text-green-800 text-center"
                                )
                                if is_vip:
                                    ui.label("👑 VIP").classes(
                                        "text-yellow-600 font-semibold"
                                    )

                    else:   # joueur en attente
                        with pending_container:
                            with ui.column().classes(
                                "p-4 bg-amber-50 rounded-xl shadow-md items-center w-40 "
                                "border border-amber-200 animate-fadeIn"
                            ):
                                ui.label(name).classes(
                                    "text-lg font-bold text-amber-800 text-center"
                                )
                                if is_vip:
                                    ui.label("👑 VIP").classes(
                                        "text-yellow-600 font-semibold"
                                    )

            ui.timer(1.0, refresh_participants)
