#!usr/bin/env python
import arrow
import json
import requests
import logging
import csv
import re
import config

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

slack_webhook = config.SLACK_WEBHOOK
TEST_MODE = False
channels = config.channels
username = 'SlacKing'

def post_to_slack(payload, webhook):
    log.debug("Attempting to post with payload %s", payload)
    json_payload = json.dumps(payload)
    r = requests.post(webhook, data=json_payload)

    log.debug(r.text)
    log.debug(r.status_code)

def get_channel(day_num):
    return channels[day_num]

def get_payload(date, rec):
    date2, weekly_message, scripture, memory_verse, q1, q2, application, prayer_message, prayer, quote = rec
    dt = date.format('MMMM D, YYYY')
    day_of_week = date.weekday() + 1
    if day_of_week == 1:
        log.info("Processing payload for Monday")
        return monday(get_channel(day_of_week), username, dt, weekly_message, scripture)
    elif day_of_week == 2:
        return tuesday(get_channel(day_of_week), username, memory_verse)
    elif day_of_week == 3:
        return wednesday(get_channel(day_of_week), username, q1, q2)
    elif day_of_week == 4:
        return thursday(get_channel(day_of_week), username, application)
    elif day_of_week == 5:
        return friday(get_channel(day_of_week), username, prayer, prayer_message, quote)


def monday(channel, username, date, weekly_msg, scripture):
    payload = {
        'username': username,
        'mrkdwn_in': True,
        'channel': channel,
        "attachments": [
            {
                "title": "Scripture of the Week",
                "pretext": "*Week of {0}*\n<!channel>\n\n".format(date) + weekly_msg,
                "text": scripture,
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }
    return payload


def tuesday(channel, username, memory_verse):
    payload = {
        'username': username,
        'mrkdwn_in': True,
        'channel': channel,
        "attachments": [
            {
                "title": "Memory Verse",
                "pretext": "<!channel>\n\nWhat are your first takeaways from this week's scripture?",
                "text": memory_verse,
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }
    return payload


def wednesday(channel, username, q1, q2):
    payload = {
        'username': username,
        'mrkdwn_in': True,
        'channel': channel,
        "attachments": [
            {
                "title": "Questions",
                "pretext": "<!channel>\n\nHere are this weeks question.  Please respond and discuss in this channel:",
                "text": "1. {0}\n2. {1}".format(q1, q2),
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }
    return payload


def thursday(channel, username, application_message):
    msg = ("It's time to put what we've studied into action.  See our application challenge and try to think up your "
    "own to post for others.  Respond to the group if you have a good story of how an application worked out "
    "in your life.")
    payload = {
        'username': username,
        'mrkdwn_in': True,
        'channel': channel,
        "attachments": [
            {
                "title": "Application Challenge",
                "pretext": "<!channel>\n\n{0}".format(msg),
                "text": application_message,
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }
    return payload


def friday(channel, username, prayer, pray_for, quote):
    if quote != '':
        quote_str = '_' + quote + '_'
    else:
        quote_str = quote
    payload = {
        'username': username,
        'mrkdwn_in': True,
        'channel': channel,
        "attachments": [
            {
                "title": "Prayer",
                "text": "{0}\n\nThis week pray for: _{1}_".format(prayer, pray_for),
                "pretext": "<!channel>\n\n{0}".format(quote_str),
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }
    return payload


def read_source(filename):
    file_data = []
    log.debug("Reading text from file %s", filename)
    with open(filename, 'rb') as f:
        file_reader = csv.reader(f)
        next(file_reader, None) # skip header
        for row  in file_reader:
            l = [clean_string(x) for x in row]
            file_data.append(l)
    return file_data


def clean_string(s):
    return s.replace("\\n","\n").replace('\xe2\x80\x99',"'").replace('\xe2\x80\x98',"'").replace('\xe2\x80\x9c','"')\
        .replace('\xe2\x80\x9d','"')


if __name__ == "__main__":
    records = read_source(config.SLACK_SOURCE_FILE_PATH)
    log.debug("Data from file: %s", records)

    now = arrow.now('US/Pacific')
    #now = arrow.get("2017-10-02", 'YYYY-MM-DD',tzinfo='US/Pacific')  # override manually for testing
    weekday = now.weekday()
    weekstart = now.shift(days=-weekday).floor('day')
    today = now.floor('day')
    log.info("Current day: %s, weekday: %s, week start: %s", today, weekday, weekstart)

    for rec in records:
        log.info(rec)
        if rec[0] is not None and rec[0] != '' and arrow.get(rec[0], 'YYYY-MM-DD', tzinfo='US/Pacific') == weekstart:
            payload = get_payload(today, rec)
            log.info("Payload received: %s", payload)
            if payload is not None and not TEST_MODE:
                post_to_slack(payload, slack_webhook)