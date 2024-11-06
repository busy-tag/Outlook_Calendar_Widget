import requests
from color_mapping import PRESET_COLOR_MAPPING
from Event import Event
from OutlookCalendar import OutlookCalendar
from datetime import datetime
import pytz
import hashlib

def get_calendar_list(access_token):
    url = "https://graph.microsoft.com/v1.0/me/calendars"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        calendars_data = response.json().get('value', [])
        calendars = []

        for calendar_data in calendars_data:
            name = calendar_data.get('name')
            color = calendar_data.get('color', 'unknown')
            hex_color = calendar_data.get('hexColor', 'unknown')
            owner = calendar_data.get('owner', {})
            owner_name = owner.get('name', 'unknown')
            owner_address = owner.get('address', 'unknown')
            calendar_id = calendar_data.get('id')

            calendar = OutlookCalendar(name, color, hex_color, owner_name, owner_address, calendar_id)
            calendars.append(calendar)

        return calendars
    else:
        print(f"Error fetching calendars: {response.status_code} {response.text}")
        return []

def select_calendar(calendars):
    if calendars:
        print("Select Calendar:")
        for i, calendar in enumerate(calendars):
            print(f"{i + 1}. Calendar Name: {calendar.name}")
        
        while True:
            try:
                selection = int(input("Enter the number of the calendar you want to select: "))
                
                if 1 <= selection <= len(calendars):
                    chosen_calendar = calendars[selection - 1]
                    return chosen_calendar
                else:
                    print(f"Please enter a number between 1 and {len(calendars)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:
        print("No calendars found.")
        return None

def fetch_categories(access_token):
    url = "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        categories_data = response.json().get('value', [])
        category_mapping = {}
        
        for category in categories_data:
            display_name = category.get('displayName')
            color = category.get('color')
            if display_name and color:
                category_mapping[display_name] = color
                
        return category_mapping
    else:
        print(f"Error fetching categories: {response.status_code} {response.text}")
        return {}

def filter_events(events):
    now = datetime.now()
    upcoming_events = []

    for event in events:
        start_datetime = datetime.fromisoformat(event.start_date + 'T' + event.start)
        end_datetime = datetime.fromisoformat(event.start_date + 'T' + event.end)

        if start_datetime <= now <= end_datetime:
            upcoming_events.append(event)
        elif start_datetime > now: 
            upcoming_events.append(event)

    return upcoming_events

def hash_event(event):
    if not event:
        return None
    
    event_string = f"{event.subject}|{event.start}|{event.end}|{event.start_date}|{event.color_code}"
    return hashlib.sha256(event_string.encode('utf-8')).hexdigest()

def get_calendar_events(access_token, category_mapping, calendar_id, default_color = '#FFFFFF'):
    url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events_data = response.json().get('value', [])
        events = []

        local_timezone = datetime.now().astimezone().tzinfo

        for event_data in events_data:
            event_id = event_data.get('id')
            subject = event_data.get('subject')

            start_time_str = event_data.get('start').get('dateTime')
            end_time_str = event_data.get('end').get('dateTime')
            time_zone = event_data.get('start').get('timeZone', 'UTC')
            
            start_datetime = datetime.fromisoformat(start_time_str)
            end_datetime = datetime.fromisoformat(end_time_str)

            if start_datetime.tzinfo is None:
                start_datetime = start_datetime.replace(tzinfo=pytz.UTC)
            if end_datetime.tzinfo is None:
                end_datetime = end_datetime.replace(tzinfo=pytz.UTC)

            start_datetime_local = start_datetime.astimezone(local_timezone)
            end_datetime_local = end_datetime.astimezone(local_timezone)

            start_time = start_datetime_local.strftime("%H:%M")
            end_time = end_datetime_local.strftime("%H:%M")
            start_date = start_datetime_local.strftime("%Y-%m-%d")

            categories = event_data.get('categories', [])
            color = None
            color_code = None

            if categories:
                for category in categories:
                    if category in category_mapping:
                        color = category_mapping[category]
                        color_code = PRESET_COLOR_MAPPING.get(color, default_color)
                        break

            if color is None:
                color_code = default_color

            event = Event(event_id, subject, start_time, start_date, end_time, categories, color=color, color_code=color_code)
            events.append(event)

        events.sort(key=lambda event: datetime.fromisoformat(event.start_date + 'T' + event.start))

        upcoming_events = filter_events(events)

        return upcoming_events
    else:
        print(f"Error fetching calendar events: {response.status_code} {response.text}")
        return []