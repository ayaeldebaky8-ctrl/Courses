import json
import os
from collections import deque

FILE_NAME = "courses.json"


def load_courses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}


def save_courses(courses):
    with open(FILE_NAME, "w") as file:
        json.dump(courses, file, indent=4)


def add_course(courses):
    print("\n--- Add Course ---")

    code = input("Course code: ").strip().upper()

    if not code:
        print("Course code cannot be empty!")
        return

    if code in courses:
        print("Course already exists!")
        return

    name = input("Course name: ").strip()
    prerequisites = input(
        "Prerequisites (separate codes with commas, or leave empty): "
    ).strip()

    prereq_list = [
        p.strip().upper()
        for p in prerequisites.split(",")
        if p.strip()
    ]

    courses[code] = {
        "name": name,
        "prerequisites": prereq_list
    }

    save_courses(courses)
    print("Course added successfully!")


def display_courses(courses):
    print("\n--- All Courses ---")

    if not courses:
        print("No courses available.")
        return

    for code, info in courses.items():
        prereqs = info["prerequisites"]

        print(f"\nCode: {code}")
        print(f"Name: {info['name']}")
        print("Prerequisites:", ", ".join(prereqs) if prereqs else "None")


def find_cycle(graph):
    visited = set()
    current_path = []
    in_path = set()

    def dfs(node):
        visited.add(node)
        current_path.append(node)
        in_path.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                result = dfs(neighbor)
                if result:
                    return result

            elif neighbor in in_path:
                start = current_path.index(neighbor)
                return current_path[start:] + [neighbor]

        current_path.pop()
        in_path.remove(node)
        return None

    for node in graph:
        if node not in visited:
            result = dfs(node)
            if result:
                return result

    return None


def topological_sort(courses):
    print("\n--- Course Planner ---")

    if not courses:
        print("No courses available!")
        return

    graph = {code: [] for code in courses}
    indegree = {code: 0 for code in courses}

    # Build the graph
    for code, info in courses.items():
        for prereq in info["prerequisites"]:

            if prereq not in courses:
                print(f"Missing prerequisite: {prereq} for {code}")
                return

            graph[prereq].append(code)
            indegree[code] += 1

    # Kahn's Algorithm
    queue = deque(
        code for code in courses if indegree[code] == 0
    )

    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(order) != len(courses):
        cycle = find_cycle(graph)

        print("\nCycle detected!")
        if cycle:
            print("Cycle path:", " -> ".join(cycle))
        print("Cannot create a valid course order.")
        return

    print("\nRecommended Course Order:")

    for index, code in enumerate(order, start=1):
        print(f"{index}. {code} - {courses[code]['name']}")

    print("\nAll courses are ordered successfully!")


def main():
    courses = load_courses()

    while True:
        print("\n===== COURSE PLANNER =====")
        print("1. Add Course")
        print("2. Display Courses")
        print("3. Order Courses (Topological Sort)")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_course(courses)

        elif choice == "2":
            display_courses(courses)

        elif choice == "3":
            topological_sort(courses)

        elif choice == "4":
            print("Thank you for using Course Planner!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
