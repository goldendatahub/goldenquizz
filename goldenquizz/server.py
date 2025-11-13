from nicegui import ui
from goldenquizz.game_engine import GameEngine

# --- Import des pages organisateur ---
from goldenquizz.organizer.organizer_prep import organizer_prep_page
from goldenquizz.organizer.organizer_question import organizer_question_page
from goldenquizz.organizer.organizer_results import organizer_results_page
from goldenquizz.organizer.organizer_final import organizer_final_page

# --- Import des pages participant ---
from goldenquizz.participant.participant_connect import participant_connect_page
from goldenquizz.participant.participant_wait import participant_wait_page
from goldenquizz.participant.participant_question import participant_question_page
from goldenquizz.participant.participant_answer import participant_answer_page
from goldenquizz.participant.participant_final import participant_final_page

# --- Initialisation du moteur du jeu ---
engine = GameEngine("config/questions.yaml")

# --- Page d'accueil ---
@ui.page("/")
def home_page():
    ui.label("🎉 Bienvenue sur GoldenQuizz !").classes("text-3xl font-bold mt-10 text-center text-amber-700")
    ui.label("Le quiz interactif pour découvrir qui connaît le mieux le VIP !").classes("text-lg text-gray-600 mb-8 text-center")

    with ui.column().classes("items-center gap-4"):
        ui.link("👑 Interface Organisateur", "/organizer/prep").classes("text-blue-600 block mt-4")
        ui.link("📱 Interface Participant", "/participant/connect").classes("text-green-600 block mt-2")


    ui.label("© GoldenQuizz 2025").classes("mt-10 text-gray-400 text-sm text-center")

# --- Pages organisateur ---
organizer_prep_page(engine)
organizer_question_page(engine)
organizer_results_page(engine)
organizer_final_page(engine)

# === Pages participant ---
participant_connect_page(engine)
participant_wait_page(engine)
participant_question_page(engine)
participant_answer_page(engine)
participant_final_page(engine)

# --- Lancement du serveur ---
ui.run(
    title="GoldenQuizz",
    reload=True,
    storage_secret="goldenquizz-secret-key-1234"  # 🔐 clé secrète pour les sessions
)

