from datetime import datetime
from itertools import cycle

from InquirerPy import inquirer
import shutil


WEEKDAYS = "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"
MUSCLE_GROUPS = "Beine", "Po", "Rücken", "Arme", "Bauch", "Brust", "Schultern"

# Das hier ist jetzt unsere "Datenbank" - ersetzen wir später durch eine echte Datenbank
# Dein Programm sollte nicht direkt auf diese Datenbank zugreifen. Stattdessesn führen get_... und set_... -Funktionen ein.
# Dadurch können wir später easy eine echte Datenbank einführen
database_keys = ["Name", "Muskelgruppe", "Kardio", "Wochentag", "Im Trainingsplan enthalten"]
database = [
    {"Name": "Bootynizer",  "Muskelgruppe": "Po",    "Kardio": False, "Wochentag": "Montag",   "Im Trainingsplan enthalten": False},
    {"Name": "Bankdrücken", "Muskelgruppe": "Brust", "Kardio": False, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False},
    {"Name": "Kniebeugen", "Muskelgruppe": "Beine", "Kardio": False, "Wochentag": "Montag", "Im Trainingsplan enthalten": False},
    {"Name": "Ausfallschritte", "Muskelgruppe": "Beine", "Kardio": False, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False},
    {"Name": "Beinpresse", "Muskelgruppe": "Beine", "Kardio": False, "Wochentag": "Mittwoch", "Im Trainingsplan enthalten": False},
    {"Name": "Hip Thrust", "Muskelgruppe": "Po", "Kardio": False, "Wochentag": "Donnerstag", "Im Trainingsplan enthalten": False},
    {"Name": "Donkey Kicks", "Muskelgruppe": "Po", "Kardio": False, "Wochentag": "Freitag", "Im Trainingsplan enthalten": False},
    {"Name": "Glute Bridge", "Muskelgruppe": "Po", "Kardio": False, "Wochentag": "Samstag", "Im Trainingsplan enthalten": False},
    {"Name": "Klimmzüge", "Muskelgruppe": "Rücken", "Kardio": False, "Wochentag": "Sonntag", "Im Trainingsplan enthalten": False},
    {"Name": "Latzug", "Muskelgruppe": "Rücken", "Kardio": False, "Wochentag": "Montag", "Im Trainingsplan enthalten": False},
    {"Name": "Rudern", "Muskelgruppe": "Rücken", "Kardio": False, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False},
    {"Name": "Bizepscurls", "Muskelgruppe": "Arme", "Kardio": False, "Wochentag": "Mittwoch", "Im Trainingsplan enthalten": False},
    {"Name": "Trizepsdrücken", "Muskelgruppe": "Arme", "Kardio": False, "Wochentag": "Donnerstag", "Im Trainingsplan enthalten": False},
    {"Name": "Hammercurls", "Muskelgruppe": "Arme", "Kardio": False, "Wochentag": "Freitag", "Im Trainingsplan enthalten": False},
    {"Name": "Crunches", "Muskelgruppe": "Bauch", "Kardio": False, "Wochentag": "Samstag", "Im Trainingsplan enthalten": False},
    {"Name": "Plank", "Muskelgruppe": "Bauch", "Kardio": False, "Wochentag": "Sonntag", "Im Trainingsplan enthalten": False},
    {"Name": "Russian Twist", "Muskelgruppe": "Bauch", "Kardio": False, "Wochentag": "Montag", "Im Trainingsplan enthalten": False},
    {"Name": "Butterfly", "Muskelgruppe": "Brust", "Kardio": False, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False},
    {"Name": "Liegestütze", "Muskelgruppe": "Brust", "Kardio": False, "Wochentag": "Mittwoch", "Im Trainingsplan enthalten": False},
    {"Name": "Dips", "Muskelgruppe": "Brust", "Kardio": False, "Wochentag": "Donnerstag", "Im Trainingsplan enthalten": False},
    {"Name": "Schulterdrücken", "Muskelgruppe": "Schultern", "Kardio": False, "Wochentag": "Freitag", "Im Trainingsplan enthalten": False},
    {"Name": "Seitheben", "Muskelgruppe": "Schultern", "Kardio": False, "Wochentag": "Samstag", "Im Trainingsplan enthalten": False},
    {"Name": "Frontheben", "Muskelgruppe": "Schultern", "Kardio": False, "Wochentag": "Sonntag", "Im Trainingsplan enthalten": False},
    {"Name": "Burpees", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Montag", "Im Trainingsplan enthalten": False},
    {"Name": "Mountain Climbers", "Muskelgruppe": "Bauch", "Kardio": True, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False},
    {"Name": "Jumping Jacks", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Mittwoch", "Im Trainingsplan enthalten": False},
    {"Name": "Laufen", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Donnerstag", "Im Trainingsplan enthalten": False},
    {"Name": "Radfahren", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Freitag", "Im Trainingsplan enthalten": False},
    {"Name": "Seilspringen", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Samstag", "Im Trainingsplan enthalten": False},
    {"Name": "Rudergerät", "Muskelgruppe": "Rücken", "Kardio": True, "Wochentag": "Sonntag", "Im Trainingsplan enthalten": False},
    {"Name": "Boxsprünge", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Montag", "Im Trainingsplan enthalten": False},
    {"Name": "Stepper", "Muskelgruppe": "Beine", "Kardio": True, "Wochentag": "Dienstag", "Im Trainingsplan enthalten": False}
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

def add_exercise(name: str, muscle_group: str, is_cardio: bool, weekday: str, part_of_schedule=False):
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
        "Name": name, "Muskelgruppe": muscle_group, "Kardio": is_cardio, "Wochentag": weekday, "Im Trainingsplan enthalten": part_of_schedule
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

def change_weekday(exercise_name: str, new_weekday: str):
    # Wochentag validieren
    if not new_weekday in WEEKDAYS:
        raise ValueError("Invalid weekday")

    for exercise_row in get_all_exercises():
        if exercise_row["Name"] == exercise_name:
            exercise_row["Wochentag"] = new_weekday
            exercise_row["Im Trainingsplan enthalten"] = True
            return

def empty_training_shedule():
    for exercise_row in database:
        exercise_row["Im Trainingsplan enthalten"] = False

# ----------------------------
def print_exercise(exercise_row):
    output = ""

    # Füge den Namen hinzu
    output += str.upper(f"{exercise_row['Name']:<50}| ")

    if exercise_row["Kardio"]: # Falls es eine Kardioübung ist, kriegt die Muskelgruppe den Suffix '[Kardio]'
        output += f"Muskelgruppe: { (exercise_row['Muskelgruppe']+"[Kardio]") :35}| "
    else:
        output += f"Muskelgruppe: {(exercise_row['Muskelgruppe']            ) :35}| "


    if exercise_row["Im Trainingsplan enthalten"]:
        output += f"Wochentag: {exercise_row['Wochentag']}"

    print(output)


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
    part_of_schedule = True
    weekday = inquirer.select(
        message="An welchem Wochentag wird diese Übung trainiert?",
        choices=["nicht Teil des Trainingsplans", ] + list(WEEKDAYS),
        pointer=">",
    ).execute()
    if weekday == "nicht Teil des Trainingsplans":
        weekday = WEEKDAYS[0]  # Montag, dient hier als Platzhalter / Default-Wert
        part_of_schedule = False
        print("Die Übung ist kein Teil eines Trainingsplans. Wähle 'Trainingsplan auswählen' im Hauptmenü, um Übungen neu zu sortieren.")
    else:
        print("Die Übung wird dem Wochentag", weekday, "hinzugefügt")

    add_exercise(
        name=exercise_name,
        muscle_group=muscle_group,
        is_cardio=is_cardio,
        weekday=weekday,
        part_of_schedule=part_of_schedule
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
    exercises = get_all_exercises()
    for exercise_row in exercises:
        print_exercise(exercise_row)

def user_create_schedule():
    training_plans = [
        "Bauch-Beine-Po + Kardio",
        "Push-Pull-Leg",
        "Oberkörper-Unterkörper-Kardio"
    ]

    plan = inquirer.select(
        message="Wähle den Trainingsplan",
        choices=training_plans,
        pointer=">",
    ).execute()

    if plan == training_plans[0]:
        # Bauch Beine Po + Kardio

        # Zunächst alle Übungen aus dem Trainingsplan entfernen
        empty_training_shedule()

        bauch = set()
        beine = set()
        po = set()
        kardio = set()

        # Sortieren der Übungen
        for exercise_row in get_all_exercises():
            if exercise_row["Kardio"]:
                kardio.add(exercise_row["Name"])
                continue

            elif exercise_row["Muskelgruppe"] == "Bauch":
                bauch.add(exercise_row["Name"])
                continue

            elif exercise_row["Muskelgruppe"] == "Beine":
                beine.add(exercise_row["Name"])
                continue

            elif exercise_row["Muskelgruppe"] == "Po":
                po.add(exercise_row["Name"])
                continue

        # Falls es nicht genug Übungen gibt, um 2 Tage mit verschiedenen Übungen zu füllen, werden Übungen an beiden Tagen eingefügt
        # So etwas geht in Python - keine festen Typen!
        bauch = cycle(bauch)
        beine = cycle(beine)
        po = cycle(po)
        kardio = cycle(kardio)

        for exercise_row in range(4):
            # 4 Übungen pro Einheit

            change_weekday(next(bauch), "Montag")
            change_weekday(next(beine), "Dienstag")
            change_weekday(next(po), "Mittwoch")

            change_weekday(next(bauch), "Donnerstag")
            change_weekday(next(beine), "Freitag")
            change_weekday(next(kardio), "Samstag")

    elif plan == training_plans[1]:
        # Push Pull Leg

        empty_training_shedule()

        push = set()
        pull = set()
        leg = set()

        # Übungen sortieren
        for exercise_row in get_all_exercises():
            if (not exercise_row["Kardio"]) and (exercise_row["Muskelgruppe"] in ("Brust", "Arme")):
                push.add(exercise_row["Name"])
                continue

            elif (not exercise_row["Kardio"]) and (exercise_row["Muskelgruppe"] in ("Rücken", "Schultern")):
                pull.add(exercise_row["Name"])

            elif (not exercise_row["Kardio"]) and (exercise_row["Muskelgruppe"] in ("Beine", "Po")):
                leg.add(exercise_row["Name"])

        push = cycle(push)
        pull = cycle(pull)
        leg = cycle(leg)

        # 5 Übungen pro Tag
        for exercise_row in range(5):
            change_weekday(next(push), "Montag")
            change_weekday(next(push), "Donnerstag")

            change_weekday(next(pull), "Dienstag")
            change_weekday(next(pull), "Freitag")

            change_weekday(next(leg), "Mittwoch")
            change_weekday(next(leg), "Samstag")

    elif plan == training_plans[2]:
        # Ganzkörper

        empty_training_shedule()

        oberkörper = set()
        unterkörper = set()
        kardio = set()

        # Übungen sortieren
        for exercise_row in get_all_exercises():
            if (not exercise_row["Kardio"]) and (exercise_row["Muskelgruppe"] in ("Brust", "Arme", "Rücken", "Schultern")):
                oberkörper.add(exercise_row["Name"])
                continue

            elif (not exercise_row["Kardio"]) and (exercise_row["Muskelgruppe"] in ("Beine", "Po", "Bauch")):
                # Bauch i.d.R. Teil des Unterkörperteils

                unterkörper.add(exercise_row["Name"])
                continue

            elif exercise_row["Kardio"]:
                kardio.add(exercise_row["Name"])

        oberkörper = cycle(oberkörper)
        unterkörper = cycle(unterkörper)
        kardio = cycle(kardio)

        # 8 Übungen pro Tag
        for exercise_row in range(8):
            change_weekday(next(oberkörper), "Montag")

            change_weekday(next(unterkörper), "Mittwoch")

            change_weekday(next(kardio), "Freitag")

    else:
        raise ValueError("Which exercise do you want to create?")


    user_show_schedule()


def user_show_schedule():
    for weekday in WEEKDAYS:
        print(weekday.upper() +":")

        exercises = get_all_exercises()
        for exercise_row in exercises:
            if exercise_row["Wochentag"] == weekday and exercise_row["Im Trainingsplan enthalten"]:
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
        user_create_schedule()

    elif choice == user_options[4]:
        user_show_schedule()

    else:
        raise ValueError("Invalid choice")

def main():
    while True:
        user_selection()
        seperator(":")

if __name__ == '__main__':
    main()



# TODO : Wenn es zu viele Übungen pro Muskelgruppe gibt, muss eine gelöscht werden.