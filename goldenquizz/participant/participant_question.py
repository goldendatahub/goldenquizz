from nicegui import ui, app


def participant_question_page(engine):

    @ui.page("/participant/question")
    def question_page():
        name = app.storage.user.get("player_name", "Joueur")
        pid = app.storage.user.get("player_id")

        ui.label(f"👤 {name}").classes("text-lg font-semibold text-blue-700 mb-2")

        # === Zone principale ===
        question_label = ui.label("⏳ En attente de la question...").classes("text-xl mb-4")
        answers_container = ui.column().classes("mt-4")
        selected_answer = {'value': None}

        # ✅ Bouton global Valider (désactivé au départ)
        validate_btn = ui.button("✅ Valider", on_click=lambda: submit_answer()).props("color=positive")
        validate_btn.set_enabled(False)

        # === FONCTIONS INTERNES ===
        def build_answers(answers):
            """Construit les boutons pour chaque réponse possible."""
            answers_container.clear()

            if not answers:
                validate_btn.set_enabled(False)
                return

            # ✅ Ajout des boutons avec "with answers_container:"
            with answers_container:
                for answer in answers:
                    def on_select(a=answer):
                        selected_answer["value"] = a
                        ui.notify(f"Tu as choisi : {a}", type="info")

                        # met à jour les couleurs
                        for b in answers_container.default_slot.children:
                            if b.text == a:
                                b.props("color=primary")
                            else:
                                b.props("color=blue-grey-5 outline")

                        validate_btn.set_enabled(True)

                    ui.button(answer, on_click=on_select).props(
                        "color=blue-grey-5 outline"
                    ).classes("w-full max-w-xs mt-2")

            validate_btn.set_enabled(False)

        def submit_answer():
            """Envoie la réponse sélectionnée au moteur de jeu."""
            if not selected_answer["value"]:
                ui.notify("Choisis une réponse avant de valider.", type="warning")
                return

            engine.submit_answer(pid, selected_answer["value"])
            ui.notify("✅ Réponse enregistrée !", type="positive")

            # 🔒 désactive tout après validation
            validate_btn.set_enabled(False)
            for b in answers_container.default_slot.children:
                b.props("disable=true")

            ui.navigate.to("/participant/answer")

        def refresh():
            """Rafraîchit la question en cours."""
            q = engine.get_current_question()
            if not q:
                question_label.set_text("⏳ En attente de la question...")
                answers_container.clear()
                validate_btn.set_enabled(False)
                return

            question_label.set_text(q.get("text") or "Question en cours")
            answers = (
                q.get("options")
                or q.get("answers")
                or q.get("choices")
                or q.get("reponses")
                or []
            )

            # ✅ Reconstruit les réponses seulement si vide
            if not answers_container.default_slot.children:
                build_answers(answers)

        # 🔁 Vérifie toutes les 2 secondes
        ui.timer(2, refresh)
