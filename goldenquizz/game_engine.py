import yaml
import json
from pathlib import Path
from nicegui import ui


class GameEngine:
    def __init__(self, config_path: str):
        self.config = self._load_yaml(config_path)
        self.players = {}      # {session_id: {"name": str, "is_vip": bool, "score": int}}
        self.answers = {}      # {question_idx: {player_id: choice}}
        self.current_q = None
        self.state = "lobby"   # lobby | running | results | finished
        self.vip_id = None

    # ---------- CONFIG ----------
    def _load_yaml(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_questions(self):
        return self.config.get("questions", [])

    # ---------- PLAYERS ----------
    def register_player(self, session_id, name):
        """
        Enregistre un joueur (ou reconnecte un joueur existant ayant le même prénom).
        """
        # 🔍 Recherche si un joueur portant ce nom existe déjà
        for pid, p in self.players.items():
            if p["name"].strip().lower() == name.strip().lower():
                # ✅ Réutilisation du joueur existant
                self.players[session_id] = p
                print(f"🔁 {name} s'est reconnecté (nouvelle session {session_id})")
                return session_id

        # 🆕 Nouveau joueur
        self.players[session_id] = {"name": name, "is_vip": False, "score": 0}
        print(f"✅ Nouveau joueur enregistré : {name} (ID={session_id})")
        return session_id

    def set_vip(self, session_id):
        for pid in self.players:
            self.players[pid]["is_vip"] = False
        self.players[session_id]["is_vip"] = True
        self.vip_id = session_id
        print(f"👑 {self.players[session_id]['name']} est maintenant le VIP")

    # ---------- GAME FLOW ----------
    def open_question(self, index):
        """Ouvre une question et réinitialise les réponses."""
        self.current_q = index
        self.state = "running"
        self.answers[index] = {}
        question = self.get_questions()[index]
        print(f"▶️ Ouverture question {index+1}: {question['text']}")

    def submit_answer(self, session_id, choice):
        """Enregistre la réponse d’un joueur."""
        if self.state != "running" or self.current_q is None:
            return
        player_name = self.players.get(session_id, {}).get("name", "Inconnu")
        self.answers[self.current_q][session_id] = choice
        print(f"📩 Réponse enregistrée: {player_name} → {choice}")

    def close_question(self):
        """Clôture la question courante et calcule les scores."""
        if self.current_q is None or self.current_q not in self.answers:
            print("⚠️ Aucune question active à clôturer.")
            return None

        print("🔒 Question clôturée, calcul des scores...")
        self.state = "results"
        self.compute_scores()

        # Vérifie la réponse du VIP
        if self.vip_id not in self.answers[self.current_q]:
            print("⚠️ Le VIP n’a pas encore répondu.")
        return True

    def compute_scores(self):
        """Attribue les points aux joueurs ayant la même réponse que le VIP."""
        if self.vip_id is None:
            return
        q = self.get_questions()[self.current_q]
        points = q.get("points", 1)
        vip_answer = self.answers[self.current_q].get(self.vip_id)

        if vip_answer is None:
            return

        for pid, answer in self.answers[self.current_q].items():
            if pid != self.vip_id and answer == vip_answer:
                self.players[pid]["score"] += points
                print(f"🏅 {self.players[pid]['name']} gagne {points} points !")

    def leaderboard(self):
        """Retourne le classement sans inclure le VIP."""
        return sorted(
            [
                {"name": p["name"], "score": p["score"]}
                for pid, p in self.players.items()
                if not p["is_vip"]  # ❌ exclure le VIP
            ],
            key=lambda p: p["score"],
            reverse=True,
        )


    def get_current_question(self):
        """Retourne la question actuellement ouverte, ou None si aucune."""
        questions = self.get_questions()
        if isinstance(self.current_q, int) and 0 <= self.current_q < len(questions):
            return questions[self.current_q]
        return None

    def get_results_summary(self):
        """Construit un résumé des résultats de la question courante."""
        if self.current_q is None or self.current_q not in self.answers:
            return None

        question = self.get_questions()[self.current_q]
        answers = self.answers[self.current_q]

        stats = {}
        for answer in answers.values():
            stats[answer] = stats.get(answer, 0) + 1

        leaderboard = self.leaderboard()
        vip_answer = answers.get(self.vip_id, None)
        return {
            "question": question.get("text", "Question"),
            "vip_answer": vip_answer or "Non répondu",
            "stats": [{"answer": k, "count": v} for k, v in stats.items()],
            "leaderboard": leaderboard,
        }

    # ---------- UTILITIES ----------
    def broadcast_state(self):
        """Compatibilité pour versions NiceGUI sans broadcast_event."""
        pass
