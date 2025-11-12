from nicegui import ui
import asyncio


def organizer_question_page(engine):

    @ui.page("/organizer/question")
    def organizer_question():
        ui.label("🎯 Question en cours").classes("text-2xl font-bold mb-4")

        # Zone d'affichage de la question
        question_label = ui.label("").classes("text-xl mt-4 font-semibold text-blue-800")

        # Conteneur pour les réponses
        answers_container = ui.column().classes("mt-4 gap-2")

        # Bouton de clôture
        ui.button("Clôturer les réponses", on_click=lambda: close_question()).props("color=primary")

        # Variable pour suivre la dernière question affichée
        last_q_index = {'value': None}

        # --- Fonction pour afficher la question en cours ---
        def show_current_question():
            q = engine.get_current_question()
            if not q:
                question_label.set_text("⏳ Aucune question active.")
                answers_container.clear()
                return

            # 🔁 Si c’est la même question qu’avant, ne pas redessiner
            if last_q_index['value'] == engine.current_q:
                return
            last_q_index['value'] = engine.current_q

            # Nettoyage du conteneur
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
                    ui.label("⚠️ Aucune réponse configurée.").classes("text-red-600 mt-2")
                return

            # ✅ Utilise le contexte pour ajouter les boutons dans la colonne
            with answers_container:
                for i, answer in enumerate(answers, start=1):
                    ui.button(
                        f"{i}. {answer}",
                        on_click=None,
                    ).props(
                        f"color={['orange', 'blue', 'green', 'purple'][i % 4]} outline"
                    ).classes("w-full max-w-md").disable()

        # --- Clôture de la question ---
        def close_question():
            """Ferme la question et affiche la page de résultats."""
            result = engine.close_question()
            if not result:
                ui.notify("⚠️ Aucune question active à clôturer.", type="warning")
                return

            ui.notify("🔒 Question clôturée, calcul des scores...", type="info")
            # ⏳ attendre un peu, puis rediriger sans tâche asynchrone
            ui.timer(1.0, lambda: ui.navigate.to("/organizer/results"), once=True)


        # Premier affichage
        show_current_question()

        # Rafraîchissement toutes les 3 secondes
        ui.timer(3, show_current_question)
