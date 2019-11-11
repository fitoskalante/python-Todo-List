import os
import sqlite3
from termcolor import colored
from datetime import datetime
from tabulate import tabulate

# 6. Define root path
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

# 7. Define SQLITE conn & cur
conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()


date = datetime.now()

def setUser(login_email):

    sql = """ SELECT * FROM users 
    WHERE Email = ?
    """
    cur.execute(sql, (login_email,))
    users = cur.fetchall()
    if len(users) == 1:
        return users[0]

    elif len(users) == 0:
        print('Please enter a Username:')
        username = input()

        sql = """
        SELECT * FROM users
        WHERE Username = ?
        """
        cur.execute(sql, (username,))
        check_username = cur.fetchall()
        
        if len(check_username) == 1:
            print('Sorry! The Username is already taken.')
            setUser(login_email)

        sql = """ 
        INSERT INTO users 
        (Email, Username) 
        VALUES (?, ?)
        """
        cur.execute(sql, (login_email, username,))
        conn.commit()

        sql = """ 
        SELECT * FROM users 
        WHERE Email = ?
        """
        cur.execute(sql, (login_email,))
        recent_added_user = cur.fetchall()
        return recent_added_user[0]

def add_task(task, user_id, email, status):
    sql = """ INSERT INTO todos (Task, Due_Date, User_Id, Email, Status)
    VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(sql, (task, date, user_id, email, status,))
    conn.commit()
    show_my_list(user_id)
    print('Great! Task added to your list')

def delete_todo(task_id, user_id):
    sql = """ DELETE FROM todos WHERE id = ?"""
    cur.execute(sql, (task_id,))
    conn.commit()
    show_my_list(user_id)
    print('The task was deleted.')

def mark_as_completed(completed_task_id, user_id):
    sql = """ UPDATE todos SET Status = 'completed' WHERE id = ?"""
    cur.execute(sql, (completed_task_id,))
    conn.commit()
    show_my_list(user_id)
    print('task completed')

def mark_as_incomplete(incomplete_task_id, user_id):
    sql = """ UPDATE todos SET Status = 'incomplete' WHERE id = ?"""
    cur.execute(sql, (incomplete_task_id,))
    conn.commit()
    show_my_list(user_id)
    print('task marked as incomplete')

def show_my_list(user_id):
    sql = """ 
    SELECT * FROM todos 
    WHERE User_Id = ?
    """
    cur.execute(sql, (user_id,))
    results = cur.fetchall()
    print(tabulate(
        results,
        headers=[colored('Id', 'yellow'),
                 colored('Task', 'yellow'),
                 colored('Date', 'yellow'),
                 colored('User Id', 'yellow'),
                 colored('Email', 'yellow'),
                 colored('Status', 'yellow')],
        tablefmt='orgtbl'))

def show_full_list():
    sql = """ SELECT * FROM todos """
    cur.execute(sql)
    results = cur.fetchall()
    print(tabulate(
        results,
        headers=[colored('Id', 'yellow'),
                 colored('Task', 'yellow'),
                 colored('Date', 'yellow'),
                 colored('User Id', 'yellow'),
                 colored('Email', 'yellow'),
                 colored('Status', 'yellow')],
        tablefmt='orgtbl'))

def show_full_list_sorted_by_status_completed():
    sql = """
    SELECT * FROM todos 
    WHERE status = "completed"
    """
    cur.execute(sql)
    results = cur.fetchall()
    print(tabulate(
        results,
        headers=[colored('Id', 'yellow'),
                 colored('Task', 'yellow'),
                 colored('Date', 'yellow'),
                 colored('User Id', 'yellow'),
                 colored('Email', 'yellow'),
                 colored('Status', 'yellow')],
        tablefmt='orgtbl'))

def show_full_list_sorted_by_status_incomplete():
    sql = """
    SELECT * FROM todos 
    WHERE status = "incomplete"
    """
    cur.execute(sql)
    results = cur.fetchall()
    print(tabulate(
        results,
        headers=[colored('Id', 'yellow'),
                 colored('Task', 'yellow'),
                 colored('Date', 'yellow'),
                 colored('User Id', 'yellow'),
                 colored('Email', 'yellow'),
                 colored('Status', 'yellow')],
        tablefmt='orgtbl'))

def show_full_list_sorted_by_most_recent():
    sql = """
    SELECT * FROM todos 
    ORDER BY Due_Date DESC
    """
    cur.execute(sql)
    results = cur.fetchall()
    print(tabulate(
        results,
        headers=[colored('Id', 'yellow'),
                 colored('Task', 'yellow'),
                 colored('Date', 'yellow'),
                 colored('User Id', 'yellow'),
                 colored('Email', 'yellow'),
                 colored('Status', 'yellow')],
        tablefmt='orgtbl'))

command_list = [
    ['a', 'Add a new task'], 
    ['d', 'Delete a task'], 
    ['c', 'Mark as completed'], 
    ['i', 'Mark as incomplete'],
    ['f', 'See full list'],
    ['fi', 'Sort full list by status incomplete'],
    ['fc', 'Sort full list by status completed'],
    ['fc', 'Sort full list by status completed'],
    ['r', 'Sort full list by most recent']
    ] 
    
def shortcuts(): 
    print(tabulate(
    command_list,
    headers=[colored('Shortcut', 'green'),
                colored('Action', 'green')],
    tablefmt='orgtbl'))

if __name__ == '__main__':
    try:
        print("Please Login using your email")
        login_email = input()
        current_user = setUser(login_email)
        username = current_user[2]
        email = current_user[1]
        user_id = current_user[0]

        while True:
            shortcuts()
            print('Hi ' + username +  ', What do you want to do?')
            choice = input()
            if choice == 'a':
                print("Enter a new task to your list:")
                task = input()
                status = 'incomplete'
                add_task(task, user_id, email, status)

            if choice == 'd':
                print("Enter the id of the task you want to delete:")
                task_id = input()
                delete_todo(task_id, user_id)

            if choice == "c":
                print("Enter the id of the task you have completed:")
                completed_task_id = input()
                mark_as_completed(completed_task_id, user_id)

            if choice == "i":
                print("Enter the id of the task you want to mark us incomplete:")
                incomplete_task_id = input()
                mark_as_incomplete(incomplete_task_id, user_id)

            if choice == "l":
                show_my_list(user_id)

            if choice == "f":
                show_full_list()

            if choice == "fc":
                show_full_list_sorted_by_status_completed()
            
            if choice == "fi":
                show_full_list_sorted_by_status_incomplete()

            if choice == "r":
                show_full_list_sorted_by_most_recent()

    except IndexError:
        print('error')
