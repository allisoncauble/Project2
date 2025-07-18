def read_course_file(filename):
    courses = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                course, section, days, start, end = parts
                courses.append({
                    "course": course,
                    "section": section,
                    "days": days,
                    "start": int(start),
                    "end": int(end)
                })
    return courses


def get_available_courses(sections):
    return sorted(set(section['course'] for section in sections))


def prompt_number_of_courses():
    while True:
        num = input("How many courses do you want to register for? ").strip()
        if num.isdigit() and int(num) > 0:
            return int(num)
        print(" Please enter a valid positive number.")


def prompt_course_numbers(n, available_courses):
    selected = set()
    print("\nAvailable Courses:")
    for c in available_courses:
        print("-", c)

    while len(selected) < n:
        course = input(f"Enter course #{len(selected)+1}: ").strip().upper()
        if course not in available_courses:
            print(" Invalid course number.")
        elif course in selected:
            print(" You've already entered that course.")
        else:
            selected.add(course)
    return list(selected)


def has_conflict(a, b):
    # Check overlapping days
    if not any(d in b["days"] for d in a["days"]):
        return False
    # Check time overlap
    return not (a["end"] <= b["start"] or b["end"] <= a["start"])


def find_schedules(sections, selected_courses):
    from itertools import product

    # Group sections by course
    by_course = {course: [] for course in selected_courses}
    for section in sections:
        if section['course'] in by_course:
            by_course[section['course']].append(section)

    all_combinations = list(product(*by_course.values()))
    valid_schedules = []

    for combo in all_combinations:
        conflict = False
        for i in range(len(combo)):
            for j in range(i + 1, len(combo)):
                if has_conflict(combo[i], combo[j]):
                    conflict = True
                    break
            if conflict:
                break
        if not conflict:
            valid_schedules.append(combo)

    return valid_schedules


def display_schedule(schedule):
    print("\n Final Schedule:")
    for s in schedule:
        start = f"{s['start']:04d}"
        end = f"{s['end']:04d}"
        print(f"{s['course']} {s['section']} | {s['days']} {start[:2]}:{start[2:]} - {end[:2]}:{end[2:]}")


def main():
    filename = "courses2.txt"  # make sure this file is in the same folder
    sections = read_course_file(filename)
    available = get_available_courses(sections)

    num = prompt_number_of_courses()
    selected = prompt_course_numbers(num, available)

    schedules = find_schedules(sections, selected)

    if not schedules:
        print("\n No conflict-free schedule found.")
    else:
        print(f"\ Found {len(schedules)} conflict-free schedule(s). Showing the first one:")
        display_schedule(schedules[0])


if __name__ == "__main__":
    main()
