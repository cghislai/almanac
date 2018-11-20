#!/usr/bin/python3

import json
import time
import argparse

import flask

from almanac.almanac import AlmanacService
from almanac.api import EventType

app = flask.Flask('Almanac API server')
almanac_service = AlmanacService()


def start(host=None, port=None, debug=False):
    app.run(host=host, port=port, debug=debug)


@app.route("/moon/event")
@app.route("/moon/event/<string:event_type>")
def get_moon_events(event_type=None):
    try:
        start_time = flask.request.args.get('start_time')
        end_time = flask.request.args.get('end_time')
        if start_time is None or end_time is None:
            return make_response("Invalid time boundaries", 400)

        if event_type is None or event_type == "":
            return make_response("Invalid event type: %s" % event_type, 400)

        if event_type == EventType.MOON_PHASE.value:
            t, i = almanac_service.search_moon_phases(from_date_string=start_time, to_date_string=end_time)
            json_array = create_events_json("moon", event_type, t, i)
            return make_response(json_array, 200)

        elif event_type == EventType.MOON_ZODIAC.value:
            t, i = almanac_service.search_zodiacs("moon", from_date_string=start_time, to_date_string=end_time)
            json_array = create_events_json("moon", event_type, t, i)
            return make_response(json_array, 200)

        else:
            return make_response("Unahandled event type: %s" % event_type, 400)
    except Exception as e:
        return make_response(e, 400)


def create_events_json(body, event_type, time_data, index_data):
    events = []
    for time_data, data in zip(time_data, index_data):
        event = create_event(body, event_type, time_data, data)
        events.append(event)
    return json.dumps(events, indent=8)


def create_event(body, event_type, time_string, index_data):
    time_iso = convert_time(time_string)
    json_tuple = {"body": body, "time_utc": time_iso, "type": event_type, "index": int(index_data)}
    return json_tuple


def convert_time(time_value):
    timetuple = time_value.utc_datetime().timetuple()
    formatted = time.strftime("%Y-%m-%dT%H:%M:%S", timetuple)
    return formatted


def make_response(data, status):
    # TODO: if returning an error message, append a newline.
    response = flask.make_response(str(data), status)
    response.headers['Access-Control-Allow-Origin'] = '*'
    if status == 200:
        response.headers['Content-type'] = 'application/json'
    else:
        response.headers['Content-type'] = 'text/plain'
        print("caught error:")
        print(data)
    return response


def main():
    parser = argparse.ArgumentParser(description="Almanac API Server")
    parser.add_argument("-p", "--port", type=int, default=2828,
                        help="Port to listen to")
    parser.add_argument("-H", "--host", default="127.0.0.1",
                        help="Host to listen to")
    args = parser.parse_args()

    start(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
