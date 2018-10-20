# Calendar Auditor

Calendar Auditor is my humble attempt at getting visibility into how my
calendar looks like over the past week(s).

You have time, you just need to [make time for time][1].

![Sample run of the Script](screenshot.png?raw=true "Script Output")


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

    cp sample.yaml config.yaml
    python analyzer.py

On the first run, a new browser window / tab will open up for you to authorize
this script.

## Configuring the Categories to Track

Copy `sample.yaml` to `config.yaml` if you have not. `config.yaml` is the default
file that the script will read to determine which events fall into which category.

Categories are defined in a YAML file, with the following format:

    <substring of event name on your Google Calendar>: Category name

For example, if you have a series of business meetings on your calendar with
the following format: "Meeting with A", "Meeting with B", you can track
these in a single category with the following:

    Meeting with: Business meetings

If you have certain events that you want to ignore, you can add the
substring of event names under the Ignore category.


## License

Apache license 2.0


[1]: https://hbr.org/2011/12/make-time-for-time.html
[2]: https://developers.google.com/calendar/quickstart/python
[3]: https://pipenv.readthedocs.io/en/latest/
