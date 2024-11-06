# Busy Tag Outlook Calendar Widget
## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)

## Introduction

The Outlook Calendar Widget is a Python-based application that fetches current and upcoming events from your Outlook Calendar and displays them on your Busy Tag device. The widget shows the current and next event's name, time, and category color, updating automatically every 20 seconds.
## Project Purpose

The main goal of this project is to:
	
- Integrate with the Microsoft Graph API to fetch calendar events.

- Display the current and upcoming calendar events on a Busy Tag device.

- Automatically update the display as events change in your Outlook Calendar.

## Prerequisites

To run this script, ensure you have the following installed:

- Python 3.6 or higher
- `imageio` , `Pillow` for image handling and rendering
- `requests` for API calls
- Microsoft 365 account with access to Outlook Calendar
- Spotify Client ID
- Spotify account

## Installation
 
  To get started with this Python script, follow these steps:

1. **Clone the repository:**
   First, clone the repository from GitHub to your local machine.
   ```
   git clone https://github.com/busy-tag/Outlook_Calendar_Widget.git
2. Navigate to the cloned repository:

	```
	cd Outlook_Calendar_Widget
	```
3. Install the required dependencies:
	Use `pip` to install the necessary packages.
	
	```
	pip install requests imageio pillow
	```

4. Ensure the default font file `MontserratBlack-3zOvZ.ttf` is in the project directory.

## Configuration

The script provides several customizable parameters:

• **Client ID and Secret:** You will need to configure your Microsoft Azure App's `Client ID`, `Client Secret`, and `Redirect URI` in the script or provide them when prompted.

• **Drive Letter:** Prompted input for the drive letter where the Busy Tag device is located (e.g., `D`).

• **Event Fetching:** The script fetches events from your Outlook Calendar and formats the display based on event data (subject, time, and category color).

## Usage
1. **Execute the script:**
You can run the script from the command line:
```
python main.py
```
2. **Provide Drive Letter:**
   
    Enter the drive letter assigned to the Busy Tag device (e.g., D) when prompted.
         
3. **Automatic Operation:**

	The widget will start fetching upcoming Outlook Calendar events, updating the Busy Tag device with event details (name, time, and category color).
	
4. **Calendar Selection:**
	
	Upon running the script, it will fetch available Outlook calendars for your account, and you will be prompted to select one for tracking events.
	
### Example

After running the script, you should see output similar to this in your terminal:
```
Enter the Busy Tag disk drive letter (e.g., D or E): D
Connected to Busy Tag device
Waiting for user authorization...
Authorization successful.
Select Calendar:
1. Calendar Name: Calendar
2. Calendar Name: Birthdays
3. Calendar Name: Work
Chosen Calendar: Calendar
Calendar tracking started
Updates every 20 seconds
To stop and exit press ctrl+c

Fetched 1 events:
Event: Christmas Event at 08:00 - 08:30, 2024-12-24
```
The Busy Tag device will display the current event and the upcoming event with relevant information like event name and start time.


Sample:

<img src="/event_sample_image.png" alt="Current Event Sample Image" width="300" height="390"/>

### Troubleshooting

If you encounter any issues, ensure:

All Python packages are installed correctly.

The font file (`MontserratBlack-3zOvZ.ttf`) is present in the project directory.

You have an active internet connection.

The drive letter is correct and the Busy Tag device is connected.

The Azure app's Client ID, Client Secret, and Redirect URI are properly configured in the script.

Your Microsoft 365 account has the necessary permissions to access Outlook Calendar.

If you are experiencing issues related to scheduling, meeting times, or event logging, please ensure that the time zone settings in your Outlook account match the system time zone on your device. Mismatched time zones can cause discrepancies in meeting schedules, reminders, and timestamps. 
