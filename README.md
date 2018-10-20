# Calendar Auditor

Calendar Auditor is my humble attempt at getting visibility into how my
calendar looks like over the past week(s).

You have time, you just need to [make time for time][1].

![Sample run of the Script](screenshot.png?raw=true "Script Output")

[1]: https://hbr.org/2011/12/make-time-for-time.html

## What this is today

A simple script that summarizes the events that I have on my calendar for the
past 7 days, and tells me how much time I've spent in different type of
meetings.

Many things are still hard-coded (e.g. the type of events that I am tracking).

## What this will be someday

This should allow you specify the type of events that you want to track, and
categorize them for you accordingly.

## Running the Analyzer

First, follow `Step 1: Turn on Google Calendar API` for the Google account that
you wish to track on [Google Calendar API's quickstart][2].

You should be able to download a file named `credentials.json` after you are
done. Place this file in this directory after you clone the project.

[pipenv][3] is used to create a virtualenv and install dependencies for this
project. Run `pipenv sync` to install the dependencies.

Once dependencies are installed, you can run the analyzer by running the follow command:

    python analyzer.py

On the first run, a new browser window / tab will open up for you to authorize
this script.

[2]: https://developers.google.com/calendar/quickstart/python
[3]: https://pipenv.readthedocs.io/en/latest/


## License

Apache license 2.0
