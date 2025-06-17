import requests
from datetime import date, timedelta

API_BASE = "http://localhost:8000"

drivers = [
    {"name": "Max Verstappen", "nationality": "Netherlands", "date_of_birth": "1997-09-30", "team": "Red Bull Racing"},
    {"name": "Sebastian Vettel", "nationality": "Germany", "date_of_birth": "1987-07-03", "team": "Red Bull Racing"},
    {"name": "Charles Leclerc", "nationality": "Monaco", "date_of_birth": "1997-10-16", "team": "Ferrari"},
    {"name": "Michael Schumacher", "nationality": "Germany", "date_of_birth": "1969-01-03", "team": "Ferrari"},
    {"name": "Lewis Hamilton", "nationality": "UK", "date_of_birth": "1985-01-07", "team": "Mercedes"},
    {"name": "Nico Rosberg", "nationality": "Germany", "date_of_birth": "1985-06-27", "team": "Mercedes"},
]

teams = [
    {"name": "Red Bull Racing", "country": "Austria"},
    {"name": "Ferrari", "country": "Italy"},
    {"name": "Mercedes", "country": "Germany"},
]

tracks = [
    {"name": "Silverstone", "country": "UK", "length_km": 5.891},
    {"name": "Monza", "country": "Italy", "length_km": 5.793},
    {"name": "Spa-Francorchamps", "country": "Belgium", "length_km": 7.004},
]

def post_json(endpoint, payload):
    response = requests.post(f"{API_BASE}{endpoint}", json=payload)
    response.raise_for_status()
    return response.json()

def main():
    team_name_to_id = {}
    driver_id_to_team_id = {}
    driver_ids = []
    season = 2025
    today = date.today().isoformat()

    # Создание команд
    for id, team in enumerate(teams):
        res = post_json("/teams/create", team)
        team_name_to_id[team["name"]] = id + 1

    # Создание гонщиков и присоединение к командам
    for id, driver in enumerate(drivers):
        driver_res = post_json("/drivers/create", {
            "name": driver["name"],
            "nationality": driver["nationality"],
            "date_of_birth": driver["date_of_birth"]
        })
        driver_id = id+1
        driver_ids.append(driver_id)
        team_id = team_name_to_id[driver["team"]]
        driver_id_to_team_id[driver_id] = team_id

        post_json("/drivers/join", {
            "driver_id": driver_id,
            "team_id": team_id,
            "season": season,
            "joined_at": today
        })

    # Добавление трасс
    track_ids = []
    for id, track in enumerate(tracks):
        res = post_json("/tracks/add", track)
        track_ids.append(id+1)

    # Планирование гонок
    race_ids = []
    for i in range(3):
        race_data = {
            "name": f"Grand Prix {i + 1}",
            "track_id": track_ids[i % len(track_ids)],
            "date": (date.today() + timedelta(days=i * 7)).isoformat(),
            "season": season
        }
        res = post_json("/races/schedule", race_data)
        race_ids.append(i+1)

    # Завершение гонок
    for race_id in race_ids:
        shuffled = driver_ids[:]
        import random
        random.shuffle(shuffled)

        results = []
        for pos, driver_id in enumerate(shuffled):
            results.append({
                "driver_id": driver_id,
                "team_id": driver_id_to_team_id[driver_id],
                "position": pos + 1,
                "points": max(0, 25 - pos * 4)
            })

        post_json("/races/finish", {
            "race_id": race_id,
            "results": results
        })


if __name__ == "__main__":
    main()
