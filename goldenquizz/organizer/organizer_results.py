from nicegui import ui
import plotly.graph_objects as go

from goldenquizz.ui.layouts import organizer_layout, organizer_header, organizer_section
from goldenquizz.ui.components import OrganizerTitle, OrganizerCard, OrganizerButton


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

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():
                OrganizerTitle(f"📊 Résultats – Question {engine.current_q + 1}")()
                ui.label("Analyse en direct").classes("text-md text-gray-500 italic")

            # ---------------- VIP ANSWER ----------------
            with OrganizerCard()():

                # Reconstruction locale si nécessaire
                vip_answer = summary["vip_answer"]
                if vip_answer == "Non répondu":
                    q = engine.get_current_question()
                    answers = (
                        q.get("answers")
                        or q.get("options")
                        or q.get("reponses")
                        or q.get("choices")
                        or []
                    )

                    if summary["stats"] and isinstance(summary["stats"][0]["answer"], int):
                        vip_index = summary["stats"][0]["answer"]
                        if 0 <= vip_index < len(answers):
                            vip_answer = answers[vip_index]

                ui.label(f"👑 Réponse du VIP : {vip_answer}").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )


            # ---------------- GRAPHIQUE ----------------
            with OrganizerCard()():
                labels = [item["answer"] for item in summary["stats"]]
                values = [item["count"] for item in summary["stats"]]

                fig = go.Figure(
                    data=[go.Pie(
                        labels=labels,
                        values=values,
                        textinfo='label+percent',
                        hole=0.3,
                    )]
                )
                fig.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10),
                )

                ui.plotly(fig).classes("w-full max-w-3xl mx-auto")

            # ---------------- LEADERBOARD ----------------
            with OrganizerCard()():
                ui.label("🏅 Classement actuel").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                table = ui.table(
                    columns=[
                        {"name": "name", "label": "Nom", "field": "name"},
                        {"name": "score", "label": "Score", "field": "score"},
                    ],
                    rows=summary["leaderboard"],
                ).classes(
                    "w-full max-w-xl border border-gray-200 rounded-xl shadow-sm "
                    "hover:shadow-md transition"
                )

            # ---------------- NEXT BUTTON ----------------
            with OrganizerCard()():

                def next_or_finish():
                    if engine.current_q + 1 < len(engine.get_questions()):
                        engine.open_question(engine.current_q + 1)
                        ui.navigate.to("/organizer/question")
                    else:
                        engine.state = "finished"
                        ui.navigate.to("/organizer/final")

                is_last = engine.current_q + 1 == len(engine.get_questions())

                label = "🏁 Terminer la partie" if is_last else "⏭️ Question suivante"

                OrganizerButton(label, next_or_finish)().classes(
                    "mt-4 bg-purple-600 hover:bg-purple-700"
                    if is_last
                    else "mt-4"
                )
