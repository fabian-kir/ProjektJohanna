from datetime import datetime
from InquirerPy import inquirer
import shutil


WEEKDAYS = "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"
MUSCLE_GROUPS = "Beine", "Po", "Rücken", "Arme", "Bauch", "Brust"

# Das hier ist jetzt unsere "Datenbank" - ersetzen wir später durch eine echte Datenbank
# Dein Programm sollte nicht direkt auf diese Datenbank zugreifen. Stattdessesn führen get_... und set_... -Funktionen ein.
# Dadurch können wir später easy eine echte Datenbank einführen
database_keys = ["Name", "Muskelgruppe", "Kardio", "Wochentag"]
database = [
    {"Name": "Bootynizer",  "Muskelgruppe": "Po",    "Kardio": False, "Wochentag": "Montag",   "Im Trainingsplan enthalten": False},
    {"Name": "Bankdrücken", "Muskelgruppe": "Brust", "Kardio": False, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False}
]

def seperator(char="-"):
    console_size = shutil.get_terminal_size((80, 20)).columns
    print(char * console_size)


# Überprüft, ob eine Übung bereits existiert
def does_exercise_exist(exercise_name: str) -> bool :
    # TODO: überarbeiten für SQL
    for row in database:
        if row["Name"] == exercise_name:
            return True

    return False

def add_exercise(name: str, muscle_group: str, is_cardio: bool, weekday: str, part_of_training_plan=False):
    # Standardmäßig ist eine Übung nicht Teil des Trainingsplans. Sobald ein Trainingsplan ausgewählt wird, wird das neu angepasst

    # Überprüfen, dass 'weekday' auch ein gültiger Wochentag ist
    if not weekday in WEEKDAYS:
        raise ValueError("Invalid weekday")

    # Überprüfen, dass Übung noch nicht existiert
    if does_exercise_exist(name):
        raise ValueError("Exercise already exists")

    # Überprüfen, dass die Muskelgruppe existiert
    if not muscle_group in MUSCLE_GROUPS:
        raise ValueError("Invalid muscle group")

    # TODO: überarbeiten für SQL
    database.append({
        "Name": name, "Muskelgruppe": muscle_group, "Kardio": is_cardio, "Wochentag": weekday, part_of_training_plan: part_of_training_plan
    })

def get_all_exercises():
    # TODO anpassen für Datenbank
    return database

def get_exercise_on_day(weekday: str):
    result = []

    for row in database:
        if row["Wochentag"] == weekday:
            result.append(row["Name"])

    return result

# ----------------------------
def print_exercise(exercise_row):
    output = ""

    # Füge den Namen hinzu
    output += str.upper(f"{exercise_row['Name']:<50}| ")
    output += f"Muskelgruppe: {exercise_row['Muskelgruppe']:25}| "

    output += f"Wochentag: {exercise_row['Wochentag']}"
    print(output)

    if exercise_row["Im Trainingsplan enthalten"]:
        output += "☑ Im Trainingsplan enthalten |"
    else:
        output += "❌ Im Trainingsplan enthalten |"


    if exercise_row['Kardio']:
        output += "[Kardioübung] "
    else:
        #Füge anstatt '[Kardioübung]' 14 Leerzeichen ein
        output += " "*14


def user_add_exercise():
    exercise_name = input("Wie heißt deine Übung?\n > ")
    # Prüfen, dass Name nicht zu lang ist
    if len(exercise_name) > 50:
        raise ValueError("Exercise name is too long")
    print("Übung heißt:", exercise_name)


    # Auswahl der Muskelgruppe
    muscle_group = inquirer.select(
        message="Zu welcher Muskelgruppe gehört deine Übung?",
        choices=MUSCLE_GROUPS,
        pointer=">",
    ).execute()
    print("Muskelgruppe ist:", muscle_group)

    # Auswahl, ob es eine Kardioübung ist
    choice = inquirer.select(
        message="Ist es eine Kardioübung?",
        choices=("Kardio", "kein Kardio"),
        pointer=">",
    ).execute()
    is_cardio = False
    if choice == "Kardio":
        is_cardio = True
        print("Die Übung ist eine Kardioübung")
    else:
        is_cardio = False
        print("Die Übung ist keine Kardioübung")

    # Auswahl des Wochentags (später über "Trainingsplan ändern" werden andere Wochentage ausgewählt)
    part_of_training_plan = True
    weekday = inquirer.select(
        message="An welchem Wochentag wird diese Übung trainiert?",
        choices=["nicht Teil des Trainingsplans", ] + list(WEEKDAYS),
        pointer=">",
    ).execute()
    if weekday == "nicht Teil des Trainingsplans":
        weekday = WEEKDAYS[0]  # Montag, dient hier als Platzhalter / Default-Wert
        part_of_training_plan = False
        print("Die Übung ist kein Teil eines Trainingsplans. Wähle 'Trainingsplan auswählen' im Hauptmenü, um Übungen neu zu sortieren.")
    else:
        print("Die Übung wird dem Wochentag", weekday, "hinzugefügt")

    add_exercise(
        name=exercise_name,
        muscle_group=muscle_group,
        is_cardio=is_cardio,
        weekday=weekday,
        part_of_training_plan=part_of_training_plan
    )


def user_show_exercise_for_muscle_group():
    muscle_group = inquirer.select(
        message="Welche Muskelgruppe wird gesucht?",
        choices=MUSCLE_GROUPS,
        pointer=">",
    ).execute()

    # Iteriere über alle Übungen, gebe alle aus, die der Muskelgruppe entsprechen
    exercises = get_all_exercises()
    for exercise_row in exercises:
        if exercise_row["Muskelgruppe"] == muscle_group:
            print_exercise(exercise_row)


def user_show_all_exercises():
    # TODO das macht Fabi
    pass

def user_create_weekplan():
    training_plans = [
        "Bauch-Beine-Po + Kardio",
        "Push-Pull-Leg",
        "Ganzkörper"
    ]

    plan = inquirer.select(
        message="Wähle den Trainingsplan",
        choices=training_plans,
        pointer=">",
    ).execute()

    if plan == training_plans[0]:
        # Bauch-Beine-Po + Kardio
        # MO: Bauch, DI: Rest, MI: Beine, DO: Rest, FR: Po, Sa: Kardio
        ...

    elif plan == training_plans[1]:
        ...
    elif plan == training_plans[2]:
        ...
    elif plan == training_plans[3]:
        ...


def user_show_weekplan():
    for weekday in WEEKDAYS:
        print(weekday.upper() +":")

        exercises = get_all_exercises()
        for exercise_row in exercises:
            if exercise_row["Wochentag"] == weekday:
                print_exercise(exercise_row)

        seperator()





def user_selection():
    user_options = "Übung hinzufügen", "Zeige alle Übungen an", "Zeige Übungen einer Muskelgruppe", "Trainingsplan auswählen", "Zeige Trainingsplan"
    choice = inquirer.select(
        message="Was möchtest du tun?",
        choices=user_options,
        pointer=">",
    ).execute()

    if choice == user_options[0]:
        user_add_exercise()

    elif choice == user_options[1]:
        user_show_all_exercises()

    elif choice == user_options[2]:
        user_show_exercise_for_muscle_group()

    elif choice == user_options[3]:
        user_create_weekplan()

    elif choice == user_options[4]:
        user_show_weekplan()

    else:
        raise ValueError("Invalid choice")

def main():
    while True:
        user_selection()

if __name__ == '__main__':
    main()



# TODO : Wenn es zu viele Übungen pro Muskelgruppe gibt, muss eine gelöscht werden.