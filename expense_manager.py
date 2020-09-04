from collections import defaultdict
import datetime as dt
import json
import os


expenses = {}
MAX_LIMIT_PER_WEEK = None 
weekOfDay = defaultdict(int) # key->date, value-> week number
weekAndExpense = defaultdict(int) # key->weekNumber, value-> TotalExpenseThatWeek 
latestDate = None


def updateLimit():
    global MAX_LIMIT_PER_WEEK
    try:
        print("The current limit per week is", MAX_LIMIT_PER_WEEK)
        MAX_LIMIT_PER_WEEK = int(input("\nEnter new limit"))
    except ValueError:
        print("Enter a number!")

    print("Limit updated successfully")
    


def report():
    n = int(input("Enter the number of weeks in past about which you want report\n"))
    endOfWeek = latestDate

    if endOfWeek!=None:
        for currentWeekNumber in range(1, n+1): # each week
            print("\nWeek number", currentWeekNumber)
            startOfWeek = endOfWeek - dt.timedelta(days=6)

            print("Week Duration-\tFROM:", startOfWeek, "To:",endOfWeek)
            endOfWeek = startOfWeek
            
            print("Daily Totals are -")
            for date, weekNumber in weekOfDay.items():
                if weekNumber == currentWeekNumber:
                    print("\tFor date:", date,"Total expenditure:", sum( expenses[date].values() ) )

            print("Weekly Total is", weekAndExpense[currentWeekNumber])
    else:
        print("None Found!")

    

def calculateWeekNumber(dates):
    global weekAndExpense
    global weekOfDay
    global latestDate

    weekAndExpense.clear()
    weekOfDay.clear()
    
    # dates are now a string so we convert them all to dates
    try:
        date_format = "%Y-%m-%d"
        convertStringToDate = lambda x: dt.datetime.strptime(x, date_format).date()
        dates = list(map( convertStringToDate, dates ))
    except ValueError:
        print("Date entered is invalid")
        return
    # finding latest date 
    latestDate = max(dates)
    print(latestDate)

    # marking week number for all dates

    # finding number of days of past my latest date
    for date in dates:
        weekOfDay[ str(date) ] = (latestDate - date).days
        weekOfDay[ str(date) ] = ( weekOfDay[ str(date) ] // 7 ) +1 

    for date, weekNumber in weekOfDay.items():
        weekAndExpense[weekNumber] += sum( expenses[str(date)].values() )

    return weekOfDay, weekAndExpense



def prettyPrint(nested_dict):
    print("\nDate \t item \t expenditure ")
    for dates in nested_dict.keys():
        print( dates )
        for items in nested_dict[dates]:
            print("\t", str(items),"\t" ,nested_dict[dates][items])



def addItem():
    item, value = input("Enter item name <space> value \n").split()

    try:
        value = int(value)
    except ValueError:
        print("Enter a number! \n")
        return

    date = input("Enter date of purchase in yyyy-mm-dd or leave empty for today's date\n")

    try:
        if date == "":
            date = str( dt.date.today() )
        else:
            date_format = "%Y-%m-%d"
            date = str( dt.datetime.strptime(date, date_format).date() )
        if date not in expenses:
            expenses[date] = defaultdict(int) # by default put price of all item to 0
    except ValueError:
        print("Enter date in valid format")
        return

    expenses[date][item]  += value

    try:
        weekOfDay, weekAndExpense = calculateWeekNumber(expenses.keys())
    except:
        print("Wrongly formatted")
        return

    thisDateExpense = weekAndExpense[ weekOfDay[date] ]
    if thisDateExpense > MAX_LIMIT_PER_WEEK:
        print("\n!!!! WARNING WARNING !!!!")
        print("Your expense for week", weekOfDay[date],"is",thisDateExpense, "and it has crossed limit" ,MAX_LIMIT_PER_WEEK)
    prettyPrint(expenses)



def generatePath(filename):
    return os.path.join( os.path.dirname(os.path.abspath(__file__)) , filename)

def jsonDump():
    filename = "expenses.json"
    dirPath = generatePath(filename)
    json.dump(expenses, open(dirPath, 'w') )
    
    filename = "weekOfDay.json"
    dirPath = generatePath(filename)
    json.dump(weekOfDay, open(dirPath, 'w') )

    filename = "weekAndExpense.json"
    dirPath = generatePath(filename)
    json.dump(weekAndExpense, open(dirPath, 'w') )

    # not 
    filename = "latestDate.json"
    dirPath = generatePath(filename)
    json.dump({"latestDate":str(latestDate) } , open(dirPath, 'w') )

    print("All data sucessfully saved")

    

def jsonLoad():
    global expenses
    global weekOfDay
    global weekAndExpense
    global latestDate

    try:
        filename = "expenses.json"
        dirPath = generatePath(filename)
        expenses = json.load(open(dirPath))
        
        filename = "weekOfDay.json"
        dirPath = generatePath(filename)
        weekOfDay = json.load(open(dirPath))
        weekOfDay = defaultdict(int, weekOfDay)

        filename = "weekAndExpense.json"
        dirPath = generatePath(filename)
        weekAndExpense = json.load(open(dirPath))

        weekAndExpense = {int(weekNumber) : int(weekExpense)   for weekNumber, weekExpense in weekAndExpense.items() }
        weekAndExpense = defaultdict(int, weekAndExpense)

        filename = "latestDate.json"
        dirPath = generatePath(filename)
        latestDate = json.load(open(dirPath))
        latestDate = latestDate["latestDate"]

        latestDate = dt.datetime.strptime(latestDate, "%Y-%m-%d").date()
        # latestDate = defaultdict(int, weekAndExpense)
    except FileNotFoundError:
        print("First save the data to read")
    else:
        print("All data successfully loaded")
    

def main(): # driver function
    global MAX_LIMIT_PER_WEEK
    user = input("Please enter your good name \n")
    user = user.title() # convert to title case

    MAX_LIMIT_PER_WEEK = int(input("Please enter the Maximum expense limit for a week\n"))

    print("Hello "+ user + " what would you like to do today ?")

    requestStatement = """
    Press
    1 For add an item
    2 For weekly report
    3 To update the maximum warning limit 
    4 Save all the expense data to a JSON file 
    5 Read previously saved JSON file
    0 To exit\n
    """

    userInput = None #random value to initialize

    while userInput != 0:
        
        while True:
            try:
                userInput = int(input( requestStatement ))       
            except ValueError:
                print("Not an integer!")
                continue
            if userInput not in range(0, 6):
                print("Invalid choice!")
            else:
                break 

        if userInput == 1:
            addItem()

        elif userInput == 2:
            report()

        elif userInput == 3:
            updateLimit()

        elif userInput == 4:
            jsonDump()

        elif userInput == 5:
            jsonLoad()

if __name__ == "__main__" :
    main()
