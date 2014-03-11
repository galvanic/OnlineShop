import sys

def ask(question, rangeList=["y","yes","oui"], errorText="Enter another value."):
    """
    Asks for and returns user's input. End program with "n".
    question:   string
    rangeList:  list of (acceptable) values
    errorText:  string
    
    Module with function which asks user for something.
    
    If the user input isn't as expected, the function will loop and ask again.
    
    The user gets the option of terminating the program
    or just continuing the program without being asked again:
    The ask function returns without returning the user input, ending the loop.
    
    However, the loop might continue depending on program architecture,
    or there might be a problem since "None" is returned in that case.
    """
    endprog = ["n", "no", "non", "end", "terminate", "finish", "0", "endprog"]
    endloop = ["endloop"]
    if rangeList:
        rangeList = map(str, rangeList)
    while True:
        try:
            user = input(question+" ")
            if user.lower() in endprog:
                sys.exit("End of program.")
            elif user.lower() in endloop:
                return
            # maybe give the option of changing ask when looking at rangeList ?
            # eg. lower() etc ?
            # can't remember what i meant by this ^
            elif not rangeList:
                return user
            elif user.lower() not in rangeList:
                raise ValueError
        except ValueError:
            print(errorText + "\n")
            continue
        break
    return user