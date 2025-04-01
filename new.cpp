#include <iostream>
#include <stack>
#include <string>

using namespace std;

void addTask(stack<string>& tasks) {
    string task;
    cout << "Enter the task description: ";
    cin.ignore();  // Clear the buffer for string input
    getline(cin, task);  // Read the task with spaces
    tasks.push(task);  // Add the task to the stack
    cout << "Task added successfully!\n";
}

void viewTasks(const stack<string>& tasks) {
    if (tasks.empty()) {
        cout << "Your to-do list is empty!\n";
    } else {
        stack<string> temp = tasks;  // Create a temporary copy to display tasks
        int count = 1;
        cout << "Your tasks (from most recent to oldest):\n";
        while (!temp.empty()) {
            cout << count << ". " << temp.top() << endl;  // Display the top task
            temp.pop();  // Remove the top task from the temporary stack
            count++;
        }
    }
}

void deleteTask(stack<string>& tasks) {
    if (tasks.empty()) {
        cout << "No tasks to delete!\n";
    } else {
        cout << "Task \"" << tasks.top() << "\" deleted successfully!\n";
        tasks.pop();  // Remove the top task from the stack
    }
}

int main() {
    stack<string> tasks;  // Stack to store tasks
    int choice;

    do {
        // Display menu
        cout << "\n--- To-Do List Menu ---\n";
        cout << "1. Add a task\n";
        cout << "2. View all tasks\n";
        cout << "3. Delete most recent task\n";
        cout << "4. Exit\n";
        cout << "Enter your choice (1-4): ";
        cin >> choice;

        // Handle the user input
        switch (choice) {
            case 1:
                addTask(tasks);  // Add a task
                break;
            case 2:
                viewTasks(tasks);  // View all tasks
                break;
            case 3:
                deleteTask(tasks);  // Delete the most recent task
                break;
            case 4:
                cout << "Exiting the program...\n";
                break;
            default:
                cout << "Invalid choice! Please enter a number between 1 and 4.\n";
        }
    } while (choice != 4);

    return 0;
}
