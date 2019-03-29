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
        "start_from":"DHBW",
        "location":"Stuttgart, Hauptbahnhof"
    }
}

```
##### answer-format TBD
