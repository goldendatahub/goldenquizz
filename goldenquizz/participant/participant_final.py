from nicegui import ui, app


def participant_final_page(engine):

    @ui.page("/participant/final")
    def participant_final():
        pid = app.storage.user.get("player_id")
        name = app.storage.user.get("player_name", "Joueur")

        ui.label("🏁 Fin de la partie").classes("text-3xl font-bold text-blue-700 mb-4")
        ui.label(f"👤 Joueur : {name}").classes("text-lg mb-6")

        # 🧠 Cas spécial : le joueur est le VIP
        if pid == engine.vip_id:
            ui.label("👑 En tant que VIP, tu ne participes pas au classement.").classes("text-lg mt-4")
            ui.label("Merci d’avoir partagé tes réponses avec les invités 🎉").classes("text-green-700 mt-2")
            return

        leaderboard = engine.leaderboard()
        leaderboard = [p for p in leaderboard if not p.get("is_vip")]

        # Trouve la position du joueur
        player_rank = None
        player_score = 0
        for i, p in enumerate(leaderboard, start=1):
            if p["name"] == name:
                player_rank = i
                player_score = p["score"]
                break

        # ✅ Affiche le message principal
        if player_rank is not None:
            ui.label(f"🎯 Ton score final : {player_score} points").classes("text-xl font-semibold text-green-600 mt-4")
            ui.label(f"🏅 Ta position : {player_rank}{'er' if player_rank == 1 else 'e'} sur {len(leaderboard)}").classes("text-lg mt-2")
        else:
            ui.label("⚠️ Impossible de retrouver ton score (erreur de session).").classes("text-red-600 mt-4")

        ui.separator().classes("my-4")

        # ✅ Classement général
        ui.label("🏆 Classement final").classes("text-xl font-bold mb-2")
        table = ui.table(
            columns=[
                {"name": "rank", "label": "#", "field": "rank"},
                {"name": "name", "label": "Nom", "field": "name"},
                {"name": "score", "label": "Score", "field": "score"},
            ],
            rows=[
                {"rank": i + 1, "name": p["name"], "score": p["score"]}
                for i, p in enumerate(leaderboard)
            ],
        ).classes("w-full max-w-md")

        ui.separator().classes("my-6")
        ui.label("🎉 Merci d’avoir joué à GoldenQuizz !").classes("text-lg text-blue-800 mt-4")
