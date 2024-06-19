

class items:
    def __init__(self , id , itemName, Price):
        self.id = id
        self.itemName = itemName
        self.price = Price
        

# create bill display function  
def display (I , cName, cAddress ):
    total = 0
    print("\n\n\n")
    print("\t   Paschal Store   ")
    print("\t   --------------   ")
    print(f"Name: {cName}  \t Address: {cAddress}")
    for obj in I:
        print(f"Id: {obj.id} \t ItemName: {obj.itemName} \t Price: {obj.price}")
        print("------------------------------------------------------")
        total += obj.price
    print(f"\t\tTotal: {total}")
    print("\n")
    print("\tThanks for for supporting our services")
    print("\n\n")
    
    
# store object array
list = []

print("\n\n")
print("Hello Everyone!!")
cName = input("Enter your Name: ")
cAddress = input("Enter your Address: ")
totalItems = int(input("Enter total Items: "))
print("\n")

# take input items details 
for i in range (0, totalItems):
    id = (i+1)
    name = input("Enter item Name: ")
    price = int (input("Enter Price: "))
    list.append(items(id, name , price))
    

# call  display function
display(list , cName, cAddress)    


