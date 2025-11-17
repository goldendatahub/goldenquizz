from nicegui import ui
import plotly.graph_objects as go

from goldenquizz.ui.layouts import organizer_layout, organizer_header
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

        # ------------------------------------------------------------------
        # QUESTION + LISTE DES REPONSES
        # ------------------------------------------------------------------
        q = engine.get_current_question()
        answers_list = (
            q.get("answers")
            or q.get("options")
            or q.get("reponses")
            or q.get("choices")
            or []
        )

        # ------------------------------------------------------------------
        # VRAIE REPONSE DU VIP = depuis engine.answers
        # ------------------------------------------------------------------
        vip_id = str(engine.vip_id)
        raw_answers = engine.answers.get(engine.current_q, {})

        if vip_id in raw_answers:
            vip_index = raw_answers[vip_id]
        else:
            vip_index = None

        vip_text = (
            answers_list[vip_index]
            if vip_index is not None and 0 <= vip_index < len(answers_list)
            else "Non répondu"
        )

        # ------------------------------------------------------------------
        # Votes exclusifs des NON-VIP
        # ------------------------------------------------------------------
        non_vip_players = {
            pid for pid in engine.players.keys()
            if str(pid) != vip_id
        }

        detailed_answers = engine.answers.get(engine.current_q, {})

        votes_by_answer = {i: 0 for i in range(len(answers_list))}
        for pid, choice in detailed_answers.items():
            if str(pid) in non_vip_players and 0 <= choice < len(answers_list):
                votes_by_answer[choice] += 1

        text_values = [str(votes_by_answer[i]) for i in range(len(answers_list))]

        # Couleurs : VIP = rouge, autres = bleu
        bar_colors = [
            "crimson" if i == vip_index else "royalblue"
            for i in range(len(answers_list))
        ]

        # Halo autour de la barre VIP
        annotations = []
        if vip_index is not None and 0 <= vip_index < len(answers_list):
            annotations.append(dict(
                x=answers_list[vip_index],
                y=votes_by_answer[vip_index],
                xref="x",
                yref="y",
                text="",
                showarrow=False,
                bgcolor="rgba(255,0,0,0.18)",
                bordercolor="crimson",
                borderwidth=3,
                opacity=0.9,
            ))

        # ------------------------------------------------------------------
        # HISTOGRAMME STYLE TV SHOW
        # ------------------------------------------------------------------
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=answers_list,
            y=[votes_by_answer[i] for i in range(len(answers_list))],
            text=text_values,
            textposition="outside",
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
            ),
            hoverinfo="skip",
            name="Votes",
        ))

        fig.add_trace(go.Bar(
            x=[None],
            y=[None],
            marker_color="crimson",
            name="Réponse VIP",
            showlegend=True,
        ))

        max_votes = max(votes_by_answer.values()) if votes_by_answer else 1

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            font=dict(
                family="Montserrat, Arial, sans-serif",
                size=16,
                color="black",
            ),
            yaxis=dict(visible=False),
            xaxis=dict(title="", tickfont=dict(size=16)),
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.25,
                x=0.5,
                xanchor="center",
                font=dict(size=14, family="Montserrat, Arial"),
            ),
            annotations=annotations,
            margin=dict(t=10, b=80, l=10, r=10),
            height=450,
        )

        # ------------------------------------------------------------------
        # CLASSEMENT (hors VIP)
        # ------------------------------------------------------------------
        leaderboard = summary["leaderboard"]
        vip_name = engine.players[engine.vip_id]["name"]

        leaderboard_no_vip = [
            entry for entry in leaderboard
            if entry["name"] != vip_name
        ]
        leaderboard_no_vip.sort(key=lambda x: x["score"], reverse=True)

        with organizer_layout():

            # ---------------- HEADER ----------------
            with organizer_header():
                OrganizerTitle(f"📊 Résultats – Question {engine.current_q + 1}")()
                ui.label("Analyse en direct").classes("text-md text-gray-500 italic")

            # ---------------- QUESTION + VIP ----------------
            with OrganizerCard()():

                # Texte de la question
                ui.label(summary["question"]).classes(
                    "text-xl font-semibold text-gray-700 mb-2"
                )

                # 🔥 Ajout : points de la question
                points = q.get("points", 0)
                ui.label(f"⭐ {points} points").classes(
                    "text-lg font-bold text-green-700 mb-2"
                )

                # Réponse du VIP
                ui.label(f"👑 Réponse du VIP : {vip_text}").classes(
                    "text-2xl font-bold text-blue-700 mb-2"
                )


            # ---------------- RÉPARTITION PAR RÉPONSES ----------------
            with OrganizerCard()():

                ui.label("📊 Répartition des réponses").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                # Grille flexible avec colonnes plus petites
                columns = ui.row().classes(
                    "w-full justify-center gap-4 flex-wrap"
                )

                for answer_index, answer_text in enumerate(answers_list):

                    with columns:
                        with ui.column().classes(
                            "bg-gray-50 p-3 rounded-xl border border-gray-300 "
                            "shadow-md w-40 items-center"   # <-- largeur réduite à ~160px
                        ):

                            # En-tête de la réponse
                            ui.label(answer_text).classes(
                                "text-md font-bold text-center text-gray-800 mb-2"
                            )

                            # Liste des joueurs ayant choisi cette réponse
                            for pid, choice in detailed_answers.items():
                                if str(pid) not in non_vip_players:
                                    continue
                                if choice != answer_index:
                                    continue

                                p = engine.players.get(pid, {})
                                pname = p.get("name", "???")

                                is_correct = (answer_index == vip_index)

                                bg = (
                                    "bg-green-100 border-green-300"
                                    if is_correct else
                                    "bg-red-100 border-red-300"
                                )
                                text_color = (
                                    "text-green-800"
                                    if is_correct else
                                    "text-red-800"
                                )

                                with ui.column().classes(
                                    f"p-2 rounded-xl shadow-sm border w-full mb-2 animate-fadeIn {bg}"
                                ):
                                    ui.label(pname).classes(
                                        f"text-sm font-bold text-center {text_color}"
                                    )



            # ---------------- CLASSEMENT ----------------
            with OrganizerCard()():
                ui.label("🏅 Classement actuel").classes(
                    "text-2xl font-bold text-blue-700 mb-4"
                )

                container = ui.column().classes("w-full gap-4")

                position = 1
                for entry in leaderboard_no_vip:
                    name = entry["name"]
                    score = entry["score"]

                    # 🔍 Retrouver le player_id à partir du nom
                    player_id = None
                    for pid, pdata in engine.players.items():
                        if pdata["name"] == name:
                            player_id = str(pid)
                            break

                    # 🔎 Vérifier si ce joueur a trouvé la bonne réponse
                    gained = False
                    if player_id in detailed_answers:
                        if detailed_answers[player_id] == vip_index:
                            gained = True

                    with container:
                        with ui.row().classes(
                            "items-center justify-between bg-white border "
                            "border-gray-300 rounded-xl shadow-sm p-4 w-full "
                        ):

                            # Nom + position
                            ui.label(f"#{position} — {name}").classes(
                                "text-lg font-bold text-gray-800"
                            )

                            # Score total
                            score_row = ui.row().classes("items-center gap-3")

                            with score_row:
                                ui.label(f"{score} pts").classes(
                                    "text-lg font-semibold text-blue-700"
                                )

                                # 💚 Gain de points pour cette question
                                if gained:
                                    ui.label(f"+{points}").classes(
                                        "text-lg font-bold text-green-700"
                                    )

                    position += 1


            # ---------------- NEXT BUTTON ----------------
            with OrganizerCard()():

                def next_or_finish():
                    if engine.current_q + 1 < len(engine.get_questions()):
                        engine.open_question(engine.current_q + 1)
                        ui.navigate.to("/organizer/question")
                    else:
                        engine.state = "finished"
                        ui.navigate.to("/organizer/final")

                last = engine.current_q + 1 == len(engine.get_questions())
                label = "🏁 Terminer la partie" if last else "⏭️ Question suivante"

                OrganizerButton(label, next_or_finish)().classes(
                    "mt-4 bg-purple-600 hover:bg-purple-700"
                    if last else "mt-4"
                )
