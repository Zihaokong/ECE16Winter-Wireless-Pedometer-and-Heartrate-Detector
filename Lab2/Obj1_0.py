"""""
Update "list_1" so that its first 3 elements get replaced with the list ["one", "two", "three"]. 
Print list_1. It should look like: ['one', 'two', 'three', 4, 5, 6, 7, 8, 9, 10]
Create a tuple containing the words "eleven", "twelve" and "thirteen". Assign it to the first three elements from 2. 
Print list_2. It should look like: ['eleven', 'twelve', 'thirteen', 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
Join the two lists into a new list in 2 different ways: 
Use the .extend() method. Give the name "joint_1" to this list.
Use the "+" operator. Give the name "joint_2" to this list.
Print the output. It should look like: ['one', 'two', 'three', 4, 5, 6, 7, 8, 9, 10, 'eleven', 'twelve', 'thirteen', 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
We want to make "joint_2" a list of fixed length that we can continously add new elements to. We will create a function to do this for us. The function should accept the "fixed length" list as well as the "to append" list as arguments and output the "new list" as output. The signature should be: 
def list_shift(base_list, new_data):
    return base_list
And the output: 
>> fixed_length_list = [1,2,3,4]
>> new_data = [5,6,7]
>> list_shift(fixed_length_list, new_data)
[4,5,6,7]
Bonus: are there any edge cases that the your function doesn't handle? Can you think how you might address them?
1. Execution Control
###
"""
list_1 = [0,1,2,3,4,5,6,7,8,9,10]
list_2 = [11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]
list_1[0:4] = ["one","two","three"]
tuple1 = ("eleven","twelve","thirteen")
for i in range(3):
    list_2[i] =  tuple1[i]

joint_1 = []
for x in list_1:
    joint_1.append(x)
joint_1.extend(list_2)

joint_2 = []
for x in list_1:
    joint_2.append(x)
 
for x in list_2:
    joint_2 = joint_2+[x]
   

#print(joint_2)

def list_shift(base_list, new_data):
    length = len(base_list)
    if(length == 0):
        return base_list
    base_list.extend(new_data)
    print(base_list)
    
    print(length)
    base_list = base_list[-length:]
    
    
    return base_list
    
lista = []
listb = [1,23,4]
print(list_shift(lista,listb))

#edge case when base list = 0, return itself
