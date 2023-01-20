from tabulate import tabulate
from operator import attrgetter


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    # methods to return cost and quantity
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    # string representation of class
    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, R{self.cost:,.2f}, {self.quantity}"

    # display attribute as list
    def __repr__(self):
        return [self.country, self.code, self.product, self.cost, self.quantity]


# =============Shoe list===========


# List to store a list of objects of shoes
shoe_list = []


# ==========Functions outside the class==============
# Function to open inventory.txt file, create shoes object with data and add to list
def read_shoes_data():
    try:
        inv_file = open("inventory.txt", "r")
    except FileNotFoundError:
        print("The file does not exist, please check the file name and location and rerun.")
    nested_list = []
    for line in inv_file:
        nested_list.append(line.rstrip().split(","))
    for each_list in nested_list:
        if each_list == nested_list[0]:
            pass
        else:
            item = Shoe(each_list[0], each_list[1], each_list[2], each_list[3], each_list[4])
            shoe_list.append(item)
    inv_file.close()


# Function to allow user to input new shoe object and add to the shoe list.
def capture_shoes():
    new_country = input("Enter the country: ")
    new_code = input("Enter the SKU code: ")
    new_product = input("Enter the product name: ")
    while True:
        try:
            new_cost = float(input("Enter the cost in the format 0.00: "))
            break
        except ValueError:
            print("invalid entry, enter the cost in the correct format, 0.00.")
            continue
    while True:
        try:
            new_quantity = int(input("Enter the quantity of the stock: "))
            break
        except ValueError:
            print("invalid entry, enter a whole number of stock")
            continue
    new_shoe = Shoe(new_country, new_code, new_product, new_cost, new_quantity)
    shoe_list.append(new_shoe)


# Function to print all details of objects in the list in table format using tabulate module.
def view_all():
    data_list = []
    for shoes in shoe_list:
        data = [shoes.country, shoes.code, shoes.product, f"R{shoes.cost:,.2f}", shoes.quantity]
        data_list.append(data)
    print(tabulate(data_list, headers=['Country', 'Code', 'Product', 'Cost', 'Quantity']))
    print("\n")


# Function to return the min stock item, ask user if they want to restock and update the value
def re_stock():
    min_stock = min(shoe_list, key=attrgetter('quantity'))
    print(f"Please see the details of the lowest stock:\n{min_stock}")
    while True:
        question = input("Would you like to restock? Y/N: ").upper()
        if question == "Y":
            while True:
                try:
                    new_stock = int(input("Enter the quantity of new stock to be added: "))
                    break
                except ValueError:
                    print("Invalid response, please enter a whole number of stock to be added to existing stock.")
                    continue
            break
        elif question == "N":
            break
        else:
            print("You have entered an invalid response, please try again.")
            continue
    for pos, i in enumerate(shoe_list):
        if min_stock == i:
            shoe_list[pos].quantity += new_stock
            print(f"The stock value has been updated:\n{i}")
            print("\n")


# Function to search for a shoe using the SKU code and print the object
def search_shoe():
    search_code = input("Enter the SKU code that you want to search for: ")
    # flag to check if search returns a result, switches to true if found
    code_found = False
    for shoe_obj in shoe_list:
        if shoe_obj.code == search_code:
            code_found = True
            print(shoe_obj)
            break
    if not code_found:
        output = "The SKU code entered was not found, "
        output += "please check that you entered the code correctly and in the following format, SKUXXXXX"
        print(output)
        print("\n")


# Function to calculate total value of each item and display the data in a table using tabulate
def value_per_item():
    data_list = []
    for shoes in shoe_list:
        data = [shoes.product, f"R{shoes.cost:,.2f}",
                shoes.quantity, f"R{float(shoes.cost) * float(shoes.quantity):,.2f}"]
        data_list.append(data)
    print(tabulate(data_list, headers=['Product', 'Cost', 'Quantity', 'Total Value']))
    print("\n")


# Function to determine the product with max quantity and print this shoe as being for sale.
def highest_qty():
    max_stock = max(shoe_list, key=attrgetter('quantity'))
    output2 = "Please see the details of the highest stock:\n"
    output2 += f"{max_stock}\n"
    output2 += "This stock item is now on sale!"
    print(output2)
    print("\n")


# ==========Main Menu=============

# read the inventory.txt file in order to generate the shoes list and execute the other functions in programme
read_shoes_data()

# menu to execute each function above.
while True:
    menu = input('''Select one of the following Options below:
a - Add entry
ve - View all entries
r - restock the lowest stock
s - search for shoe with SKU code
va - view total value of each item
h - display highest quantity product as on sale
e - Exit
: ''').lower()
    # If user selects 'a', allow user to add new entry to the shoe list
    if menu == 'a':
        capture_shoes()

    # if user selects 'v' call view_all function to print all details of objects in table format
    elif menu == 've':
        view_all()

    # If user selects 'r' call function to return the min stock item and restock depleted stock
    elif menu == 'r':
        re_stock()

    # if admin user selects 's' call function to search for a shoe by the SKU code
    elif menu == 's':
        search_shoe()

    # If user selects 'va' call function to calculate total value of each item
    elif menu == 'va':
        value_per_item()

    # If user selects 'h' call function to print shoe with max quantity as on sale.
    elif menu == 'h':
        highest_qty()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
