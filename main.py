import tomllib
import json


def parse_toml(filename, schedules):
    with open(filename, "rb") as f:
        data = tomllib.load(f)

    day = None
    weather = None

    # Get the day and weather from "requires"
    for requirement in data["requires"]:
        if "day_of_the_week" in requirement:
            day = requirement["day_of_the_week"]

        if "weather" in requirement:
            weather = requirement["weather"]

    # Add each NPC
    for villager, schedule in data.items():

        # Ignore non-NPC sections
        if villager in ("requires", "start_writes", "end_writes"):
            continue

        # Create the nested dictionaries if necessary
        if villager not in schedules:
            schedules[villager] = {}

        if day not in schedules[villager]:
            schedules[villager][day] = {}

        if weather not in schedules[villager][day]:
            schedules[villager][day][weather] = {}

        # Add each time/location
        for time, information in schedule.items():

            # Format:
            # "6:00am" = "some/location"
            if isinstance(information, str):
                schedules[villager][day][weather][time] = information

            # Format:
            # [npc."6:00am"]
            # destination = "some/location"
            else:
                schedules[villager][day][weather][time] = information["destination"]


schedules = {}

parse_toml("./toml_files/spring_monday.s.toml", schedules)
parse_toml("./toml_files/spring_tuesday.s.toml", schedules)
parse_toml("./toml_files/spring_wednesday.s.toml", schedules)
parse_toml("./toml_files/spring_thursday.s.toml", schedules)
parse_toml("./toml_files/spring_saturday.s.toml", schedules)
parse_toml("./toml_files/spring_sunday.s.toml", schedules)


with open("schedules_spring.json", "w") as f:
    json.dump(schedules, f, indent=4)