from nicegui import ui
from goldenquizz.game_engine import GameEngine
from goldenquizz.ui.theme import GLOBAL_CSS



# ---------------------------------------------------------
#   Initialisation du moteur
# ---------------------------------------------------------
engine = GameEngine("config/questions.yaml")


from goldenquizz.organizer.organizer_prep import organizer_prep_page
from goldenquizz.organizer.organizer_question import organizer_question_page
from goldenquizz.organizer.organizer_results import organizer_results_page
from goldenquizz.organizer.organizer_final import organizer_final_page

from goldenquizz.participant.participant_connect import participant_connect_page
from goldenquizz.participant.participant_wait import participant_wait_page
from goldenquizz.participant.participant_question import participant_question_page
from goldenquizz.participant.participant_answer import participant_answer_page
from goldenquizz.participant.participant_final import participant_final_page

# ---------------------------------------------------------
#   Enregistrement de toutes les pages
# ---------------------------------------------------------
@ui.page("/")
def home_page():

    # ---------------------------------------------------------
    #   CSS GLOBAL
    # ---------------------------------------------------------
    ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

    # ---------------------------------------------------------
    #   CONTENU CENTRÉ & MODERNE
    # ---------------------------------------------------------
    with ui.column().classes(
        "min-h-screen w-full flex items-center justify-center bg-gray-100 p-8"
    ):

        with ui.card().classes(
            "bg-white p-10 rounded-2xl shadow-2xl w-full max-w-2xl animate-fadeIn flex flex-col items-center gap-6"
        ):

            # ---- TITRE PRINCIPAL ----
            ui.label("🎉 GoldenQuizz").classes(
                "text-5xl font-extrabold text-blue-700 text-center tracking-tight"
            )

            ui.label("Le quiz interactif 👑").classes(
                "text-xl text-gray-600 text-center -mt-4"
            )

            ui.separator().classes("w-1/2 my-4")

            # ---- DESCRIPTION ----
            ui.label(
                "Choisissez votre rôle pour commencer l'expérience."
            ).classes("text-gray-600 text-center text-lg")

            # ---- BOUTONS ----
            with ui.column().classes("w-full items-center gap-4 mt-6"):

                #  Ajoute  emoji  personne
                ui.link("Je suis Participant", "/participant/connect") \
                    .classes(
                        "bg-green-600 hover:bg-green-700 text-white font-semibold "
                        "text-lg py-3 px-6 rounded-xl shadow-md transition w-64 text-center "
                        "no-underline"
                    )
                
                # Ajoute emoji organisateur
                ui.link("Je suis Organisateur", "/organizer/prep") \
                    .classes(
                        "bg-blue-600 hover:bg-blue-700 text-white font-semibold "
                        "text-lg py-3 px-6 rounded-xl shadow-md transition w-64 text-center "
                        "no-underline"
                    )



            # ---- FOOTER ----
            ui.label("© GoldenQuizz 2025").classes(
                "mt-8 text-gray-400 text-sm text-center"
            )


# -----------------------------------------------------
#   PAGES ORGANISATEUR
# -----------------------------------------------------
organizer_prep_page(engine)
organizer_question_page(engine)
organizer_results_page(engine)
organizer_final_page(engine)

# -----------------------------------------------------
#   PAGES PARTICIPANT
# -----------------------------------------------------
participant_connect_page(engine)
participant_wait_page(engine)
participant_question_page(engine)
participant_answer_page(engine)
participant_final_page(engine)

# ---------------------------------------------------------
#   RUN DU SERVEUR
# ---------------------------------------------------------
ui.run(
    title="GoldenQuizz",
    reload=True,
    storage_secret="goldenquizz-secret-key-1234"
)
