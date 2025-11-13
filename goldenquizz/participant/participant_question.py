from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, Title, Subtitle, PrimaryButton
from goldenquizz.ui import theme


def participant_question_page(engine):

    @ui.page('/participant/question')
    def question_page():
        name = app.storage.user.get("player_name", "Joueur")
        pid = app.storage.user.get("player_id")

        with mobile_layout():

            with Card()():

                ui.label(f"👤 {name}") \
                    .classes("text-xl font-semibold text-blue-600 mb-4 text-center")

                # === Zone principale ===
                question_label = ui.label("⏳ En attente de la question...") \
                    .classes("text-xl mb-4 text-center")

                answers_container = ui.column().classes("mt-4 w-full")

                # ✔ Flag interne pour empêcher la duplication
                answers_built = {'done': False}

                # --- Build answers ---
                def build_answers(answers):
                    answers_container.clear()
                    for index, answer_text in enumerate(answers):

                        def make_click_handler(idx=index):
                            def handler():
                                engine.submit_answer(pid, idx)
                                ui.navigate.to("/participant/answer")
                            return handler

                        PrimaryButton(answer_text, make_click_handler())() \
                            .classes("mt-2 w-full")

                # --- Refresh ---
                def refresh():
                    q = engine.get_current_question()
                    if not q:
                        return

                    question_label.set_text(q.get("text", "❓ Question"))

                    answers = (
                        q.get("options")
                        or q.get("answers")
                        or q.get("choices")
                        or q.get("reponses")
                        or []
                    )

                    # 🟢 condition robuste
                    if not answers_built['done']:
                        build_answers(answers)
                        answers_built['done'] = True

                ui.timer(2, refresh)

                ui.label("Réponds dès que les réponses apparaissent 👇") \
                    .classes("text-gray-400 text-sm mt-6 text-center")

                ui.label("GoldenQuizz © 2025") \
                    .classes(theme.TEXT_FOOTER + " mt-4")
    
