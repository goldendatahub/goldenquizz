from nicegui import ui, app


def participant_answer_page(engine):

    @ui.page("/participant/answer")
    def participant_answer():
        name = app.storage.user.get("player_name", "Joueur")
        pid = app.storage.user.get("player_id")

        ui.label(f"👤 {name}").classes("text-lg font-semibold text-blue-700 mb-2")
        status_label = ui.label("⏳ En attente de la réponse du VIP...").classes("text-xl mt-6")

        shown_result = {"done": False}
        previous_state = {"value": engine.state}

        def refresh():
            q = engine.get_current_question()
            current_state = engine.state

            # 🟢 Cas 1 : fin du jeu → redirection vers la page finale
            if current_state == "finished":
                ui.navigate.to("/participant/final")
                return

            # 🟡 Cas 2 : passage results → running → nouvelle question
            if previous_state["value"] == "results" and current_state == "running":
                ui.navigate.to("/participant/question")
                return

            previous_state["value"] = current_state

            # 🕐 Cas 3 : attente de la réponse VIP
            if current_state != "results":
                status_label.set_text("⏳ En attente de la réponse du VIP...")
                return

            # 🧩 Cas 4 : affichage du résultat (une seule fois)
            if not shown_result["done"]:
                vip_id = engine.vip_id
                vip_answer = engine.answers.get(engine.current_q, {}).get(vip_id, None)
                player_answer = engine.answers.get(engine.current_q, {}).get(pid, None)

                if vip_answer is None:
                    status_label.set_text("⚠️ En attente de la réponse du VIP...")
                    return

                # 🧠 Cas spécial : le joueur est le VIP
                if pid == vip_id:
                    if player_answer:
                        status_label.set_text(f"👑 Ta réponse : « {player_answer} »")
                    else:
                        status_label.set_text("👑 Tu n’as pas encore répondu.")
                    shown_result["done"] = True
                    return

                # Cas standard : joueur normal
                gained = player_answer == vip_answer
                points = q.get("points", 0)

                if gained:
                    status_label.set_text(
                        f"✅ Le VIP a répondu « {vip_answer} » — Tu as trouvé la même réponse ! 🎉 +{points} pts"
                    )
                else:
                    status_label.set_text(
                        f"❌ Le VIP a répondu « {vip_answer} » — Tu avais choisi « {player_answer} »."
                    )

                shown_result["done"] = True

        ui.timer(2, refresh)
