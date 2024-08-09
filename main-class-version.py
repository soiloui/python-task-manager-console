import uuid
import inquirer
from task_types import Tasks
from utils.print_utils import print_success, print_error, print_neutral
from utils.file_utils import load_data_from_json_file, write_data_to_json_file, write_data_to_txt_file


class TaskManager:
    def __init__(self, json_file_path: str, txt_file_path: str):
        self.json_file_path = json_file_path
        self.txt_file_path = txt_file_path
        self.tasks = self.load_tasks()

    def load_tasks(self) -> Tasks | None:
        """Load tasks from the JSON file."""
        return load_data_from_json_file(self.json_file_path) or None

    def save_tasks(self) -> None:
        """Save the current list of tasks to files."""
        write_data_to_json_file(self.json_file_path, self.tasks)
        write_data_to_txt_file(self.txt_file_path, self.format_tasks_as_txt())

    def format_tasks_as_txt(self) -> str:
        """Format tasks as a string with one task per line."""
        return "\n".join(task['name'] for task in self.tasks)

    def view_tasks(self) -> None:
        """Display the list of tasks."""
        if not self.tasks:
            print_neutral("Tasks list is empty.")
            return

        task_choices = list(
            map(lambda task: (task["name"], task["ID"]), self.tasks))
        questions = [inquirer.List(
            'task', message="List of tasks", choices=task_choices)]
        inquirer.prompt(questions)

    def add_task(self) -> None:
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

        self.tasks.append(task)
        self.save_tasks()
        print_success("Task added successfully.")

    def remove_task(self) -> None:
        """Prompt user to select tasks to remove and remove them."""
        if not self.tasks:
            print_neutral("Tasks list is empty.")
            return

        task_choices = list(
            map(lambda task: (task["name"], task["ID"]), self.tasks))
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

        self.tasks = [task for task in self.tasks if task["ID"]
                      not in tasks_to_remove]
        self.save_tasks()
        print_success("Tasks removed successfully.")

    def remove_all_tasks(self) -> None:
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

        self.tasks = []
        self.save_tasks()
        print_success("All tasks removed successfully.")

    def exit_app(self) -> None:
        """Exit the program."""
        print_neutral("Bye!")
        exit()

    def run(self) -> None:
        """Run program until user exits."""
        possible_actions = [
            ("View tasks", self.view_tasks),
            ("Add task", self.add_task),
            ("Remove task", self.remove_task),
            ("Remove all tasks", self.remove_all_tasks),
            ("Exit", self.exit_app),
        ]

        inquirer_questions = [
            inquirer.List('action',
                          message="What do you want to do?",
                          choices=possible_actions,
                          ),
        ]

        while True:
            answers = inquirer.prompt(inquirer_questions)
            selected_action = answers["action"]
            selected_action()


def main() -> None:
    """Entry point of the program."""
    task_manager = TaskManager(
        json_file_path="./tasks.json", txt_file_path="./tasks.txt")
    task_manager.run()


if __name__ == '__main__':
    main()
