import feedparser
import json
from time import sleep
from mastodon import Mastodon

with open('config.json') as file:
    data = json.load(file)

mastodon = Mastodon(
    client_id = data["key"],
    client_secret = data["secret"],
    access_token = data["token"],
    api_base_url = 'https://lgbtq.cool'
)

# Config
nws_feed = "https://alerts.weather.gov/cap/us.php?x=1"
alert_thresholds = ("Moderate","Severe")


# Local Data
recent_date = None

def get_recent_date(feed):
    global recent_date
    recent_date = feed.entries[0].published_parsed
    for i in feed.entries:
        if i.published_parsed < recent_date:
            recent_date = i.published_parsed
    print("Most Recent Date: {}".format(recent_date))


def main():
    global recent_date
    global mastodon

    current_feed = feedparser.parse(nws_feed)
    if recent_date is None:
        print("First run, getting the most recent date.")
        get_recent_date(current_feed)

    for i in current_feed.entries:
        if i.cap_severity in alert_thresholds:
            if i.published_parsed < recent_date:
                status = "{}  More Info: {}".format(i["summary"], i["link"])
                mastodon.status_post(status, spoiler_text="Weather alert in {}".format(i["cap_areadesc"]))
                recent_date = i.published_parsed
                print("Date condition met.")
            """else:
                print("Date condition not met.")"""
    sleep(10)
    main()


main()
