import webbrowser
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs
import threading
import time
from datetime import datetime, timezone
from image_operations import create_zoned_image, draw_text_on_zoned_image
from calendar_utils import get_calendar_events, fetch_categories, get_calendar_list, select_calendar, hash_event
from utils import get_system_time, get_busy_tag_drive_letter, config_setup
from serial_operations import open_serial_connection, send_serial_command, close_serial_connection, find_busy_tag_device

CLIENT_ID = "1d591782-8137-48b2-9478-3ae9e34e8314"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "Calendars.Read User.Read offline_access openid profile"


class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        self.server.auth_code = params.get('code', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authorization successful. You can close this window.")

        threading.Thread(target=self.server.shutdown).start()


def authorize_user():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI,
    }

    auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(params)}"
    webbrowser.open(auth_url)

    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, AuthHandler)

    print("Waiting for user authorization...")

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    try:
        while server_thread.is_alive():
            server_thread.join(timeout=1)
    except KeyboardInterrupt:
        pass

    if hasattr(httpd, 'auth_code') and httpd.auth_code:
        print("Authorization successful.")
        return httpd.auth_code
    else:
        print("Authorization failed.")
        return None


def exchange_code_for_token(auth_code):
    token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'code': auth_code,
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error exchanging code for token: {response.status_code} {response.text}")
        return None


def main():
    drive_letter = get_busy_tag_drive_letter()
    port = find_busy_tag_device()
    config_setup(drive_letter)

    auth_code = authorize_user()
    if auth_code is None:
        print("Authorization failed.")
        return

    access_token = exchange_code_for_token(auth_code)
    if not access_token:
        print("Failed to obtain access token.")
        return
    
    calendars = get_calendar_list(access_token)
    chosen_calendar = select_calendar(calendars)

    if chosen_calendar:
        print(f"Chosen Calendar: {chosen_calendar.name}")

    category_mapping = fetch_categories(access_token)
    print("Calendar tracking started")
    print("Updates every 20 seconds")
    print("To stop and exit press ctrl+c \n")

    events = get_calendar_events(access_token, category_mapping, chosen_calendar.id)
    print(f"Fetched {len(events)} events:")
    
    for event in events:
        print(f"Event: {event.subject} at {event.start} - {event.end}, {event.start_date}")

    previous_first_event_hash = None
    previous_second_event_hash = None

    while True:
        local_timezone = datetime.now().astimezone().tzinfo
        local_now = datetime.now(local_timezone).replace(second=0, microsecond=0)

        events = get_calendar_events(access_token, category_mapping, chosen_calendar.id)

        first_event = None
        second_event = None

        if len(events) >= 1:
            first_event_start = datetime.fromisoformat(f"{events[0].start_date}T{events[0].start}").astimezone(local_timezone).replace(second=0, microsecond=0)
            first_event_end = datetime.fromisoformat(f"{events[0].start_date}T{events[0].end}").astimezone(local_timezone).replace(second=0, microsecond=0)

            if first_event_start <= local_now <= first_event_end:
                first_event = events[0]

            if first_event is None and len(events) > 0:
                second_event = events[0]
            elif first_event is not None and len(events) > 1:
                second_event = events[1]

        current_first_event_hash = hash_event(first_event)
        current_second_event_hash = hash_event(second_event)

        if (current_first_event_hash != previous_first_event_hash) or (current_second_event_hash != previous_second_event_hash):
            previous_first_event_hash = current_first_event_hash
            previous_second_event_hash = current_second_event_hash

            color1 = first_event.color_code if first_event else "#FFFFFF"
            color2 = second_event.color_code if second_event else "#FFFFFF"
            zoned_image = create_zoned_image(color1, color2)
            image_with_text = draw_text_on_zoned_image(zoned_image, local_now.strftime("%H:%M"), first_event, second_event)
            image_with_text.save(f"{drive_letter}://calendar_image.png")
            time.sleep(3.5)
            ser = open_serial_connection(port)
            time.sleep(0.5)
            send_serial_command(ser, 'AT+SP=calendar_image.png')
            time.sleep(0.1)

            serial_color_command = f'AT+SC=127,{color1.lstrip("#")}' if first_event else 'AT+SC=127,FFFFFF'
            send_serial_command(ser, serial_color_command)

            close_serial_connection(ser)
            print("Events changed!")
            if first_event:
                print(f"Current event: {first_event.subject}, time: {first_event.start} - {first_event.end}, date: {first_event.start_date}")
            else: 
                print(f"No current event")
            if second_event:
                print(f"Upcoming event: {second_event.subject}, time: {second_event.start} - {second_event.end}, date: {second_event.start_date}")
            else: 
                print(f"No upcoming event")
    
        time.sleep(20)

if __name__ == "__main__":
    main()