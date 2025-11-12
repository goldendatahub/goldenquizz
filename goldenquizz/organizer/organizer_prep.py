from nicegui import ui


def organizer_prep_page(engine):

    @ui.page("/organizer/prep")
    def organizer_prep():
        if engine.state != "lobby":
            ui.navigate.to(f"/organizer/{engine.state}")
            return

        ui.label("🎛️ Préparation de la partie").classes("text-3xl font-bold mb-4 text-blue-700")

        # --- Liste des joueurs connectés
        ui.label("👥 Joueurs connectés :").classes("text-lg font-semibold mt-4")

        table = ui.table(
            columns=[
                {"name": "name", "label": "Nom", "field": "name"},
                {"name": "vip", "label": "VIP", "field": "vip"},  # ✅ Nouvelle colonne
            ],
            rows=[],
        ).classes("w-full max-w-md mb-4")

        # --- Sélection du VIP
        ui.label("👑 Sélection du VIP :").classes("mt-4 text-lg font-semibold")
        vip_selector = ui.select(options={}, label="Choisir le VIP").classes("w-64")

        def define_vip():
            pid = vip_selector.value
            if not pid:
                ui.notify("Veuillez sélectionner un joueur.", type="warning")
                return
            pid = int(pid)
            engine.set_vip(pid)
            ui.notify(f"{engine.players[pid]['name']} est maintenant le VIP 👑", type="positive")

        ui.button("✅ Valider le VIP", on_click=define_vip).props("color=secondary mt-2")

        def start_game():
            if not engine.vip_id:
                ui.notify("Veuillez définir le VIP avant de démarrer.", type="warning")
                return
            engine.open_question(0)
            ui.navigate.to("/organizer/question")

        ui.button("▶️ Démarrer la partie", on_click=start_game).props("color=positive mt-6 text-lg")

        # --- Rafraîchissement dynamique
        def refresh():
            """Met à jour la liste des joueurs et le sélecteur VIP."""
            rows = []
            for pid, p in engine.players.items():
                rows.append({
                    "name": p["name"],
                    "vip": "👑" if p.get("is_vip") else "",  # ✅ affiche l’emoji VIP
                })
            table.rows = rows

            # Rafraîchit les options du sélecteur VIP
            vip_selector.options = {str(pid): p["name"] for pid, p in engine.players.items()}
            vip_selector.update()

        # 🔁 Mise à jour toutes les 2 secondesui.timer(2, refresh)
