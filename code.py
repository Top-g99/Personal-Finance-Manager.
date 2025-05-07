
---

### 🧾 `finance_manager.py`
```python
import json
from getpass import getpass
from collections import defaultdict
from hashlib import sha256

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def find_user(users, username):
    for user in users:
        if user["username"] == username:
            return user
    return None

def register_user():
    users = load_data()["users"]
    username = input("Enter your username: ")

    if find_user(users, username):
        print("Username already exists!")
        return

    password = getpass("Enter your password: ")
    hashed_password = hash_password(password)

    users.append({
        "username": username,
        "password": hashed_password,
        "income": 0,
        "expenses": []
    })

    save_data({"users": users})
    print("User registered successfully!")

def login_user():
    users = load_data()["users"]
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    hashed_password = hash_password(password)

    user = find_user(users, username)
    if user and user["password"] == hashed_password:
        return user
    else:
        print("Invalid login credentials.")
        return None

def add_income(user):
    income = float(input("Enter income amount: "))
    user["income"] += income
    save_data({"users": load_data()["users"]})
    print(f"Income of ${income} added!")

def add_expense(user):
    category = input("Enter expense category: ")
    amount = float(input("Enter expense amount: "))
    user["expenses"].append({"category": category, "amount": amount})
    save_data({"users": load_data()["users"]})
    print(f"Expense of ${amount} added to category '{category}'.")

def view_finances(user):
    print(f"\nYour financial summary:")
    print(f"Income: ${user['income']}")
    print("Expenses:")
    category_totals = defaultdict(float)
    for expense in user["expenses"]:
        category_totals[expense["category"]] += expense["amount"]
    for category, total in category_totals.items():
        print(f"  {category}: ${total}")
    print(f"Remaining balance: ${user['income'] - sum(category_totals.values())}\n")

def main_menu():
    print("===== PERSONAL FINANCE MANAGER =====")
    print("1. Register a new user")
    print("2. Login")
    print("3. Exit")
    choice = input("Select an option (1-3): ")

    if choice == "1":
        register_user()
    elif choice == "2":
        user = login_user()
        if user:
            user_menu(user)
    elif choice == "3":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Try again.")
        main_menu()

def user_menu(user):
    while True:
        print("\n===== User Menu =====")
        print("1. Add income")
        print("2. Add expense")
        print("3. View finances")
        print("4. Logout")
        choice = input("Select an option (1-4): ")

        if choice == "1":
            add_income(user)
        elif choice == "2":
            add_expense(user)
        elif choice == "3":
            view_finances(user)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
