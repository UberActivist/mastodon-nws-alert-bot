import feedparser
from time import sleep

# Config
nws_feed = "https://alerts.weather.gov/cap/us.php?x=1"
alert_thresholds = ("Moderate","Severe")


# Local Data
recent_date = None

def get_recent_date(feed):
    global recent_date
    recent_date = feed.entries[0].updated
    for i in feed.entries:
        if i.updated < recent_date:
            recent_date = i.updated


def main():
    global recent_date

    current_feed = feedparser.parse(nws_feed)
    if recent_date is None:
        print("First run, getting the most recent date.")
        get_recent_date(current_feed)

    for i in current_feed.entries:
        if i.cap_severity in alert_thresholds:
            if i.updated < recent_date:
                print("{} in {}".format(i["title"], i["cap_areadesc"]))
                recent_date = i.updated
                print("Date condition met.")
            """else:
                print("Date condition not met.")"""
    sleep(10)
    main()


main()
