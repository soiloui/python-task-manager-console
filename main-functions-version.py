import uuid
import inquirer
from typing import Callable, List, Tuple
from task_types import Tasks
from utils.print_utils import print_success, print_error, print_neutral
from utils.file_utils import load_data_from_json_file, write_data_to_json_file, write_data_to_txt_file

JSON_FILE_PATH = "./tasks.json"
TXT_FILE_PATH = "./tasks.txt"


def format_tasks_as_txt(tasks: Tasks) -> str:
    """Format tasks as a string with one task per line."""
    return "\n".join(task['name'] for task in tasks)


def update_files(tasks: Tasks) -> None:
    """Update JSON and text files with the given tasks."""
    write_data_to_json_file(JSON_FILE_PATH, tasks)
    write_data_to_txt_file(TXT_FILE_PATH, format_tasks_as_txt(tasks))


def view_tasks() -> None:
    """Display list of tasks."""
    tasks = load_data_from_json_file(JSON_FILE_PATH)
    if not tasks:
        print_neutral("Tasks list is empty.")
        return

    task_choices = list(map(lambda task: (task["name"], task["ID"]), tasks))
    questions = [inquirer.List(
        'task', message="List of tasks", choices=task_choices,)]
    inquirer.prompt(questions)


def add_task() -> None:
    """Prompt user to enter a task name and add it to the tasks list."""
    task_name = input("Task name: ")
    if not task_name:
        print_error("Task name cannot be empty.")
        return

    task_ID = str(uuid.uuid4())
    task = {
        "ID": task_ID,
        "name": task_name,
    }

    tasks = load_data_from_json_file(JSON_FILE_PATH) or []
    tasks.append(task)
    update_files(tasks)
    print_success("Task added successfully.")


def remove_task() -> None:
    """Prompt user to select tasks to remove and remove them."""
    tasks = load_data_from_json_file(JSON_FILE_PATH)
    if not tasks:
        print_neutral("Tasks list is empty.")
        return

    task_choices = list(map(lambda task: (task["name"], task["ID"]), tasks))
    questions = [
        inquirer.Checkbox('tasks',
                          message="Which tasks do you want to remove?",
                          choices=task_choices,
                          ),
    ]
    answers = inquirer.prompt(questions)
    tasks_to_remove = answers["tasks"]
    if (not tasks_to_remove):
        print_neutral("No tasks were removed.")
        return

    updated_tasks = [task for task in tasks if task["ID"]
                     not in tasks_to_remove]

    update_files(updated_tasks)
    print_success("Tasks removed successfully.")


def remove_all_tasks() -> None:
    """Removes all tasks after confirmation."""
    questions = [
        inquirer.Confirm('delete_all',
                         message="Are you sure you want to delete all tasks?",
                         ),
    ]
    answers = inquirer.prompt(questions)
    should_delete_all = answers["delete_all"]

    if not should_delete_all:
        print_neutral("No tasks were removed.")
        return

    update_files([])
    print_success("All tasks removed successfully.")


def exit_app() -> None:
    """Exit the program."""
    print_neutral("Bye!")
    exit()


def get_user_action(possible_actions: List[Tuple[str, Callable]]) -> Callable:
    """Prompt user to select an action."""
    questions = [
        inquirer.List('action',
                      message="What do you want to do?",
                      choices=possible_actions,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["action"]


def user_input_loop() -> None:
    """Run program until user exits."""
    possible_actions = [
        ("View tasks", view_tasks),
        ("Add task", add_task),
        ("Remove task", remove_task),
        ("Remove all tasks", remove_all_tasks),
        ("Exit", exit_app),
    ]
    while True:
        selected_action = get_user_action(possible_actions)
        if selected_action:
            selected_action()
        else:
            print_error("Invalid action. Please select a valid action.")


def main() -> None:
    """Entry point of the program."""
    user_input_loop()


if __name__ == '__main__':
    main()
