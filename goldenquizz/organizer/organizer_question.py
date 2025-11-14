from nicegui import ui
from goldenquizz.ui.layouts import organizer_layout, organizer_header, organizer_section
from goldenquizz.ui.components import OrganizerTitle, OrganizerCard, OrganizerButton


def organizer_question_page(engine):

    @ui.page("/organizer/question")
    def organizer_question():

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():
                OrganizerTitle("🎯 Question en cours")()
                ui.label("Mode organisateur").classes("text-md text-gray-500 italic")

            # ---------------- QUESTION ----------------
            with OrganizerCard()():
                question_label = ui.label("").classes(
                    "text-2xl font-semibold text-blue-800 mb-4"
                )

                answers_container = ui.column().classes("mt-6 gap-3 w-full")

                # Bouton de clôture
                def close_question():
                    result = engine.close_question()
                    if not result:
                        ui.notify("⚠️ Aucune question active à clôturer.", type="warning")
                        return

                    ui.notify("🔒 Question clôturée, calcul des scores...", type="info")
                    ui.timer(1.0, lambda: ui.navigate.to("/organizer/results"), once=True)

                OrganizerButton("Clôturer les réponses", close_question)().classes(
                    "mt-6 bg-red-600 hover:bg-red-700"
                )

                # Variable de contrôle
                last_q_index = {'value': None}

                # Fonction d'affichage
                def show_current_question():
                    q = engine.get_current_question()
                    if not q:
                        question_label.set_text("⏳ Aucune question active.")
                        answers_container.clear()
                        return

                    if last_q_index['value'] == engine.current_q:
                        return

                    last_q_index['value'] = engine.current_q

                    answers_container.clear()

                    question_label.set_text(f"❓ {q.get('text', 'Question')}")

                    answers = (
                        q.get("answers")
                        or q.get("options")
                        or q.get("reponses")
                        or q.get("choices")
                        or []
                    )

                    if not answers:
                        with answers_container:
                            ui.label("⚠️ Aucune réponse configurée.").classes(
                                "text-red-600 mt-2"
                            )
                        return

                    # Construction UI
                    with answers_container:
                        for i, answer in enumerate(answers, start=1):
                            ui.button(
                                f"{i}. {answer}",
                                on_click=None,
                            ).props(
                                f"color={['orange', 'blue', 'green', 'purple'][i % 4]} outline"
                            ).classes(
                                "w-full max-w-xl py-3 text-lg font-semibold"
                            ).disable()

                # Premier affichage
                show_current_question()

                # Timer
                ui.timer(3, show_current_question)
