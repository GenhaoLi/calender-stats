import os
from typing import TypedDict
import logging
from datetime import timedelta, datetime

from icalendar import Calendar
from dotenv import load_dotenv

from calendar_stats.utils import download_to_local
from calendar_stats.utils import format_timedelta, truncate_time_zone, target_event_group_file_name
from calendar_stats.utils import config_logger
from calendar_stats.utils import data_dir

from calendar_stats.constants import TARGET_EVENT_GROUP_NAME, FROM_TIME


logger = config_logger()


class CalendarEvent(TypedDict):
    summary: str
    start_time: datetime
    end_time: datetime


class EventGroup:
    def __init__(self, first_event: CalendarEvent):
        self.summary = first_event['summary']
        self.events = [first_event]
        self.total_time = timedelta()  # initialize to 0

    def add_event(self, new_event: CalendarEvent):
        # ignore events that have not ended yet
        now = datetime.now()
        if datetime.strptime(FROM_TIME, '%Y-%m-%d %H:%M') < new_event['end_time'] < now:
            self.events.append(new_event)
            self.total_time += new_event['end_time'] - new_event['start_time']

    def print_total_time(self, logging_level=logging.DEBUG):
        logger.log(logging_level, f"[Event group]: \t{self.summary}\n"
                                  f"[Total time]: \t{format_timedelta(self.total_time)}\n")

    def print_events(self, logging_level=logging.INFO):
        # sort events by start time
        self.events.sort(key=lambda e: e['start_time'])
        logger.log(logging_level, f'--- Events: {self.summary} ---')
        for event in self.events:
            logger.log(logging_level,
                       # f"[Event]: \t{event['summary']}\n"
                       f"[Start]: \t{event['start_time']}\n"
                       f"[End]: \t\t{event['end_time']}\n"
                       )


def get_all_calendar_events(file_path):
    all_events = []
    with open(file_path, 'rb') as f:
        cal: Calendar = Calendar.from_ical(f.read())
        for component in cal.walk():
            if component.name == "VEVENT":
                event: CalendarEvent = {
                    'summary': str(component.get('summary', "")),
                    'start_time': truncate_time_zone(component.get('dtstart').dt),
                    'end_time': truncate_time_zone(component.get('dtend').dt)
                }
                all_events.append(event)
    return all_events


def group_events_by_summary(all_events: list[CalendarEvent]):
    event_groups: dict[str, EventGroup] = {}
    for event in all_events:
        summary = event['summary']
        if summary not in event_groups:
            event_groups[summary] = EventGroup(event)
        event_groups[summary].add_event(event)
    return event_groups


def sort_event_groups_by_total_time(groups: list[EventGroup]):
    return list(sorted(groups, key=lambda group: group.total_time, reverse=True))


def export_events_to_csv(events: list[CalendarEvent], export_path: str = None):
    # events do not have to have the same name (summary)
    total_time = sum([event['end_time'] - event['start_time'] for event in events], timedelta())

    if not export_path:
        export_path = f'{data_dir}/exported_events.csv'
    with open(export_path, 'w') as f:
        f.write("Event,Start,End,Duration (hh:mm:ss)\n")
        for event in events:
            f.write(f"{event['summary']},"
                    f"{event['start_time']},"
                    f"{event['end_time']},"
                    f"{event['end_time'] - event['start_time']}\n")

        # add a row for the total time
        # total_time is a timedelta object, so we need to convert it to a string in the format hh:mm:ss
        total_time = format_timedelta(total_time)
        f.write(f"Total time,"
                f","
                f","
                f"{total_time}\n")


def main():
    load_dotenv()
    cal_url = os.getenv('CALENDAR_URL')
    ics_file_path = download_to_local(cal_url)

    # Parse the .ics file
    my_all_events = get_all_calendar_events(ics_file_path)
    event_group_dict = group_events_by_summary(my_all_events)
    sorted_groups = sort_event_groups_by_total_time(list(event_group_dict.values()))

    # Print the total time spent on each event type
    for group in sorted_groups:
        group.print_total_time()

    # Print all events in the 'Work' group
    work_event_group = event_group_dict[TARGET_EVENT_GROUP_NAME]
    work_event_group.print_total_time(logging_level=logging.INFO)
    work_event_group.print_events()
    export_events_to_csv(work_event_group.events, f'{data_dir}/{target_event_group_file_name}.csv')

    # breakpoint()


if __name__ == "__main__":
    main()
