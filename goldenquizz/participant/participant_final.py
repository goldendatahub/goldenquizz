from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, QuestionCard
from goldenquizz.ui import theme


def participant_final_page(engine):

    @ui.page('/participant/final')
    def participant_final():

        name = app.storage.user.get("player_name", "Joueur")
        pid = app.storage.user.get("player_id")
        is_vip = (pid == engine.vip_id)

        questions = engine.get_questions()
        answers = engine.answers  # {q_idx: {player_id: choice}}

        with mobile_layout():

            with Card()():

                # -------------------------------------------------------
                # TITRE
                # -------------------------------------------------------
                ui.label("🏁 Fin de la partie !") \
                    .classes("text-3xl font-bold text-center text-blue-600 mb-6")

                ui.label(f"Merci d'avoir joué, {name} !") \
                    .classes("text-xl text-center text-gray-700 mb-8")

                # -------------------------------------------------------
                # LEADERBOARD
                # -------------------------------------------------------
                leaderboard = engine.leaderboard()

                ui.label("📊 Classement final") \
                    .classes("text-2xl font-semibold text-center text-gray-800 mt-4 mb-3")

                if not leaderboard:
                    ui.label("Aucun score disponible.") \
                        .classes("text-center text-gray-500 mb-4")
                else:
                    for rank, item in enumerate(leaderboard, start=1):
                        ui.label(f"{rank}. {item['name']} – {item['score']} points") \
                            .classes("text-lg text-gray-700 text-center")

                ui.separator().classes("my-6")

                # -------------------------------------------------------
                # TABLEAU RECAPITULATIF DE TOUTES LES QUESTIONS
                # -------------------------------------------------------
                ui.label("📝 Récapitulatif des questions") \
                    .classes("text-2xl font-semibold text-center text-gray-800 mb-4")

                for q_idx, q in enumerate(questions):

                    answers_list = (
                        q.get("options")
                        or q.get("answers")
                        or q.get("choices")
                        or q.get("reponses")
                        or []
                    )

                    answers_for_question = answers.get(q_idx, {})

                    vip_choice = answers_for_question.get(engine.vip_id)
                    player_choice = answers_for_question.get(pid)

                    vip_text = (
                        answers_list[vip_choice]
                        if isinstance(vip_choice, int) and vip_choice < len(answers_list)
                        else "—"
                    )

                    me_text = (
                        answers_list[player_choice]
                        if isinstance(player_choice, int) and player_choice < len(answers_list)
                        else "—"
                    )

                    total = len(answers_for_question)
                    correct = sum(1 for c in answers_for_question.values() if c == vip_choice)

                    points_value = q.get("points", 1)
                    gained = points_value if (player_choice == vip_choice) else 0

                    ok = player_choice == vip_choice if player_choice is not None else None

                    QuestionCard(
                        number=q_idx + 1,
                        question_text=q.get("text"),
                        vip_text=vip_text,
                        me_text=None if is_vip else me_text,
                        ok=None if is_vip else ok,
                        points=None if is_vip else gained,
                        correct_stats=f"{correct}/{total}",
                        is_vip=is_vip,
                    )()
    

