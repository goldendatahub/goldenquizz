from nicegui import ui
import plotly.graph_objects as go

def organizer_results_page(engine):

    @ui.page("/organizer/results")
    def organizer_results():
        if engine.state != "results":
            ui.navigate.to(f"/organizer/{engine.state}")
            return

        summary = engine.get_results_summary()
        if not summary:
            ui.label("Aucun résultat à afficher.")
            return

        ui.label(f"📊 Résultats de la question {engine.current_q + 1}").classes("text-3xl font-bold mb-4 text-purple-700")
        ui.label(f"👑 Réponse du VIP : {summary['vip_answer']}").classes("text-lg text-blue-800 mb-4")

        # --- Graphique Plotly
        labels = [item["answer"] for item in summary["stats"]]
        values = [item["count"] for item in summary["stats"]]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])
        ui.plotly(fig).classes("w-1/2 max-w-md mb-6")

        # --- Classement
        ui.label("🏅 Classement actuel").classes("text-xl font-semibold mt-4")
        table = ui.table(
            columns=[
                {"name": "name", "label": "Nom", "field": "name"},
                {"name": "score", "label": "Score", "field": "score"},
            ],
            rows=summary["leaderboard"],
        ).classes("w-full max-w-md mb-6")

        # --- Boutons de navigation
        def next_or_finish():
            if engine.current_q + 1 < len(engine.get_questions()):
                engine.open_question(engine.current_q + 1)
                ui.navigate.to("/organizer/question")
            else:
                engine.state = "finished"
                ui.navigate.to("/organizer/final")

        if engine.current_q + 1 < len(engine.get_questions()):
            ui.button("⏭️ Question suivante", on_click=next_or_finish).props("color=secondary text-lg")
        else:
            ui.button("🏁 Terminer la partie", on_click=next_or_finish).props("color=positive text-lg")
