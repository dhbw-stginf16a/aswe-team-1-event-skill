#!/usr/bin/env python3

import logging
import requests
import json
import random

logger = logging.getLogger(__name__)

from app import PREFSTORE_CLIENT

def getLatestAppointmentOnDay(user, date):
    raise BaseException("Not yet implemented")  # TODO Erik same as in commute skill

def getPossibleEvents(user, date, freeTimeStarts):
    raise BaseException("Not yet implemented")

def getTimeToDrive(user, param, location):
    raise BaseException("Not yet implemented")

def get_evening_event(user, date, location):
    freeTimeStarts = getLatestAppointmentOnDay(user, date)
    if freeTimeStarts is None:
        return {"success": True, "noFreeTime": True}, 200

    preferences = PREFSTORE_CLIENT.get_user_prefs(user)

    if location is None:
        if preferences['home'] is None:
            logger.error("Couldn't find home location for user: " + user)
            return {"error": "Couldn't find home location for user: " + user}, 400
        location = preferences['home']

    possibilities = getPossibleEvents(user, date, freeTimeStarts)

    for possibility in possibilities:
        possibility['realStartTime'] = getTimeToDrive(user, possibility['start_time'], location)

    filter(lambda o: o['realStartTime'] > freeTimeStarts, possibilities)

    if len(possibilities) is 0:
        return {"success": False, "noEvents": True}, 200

    random.shuffle(possibilities)

    return possibilities[0], 200  # TODO Adjust the structure of the return value

def request(body):
    print("Skill request: {}".format(body))
    if body["type"] == "event_get_evening":
        return get_evening_event(body["user"], body["payload"]["date"], body["payload"]["location"])
    else:
        logger.error("Unknown request type: " + body["type"])
        return {"error": "Unknown request Type"}, 404

