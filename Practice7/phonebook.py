# phonebook.py
import csv
import os
from connect import get_connection


# Requirement 1: Design table(s) for the PhoneBook
def create_table():
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL UNIQUE
                );
            """
            )
            conn.commit()
            print("Table 'contacts' is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


# Requirement 2: Implement inserting data from a CSV file
def insert_from_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # Using ON CONFLICT to avoid errors on duplicate phone numbers
                    cur.execute(
                        """
                        INSERT INTO contacts (username, phone) 
                        VALUES (%s, %s)
                        ON CONFLICT (phone) DO NOTHING;
                    """,
                        (row["username"], row["phone"]),
                    )
                    if cur.rowcount > 0:
                        count += 1
            conn.commit()
            print(f"Successfully imported {count} new contacts from CSV.")
    except Exception as e:
        print(f"Error importing CSV: {e}")
    finally:
        conn.close()


# Requirement 3: Implement inserting data entered from the console
def insert_contact(username, phone):
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contacts (username, phone) VALUES (%s, %s);",
                (username, phone),
            )
            conn.commit()
            print(f"Contact '{username}' added successfully.")
    except Exception as e:
        print(f"Error inserting contact: {e}")
    finally:
        conn.close()


# Requirement 4: Implement updating a contact's first name or phone number
def update_contact(old_username, new_username=None, new_phone=None):
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            if new_username and new_phone:
                cur.execute(
                    "UPDATE contacts SET username=%s, phone=%s WHERE username=%s;",
                    (new_username, new_phone, old_username),
                )
            elif new_username:
                cur.execute(
                    "UPDATE contacts SET username=%s WHERE username=%s;",
                    (new_username, old_username),
                )
            elif new_phone:
                cur.execute(
                    "UPDATE contacts SET phone=%s WHERE username=%s;",
                    (new_phone, old_username),
                )

            conn.commit()
            if cur.rowcount > 0:
                print(f"Contact '{old_username}' updated successfully.")
            else:
                print(f"No contact found with username '{old_username}'.")
    except Exception as e:
        print(f"Error updating contact: {e}")
    finally:
        conn.close()


# Requirement 5: Implement querying contacts with different filters
def query_contacts(filter_by, value):
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            if filter_by == "name":
                cur.execute(
                    "SELECT * FROM contacts WHERE username ILIKE %s;",
                    (f"%{value}%",),
                )
            elif filter_by == "prefix":
                cur.execute(
                    "SELECT * FROM contacts WHERE phone LIKE %s;", (f"{value}%",)
                )
            else:
                cur.execute("SELECT * FROM contacts;")

            rows = cur.fetchall()
            print(f"\nFound {len(rows)} contacts:")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
            print("")
    except Exception as e:
        print(f"Error querying contacts: {e}")
    finally:
        conn.close()


# Requirement 6: Implement deleting a contact by username or phone number
def delete_contact(identifier, by_type="name"):
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            if by_type == "name":
                cur.execute(
                    "DELETE FROM contacts WHERE username = %s;", (identifier,)
                )
            elif by_type == "phone":
                cur.execute(
                    "DELETE FROM contacts WHERE phone = %s;", (identifier,)
                )

            conn.commit()
            if cur.rowcount > 0:
                print(f"Deleted contact successfully.")
            else:
                print("No matching contact found to delete.")
    except Exception as e:
        print(f"Error deleting contact: {e}")
    finally:
        conn.close()


# Simple menu to test everything
if __name__ == "__main__":
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Import from CSV")
        print("2. Add new contact manually")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact")
        print("7. Exit")

        choice = input("Select an option (1-7): ")

        if choice == "1":
            # Using absolute path structure from image
            insert_from_csv("Practice7/contacts.csv")
        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(name, phone)
        elif choice == "3":
            old_name = input("Enter username to update: ")
            new_name = (
                input("Enter new name (leave empty to skip): ") or None
            )
            new_phone = (
                input("Enter new phone (leave empty to skip): ") or None
            )
            update_contact(old_name, new_name, new_phone)
        elif choice == "4":
            name_filter = input("Enter name to search: ")
            query_contacts("name", name_filter)
        elif choice == "5":
            prefix = input("Enter phone prefix (e.g., 555): ")
            query_contacts("prefix", prefix)
        elif choice == "6":
            id_type = input("Delete by 'name' or 'phone'?: ").strip().lower()
            val = input("Enter the name or phone to delete: ")
            delete_contact(val, id_type)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")