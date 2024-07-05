# Calendar Stats

This project analyzes calendar data to compute statistics such as total time spent on specific events,
and export event details to CSV files.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd calendar_stats
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Create a .env file in the root directory with the following content:
   ```bash
   CALENDAR_URL=<your-calendar-url>
   ```
   
## Usage

Run the main script to download the calendar data, process events, and generate statistics:
```bash
poetry run calendar_stats
```

Output:
- Console Logging: Logs are generated in the console with event details and total time spent.
- Data Files: CSV files are generated in directory `data` with detailed event information.

## Project Structure

```bash
.
├── README.md               # This file
├── calendar_stats
│   ├── __init__.py
│   ├── constants.py        # Defines constants like TARGET_EVENT_GROUP_NAME
│   ├── main.py             # Main script to process calendar events
│   └── utils.py            # Utility functions for file handling, logging, and datetime operations
├── data
│   ├── (gitignored) Work_till_2024-07-05 03:06.csv   # Exported CSV file with work event details
│   ├── (gitignored) Work_till_2024-07-05 03:06.txt   # Logging file for work event group
│   ├── (gitignored) calendar.ics        # Downloaded calendar file
│   └── (gitignored) debug_2024-07-05 03:06.log      # Debug logging file
├── .env                    # Calendar URL should be stored here
├── poetry.lock
└── pyproject.toml          # Poetry configuration file
```

