#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : BOTIN POV                                      |
#  | EMAIL: botin.pov@gmail.com                            |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 10.8.2023.                                   |
#  +-------------------------------------------------------+

from datetime import datetime, timedelta


def timestampToDatetime(timeStamp):
    try:
        if not timeStamp:
            return ''
        timestamp_str = str(timeStamp)
        timestamp = int(timestamp_str) / 1000
        timestamp_datetime = datetime.fromtimestamp(timestamp) # Use datetime.fromtimestamp
        formatted_datetime = timestamp_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z') # Format according to ISO 8601

        return formatted_datetime
    except Exception as e:
        raise Exception("An error occurred:", str(e))


def calculateProcessingTime(start_created_at, log):
    try:
        if not start_created_at or not (len(log) > 0):
            return None
        start_time = datetime.fromisoformat(str(start_created_at))
        previous_date = start_time

        for entry in log:
            current_date = datetime.fromisoformat(entry["date"])
            time_difference = current_date - previous_date
            days = time_difference.days
            hours = (time_difference.seconds // 3600) % 24
            minutes = (time_difference.seconds // 60) % 60
            # seconds = time_difference.seconds % 60
            entry["processing_time"] = f"{days} Days, {hours} Hours, {minutes} Minutes"
            previous_date = current_date

        return log
    except Exception as e:
        raise Exception("An error occurred:", str(e))


def totalProcessingTime(start_created_at, log):
    try:
        logs = log if log else []
        if not start_created_at or not (len(logs) > 0):
            return f"{0} Days, {0} Hours, {0} Minutes"

        start_time = datetime.fromisoformat(str(start_created_at))
        previous_date = start_time
        total_time = timedelta()

        for entry in logs:
            current_date = datetime.fromisoformat(entry["date"])
            time_difference = current_date - previous_date
            total_time += time_difference
            previous_date = current_date

        days = total_time.days
        hours = (total_time.seconds // 3600) % 24
        minutes = (total_time.seconds // 60) % 60

        total_time_str = f"{days} Days, {hours} Hours, {minutes} Minutes"
        return total_time_str
    except Exception as e:
        raise Exception("An error occurred:", str(e))
