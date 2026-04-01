import mysql.connector
import csv

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Dharan@prathi",
    database="mess_management",
    use_pure=True
)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS students(stud_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), room_no VARCHAR(10))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS meals(meal_id INT AUTO_INCREMENT PRIMARY KEY, stud_id INT, breakfast INT, lunch INT, dinner INT)""")

# Meal Costs
cost_breakfast=50
cost_lunch=100
cost_dinner=80


while True:

    print("\n----- Mess Bill Management System -----")
    print("1. Add Student")
    print("2. View Students")
    print("3. Record Meal")
    print("4. View all meals")
    print("5. Delete Student")
    print("6. View mess Bill")
    print("7. Search Student")
    print("8. Export mess bill report as whole")
    print("9. View mess bill for single student")
    print("10. Exit")
    choice = input("Enter your choice: ")


    if choice == "1":
        name = input("Enter student name: ")
        room_number = input("Enter room number: ")
        cursor.execute("INSERT INTO students (name, room_no) VALUES (%s, %s)", (name, room_number))
        conn.commit()
        print("Student added successfully!")


    elif choice == "2":
        cursor.execute("SELECT * FROM students")
        print("\nStudent List:")
        for row in cursor.fetchall():
            print(row)


    elif choice == "3":
        stud_id = int(input("Enter student ID: "))
        cursor.execute("SELECT * FROM students WHERE stud_id = %s", (stud_id,))
        student = cursor.fetchone()  

        if student is None:
            print(f"Student ID {stud_id} not found in database!")
        else:
            #check if the student already has a meal record
            cursor.execute("Select breakfast, lunch, dinner from meals where stud_id=%s", (stud_id,))
            meal=cursor.fetchone()
            if meal is None:
                # No existing record, start from 0
                print("No existing meal record for this student.")
                current_breakfast=0
                current_lunch=0
                current_dinner=0
            else:
                current_breakfast=meal[0]
                current_lunch=meal[1]
                current_dinner=meal[2]
                print(f"Exisitng meals for this student -> Breakfast: {current_breakfast}, Lunch: {current_lunch}, Dinner: {current_dinner}")

            # Only ask for meals if student exists
            breakfast = max(0, int(input("Enter breakfast count: ")))
            lunch = max(0, int(input("Enter lunch count: ")))
            dinner = max(0, int(input("Enter dinner count: ")))
           
            # Calculate new totals
            total_breakfast=current_breakfast + breakfast
            total_lunch=current_lunch+lunch
            total_dinner=current_dinner+dinner

            if meal is None:
                # Insert new record
                cursor.execute("INSERT INTO meals (stud_id, breakfast, lunch, dinner) VALUES (%s,%s,%s,%s)", (stud_id, breakfast, lunch, dinner))
                conn.commit()
                print("Meal recorded successfully!")
            else:
                cursor.execute("Update meals set breakfast=%s, lunch=%s, dinner=%s where stud_id=%s",(total_breakfast, total_lunch, total_dinner, stud_id))
                conn.commit()
                print(f"Meal updated successfully New totals -> Breakfast: {total_breakfast}, Lunch: {total_lunch}, Dinner: {total_dinner}")


    elif choice=="4":
        cursor.execute("""Select s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner from Students s join meals m on s.stud_id=m.stud_id""")
        records=cursor.fetchall()

        if not records:
            print("No meal record found")
        else:
            print("\n----Meals Recorded----")
            for row in records:
                print(f"Student ID: {row[0]}, Name: {row[1]}, Room Number: {row[2]}, Breakfast: {row[3]}, Lunch: {row[4]}, Dinner: {row[5]}")



    elif choice=="5":
        stud_id=int(input("Enter the student id to delete the student: "))
        # Check if student exists
        cursor.execute("Select * from students where stud_id=%s", (stud_id,))
        student=cursor.fetchone()

        if student is None:
            print(f"No student found with ID {stud_id}.")
        else:
            #confirm deletion
            confirm=input(f"Are you sure you want to delete student '{student[1]}' and their meals? (y/n):")
            if confirm.lower()=='y':
                # Delete meals first
                cursor.execute("Delete from meals where stud_id=%s", (stud_id,))
                # Delete Student
                cursor.execute("Delete from students where stud_id=%s", (stud_id,))
                conn.commit()
                print(f"Student ID {stud_id} and their meal records have been deleted successfully")
            else:
                print("Delection cancelled.")



    elif choice=="6":
        cursor.execute("Select s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner from students s left join meals m on s.stud_id=m.stud_id")
        records=cursor.fetchall()

        if not records:
            print("No Student or meal records found!")
        else:
            print("\n-----Mess Bill----")
            for row in records:
                stud_id, name, room, breakfast, lunch, dinner=row
                breakfast=breakfast if breakfast else 0
                lunch=lunch if lunch else 0
                dinner=dinner if dinner else 0
                total_meals=breakfast+lunch+dinner
                total_bill=(breakfast*cost_breakfast)+(lunch*cost_lunch)+(dinner*cost_dinner)
                print(f"ID: {stud_id}, Name: {name}, Room: {room}, Total Meals: {total_meals}, Total Bill: ₹{total_bill} ")



    elif choice=="7":
        search=input("Enter student id or name to search:")
        if search.isdigit():
            # Search by ID
            cursor.execute("Select s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner from students s left join meals m on s.stud_id=m.stud_id where s.stud_id=%s", (int(search),))
        else:
            # Search By Name
            cursor.execute("select s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner from students s left join meals m on s.stud_id=m.stud_id where s.name like %s", (f"%{search}%",))
        records=cursor.fetchall()
        if not records:
            print("No student found.")
        else:
            print("\n----Search results----")
            for row in records:
                stud_id, name, room, breakfast, lunch, dinner=row
                breakfast=breakfast if breakfast else 0
                lunch=lunch if lunch else 0
                dinner=dinner if dinner else 0
                total_meals=breakfast+lunch+dinner
                total_bill=(breakfast*cost_breakfast)+(lunch*cost_lunch)+(dinner*cost_dinner)
                print(f"ID: {stud_id}, Name: {name}, Room: {room}, Total Meals: {total_meals}, Total Bill: ₹{total_bill} ")



    elif choice=="8":
        cursor.execute("Select s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner from students s left join meals m on s.stud_id=m.stud_id")
        records=cursor.fetchall()
        if not records:
            print("No records to export.")
        else:
            with open("Mess_Bill_report.csv", "w", newline="") as f:
                writer=csv.writer(f)
                writer.writerow(["Student ID", "Name", "Room No", "Breakfast", "Lunch", "Dinner", "Total Meals", "Total Bill"])
                for row in records:
                    stud_id, name, room, breakfast, lunch, dinner=row
                    breakfast=breakfast if breakfast else 0
                    lunch=lunch if lunch else 0
                    dinner=dinner if dinner else 0
                    total_meals=breakfast+lunch+dinner
                    total_bill=(breakfast*cost_breakfast)+(lunch*cost_lunch)+(dinner*cost_dinner)
                    writer.writerow([stud_id, name, room, breakfast, lunch, dinner, total_meals, total_bill])
            print("Mess Bill Report generated successfully as Mess_Bill_Report.csv")



    elif choice=="9":
        search = input("Enter student ID or name to generate mess bill: ")

        if search.isdigit():
            cursor.execute("""SELECT s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner FROM students s LEFT JOIN meals m ON s.stud_id = m.stud_id WHERE s.stud_id = %s
        """, (int(search),))
        else:
            cursor.execute("""SELECT s.stud_id, s.name, s.room_no, m.breakfast, m.lunch, m.dinner FROM students s LEFT JOIN meals m ON s.stud_id = m.stud_id WHERE s.name LIKE %s
        """, (f"%{search}%",))

        record = cursor.fetchone()  # Only fetch one student

        if record is None:
            print("No student found.")
        else:            
            stud_id, name, room, breakfast, lunch, dinner = record
            breakfast = breakfast if breakfast else 0
            lunch = lunch if lunch else 0
            dinner = dinner if dinner else 0
            total_meals = breakfast + lunch + dinner
            total_bill = (breakfast*cost_breakfast) + (lunch*cost_lunch) + (dinner*cost_dinner)
            print("\n-----Single Student Mess Bill-----")
            print(f"Student ID: {stud_id}")
            print(f"Name: {name}")
            print(f"Room No: {room}")
            print(f"Breakfast: {breakfast}, Lunch: {lunch}, Dinner: {dinner}")
            print(f"Total Meals: {total_meals}")
            print(f"Total Bill: ₹{total_bill}")

            # Ask if user wants to generate the bill
            export = input("Do you want to export this bill as CSV? (y/n): ")
            if export.lower() == 'y':
                filename = f"Mess_Bill_{name.replace(' ', '_')}.csv"
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Student ID", "Name", "Room No", "Breakfast", "Lunch", "Dinner", "Total Meals", "Total Bill"])
                    writer.writerow([stud_id, name, room, breakfast, lunch, dinner, total_meals, total_bill])
                print(f"Bill exported successfully as {filename}")


    elif choice == "10":
        print("Exiting program...")
        break

    else:
        print("Invalid choice!")




## Enter your choice: 9   
# Enter student ID or name to generate mess bill: ER56
# No student found.
# Have to check for the student id for single report generation