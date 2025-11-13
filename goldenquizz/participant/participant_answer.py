from nicegui import ui, app
from goldenquizz.ui.layouts import mobile_layout
from goldenquizz.ui.components import Card
from goldenquizz.ui import theme


def participant_answer_page(engine):

    @ui.page('/participant/answer')
    def participant_answer():
        name = app.storage.user.get("player_name", "Joueur")
        pid = str(app.storage.user.get("player_id"))

        last_q = {"value": engine.current_q}

        with mobile_layout():

            with Card()():

                ui.label(f"👤 {name}") \
                    .classes("text-xl font-semibold text-blue-600 mb-2 text-center")

                status_label = ui.label(
                    "⏳ En attente de la clôture de la question par l’organisateur..."
                ).classes("text-lg text-gray-700 mt-4 mb-4 text-center animate-pulse")

                shown_result = {"done": False}

                def refresh():

                    current_q = engine.current_q

                    # 🔥 FORCE LES CLÉS EN STRING POUR ÉVITER LE BUG INT/STRING
                    answers_for_question = engine.answers.get(current_q, {})
                    normalized_answers = {str(k): v for k, v in answers_for_question.items()}

                    player_answer = normalized_answers.get(pid)

                    # ---------------------------------------------------------
                    # 0. FIN DE PARTIE → aller vers participant_final
                    # ---------------------------------------------------------
                    if engine.state == "finished":
                        ui.navigate.to("/participant/final")
                        return

                    # ---------------------------------------------------------
                    # 1. Question suivante → redirection vers /question
                    # ---------------------------------------------------------
                    if current_q != last_q["value"]:
                        ui.navigate.to("/participant/question")
                        return

                    # ---------------------------------------------------------
                    # 2. Question en cours (running)
                    # ---------------------------------------------------------
                    if engine.state == "running":
                        if player_answer is None:
                            ui.navigate.to("/participant/question")
                            return
                        return  # joueur ayant répondu → rester

                    # ---------------------------------------------------------
                    # 3. Tant qu'on n'est pas en mode résultats : attente
                    # ---------------------------------------------------------
                    if engine.state != "results":
                        return

                    # ---------------------------------------------------------
                    # 4. Affichage des résultats une seule fois
                    # ---------------------------------------------------------
                    if shown_result["done"]:
                        return

                    vip_answer = normalized_answers.get(str(engine.vip_id))

                    q = engine.get_current_question()
                    points = q.get("points", 0) if q else 0

                    answers_list = (
                        q.get("options")
                        or q.get("answers")
                        or q.get("choices")
                        or q.get("reponses")
                        or []
                    )

                    vip_text = (
                        answers_list[vip_answer] if vip_answer is not None else None
                    )
                    player_text = (
                        answers_list[player_answer] if player_answer is not None else None
                    )

                    is_vip = (pid == str(engine.vip_id))

                    if is_vip:
                        status_label.set_text(
                            f"👑 Tu as répondu « {vip_text} ».\n"
                            f"Merci d’avoir donné ta réponse !"
                        )
                        status_label.classes("text-blue-600 text-xl text-center mt-4")

                    else:
                        gained = (player_text == vip_text)

                        if gained:
                            status_label.set_text(
                                f"🎉 Le VIP a répondu « {vip_text} ».\n"
                                f"Tu as trouvé ! +{points} points"
                            )
                            status_label.classes("text-green-600 text-xl text-center mt-4")
                        else:
                            status_label.set_text(
                                f"❌ Le VIP a répondu « {vip_text} ».\n"
                                f"Tu avais choisi « {player_text} »."
                            )
                            status_label.classes("text-red-600 text-xl text-center mt-4")

                    shown_result["done"] = True

                ui.timer(2, refresh)

                ui.label("Résultats en cours de calcul…") \
                    .classes("text-gray-400 text-sm mt-6 text-center")

                ui.label("GoldenQuizz © 2025") \
                    .classes(theme.TEXT_FOOTER + " mt-4")
