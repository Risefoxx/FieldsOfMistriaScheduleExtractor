import tomllib
import json

def parse_toml(filename, schedules):
    with open(filename, "rb") as f:
        data = tomllib.load(f)

    day = None
    weather = None

    # get day and weather
    for requirement in data["requires"]:
        if "day_of_the_week" in requirement:
            day = requirement["day_of_the_week"]

        if "weather" in requirement:
            weather = requirement["weather"]

    if day not in schedules:
        schedules[day] = {}

    if weather not in schedules[day]:
        schedules[day][weather] = {}

    # add npc
    for villager, schedule in data.items():

        if villager in ("requires", "start_writes", "end_writes"):
            continue

        schedules[day][weather][villager] = {}

        # add time/location
        for time, information in schedule.items():


            # "6:00am" = "some/location"
            if isinstance(information, str):
                schedules[day][weather][villager][time] = information

            # [npc."6:00am"]
            # destination = "some/location"
            else:
                schedules[day][weather][villager][time] = information["destination"]


schedules = {}

parse_toml("./toml_files/spring_monday.s.toml", schedules)
parse_toml("./toml_files/spring_tuesday.s.toml", schedules)
parse_toml("./toml_files/spring_wednesday.s.toml", schedules)
parse_toml("./toml_files/spring_thursday.s.toml", schedules)
parse_toml("./toml_files/spring_saturday.s.toml", schedules)
parse_toml("./toml_files/spring_sunday.s.toml", schedules)

with open("schedules_spring.json", "w") as f:
    json.dump(schedules, f, indent=4)