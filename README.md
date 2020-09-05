# expense-manager
A expense manager to add daily expenses, alerts if expense exceeds the set limit, generate weekly reports and can be saved and loaded locally. Written in python

How to run?

1.	Tested on Python 3.7.4 windows 10 environment.
a.	Download it form here - https://www.python.org/downloads/release/python-374/
b.	Refer - https://www.youtube.com/watch?v=4Rx_JRkwAjY
2.	To run execute this command in cmd, in same directory where the python file is present.
python expense_manager.py
3. The JSON files contains my previously saved expense data. No need to download them.  
Features
1.	 Add an item
a.	You can add an item and its cost for any day.
b.	Not limited to today or the system’s date.
c.	To add expense for a past of future date just mention the date in YYYY-MM-DD format.
d.	Start of week is calculated at runtime. Start of week is the latest day for which at least one expense is provided.
e.	After adding an item, if it exceeds the weekly limit a warning is shown to the user.

2.	Weekly report
a.	Report is generated for “n” week in past with respect to the latest date provided.
b.	Report includes
i.	Week number in past
ii.	Week duration 
iii.	 Daily totals
iv.	Weekly totals

3.	Update weekly limit

4.	Save data to JSON file
a.	Even after you close the program you can save your data locally.
b.	It means next time when you start the program you can start from where you left. No need to again feed all previous expenses.
c.	Just click option 4 before exiting the program.
d.	It overwrites the data not updates it.

5.	Read previously saved data.
a.	If you want to load previous expense then simply click on 5.
b.	Now the state of program is same as how you left.

6.	Exit 
