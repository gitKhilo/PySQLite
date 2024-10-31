import sqlite3

# Connect to the SQLite database (it will create a new one if it doesn't exist)
conn = sqlite3.connect('Hospital.db')
cursor = conn.cursor()

# Part 1: Create the CovidPatients table if it doesn't exist (Practice 1)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CovidPatients (
        PatientID INTEGER PRIMARY KEY,
        PatientName TEXT,
        SSN TEXT,
        OxygenLevel INTEGER,
        Vaccines_Taken_No INTEGER
    )
''')

# Insert initial data into CovidPatients (Practice 1)
try:
    cursor.execute('''INSERT INTO CovidPatients VALUES (1, 'Fadi Samad', '6534A', 77, 1)''')
    cursor.execute('''INSERT INTO CovidPatients VALUES (2, 'Bassem Lotfi', '4689B', 79, 2)''')
    cursor.execute('''INSERT INTO CovidPatients VALUES (3, 'Lama ElAmir', '7485C', 82, 0)''')
    conn.commit()
except Exception as e:
    print("Data already exists or error occurred: ", e)

# Practice 2: Display all patients
cursor.execute("SELECT * FROM CovidPatients")
results = cursor.fetchall()

# a. Display each patient on a line
print("Patients data:")
for row in results:
    print(row)

# b. Highest oxygen level and corresponding patient
highest_oxygen = max(results, key=lambda x: x[3])
print(f"Highest oxygen level: {highest_oxygen[3]} (Patient: {highest_oxygen[1]})")

# c. Average oxygen level for all patients
avg_oxygen = sum([row[3] for row in results]) / len(results)
print(f"Average oxygen level: {avg_oxygen}")

# d. Patients with oxygen levels above average
above_avg = [row[1] for row in results if row[3] > avg_oxygen]
print(f"Patients with oxygen above average: {above_avg}")

# e. Patients with oxygen levels below average
below_avg = [row[1] for row in results if row[3] < avg_oxygen]
print(f"Patients with oxygen below average: {below_avg}")

# f. Number of patients who took no vaccines
no_vaccine_count = len([row for row in results if row[4] == 0])
print(f"Number of patients with no vaccines: {no_vaccine_count}")

# Practice 3: Add a new patient interactively
new_patient_name = input("Enter patient name: ")
new_ssn = input("Enter SSN: ")
new_oxygen_level = int(input("Enter oxygen level: "))
new_vaccines_taken = int(input("Enter number of vaccines taken: "))

# Check if patient already exists by SSN
cursor.execute("SELECT * FROM CovidPatients WHERE SSN = ?", (new_ssn,))
existing_patient = cursor.fetchone()

if existing_patient:
    print("Patient already exists, cannot insert duplicate.")
else:
    cursor.execute("INSERT INTO CovidPatients (PatientName, SSN, OxygenLevel, Vaccines_Taken_No) VALUES (?, ?, ?, ?)", 
                   (new_patient_name, new_ssn, new_oxygen_level, new_vaccines_taken))
    conn.commit()
    print("New patient added successfully.")

# Practice 4: Expanding the database with CovidRoom table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CovidRoom (
        RoomID INTEGER PRIMARY KEY,
        RoomUse TEXT,
        FloorNo INTEGER
    )
''')
# Insert rows into CovidRoom table
cursor.execute("INSERT INTO CovidRoom VALUES (1, 'ICU', 2)")
cursor.execute("INSERT INTO CovidRoom VALUES (2, 'Recovery', 3)")
cursor.execute("INSERT INTO CovidRoom VALUES (3, 'General', 1)")
conn.commit()

# Adding RoomID column to CovidPatients table
cursor.execute("ALTER TABLE CovidPatients ADD COLUMN RoomID INTEGER")
conn.commit()

# Update RoomID for a patient
room_id = int(input("Enter RoomID for the patient: "))
patient_id = int(input("Enter PatientID: "))

# Check if the room exists
cursor.execute("SELECT * FROM CovidRoom WHERE RoomID = ?", (room_id,))
room_exists = cursor.fetchone()

if room_exists:
    cursor.execute("UPDATE CovidPatients SET RoomID = ? WHERE PatientID = ?", (room_id, patient_id))
    conn.commit()
    print("Room updated successfully.")
else:
    print("Room ID does not exist!")

# Practice 5: Interactive and dynamic data entry with validation
while True:
    new_patient_name = input("Enter patient name (or '0' to quit): ")
    if new_patient_name == '0':
        break

    new_ssn = input("Enter SSN: ")
    new_oxygen_level = int(input("Enter oxygen level: "))
    new_vaccines_taken = int(input("Enter number of vaccines taken: "))
    new_room_id = int(input("Enter RoomID: "))

    # Check if room exists
    cursor.execute("SELECT * FROM CovidRoom WHERE RoomID = ?", (new_room_id,))
    room_exists = cursor.fetchone()

    if room_exists:
        cursor.execute("INSERT INTO CovidPatients (PatientName, SSN, OxygenLevel, Vaccines_Taken_No, RoomID) VALUES (?, ?, ?, ?, ?)", 
                       (new_patient_name, new_ssn, new_oxygen_level, new_vaccines_taken, new_room_id))
        conn.commit()
        print("New patient added successfully.")
    else:
        print("Invalid RoomID. Try again.")

# Close the database connection when done
conn.close()
