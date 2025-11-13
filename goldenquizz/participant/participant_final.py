from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card, Title, Subtitle, QuestionCard
from goldenquizz.ui import theme



def participant_final_page(engine):

    @ui.page("/participant/final")
    def participant_final():

        print("RENDERING COLUMN")
        with ui.column().classes("border border-red-500 p-2") as col:
            ui.label("test")

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

                if not is_vip:
                    leaderboard = engine.leaderboard()
                    ui.label("🏆 Classement général").classes(
                        "text-xl font-bold text-blue-700 mt-4 mb-2 text-center"
                    )
                    for entry in leaderboard:
                        ui.label(f"{entry['name']} — {entry['score']} pts").classes(
                            "text-gray-700 text-md text-center"
                        )

                ui.label("📋 Récapitulatif des questions").classes(
                    "text-2xl font-semibold text-amber-700 mt-6 mb-4 text-center"
                )

            # ---------------------------------------------------
            # CONTENEUR STABLE POUR LES CARTES
            # ---------------------------------------------------
            with ui.column().classes("w-full gap-2") as cards_container:

                questions = engine.get_questions()

                for q_index, q_data in enumerate(questions):

                    raw_answers = engine.answers.get(q_index, {})
                    answers = {str(k): v for k, v in raw_answers.items()}

                    question_text = q_data.get("text", "Question")
                    points = q_data.get("points", 1)

                    vip_choice = answers.get(vip_id)

                    options = (
                        q_data.get("options")
                        or q_data.get("answers")
                        or q_data.get("choices")
                        or q_data.get("reponses")
                        or []
                    )
                    vip_text = options[vip_choice] if vip_choice is not None else "—"

                    player_choice = answers.get(pid)
                    player_text = options[player_choice] if player_choice is not None else None

                    ok = None
                    gained_points = 0
                    if not is_vip and player_choice is not None and vip_choice is not None:
                        ok = (player_choice == vip_choice)
                        gained_points = points if ok else 0

                    good_answers = list(answers.values()).count(vip_choice)
                    correct_stats = f"{good_answers} / {len(answers)}"

                    # 🔥 ENFIN : affichage stable de la carte
                    QuestionCard(
                        number=q_index + 1,
                        question_text=question_text,
                        vip_text=vip_text,
                        me_text=player_text,
                        ok=ok,
                        points=gained_points,
                        correct_stats=correct_stats,
                        is_vip=is_vip,
                    )()

            ui.label("GoldenQuizz © 2025").classes(
                theme.TEXT_FOOTER + " mt-8 text-center"
            )
