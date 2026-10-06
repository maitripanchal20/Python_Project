import json

# =====================================================
# BACKEND - STUDENT STUDY PLANNER
# =====================================================

tasks = []


# =====================================================
# FILE HANDLING
# =====================================================

def save_data():
    with open("study_tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


def load_data():
    global tasks

    try:
        with open("study_tasks.json", "r") as file:
            tasks = json.load(file)

    except:
        tasks = []


# =====================================================
# TIME SORTING
# =====================================================

def time_to_minutes(time_text):

    try:
        time_text = time_text.strip().upper()

        # Example: 8:00 AM / 1:00 PM
        if "AM" in time_text or "PM" in time_text:

            parts = time_text.replace("AM", "").replace("PM", "").strip()

            hour, minute = parts.split(":")

            hour = int(hour)
            minute = int(minute)

            if hour < 1 or hour > 12:
                return None

            if minute < 0 or minute > 59:
                return None

            if "PM" in time_text and hour != 12:
                hour += 12

            if "AM" in time_text and hour == 12:
                hour = 0

            return hour * 60 + minute

        # Example: 08:00
        else:

            hour, minute = time_text.split(":")

            hour = int(hour)
            minute = int(minute)

            if hour < 0 or hour > 23:
                return None

            if minute < 0 or minute > 59:
                return None

            return hour * 60 + minute

    except:
        return None


# =====================================================
# DURATION TO MINUTES
# =====================================================

def duration_to_minutes(duration_text):

    try:

        duration_text = duration_text.strip().lower()

        # Example: 2 hours
        if "hour" in duration_text:

            number = float(
                duration_text
                .replace("hours", "")
                .replace("hour", "")
                .strip()
            )

            return int(number * 60)

        # Example: 2 h
        elif "h" in duration_text:

            number = float(
                duration_text
                .replace("h", "")
                .strip()
            )

            return int(number * 60)

        # Example: 90 minutes
        elif "minute" in duration_text:

            number = float(
                duration_text
                .replace("minutes", "")
                .replace("minute", "")
                .strip()
            )

            return int(number)

        # Example: 90 min
        elif "min" in duration_text:

            number = float(
                duration_text
                .replace("min", "")
                .strip()
            )

            return int(number)

        # If only number is entered,
        # consider it as hours
        else:

            number = float(duration_text)

            return int(number * 60)

    except:
        return None


# =====================================================
# MINUTES TO DISPLAY TIME
# =====================================================

def minutes_to_time(total_minutes):

    total_minutes = total_minutes % 1440

    hour = total_minutes // 60
    minute = total_minutes % 60

    if hour == 0:

        display_hour = 12
        period = "AM"

    elif hour < 12:

        display_hour = hour
        period = "AM"

    elif hour == 12:

        display_hour = 12
        period = "PM"

    else:

        display_hour = hour - 12
        period = "PM"

    return f"{display_hour}:{minute:02d} {period}"


# =====================================================
# SORT TASKS
# =====================================================

def sort_tasks():

    tasks.sort(
        key=lambda task:
        time_to_minutes(task["time"])
        if time_to_minutes(task["time"]) is not None
        else 9999
    )


# =====================================================
# CHECK TIME CONFLICT
# =====================================================

def check_time_conflict(new_time, new_duration):

    new_start = time_to_minutes(new_time)

    if new_start is None:

        return (
            "Invalid study time.\n\n"
            "Please enter time like 1:00 PM."
        )

    new_duration_minutes = duration_to_minutes(new_duration)

    if new_duration_minutes is None or new_duration_minutes <= 0:

        return (
            "Invalid duration.\n\n"
            "Please enter duration like 2 hours "
            "or 90 minutes."
        )

    new_end = new_start + new_duration_minutes

    # Check against every existing task
    for task in tasks:

        existing_start = time_to_minutes(task["time"])
        existing_duration = duration_to_minutes(
            task["duration"]
        )

        if existing_start is None:
            continue

        if existing_duration is None:
            continue

        existing_end = (
            existing_start + existing_duration
        )

        # Check overlap
        if (
            new_start < existing_end
            and new_end > existing_start
        ):

            existing_end_time = minutes_to_time(
                existing_end
            )

            return (
                "Time Conflict!\n\n"
                f'"{task["subject"]}" is already scheduled '
                f'from {task["time"]} to {existing_end_time}.\n\n'
                f'Please choose a time at or after '
                f'{existing_end_time}.'
            )

    return None


# =====================================================
# GET TASK INFORMATION
# =====================================================

def get_counts():

    total = len(tasks)

    completed = 0

    for task in tasks:

        if task["status"] == "Completed":
            completed += 1

    pending = total - completed

    if total > 0:
        percentage = (completed / total) * 100
    else:
        percentage = 0

    return total, completed, pending, percentage


# =====================================================
# ADD TASK
# =====================================================

def add_task(subject, time, duration):

    # Check for invalid time or overlapping task
    conflict_message = check_time_conflict(
        time,
        duration
    )

    if conflict_message:

        return False, conflict_message

    task = {
        "subject": subject,
        "time": time,
        "duration": duration,
        "status": "Pending"
    }

    tasks.append(task)

    # Sort according to time
    sort_tasks()

    save_data()

    return True, ""


# =====================================================
# CHANGE TASK STATUS
# =====================================================

def change_status(index):

    if tasks[index]["status"] == "Pending":

        tasks[index]["status"] = "Completed"

    else:

        tasks[index]["status"] = "Pending"

    save_data()


# =====================================================
# DELETE TASK
# =====================================================

def delete_task(index):

    tasks.pop(index)

    save_data()


# =====================================================
# GET ALL TASKS
# =====================================================

def get_tasks():

    sort_tasks()

    return tasks