import feedparser
from time import sleep

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

    current_feed = feedparser.parse(nws_feed)
    if recent_date is None:
        print("First run, getting the most recent date.")
        get_recent_date(current_feed)

    for i in current_feed.entries:
        if i.cap_severity in alert_thresholds:
            if i.published_parsed < recent_date:
                print("{} in {}".format(i["title"], i["cap_areadesc"]))
                recent_date = i.published_parsed
                print("Date condition met.")
            """else:
                print("Date condition not met.")"""
    sleep(10)
    main()


#main()
