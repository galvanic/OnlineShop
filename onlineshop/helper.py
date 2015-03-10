# coding: utf-8

import os
import sys


def ask(question, rangeList=['y','yes','oui'], errorText='Enter another value.'):
    """
    Asks for and returns user's input.
    question:   string
    rangeList:  list of (acceptable) values
    errorText:  string

    If the user input isn't as expected, the function will loop and ask again.
    """
    if rangeList:
        rangeList = map(str, rangeList)
    while True:
        try:
            user = input('{} '.format(question))
            if not rangeList:
                return user
            elif user.lower() not in rangeList:
                raise ValueError
        except ValueError:
            print(errorText + '\n')
            continue
        break
    return user


def get_latest_file(directory, file_extension='txt'):
    """
    Returns a string with the filepath of the last modified file in
    the given directory.
    """
    filenames = ['{}{}'.format(directory, fn) for fn in os.listdir(directory)
        if fn[-3:] == file_extension]
    newest = max(filenames, key=lambda x: os.stat(x).st_mtime)
    return newest

