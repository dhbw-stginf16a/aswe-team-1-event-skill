#!/usr/bin/env python3

import logging
import requests
import json
import random
import datetime
import dateutil.parser
import calendar

logger = logging.getLogger(__name__)

from app import PREFSTORE_CLIENT, CONCERN_CLIENT

def getLatestAppointmentOnDay(user, date):
    payload = {
        "date": "2019-04-08T15:00:00+00:00",
        "user": user
    }

    data = CONCERN_CLIENT.getConcern(user, "calendar", "event_date", payload)
    event = max(data.setdefault('events', []), key=lambda x: dateutil.parser.parse(x['end']))
    logger.error("Last Event of date is: " + repr(event))
    startTime = dateutil.parser.parse(event['end'])
    return calendar.timegm(startTime.utctimetuple())

def getPossibleEvents(user, date, freeTimeStarts, categories):
    # Convert time to datetime object to work with it
    dt = dateutil.parser.parse(date)
    # Add a day to get a 1 day timeframe
    dt_end = dt.now() + datetime.timedelta(days=1)
    cat = categories.split(';')

    payload = {
        "categories": cat,
        "location": "@48.7744476,9.1714984,17.5",
        "start_date": dt.strftime("%Y-%m-%d"),
        "end_date": dt_end.strftime("%Y-%m-%d")
    }
    data = CONCERN_CLIENT.getConcern(user, "events", "current_events", payload)
    return data.setdefault('events', None)

def getRoute(user, start, destination):
    payload = {
        "location": start,
        "destination": destination,
        "travelmode": ["driving"]
    }
    data = CONCERN_CLIENT.getConcern(user, "traffic", "traffic_route", payload)
    logger.error(data.setdefault('routes', "routes Key Not Found in response"))
    routes = data.setdefault('routes', None)
    if routes is not None:
        return routes[0] # just return the first route
    else:
        raise BaseException("This shouldn't happen. No route was returned")

def getTimeToDrive(user, start_location, start_time, event_location):
    dt = dateutil.parser.parse(start_time)

    route = getRoute(user, start_location, event_location)
    if route.setdefault('duration', None) is not None:
        duration = route['duration']
        dt_leaveby = dt - datetime.timedelta(seconds=duration)
        leaveby = calendar.timegm(dt_leaveby.utctimetuple())
        logger.error(f"LeaveBy: {leaveby}")
        return leaveby
    else:
        raise BaseException("Duration information not found") 

def get_evening_event(user, date, location):
    freeTimeStarts = getLatestAppointmentOnDay(user, date)
    if freeTimeStarts is None:
        return {"success": True, "noFreeTime": True}, 200

    preferences = PREFSTORE_CLIENT.get_user_prefs(user)

    if location is None:
        if preferences['home_address'] is None:
            logger.error("Couldn't find home location for user: " + user)
            return {"error": "Couldn't find home location for user: " + user}, 400
        location = preferences['home_address']

    possibilities = getPossibleEvents(user, date, freeTimeStarts, preferences.setdefault('event_types', "concerts;performing-arts"))
    logger.error(f"Events: {possibilities}")

    for possibility in possibilities:
        eventlocation = possibility.setdefault('location', None)
        if eventlocation is not None:
            coords = f"{eventlocation[1]},{eventlocation[0]}"
            logger.error(f"Event Location: {eventlocation}")
            logger.error(f"Event Start: {possibility['start']}")
            possibility['realStartTime'] = getTimeToDrive(user, location, possibility['start'], coords)
            logger.error(f"LeavyBy (realStartTime): {possibility['realStartTime']}")
        else:
            ## if location not found just skip and write to log
            logger.error("Event Location not set" % possibility)

    filter(lambda o: o['realStartTime'] > freeTimeStarts, possibilities) # TODO make sure time comparision works as expected

    if len(possibilities) is 0:
        return {"success": False, "noEvents": True}, 200

    random.shuffle(possibilities)

    return { "success": True, "payload": possibilities[0] }, 200

def request(body):
    print("Skill request: {}".format(body))
    if body["type"] == "event_get_evening":
        return get_evening_event(body["user"], body["payload"]["date"], body["payload"]["location"])
    else:
        logger.error("Unknown request type: " + body["type"])
        return {"error": "Unknown request Type"}, 404

