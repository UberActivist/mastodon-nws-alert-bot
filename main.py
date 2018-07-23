import feedparser
from time import sleep

# Config
nws_feed = "https://alerts.weather.gov/cap/us.php?x=1"
alert_threshold = "Severe"


# Local Data
recent_date = None


def main():
    current_feed = feedparser.parse(nws_feed)
    for i in current_feed.entries:
        global recent_date
        if recent_date is None:
            recent_date = i.date
            print("First run, picked a date and stuck with it.")
            break
        elif i.cap_severity == alert_threshold:
            if i.date < recent_date:
                print("{} in {}".format(i["title"], i["cap_areadesc"]))
                print("Date condition met.")
            else:
                print("Date condition not met.")
    sleep(10)
    main()


main()
