from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

mat_state = {
    "healthy_train": {
        "start": "2020-07-31T23:52:09",
        "end": "2020-09-30T23:44:41",
        "description": "healthy state",
    },
    "healthy_test": {
        "start": "2020-09-30T23:54:40",
        "end": "2020-10-09T08:30:12",
        "description": "healthy state test period",
    },
    "damage1": {
        "start": "2020-10-13T18:29:56",
        "end": "2020-10-27T11:32:37",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM6",
        "closest_sensor": 9,
    },
    "healthy1": {
        "start": "2020-10-27T15:46:21",
        "end": "2020-11-09T09:39:32",
        "description": "healthy state after damage",
    },
    "damage2": {
        "start": "2020-11-09T14:28:35",
        "end": "2020-11-24T09:40:41",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM4",
        "closest_sensor": 6,
    },
    "healthy2": {
        "start": "2020-11-24T13:50:35",
        "end": "2021-03-18T08:49:45",
        "description": "healthy state after damage",
    },
    "damage3": {
        "start": "2021-03-18T15:29:36",
        "end": "2021-04-20T11:40:16",
        "description": "all damage mechanisms removed",
        "severity": "high",
        "location": "DAM3",
        "closest_sensor": 5,
    },
    "healthy3": {
        "start": "2021-04-20T16:50:09",
        "end": "2021-05-04T10:13:49",
        "description": "healthy state after damage",
    },
    "damage4": {
        "start": "2021-05-04T15:23:42",
        "end": "2021-05-19T10:45:47",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM6",
        "closest_sensor": 9,
    },
    "healthy4": {
        "start": "2021-05-19T15:55:41",
        "end": "2021-05-28T07:11:04",
        "description": "healthy state after damage",
    },
    "damage5": {
        "start": "2021-05-28T12:20:57",
        "end": "2021-06-14T06:41:59",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM4",
        "closest_sensor": 6,
    },
    "healthy5": {
        "start": "2021-06-14T12:59:03",
        "end": "2021-06-25T05:43:20",
        "description": "healthy state after damage",
    },
    "damage6": {
        "start": "2021-06-25T11:55:57",
        "end": "2021-07-12T07:16:58",
        "description": "one damage mechanism removed",
        "severity": "low",
        "location": "DAM3",
        "closest_sensor": 5,
    },
    "healthy6": {
        "start": "2021-07-12T12:26:51",
        "end": "2021-07-31T23:46:27",
        "description": "healthy state after damage",
    },
}
