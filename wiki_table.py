import json
import sys

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

def format_time(time):
    time = time.strip().lower()

    if time.endswith("am"):
        period = "AM"
        time = time[:-2]
    elif time.endswith("pm"):
        period = "PM"
        time = time[:-2]
    else:
        return time

    return f"{time} {period}"

def character_to_wiki(data, character, mood="pleasant"):
    if character not in data:
        raise ValueError(f"Character '{character}' not found.")

    character_data = data[character]

    output = []

    for day in DAYS:
        if day not in character_data:
            continue

        day_data = character_data[day]

        if mood not in day_data:
            continue

        schedule = day_data[mood]

        output.append(f"=== {day.title()} ===")
        output.append("{| {{#var:tableDeets}}")
        output.append("{{#var:header1}}")

        for time, location in schedule.items():
            output.append("|-")
            output.append(f"|{format_time(time)}")
            output.append(f"|{location}")

        output.append("|}")
        output.append("")

    return "\n".join(output)


def main():
    if len(sys.argv) < 3:
        print("Usage: python wiki_table.py <json_file> <character>")
        return

    json_file = sys.argv[1]
    character = sys.argv[2]

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    result = character_to_wiki(data, character)

    print(result)

if __name__ == "__main__":
    main()