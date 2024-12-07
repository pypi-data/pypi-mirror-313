#!/bin/env python3

"""
to-do list manager
"""

from pathlib import Path
from os.path import join, isfile
from json import load, dump, JSONDecodeError
from sys import argv

HOME = str(Path.home())

todolist = join(HOME, ".todolist")


def load_file(path_to_load):
    """Load the list from a file"""
    list_elements = []
    if isfile(path_to_load):
        with open(path_to_load, "r", encoding="utf-8") as file:
            try:
                list_elements = load(file)
            except JSONDecodeError:
                print(f"Error with the file {todolist}")
    else:
        write_todolist(path_to_load, [])
    return list_elements


def write_todolist(todolist_path, list_elements):
    """Write list (as json) into file"""
    with open(todolist_path, "w", encoding="utf-8") as file:
        dump(list_elements, file, indent=4)


def print_question(questions, answers):
    """Print a question to the console and return the index of the answer"""
    print(questions)
    for idx, one_answer in enumerate(answers):
        print(f"{idx} - {one_answer}")
    res = input()
    try:
        index = int(res)
        if index < len(answers) and index >= 0:
            return index
    except ValueError:
        pass
    return None


def add_item(list_elements):
    """Add a new item to the list"""
    res = input("Enter the new item\n")
    list_elements.append(res)
    write_todolist(todolist, list_elements)
    return list_elements


def print_list(list_elements):
    """Print the list"""
    print("Your TODO list is :")
    for index_of_element, one_element in enumerate(list_elements):
        print(f"{index_of_element} - {one_element}")


def delete_item(list_of_task):
    """Delete an item of the list"""
    res = print_question("Which element to delete ?", [str(i) for i in list_of_task])
    if res is not None:
        if res < len(list_of_task):
            del list_of_task[res]
        else:
            print("Error: wrong index")
    write_todolist(todolist, list_of_task)
    return list_of_task


def main():
    """main function"""
    list_of_task = load_file(todolist)
    if "add" in argv:
        list_of_task = add_item(list_of_task)
        print_list(list_of_task)
    elif "del" in argv:
        list_of_task = delete_item(list_of_task)
        print_list(list_of_task)
    else:
        print_list(list_of_task)
