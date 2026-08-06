 
Module: Python Fundamentals & Easy Real-World Logic
Author: Tarun Das
Portfolio: Data Analytics Foundations
"""

# ============================================================
# PART 1: EASY THEORY & REAL-WORLD CONCEPTS (Q1 - Q3)
# ============================================================

"""
Question 1: What is Python and why is it widely used in Data Analytics? Mention any three reasons.

Simple Answer:
Python is a popular computer programming language. It is famous because it is written in simple, English-like words that are easy to read and write.

Three Reasons Why Data Analysts Use Python:
1. Ready-Made Helper Tools: Python has built-in toolkits (like Pandas and Matplotlib) that easily clean big sales data and draw colorful charts.
2. Easy to Learn: Writing Python code feels like writing normal English sentences, so you can solve business problems quickly.
3. Connects to Everything: Python easily connects with database systems (SQL), online store APIs, and Excel files.

------------------------------------------------------------

Question 2: Explain the difference between List and Tuple in Python.

Simple Answer:
- List (Changeable Box):
  A list lets you change, add, or remove items anytime.
  Real-World Example: A shopping cart where customers keep adding or removing items.
  Syntax: Uses square brackets -> [10, 20, 30]

- Tuple (Fixed Box):
  A tuple cannot be changed once created. It is permanently locked.
  Real-World Example: Fixed tax rates (like GST = 18%) or month names that never change.
  Syntax: Uses round brackets -> (10, 20, 30)

- Speed: Tuples use less computer memory and run faster than lists.

------------------------------------------------------------

Question 3: What is a function in Python? Why are functions useful?

Simple Answer:
A function is a named recipe or button for a specific job. You write the code once, and you can press the button (call the function) whenever you need it.

Why Functions Are Useful:
1. Saves Time: You don't have to rewrite the same math formula again and again.
2. Easy Fixing: If a business rule changes (e.g., store discount changes from 10% to 15%), you only update it in one place inside the function.
3. Keeps Code Clean: It divides a huge project into small, neat steps.
"""


# ============================================================
# PART 2: PRACTICAL CODE WITH REAL-WORLD EXAMPLES (Q4 - Q10)
# ============================================================

 # ------------------------------------------------------------
# Question 4: Take user's name as input and print a greeting message.
# Real-World Scenario: Greeting a customer when they log into a shopping app.
# ------------------------------------------------------------
# Interactive input for user environment:
user_name = input("Enter your name: ")

# Hardcoded fallback placeholder for automated testing:
# user_name = "Tarun"

print(f"Hello, {user_name}! Welcome to our Store Analytics Dashboard.\n")


# ------------------------------------------------------------
# Question 5: Check whether a number is even or odd using conditional statements.
# Real-World Scenario: Checking an order ID to decide odd/even day delivery schedules.
# ------------------------------------------------------------
order_id = 1014

if order_id % 2 == 0:
    print(f"Order #{order_id} is an EVEN number -> Scheduled for Tuesday Delivery.")
else:
    print(f"Order #{order_id} is an ODD number -> Scheduled for Wednesday Delivery.")
print()


# ------------------------------------------------------------
# Question 6: Print numbers from 1 to 10 using a loop.
# Real-World Scenario: Counting sales days from Day 1 to Day 10 of a monthly sale.
# ------------------------------------------------------------
print("Printing Sales Days (Day 1 to Day 10):")
for day in range(1, 11):
    print(f"Day-{day}", end=" ")
print("\n\n")


# ------------------------------------------------------------
# Question 7: Create a list of five numbers and print the maximum number.
# Real-World Scenario: Finding the highest daily sale amount from a weekly sales list.
# ------------------------------------------------------------
daily_sales_inr = [4500, 12000, 8900, 3300, 6700]
highest_sale = max(daily_sales_inr)

print(f"Daily Store Sales List (in ₹): {daily_sales_inr}")
print(f"Highest Sale Achieved in a Single Day: ₹{highest_sale}\n")


# ------------------------------------------------------------
# Question 8: Remove duplicate values from a list using a set.
# Real-World Scenario: Removing duplicate customer phone numbers or barcode scans.
# ------------------------------------------------------------
raw_scanned_barcodes = [101, 102, 101, 103, 104, 102, 105]
clean_unique_barcodes = list(set(raw_scanned_barcodes))

print(f"Raw Scanned Barcodes (With Duplicates): {raw_scanned_barcodes}")
print(f"Clean Unique Product List: {clean_unique_barcodes}\n")


# ------------------------------------------------------------
# Question 9: Write a function that returns the square of a number.
# Real-World Scenario: Calculating area size or compounding score factor.
# ------------------------------------------------------------
def calculate_square(number):
    """Simple function that multiplies a number by itself."""
    return number * number

sample_input = 7
print(f"Input Number: {sample_input}")
print(f"Square Output: {calculate_square(sample_input)}\n")


# ------------------------------------------------------------
# Question 10: Count how many times a number appears in a list.
# Real-World Scenario: Checking how many times a specific item (Item #2) was bought today.
# ------------------------------------------------------------
items_sold_today = [2, 3, 4, 2, 5, 2]
target_item_id = 2

times_sold = items_sold_today.count(target_item_id)

print(f"Today's Items Sold List: {items_sold_today}")
print(f"Item #{target_item_id} was sold exactly {times_sold} times today.")