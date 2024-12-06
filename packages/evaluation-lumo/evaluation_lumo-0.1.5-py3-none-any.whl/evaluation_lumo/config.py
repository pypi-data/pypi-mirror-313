from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

mat_state = {
    "healthy_train": {
        "start": "2020-08-01",
        "end": "2020-10-01",
        "description": "healthy state",
    },
    "healthy_test": {
        "start": "2020-10-01",
        "end": "2020-10-13",
        "description": "healthy state test period",
    },
    "damage1": {
        "start": "2020-10-13",
        "end": "2020-10-27T10:00:00",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM6",
        "closest_sensor": 9,
    },
    "healthy1": {
        "start": "2020-10-27",
        "end": "2020-11-09",
        "description": "healthy state after damage",
    },
    "damage2": {
        "start": "2020-11-09",
        "end": "2020-11-24",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM4",
        "closest_sensor": 6,
    },
    "healthy2": {
        "start": "2020-11-24",
        "end": "2021-03-18",
        "description": "healthy state after damage",
    },
    "damage3": {
        "start": "2021-03-18",
        "end": "2021-04-20",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM3",
        "closest_sensor": 5,
    },
    "healthy3": {
        "start": "2021-04-20",
        "end": "2021-05-04",
        "description": "healthy state after damage",
    },
    "damage4": {
        "start": "2021-05-04",
        "end": "2021-05-19",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM6",
        "closest_sensor": 9,
    },
    "healthy4": {
        "start": "2021-05-19",
        "end": "2021-05-28",
        "description": "healthy state after damage",
    },
    "damage5": {
        "start": "2021-05-28",
        "end": "2021-06-14",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM4",
        "closest_sensor": 6,
    },
    "healthy5": {
        "start": "2021-06-14",
        "end": "2021-06-25",
        "description": "healthy state after damage",
    },
    "damage6": {
        "start": "2021-06-25",
        "end": "2021-07-12",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM3",
        "closest_sensor": 5,
    },
    "healthy6": {
        "start": "2021-07-12",
        "end": "2021-08-01",
        "description": "healthy state after damage",
    },
}
