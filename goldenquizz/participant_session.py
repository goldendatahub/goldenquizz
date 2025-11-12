from nicegui import ui, app
import uuid


def participant_page(engine):

    from nicegui import app

    @ui.page("/participant")
    def participant():
        ui.label("📱 Session Participant").classes("text-2xl font-bold mb-4")
        session_id = app.storage.user.get('player_id', None)
        name_input = ui.input("Entre ton prénom").classes("w-64")
        ui.button("Valider", on_click=lambda: register_player(name_input.value)).props("color=primary")

        # === Zone principale ===
        question_label = ui.label("").classes("text-lg mt-6 font-semibold")
        answer_buttons = []
        selected_answer = {'value': None}
        last_question_id = {'index': None}

        # ✅ Le bouton Valider est créé UNE FOIS pour toute la session
        validate_btn = ui.button("✅ Valider la réponse", on_click=lambda: submit_answer())
        validate_btn.props("color=positive")
        validate_btn.set_enabled(False)  # démarre grisé

        def safe_disable(btn):
            """Désactive un bouton uniquement s'il existe."""
            if btn is not None:
                try:
                    btn.disable()
                except Exception:
                    pass

        def safe_enable(btn):
            """Active un bouton uniquement s'il existe."""
            if btn is not None:
                try:
                    btn.enable()
                except Exception:
                    pass


        # ---------- Fonctions internes ----------
        def register_player(name):
            if not name:
                ui.notify("Merci d’entrer ton prénom avant de valider.", type="warning")
                return

            # 🔹 Récupération ou création du player_id stocké par session navigateur
            session_id = app.storage.user.get('player_id', None)
            if not session_id:
                session_id = str(uuid.uuid4())
                app.storage.user['player_id'] = session_id

            # 🔹 Enregistrement (ou reconnexion) du joueur
            engine.register_player(session_id, name)

            # ✅ Feedback visuel
            ui.notify(f"Bienvenue {name} !", type="positive")
            refresh_ui()


        def refresh_ui():
            nonlocal validate_btn
            question = engine.get_current_question()
            if not question:
                question_label.set_text("⏳ En attente de la prochaine question...")
                for btn in answer_buttons:
                    btn.delete()
                answer_buttons.clear()
                validate_btn.set_enabled(False)
                last_question_id['index'] = None
                return

            current_index = engine.current_q
            if current_index == last_question_id['index']:
                return

            last_question_id['index'] = current_index
            question_label.set_text(question.get('text') or question.get('question') or '')
            answers = (
                question.get('answers')
                or question.get('options')
                or question.get('reponses')
                or question.get('choices')
                or []
            )
            build_answers(answers)

        def build_answers(answers):
            """Construit les boutons de réponses colorés."""
            for btn in answer_buttons:
                btn.delete()
            answer_buttons.clear()

            if not answers:
                return

            for answer in answers:
                btn = ui.button(answer, on_click=lambda a=answer: select_answer(a)).props("color=primary outline")
                btn.classes("w-full max-w-xs mt-2")
                answer_buttons.append(btn)

            validate_btn.set_enabled(False)

        def select_answer(answer):
            """Quand une réponse est sélectionnée."""
            selected_answer['value'] = answer
            ui.notify(f"Tu as choisi : {answer}", type="info")

            for btn in answer_buttons:
                if btn.text == answer:
                    btn.props("color=primary")
                else:
                    btn.props("color=blue-grey-5 outline")

            # ✅ Active le bouton “Valider”
            validate_btn.set_enabled(True)

        def submit_answer():
            pid = app.storage.user.get('player_id', None)
            if pid is None:
                ui.notify("Erreur : joueur non reconnu. Reconnecte-toi.", type="negative")
                return
            if not selected_answer['value']:
                ui.notify("Choisis une réponse avant de valider !", type="warning")
                return
            engine.submit_answer(pid, selected_answer['value'])
            ui.notify("✅ Réponse enregistrée !", type="positive")
            safe_disable(validate_btn)
            for btn in answer_buttons:
                btn.disable()


        # Timer pour rafraîchir les questions ouvertes
        ui.timer(3, refresh_ui)
