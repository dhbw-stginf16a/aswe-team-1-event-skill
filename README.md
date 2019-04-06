# dhbw-stginf16a-aswe-team-1-event-skill
Event skill for telling weather there is a possibillity to go to an event and how to get there

### Needed monitoring entities
 - preferences
    - same as commute skill
 - calendar
 - events

### Proactive output
Daily trigger to tell evening activities (optional)

### Requests

#### Get route to destinations
`type`:`event_get_evening`

##### request-format
 - `date`: Date to calculate when to get to work
 - `location`: String that google magically parses to an to location (If ommited defaults to home of the user)

```json
{
    "payload":{
        "date":"2019-04-01", // YYYY-MM-DD
        "location":"Stuttgart, Hauptbahnhof"
    }
}

```
##### response-format 
```json
{
    "category": "concerts",
    "description": "",
    "location": [
            9.16122,
            48.770088
        ],
    "start": "2019-04-27T19:00:00Z",
    "title": "Bernd Begemann - Der elektrische Liedermacher",
    "realStartTime": "2019-04-27T18:00:00Z" // latest time to leave towards the event
}
```