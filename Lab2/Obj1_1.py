"""
Create a list of "AT" commands. It should include "AT", "AT+IMME1", "AT+NOTI1", "AT+ROLE1". 
These just "happen" to be the commands used to set up BLE connection!
Create a for loop that loops over each command and prints it to the console.
Create a seperate list of strings that has the following in order
: "CONNECTION FAILURE", "BANANAS", "CONNECTION SUCCESS", "APPLES"
Assign the value "SUCCESS" to a variable called text.
Test the following logic statements: 

Are these comparing the whole string, or character by character?
Make a while loop that loops over the list from step 3. Print each word 
unless it contains the string from step 4, in which case you should exit the loop and print: "This worked!"
"""
LIST = ["AT", "AT+IMME1", "AT+NOTI1", "AT+ROLE1"]
for x in LIST:
    print(x)

list1 = ["CONNECTION FAILURE", "BANANAS", "CONNECTION SUCCESS", "APPLES"]
text = "SUCCESS"
if "SUCCESS" in "SUCCESS":
    print("1")
if "SUCCESS" in "ijoisafjoijiojSUCCESS":
    print("2")
if "SUCCESS" == "ijoisafjoijiojSUCCESS":
    print("3")
if "SUCCESS" == text:
    print("4")
#they are comparing character by character

i = 0
while 1:
    if text in list1[i]:
        print("This worked!")
        break
    else:
        print(list1[i])
    i=i+1















