#Library Member(Non-Staff)
#Global variable
MemID = "#"
def Member_login(emailaddress, Password):
    global MemID
    # Normalize input for case-insensitive comparison of email
    emailaddress = emailaddress.strip().lower()
    Password = Password.strip()
    login = False

    try:
        with open("members.txt", "r") as file:
            # Skip the first line (header)
            next(file)

            for line in file:
                # Split each line by " | " and strip whitespace
                parts = [part.strip() for part in line.strip().split(" | ")]

                # Ensure we have the expected number of fields
                if len(parts) < 6:
                    continue

                # Retrieve stored email and password
                stored_email = parts[3].strip().lower()
                stored_password = parts[5].strip()

                # Check if the email and password match
                if emailaddress == stored_email and Password == stored_password:
                    MemID = parts[0].strip()
                    login = True
                    print("Login successful")
                    return login


        # Allow 3 retry attempts if login fails initially
        attempts = 3
        while (login == False) and (attempts > 1):
            print(f"Incorrect email address or password! {attempts - 1} attempt(s) left.")

            # Prompt user for re-entry
            emailaddress = input("Enter your email address: ").strip().lower()
            Password = input("Enter your Password: ").strip()

            with open("members.txt", "r") as file:
                next(file)  # Skip the header line in each attempt

                for line in file:
                    parts = [part.strip() for part in line.strip().split(" | ")]
                    if len(parts) < 6:
                        continue

                    stored_email = parts[3].strip().lower()
                    stored_password = parts[5].strip()

                    if emailaddress == stored_email and Password == stored_password:
                        MemID = parts[0].strip()
                        login = True
                        print("Login successful")
                        return login
            attempts -= 1

        # Final message after all attempts fail
        print("Login failed after 3 attempts. Contact librarian.")
        return False
    except FileNotFoundError:
        print("File not found!")
def StrongPassword(UserPassword):
    import re
    #Minimum Length-
    if len(UserPassword) < 8:
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", UserPassword):
        return False

    # At least one lowercase letter
    if not re.search(r"[a-z]", UserPassword):
        return False

    # At least one digit
    if not re.search(r"\d", UserPassword):
        return False

    # At least one special character
    if not re.search(r"[@$!%*?&#]", UserPassword):
        return False

    return True

def ValidateContactNumber(PhoneNumber):
    #Hypothetical phone number: +60 11 1234 1234; length = 16
    if len(PhoneNumber) < 16 or len(PhoneNumber) > 16:
        return False
    else:
        try:
            with open("members.txt", "r") as file:
                for line in file:
                    # Skip empty lines
                    if not line.strip():
                        continue

                    # Split the line by "|" and check if there are at least 5 elements (for a valid row)
                    parts = [part.strip() for part in line.strip().split("|")]

                    if len(parts) >= 5:  # Ensure there are enough columns
                        existing_phoneNumber = parts[4]  # Email is in the 4th column

                        # Compare email addresses
                        if existing_phoneNumber.lower() == PhoneNumber:
                            print("This contact already exists.")
                            file.close()
                            return False
                file.close()
                return True  # If no match is found after checking all lines

        except FileNotFoundError:
            print("No user data found.")
            return False

#System  generating random but unique numbers for members
import random
def generate_unique_member_id():
    exists = True  # To enter the loop
    id = None

    # Generating unique MemberID in the form "MEM####"
    while exists:
        exists = False  # Reset for each new ID generation
        id_number = random.randint(1, 9999)  # Generate a random number between 1 and 9999
        id = (f"MEM{id_number:04d}")  # Format as "MEM" followed by a 4-digit number

        try:
            with open("members.txt", "r") as file:
                for line in file:
                    # Split the line by "|" and extract the MemberID (first column)
                    existing_id = line.strip().split("|")[0].strip()

                    if existing_id == id:  # Compare the new ID with existing IDs
                        exists = True
                        file.close()
                        break  # No need to check further if a match is found

        except FileNotFoundError:
            # If the file doesn't exist, we can assume no IDs are in use yet
            break

    return id

def check_existing_user(email_to_check, file_name):
    try:
        with open(file_name, "r") as file:
            for line in file:
                # Skip empty lines
                if not line.strip():
                    continue

                # Split the line by "|" and check if there are at least 5 elements (for a valid row)
                parts = [part.strip() for part in line.strip().split(" | ")]

                if len(parts) >= 5:  # Ensure there are enough columns
                    existing_email = parts[3]  # Email is in the 4th column

                    # Compare email addresses
                    if existing_email.lower() == email_to_check.lower():
                        file.close()
                        return True  # Exit as soon as we find a match
            return False  # If no match is found after checking all lines


    except FileNotFoundError:
        print("No user data found.")
        return False
def SignUp():
    global MemID  # Declare MemID so it can be modified
    counter = ["Firstname", "Lastname", "Email address", "Contact Number", "Password"]
    ListDetails = ["","","","",""]
    counts = 0
    while counts < len(counter):
        while len(ListDetails[counts]) == 0: #Presence check
            ListDetails[counts] = input(f"Enter your {counter[counts]}: ")
            if len(ListDetails[counts]) == 0:
                print("It is mandatory to fill up this field.")


        #Length and uniqueness check for contact number
        if counter[counts] == "Contact Number":
            ContactNumber = ValidateContactNumber(ListDetails[3])
            while ContactNumber == False:
                print("Invalid phone number! The phone number should be in this format: +60 11 1234 1234")
                ListDetails[counts] = input(f"Enter your {counter[counts]}: ")
                ContactNumber = ValidateContactNumber(ListDetails[3])

        #Checking if password entered is a strong password
        if counter[counts] == "Password":
            StrongUserPassword = StrongPassword(ListDetails[-1])
            while (StrongUserPassword != True):
                print("Password is not strong enough! Your password should be at least 8 characters long and must contain the following:")
                PasswordCredentials = ["1. At least 1 UpperCase letter; W,S,D,R", "2. At least 1 special symbol; @,!,&,*", "3. At least 1 digit; 0,1,2,3", "4. At least 1 lowercase letter; w,s,d,r"]
                for requirement in PasswordCredentials:
                    print(requirement)
                ListDetails[-1] = input("Enter password again: ")
                StrongUserPassword = StrongPassword(ListDetails[-1])

        #Checking member details before they sign in to avoid duplication of data
        exists = False
        if counter[counts] == "Email address":
            exists = check_existing_user(ListDetails[2], "members.txt")
            if exists == True:
                print("This account already exists. Try logging in!")
                email = ListDetails[counts]
                Password = input("Enter your password to log in: ")
                login = Member_login(email, Password)
                if login == False:
                    return False
                return

        counts += 1
        #Before storing data in file, the first letter of both first and last names should be capital letters, and email address should be lowercase
        ListDetails[0] = ListDetails[0].capitalize()
        ListDetails[1] = ListDetails[1].capitalize()
        ListDetails[2] = ListDetails[2].lower()
    #Storing data in file
    try:
        f = open("members.txt", "a")
        New_id = generate_unique_member_id()
        MemID = New_id
        f.write(New_id + " | " + " | ".join(ListDetails) + "\n")
        f.close()
        print("SignUp Successful!")
    except:
        print("SignUp not successful. An error has occurred! Contact Librarian.")
        return False

def DisplayBorrowedBooks(memID):
    try:
        # Open both files with context managers
        with open("MemberBorrowedBooksInfo.txt", "r") as book_lent_file, \
             open("BookList.txt", "r") as book_list_file:

            for line in book_lent_file:
                # Skip empty lines and lines with insufficient columns
                if not line.strip() or len(line.split(" | ")) < 4:
                    continue

                # Extract data from the line
                data = line.strip().split(" | ")
                member_id, book_id, Due_Date, Overdue_Fees, PaymentStatus = data[:5]

                #removing more whitespaces
                member_id = member_id.strip()
                book_id = book_id.strip()
                Due_Date = Due_Date.strip()
                Overdue_Fees = Overdue_Fees.strip()
                PaymentStatus = PaymentStatus.strip()

                # Split book IDs
                book_id = book_id.strip().split(", ")
                for i in range(len(book_id)):
                    book_id[i] = book_id[i].strip()  # Strip whitespace from each book ID

                # Check if the member ID matches the provided one
                if member_id == memID:
                    print("Here are the details about your borrowed books:\n")

                    # Search for matching book information in the book list
                    for book_line in book_list_file:
                        # Skip empty lines and lines with insufficient columns
                        if not book_line.strip() or len(book_line.split(" | ")) < 4:
                            continue

                        # Extract book information from the line
                        book_info = book_line.strip().split(" | ")
                        book_info[0] = book_info[0].strip()  # Strip leading/trailing whitespace

                        # Check if the book ID matches any borrowed book ID
                        for borrowed_id in book_id:
                            if borrowed_id == book_info[0]:
                                print(f"{borrowed_id}. Title: {book_info[1]}, Author: {book_info[2]}, Publisher: {book_info[3]} \n")
                                print(f" Due Date: {Due_Date} \n Overdue fees: RM {Overdue_Fees} \n Payment Status: {PaymentStatus}\n")
                    return   # Member has borrowed books

        # Member ID not found in borrowed books file
        print("You do not have any borrowed books!")
        return False

    except FileNotFoundError:
        print("One or both files (MemberBorrowedBooksInfo.txt or BookList.txt) not found.")
        return False

def load_books(file_name):
    """Load books from a file and return them as a list."""
    try:
        with open(file_name, 'r') as file:
            return [line.strip().split(" | ") for line in file]
    except FileNotFoundError:
        print(f"File '{file_name}' not found!")
        return None

def save_books(file_name, books):
    """Save books to a file."""
    with open(file_name, 'w') as file:
        for book in books:
            file.write(" | ".join(book) + "\n")

def return_book(member_id, book_id):
    # Helper function to load books from a file

    # Load MemberBorrowedBooksInfo.txt
    member_file = load_books("MemberBorrowedBooksInfo.txt")
    if member_file is None:
        return False  # Exit if the file couldn't be loaded

    header, *entries = member_file
    updated_lines = [header]  # Keep the header
    member_found = False
    book_found = False

    for line in entries:
        # Check if row has exactly 5 parts (ID, BookID, Due Date, Overdue Fees, Payment Status)
        if len(line) != 5:
            updated_lines.append(line)
            continue

        # Check if the current row corresponds to the member
        if line[0].strip() == member_id:
            member_found = True
            books = [b.strip() for b in line[1].split(", ")]

            # Check if book_id is in the member's borrowed books
            if book_id in books:
                book_found = True
                books.remove(book_id)  # Remove only the specific book being returned

                if books:
                    # Update the row with the remaining books
                    line[1] = ", ".join(books)
                    updated_lines.append(line)
                else:
                    # No books left, skip adding the row back to updated_lines (remove entire row)
                    continue
            else:
                # If member_id matches but not the book_id, keep the row as it is
                updated_lines.append(line)
        else:
            # Keep other members' records as-is
            updated_lines.append(line)

    # Notify if member or book was not found
    if not member_found:
        print("You do not have any borrowed books in the system.")
        return
    if not book_found:
        print("The system does not recognize this book as borrowed by you. Please verify the Book ID.")
        return

    # Save updated member file (with the returned book entry removed from the specific row)
    save_books("MemberBorrowedBooksInfo.txt", updated_lines)

    # Add returned book to availablebooks.txt if it exists in BookList.txt
    book_list = load_books("BookList.txt")
    if book_list is None:
        return False  # Exit if the file couldn't be loaded

    with open("availablebooks.txt", "a") as available_books_file:
        for lines in book_list[1:]:  # Skip header in BookList.txt
            if lines[0].strip() == book_id:
                available_books_file.write(" | ".join(lines) + "\n")
                print(f"Book '{book_id}' returned successfully and added back to available books.")
                return True

    print(f"Book ID '{book_id}' was not found in the BookList. Please verify the Book ID.")
    return False

def payment(memberid):
    print("Here is the general fee charges:")
    print("  Days  |  Fee (RM)")
    print("1 day   |   2.00")
    print("2 days  |   3.00")
    print("3 days  |   4.00")
    print("4 days  |   5.00")
    print("5 days  |   6.00")
    print(">5 days |   10.00")

    updated_Lines = []
    member_found = False

    try:
        with open("MemberBorrowedBooksInfo.txt", "r") as file:
            # Read and keep the header
            header = file.readline().strip()
            updated_Lines.append(header)

            # Process each line after the header
            for line in file:
                row = line.strip().split(" | ")

                # Check if row has the correct number of columns
                if len(row) != 5:
                    updated_Lines.append(line.strip())
                    continue

                # If member ID matches, process this row
                if row[0] == memberid:
                    member_found = True
                    overdue_fee = float(row[3])
                    payment_status = row[4].strip().split(" |")
                    payment_status = payment_status[0].lower()

                    print(f"\n The due amount you must pay is RM{overdue_fee}, and your payment status is '{payment_status}'.\n")

                    # If payment is pending and overdue_fee > 0, allow the user to "pay"
                    if overdue_fee > 0 and payment_status == "pending":
                        print("Please consult a librarian to process your payment.")
                        print("Processing payment...")

        if not member_found:
            print("You do not have any record in the system.")
            return False

    except FileNotFoundError:
        print("File is not found, so your request cannot be processed!")

def BookID_exist(bookID):
    exist = False
    try:
        with open("BookList.txt", "r") as file:
            for line in file:
                #Skip empty lines
                if not line.strip():
                    continue

                parts = [part.strip() for part in line.strip().split(" | ")]

                if len(parts) >= 4:  # Ensure there are enough columns
                    existing_bookid = parts[0]
                    if existing_bookid == bookID:
                        exist = True

        return exist

    except FileNotFoundError:
        print ("File not found!")
        return False

def UpdateProfile(memID):
    # Members cannot edit their personal information by themselves as only system admin can do so.
    # Members can only process their book returns and payment
    text, text1 = "1. Return Books", "2. Process fee payments"
    centered_text = text.center(22)
    centered_text1 = text1.center(30)
    print(centered_text)
    print(centered_text1)
    choice = int(input("What do you wish to update? (1/2): "))
    while choice < 1 and choice > 2:
        print("Invalid input!")
        choice = int(input("Enter again!(1/2): "))

    if choice == 1:
        #Verify if book ID entered exists already
        BK_ID = input("Enter the book ID of the book you want to return: ")
        exists_BK = BookID_exist(BK_ID)
        while exists_BK != True:
            print ("Incorrect book ID entered!")
            BK_ID = input("Enter the book ID of the book you want to return again: ")
            exists_BK = BookID_exist(BK_ID)

        return_book(memID, BK_ID)
    else:
        payment(memID)
def DisplayavailableBooks():
    try:
        with open("availablebooks.txt", "r") as file:
            with open ("BookList.txt", "r") as bookfile:
                print("Existing books in the library:")
                for line in bookfile:
                    print(line)

            print("\nHere is a list of all available books(not lent) in the Library:")
            for line in file:
                print(line)

    except FileNotFoundError:
        print("File not found!")
        return False

def menu_member():
    global MemID  # Declare MemID so it can be modified
    # Centering the text
    Text1, Text2 = "1: Login", "2: Sign Up"
    centered_text1 = Text1.center(17)
    centered_text2 = Text2.center(20)


    print(centered_text1)
    print(centered_text2)
    print("Press '1' for login and '2' for sign up")
    print("")

    option = input("If you already have an account, please login else sign up for a new account. Enter your option: ")

    #validating choice
    while option != "1" and option != "2":
        option = input("Invalid! Enter again from the 2 choices(1/2): ")

    print("--" * 50)

    if option == "1":
        emailadd = input("Enter your email address: ")
        password = input("Enter your password: ")
        Login = Member_login(emailadd, password)
        #print("Hold on! System verifying your ID number.")
        #MemID = Member_login(emailadd, password)
        if Login == False:
            return
    else:
        signup = SignUp()
        #print("Sorry for inconvenience. Please enter data again to get your member ID.")
        #MemID = SignUp()
        if signup == False:
            return

    while True:
        choice = int(input("\nDo you wish to continue(1) or exit back to main menu(2)? Enter either 1/2: "))
        while choice < 1 or choice > 2:
            choice = int(input("Invalid! Enter again: "))
        if choice == 2:
            print("Exiting...")
            return

        if choice == 1:

            # After login or signUp, member can access his/her account
            #Displaying the menu for library members
            MemberMenu = ["1. View details of borrowed books", "2. Update Profile (Return Books or make payment)", "3. Search for new books", "4. Logout"]
            print("--" * 50)
            print("")
            for i in MemberMenu:
                print(i)
            option = input("What do you wish to do? Choose 1-4:")
            while option < "1" or option > "4":
                print("invalid Input!")
                option = input("Enter again from the 4 choices(1-4): ")

            print("--" * 50)

            memberID = MemID  # Initialising memberID

            if option == "1":
                DisplayBorrowedBooks(memberID)
            elif option == "2":
                UpdateProfile(memberID)
            elif option == "3":
                DisplayavailableBooks()
            elif option == "4":
                print("Logging out...")
                return



#Librarian(Staff)
def Librarian_login():
    login = False
    count = 0

    try:
        while count < 3:
            Lib_ID = input("Enter your librarian ID: ")
            Password = input("Enter your password: ")
            with open("librarians.txt", "r") as file:
                for line in file:
                    # Skip empty lines
                    if not line.strip():
                        continue

                    parts = [part.strip() for part in line.strip().split(" | ")]
                    if len(parts) > 5:  # Ensure there are enough columns
                        existing_LibID = parts[0]
                        existing_Password = parts[5]

                        if existing_Password == Password:
                            if existing_LibID == Lib_ID:
                                login = True

            count += 1

            if login:
                print("Login Successful!")
                return
            else:
                print("Login Unsuccessful! Either ID or password id wrongly entered")
                print(f"You have {3 - count} attempt(s)!")

            if count == 3:
                print("Attempts exceeded! Contact System admin!")
        return

    except FileNotFoundError:
        print("File not found!")
def generate_unique_Book_ID():
    exists = True  # To enter the loop
    id = None

    # Generating unique MemberID in the form "B####"
    while exists:
        exists = False  # Reset for each new ID generation
        id_number = random.randint(1, 9999)  # Generate a random number between 1 and 9999
        id = (f"B{id_number:04d}")  # Format as "B" followed by a 4-digit number

        try:
            with open("BookList.txt", "r") as file:
                for line in file:
                    # Split the line by "|" and extract the MemberID (first column)
                    existing_id = line.strip().split("|")[0].strip()

                    if existing_id == id:  # Compare the new ID with existing IDs
                        exists = True
                        file.close()
                        break  # No need to check further if a match is found

        except FileNotFoundError:
            # If the file doesn't exist, we can assume no IDs are in use yet
            break

    return id

def add_book():
    counter = ["Title", "Author", "Publisher"]
    ListDetails = ["", "", "", ""]
    counts = 0
    while counts < len(counter):
        while len(ListDetails[counts]) == 0:  # Presence check
            ListDetails[counts] = input(f"Enter the book's {counter[counts]}: ")
            if len(ListDetails[counts]) == 0:
                print("It is mandatory to fill up this field.")

            if counts == 0:
                # Verifying if book already exists
                # Fetching title from the file
                try:
                    with open("BookList.txt", "r") as BookFile:
                        for line in BookFile:
                            # Skip empty lines
                            if not line.strip():
                                continue
                            data = [part.strip() for part in line.strip().split(" | ")]

                            if len(data) >= 4:  # Ensure there are enough columns
                                existing_book = data[1]  # Title is in the 1st column

                                BookTitle = ListDetails[0]

                                # Comparing titles
                                if existing_book.lower() == BookTitle.lower():
                                    print(f"Book already exists in system with Book Id {data[0]}. Hence, cannot add again.")
                                    return  # Exit as soon as we find a match
                except FileNotFoundError:
                    print("The Book list File is not found!")

        counts += 1

    # Assigning data
    Book_ID = generate_unique_Book_ID()
    Title = ListDetails[0]
    Author = ListDetails[1]
    Publisher = ListDetails[2]

    # Adding data to file
    try:
        with open("BookList.txt", "a") as file:
            file.write(f"{Book_ID} | {Title} | {Author} | {Publisher}  \n")
        with open("availablebooks.txt", "a") as avFile:
            avFile.write(f"{Book_ID} | {Title} | {Author} | {Publisher}  \n")
        print(f"Book added successfully with Book ID: {Book_ID}.")
    except FileNotFoundError:
        print("The Book list File is not found!")

def View_BookList():
    try:
        with open("BookList.txt", "r") as file:
            print("Here is the list of all books:")
            for line in file:
                print(line)
        with open("availablebooks.txt", "r") as avFile:
            print("Here is the list of all available(not lent) books:")
            for lines in avFile:
                print(lines)

    except FileNotFoundError:
        print("Error! File not found.")

def SearchBook(Detail, data):
    Book_found = False
    try:
        with open("BookList.txt", "r") as file:
            for line in file:
                #ignoring blank lines
                if not line.strip():
                    continue

                parts = [part.strip() for part in line.strip().split(" | ")]
                if len(parts) >= 4:  # Ensure there are enough columns
                    BookID = parts[0]
                    Title = parts[1]

                if Detail == 1:
                    if BookID.lower() == data.lower():
                        Book_found = True
                        print("Book Found! Here are the details:")
                        print("BookID | Title | Author | Publisher |")
                        print(line)
                else:
                    if Title.lower() == data.lower():
                        Book_found = True
                        print("Book Found! Here are the details:")
                        print("BookID | Title | Author | Publisher |")
                        print(line)

        if not Book_found:
            print("Book not found in system.")

    except FileNotFoundError:
        print("Error! File not found!")

def edit_book_info():
    book_id = input("Enter the Book ID of the book you want to edit: ").strip()

    # Load book lists from both files
    book_list = load_books("BookList.txt")
    available_books = load_books("availablebooks.txt")

    if book_list is None or available_books is None:
        return  # Exit if files couldn't be loaded

    # Find and edit the book in both lists
    book_found = False
    for book in book_list:
        if book[0] == book_id:
            book_found = True
            print("Current details:")
            print("BookID | Title | Author | Publisher |")
            print(" | ".join(book) + "\n")

            # Get new values or keep current ones
            new_title = input("Enter new Book Title (leave blank to keep current): ") or book[1]
            new_author = input("Enter new Author (leave blank to keep current): ") or book[2]
            new_publisher = input("Enter new Publisher (leave blank to keep current): ") or book[3]

            # Confirm changes
            confirm = input("Do you want to save changes? (yes/no): ").strip().lower()
            while confirm not in {"yes", "no"}:
                print("Invalid input! Enter again.")
                confirm = input("Do you want to save changes? (yes/no): ").strip().lower()

            if confirm == "yes":
                # Update book details
                book[1], book[2], book[3] = new_title, new_author, new_publisher

                # Update in available_books if found
                for av_book in available_books:
                    if av_book[0] == book_id:
                        av_book[1], av_book[2], av_book[3] = new_title, new_author, new_publisher

                # Save changes to both files
                save_books("BookList.txt", book_list)
                save_books("availablebooks.txt", available_books)

                print("Book details updated successfully.")
            else:
                print("Changes not saved.")
            break

    if not book_found:
        print("Book not found!")

def remove_book():
    book_id = input("Enter the ID of the book you want to remove from the catalogue: ")

    try:
        with open("availablebooks.txt", "r") as AvFile:
            for line in AvFile:
                BookNotLent = line.strip().split(" | ")
                if BookNotLent[0] == book_id:
                    def update_file(file_name, book_id):
                        books = []
                        book_found = False
                        try:
                            # Read and filter books in the file
                            with open(file_name, "r") as file:
                                for line in file:
                                    book = line.strip().split(" | ")
                                    if book[0] != book_id:  # Keep book if ID doesn't match
                                        books.append(book)
                                    else:
                                        book_found = True  # Mark as found for message output

                            # Write updated list back to file
                            with open(file_name, "w") as file:
                                for book in books:
                                    file.write(" | ".join(book) + "\n")

                            return book_found

                        except FileNotFoundError:
                            print(f"File '{file_name}' not found!")
                            return False

                    # Update both files and check if the book was found
                    found_in_catalogue = update_file("BookList.txt", book_id)
                    found_in_available_books = update_file("availablebooks.txt", book_id)

                    # Provide feedback to the user
                    if found_in_catalogue or found_in_available_books:
                        print("Book removed.")
                        return
                    else:
                        print("Book not found!")
                        return

            print("Book is lent to members. So, cannot remove.")
    except FileNotFoundError:
        print("availablebooks.txt file is not found.")

def MemberID_exist(memberid):
    exist = False
    try:
        with open("members.txt", "r") as file:
            for line in file:
                #Skip empty lines
                if not line.strip():
                    continue

                parts = [part.strip() for part in line.strip().split(" | ")]

                if len(parts) >= 6:  # Ensure there are enough columns
                    existing_memberid = parts[0]
                    if existing_memberid == memberid:
                        exist = True

        return exist

    except FileNotFoundError:
        print ("File not found!")
        return False

import datetime
def Process_BookLoan():
    Book_ID = input("Enter the Book ID of the book you want to loan: ")
    MemberID = input("Enter the member ID of the member to whom the book is being loaned: ")

    # Check for valid member and book ID
    while not MemberID_exist(MemberID):
        print("Member ID not found in system. Make sure it is in the 'MEM####' format.")
        MemberID = input("Enter the member ID of the member to whom the book is being loaned: ")

    while not BookID_exist(Book_ID):
        print("Book ID not found in system. Make sure it is in the 'B####' format.")
        Book_ID = input("Enter the Book ID of the book you want to loan: ")

    # Load borrowed books and available books data
    membersBorrowed = load_books("MemberBorrowedBooksInfo.txt")
    available_books = load_books("availablebooks.txt")

    if membersBorrowed is None or available_books is None:
        return

    header, *entries = membersBorrowed
    updated_lines = [header]  # Start with header for new file data
    member_found = False
    book_already_loaned = False

    # Process member borrowing information
    for line in entries:
        row = line
        if len(row) != 5:
            updated_lines.append(line)
            continue

        # If member is found, update their book list
        if row[0].strip() == MemberID:
            member_found = True
            books = [b.strip() for b in row[1].split(", ")]

            if len(books) >= 5:
                print("You cannot borrow more than 5 books! Book loan cannot be processed.")
                return

            # Add the book if not already loaned
            if len(books) > 1:
                books.append(Book_ID)
                row[1] = ", ".join(books)
                updated_lines.append(row)
                book_already_loaned = True
            else:
                updated_lines.append(row)

        else:
            updated_lines.append(row)

    # If member is new, add them with their book and default values
    if not member_found:
        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=7)
        data = [MemberID, Book_ID, due_date.strftime("%d/%m/%Y"), "0", "-"]
        updated_lines.append(data)

    # Save updated MemberBorrowedBooksInfo.txt
    save_books("MemberBorrowedBooksInfo.txt", updated_lines)

    # Update availablebooks.txt by removing the loaned book
    available_books_updated = [book for book in available_books if book[0] != Book_ID]
    save_books("availablebooks.txt", available_books_updated)

    print(f"Book '{Book_ID}' loaned successfully to member '{MemberID}'.")

def Librarian_menu():
    Librarian_login()

    print("|__________________________________|")
    print("|_______Welcome Librarians_________|")
    print("|_What do you wish to do?__________|")
    print("|__1. Add new book in catalogue____|")
    print("|__2. View books in catalogue______|")
    print("|__3. Search books in catalogue____|")
    print("|__4. Edit books' info in catalogue|")
    print("|__5. Remove books from catalogue__|")
    print("|__6. Book loan to members_________|")
    print("|__7. Logout_______________________|")
    print("|__________________________________|")

    choice = int(input("\nDo you wish to continue(1) or exit back to main menu(2)? Enter either 1/2: "))
    while choice < 1 or choice > 2:
        choice = int(input("Invalid! Enter again: "))

    while choice == 1:
        print("|__________________________________|")
        print("|_______Welcome Librarians_________|")
        print("|_What do you wish to do?__________|")
        print("|__1. Add new book in catalogue____|")
        print("|__2. View books in catalogue______|")
        print("|__3. Search books in catalogue____|")
        print("|__4. Edit books' info in catalogue|")
        print("|__5. Remove books from catalogue__|")
        print("|__6. Book loan to members_________|")
        print("|__7. Logout_______________________|")
        print("|__________________________________|")

        option = int(input("\nWhat do you wish to do?(1-7): "))
        while option < 1 or option  > 7:
            option = int(input("Invalid! Choose from the 7 options displayed: "))

        if option == 1:
            add_book()
        elif option == 2:
            View_BookList()
        elif option == 3:
            detail = int(input("Do you want to search by BookID(1) or Book title(2): "))
            while detail < 1 or detail > 2:
                detail = int(input("Enter only 1/2: "))
            if detail == 1:
                Data = input("Enter the Book ID: ")
            else:
                Data = input("Enter the Book Title: ")
            SearchBook(detail, Data)
        elif option == 4:
            edit_book_info()
        elif option == 5:
            remove_book()
        elif option == 6:
            Process_BookLoan()
        else:
            print("Logging out...")
            return
        choice = int(input("\nDo you wish to continue(1) or exit back to main menu(2)? Enter either 1/2: "))
        while choice < 1 or choice > 2:
            choice = int(input("Invalid! Enter again: "))
        if choice == 2:
            print("Exiting...")
            return



#System administration( Staff)
# Constants for file names
MEMBERS_FILE = "members.txt"
LIBRARIANS_FILE = "librarians.txt"


#Member Info Management
def add_user(user_type):
    counter = ["Firstname", "Lastname", "Email address", "Contact Number", "Password"]
    ListDetails = ["", "", "", "", ""]
    counts = 0
    while counts < len(counter):
        while len(ListDetails[counts]) == 0:  # Presence check
            ListDetails[counts] = input(f"Enter {counter[counts]}: ")
            if len(ListDetails[counts]) == 0:
                print("It is mandatory to fill up this field.")

        # Length check for contact number
        if counter[counts] == "Contact Number":
            ContactNumber = ValidateContactNumber(ListDetails[3])
            while ContactNumber == False:
                print("Invalid phone number! The phone number should be in this format: +60 11 1234 1234")
                ListDetails[counts] = input(f"Enter your {counter[counts]}: ")
                ContactNumber = ValidateContactNumber(ListDetails[3])

        # Checking if password entered is a strong password
        if counter[counts] == "Password":
            StrongUserPassword = StrongPassword(ListDetails[-1])
            while not StrongUserPassword:
                print("Password is not strong enough! Your password should be at least 8 characters long and must contain the following:")
                PasswordCredentials = [
                    "1. At least 1 UpperCase letter; W,S,D,R",
                    "2. At least 1 special symbol; @,!,&,*",
                    "3. At least 1 digit; 0,1,2,3",
                    "4. At least 1 lowercase letter; w,s,d,r"
                ]
                for requirement in PasswordCredentials:
                    print(requirement)
                ListDetails[-1] = input("Enter password again: ")
                StrongUserPassword = StrongPassword(ListDetails[-1])

        # Checking if the email already exists
        if counter[counts] == "Email address":
            file_to_check = MEMBERS_FILE if user_type == "member" else LIBRARIANS_FILE
            exists = check_existing_user(ListDetails[2], file_to_check)
            if exists:
                print("This account already exists. Try logging in!")
                return  # Stop the sign-up process if email already exists

        counts += 1

        # Once all details are collected, save the user details
    if user_type == "member":
        user_id = generate_unique_member_id()  # Generate a unique member ID
    else:
        user_id = generate_librarian_id()  # Generate a unique librarian ID

    firstname, lastname, email, contact_number, password = ListDetails

    if user_type == "member":
        with open(MEMBERS_FILE, 'a') as file:
            file.write(f"{user_id} | {firstname} | {lastname} | {email} | {contact_number} | {password}\n")
    else:
        with open(LIBRARIANS_FILE, 'a') as file:
            file.write(f"{user_id} | {firstname} | {lastname} | {email} | {contact_number} | {password}\n")

    print(f"{user_type.capitalize()} signed up successfully with ID: {user_id}.")
    go_back()
def go_back():
    """Prompt user to go back to the main menu or exit."""
    while True:
        choice = input("Do you want to go back to the main menu? (yes/no): ").strip().lower()
        if choice == 'yes':
            admin_menu()
            return
        elif choice == 'no':
            print("Exiting.....😔")
            exit()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
def view_members():
    """View all members."""
    try:
        with open("members.txt", "r") as file:
            print("Here is the list of all members:")
            for line in file:
                print(line)
    except FileNotFoundError:
        print("Error! File not found.")
def search_member():
    """Search for a member."""
    detail = int(input("Do you want to search by Member ID(1) or member's Email address(2): "))
    while detail < 1 or detail > 2:
        detail = int(input("Enter only 1/2: "))
    if detail == 1:
        membID = input("Enter the Member ID of the member to search: ")
    else:
        email = input("Enter the email address of the member to search: ")
        email = email.lower()#In case email address is wrongly written in upperccase
    try:
        with open("members.txt", 'r') as file:
            members = file.readlines()
            for member in members:
                if detail == 2:
                    if email in member :
                        print("Member found: ")
                        print("MemberID | Firstname | Lastname | Email address | Contact Number |  Password")
                        print(f"{member}")
                        return
                if detail == 1:
                    if membID in member:
                        print("Member found: ")
                        print("MemberID | Firstname | Lastname | Email address | Contact Number |  Password")
                        print(f"{member}")
                        return
            print("Member not found!")
    except FileNotFoundError:
        print("No members file found.")
def edit_member():
    member_id = input("Enter the Member ID to edit: ").strip()
    members = []
    exists = False

    # Load existing members from the file
    try:
        with open(MEMBERS_FILE, 'r') as file:
            for line in file:
                members.append(line.strip().split(" | "))
    except FileNotFoundError:
        print("No user data found.")
        return

    # Find the member to edit
    for member in members:
        if member[0] == member_id:
            print("Current details:")
            print(f"ID: {member[0]}, Name: {member[1]} {member[2]}, Email: {member[3]}, Contact Number: {member[4]}")

            # Get new values or keep current ones
            new_firstname = input("Enter new First Name (leave blank to keep current): ").strip() or member[1]
            new_lastname = input("Enter new Last Name (leave blank to keep current): ").strip() or member[2]

            # Check if the new email is already taken
            while True:
                new_email = input("Enter new Email (leave blank to keep current): ").strip() or member[3]
                if new_email != member[3] and check_existing_user(new_email, MEMBERS_FILE):
                    print("This email already exists. Please enter a different email.")
                else:
                    break

            # Validate new contact number
            while True:
                new_contact = input("Enter new Contact Number (leave blank to keep current): ").strip() or member[4]
                if new_contact != member[4] and not ValidateContactNumber(new_contact):
                    print("Invalid phone number! It should be in this format: +60 11 1234 1234 and unique.")
                else:
                    break

            # Confirm changes
            confirm = input("Do you want to save changes? (yes/no): ").strip().lower()
            if confirm == 'yes':
                # Update the member details
                member[1] = new_firstname
                member[2] = new_lastname
                member[3] = new_email
                member[4] = new_contact

                # Write updated members back to file
                with open(MEMBERS_FILE, 'w') as file:
                    for m in members:
                        file.write(" | ".join(m) + "\n")

                print("Member details updated successfully.")
            else:
                print("Changes not saved.")
            return

    print("Member not found!")
def remove_member():
    """Remove a member."""
    detail = int(input("Do you want to remove member by Member ID(1) or member's Email address(2): "))
    while detail < 1 or detail > 2:
        detail = int(input("Enter only 1/2: "))
    if detail == 1:
        membID = input("Enter the Member ID of the member to remove: ")
    else:
        email = input("Enter the email address of the member to remove: ")
        email = email.lower()  # In case email address is wrongly written in uppercase
    members = []
    member_found = False

    try:
        with open(MEMBERS_FILE, 'r') as file:
            members = file.readlines()
    except FileNotFoundError:
        print("No members file found.")
        return

    for i, member in enumerate(members):
        if detail == 2:
            if email in member:
                member_found = True
                del members[i]
                break
        if detail == 1:
            if membID in member:
                member_found = True
                del members[i]
                break

    if not member_found:
        print("Member not found!")
    else:
        with open(MEMBERS_FILE, 'w') as file:
            file.writelines(members)
        print("Member removed.")
def manage_members():
    """Displays the manage members menu and handles user choices."""
    continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
    while continue_choice != "yes" and continue_choice != "no":
        print("invalid input!")
        continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
    while continue_choice == "yes":
        print("\n|------------------------------------|")
        print("|------Manage Members----------------|")
        print("|------------------------------------|")
        print("| 1. View All Members                |")
        print("| 2. Add New Member                  |")
        print("| 3. Search Member                   |")
        print("| 4. Edit Member                     |")
        print("| 5. Remove Member                   |")
        print("| 6. Back to Admin Menu              |")
        print("|------------------------------------|")

        choice = int(input("\nEnter choice(1-6): "))
        while choice < 1 or choice > 6:
            print("Invalid Input!")
            choice = input("Enter choice(1-6): ")

        if choice == 1:
            view_members()  # Placeholder function
        elif choice == 2:
            add_user("member")  # Call add_member function for member
        elif choice == 3:
            search_member()  # Placeholder function
        elif choice == 4:
            edit_member()  # Placeholder function
        elif choice == 5:
            remove_member()  # Placeholder function
        elif choice == 6:
            admin_menu()
            return

            # Ask user if they want to continue or exit
        continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
        while continue_choice != "yes" and continue_choice != "no":
            print("invalid input!")
            continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
        if continue_choice == 'no':
            admin_menu()
            return

#Librarian Info Management
def generate_librarian_id():
    """Generate a unique librarian ID (placeholder)."""
    return "LIB" + str(1000 + len(open(LIBRARIANS_FILE).readlines()))  # Simple ID generation
def view_librarians():
    """View all librarians."""
    try:
        with open(LIBRARIANS_FILE, 'r') as file:
            librarians = file.readlines()
            if librarians:
                print("\n|------ Librarians List ------|")
                for librarian in librarians:
                    print(librarian)
            else:
                print("No librarians found.")
    except FileNotFoundError:
        print("No librarians file found.")
def search_librarian():
    """Search for a librarian."""
    detail = int(input("Do you want to search by Librarian ID(1) or librarian's Email address(2): "))
    while detail < 1 and detail > 2:
        detail = int(input("Enter only 1/2: "))
    if detail == 1:
        LibID = input("Enter the Librarian ID of the librarian to search: ")
    else:
        email = input("Enter the email address of the librarian to search: ")
        email = email.lower()#In case email address is wrongly written in upperccase
    try:
        with open(LIBRARIANS_FILE, 'r') as file:
            librarians = file.readlines()
            for librarian in librarians:
                if detail == 2:
                    if email in librarian:
                        print("Librarian found:")
                        print("Librarian ID | First Name | Last Name | Email Address | Contact Number | Password")
                        print(f"{librarian}")
                        return
                if detail == 1:
                    if LibID in librarian:
                        print("Librarian found:")
                        print("Librarian ID | First Name | Last Name | Email Address | Contact Number | Password")
                        print(f"{librarian}")
                        return
            print("Librarian not found.")
    except FileNotFoundError:
        print("No librarians file found.")
def edit_librarian():
    """Edit an existing librarian's details."""
    librarian_id = input("Enter the Librarian ID to edit: ")
    librarians = []

    # Load existing librarians from the file
    with open(LIBRARIANS_FILE, 'r') as file:
        for line in file:
            librarians.append(line.strip().split(" | "))

    # Find the librarian to edit
    for librarian in librarians:
        if librarian[0] == librarian_id:
            print("Current details:")
            print(f"ID: {librarian[0]}, Name: {librarian[1]} {librarian[2]}, Email: {librarian[3]}, Contact Number: {librarian[4]}")

            # Get new values or keep current ones
            new_firstname = input("Enter new First Name (leave blank to keep current): ") or librarian[1]
            new_lastname = input("Enter new Last Name (leave blank to keep current): ") or librarian[2]

            # Check if the new email is already taken
            while True:
                new_email = input("Enter new Email (leave blank to keep current): ").strip() or librarian[3]
                if new_email != librarian[3] and check_existing_user(new_email, LIBRARIANS_FILE):
                    print("This email already exists. Please enter a different email.")
                else:
                    break

            # Validate new contact number
            while True:
                new_contact = input("Enter new Contact Number (leave blank to keep current): ").strip() or librarian[4]
                if new_contact != librarian[4] and not ValidateContactNumber(new_contact):
                    print("Invalid phone number! It should be in this format: +60 11 1234 1234 and unique.")
                else:
                    break

            # Confirm changes
            confirm = input("Do you want to save changes? (yes/no): ").strip().lower()
            if confirm == 'yes':
                # Update the librarian details
                librarian[1] = new_firstname
                librarian[2] = new_lastname
                librarian[3] = new_email
                librarian[4] = new_contact

                # Write updated librarians back to file
                with open(LIBRARIANS_FILE, 'w') as file:
                    for l in librarians:
                        file.write(" | ".join(l) + "\n")

                print("Librarian details updated successfully.")
            else:
                print("Changes not saved.")
            return

    print("Librarian not found!")
def remove_librarian():
    """Remove a librarian."""
    detail = int(input("Do you want to remove Librarian by Librarian ID(1) or librarian's Email address(2): "))
    while detail < 1 or detail > 2:
        detail = int(input("Enter only 1/2: "))
    if detail == 1:
        LibID = input("Enter the Librarian ID, of the librarian, to remove: ")
    else:
        email = input("Enter the email address of the librarian to remove: ")
        email = email.lower()  # In case email address is wrongly written in uppercase

    librarian_found = False
    librarians = []

    try:
        with open(LIBRARIANS_FILE, 'r') as file:
            librarians = file.readlines()
    except FileNotFoundError:
        print("No librarians file found.")
        return

    for i, librarian in enumerate(librarians):
        if detail == 2:
            if email in librarian:
                librarian_found = True
                del librarians[i]
                break
        if detail == 1:
            if LibID in librarian:
                librarian_found = True
                del librarians[i]
                break
    if not librarian_found:
        print("Librarian not found")
    else:
        with open(LIBRARIANS_FILE, 'w') as file:
            file.writelines(librarians)
        print("Librarian removed.")
def manage_librarians():
    continue_choice = input("Do you want to continue managing librarians? (yes/no): ").strip().lower()
    while continue_choice != "yes" and continue_choice != "no":
        print("invalid input!")
        continue_choice = input("Do you want to continue managing librarians? (yes/no): ").strip().lower()
    """Displays the manage librarians menu and handles user choices."""
    while continue_choice == "yes":
        print("\n|----------------------------------|")
        print("|      Manage Librarians           |")
        print("|----------------------------------|")
        print("| 1. View All Librarians           |")
        print("| 2. Add New Librarian             |")
        print("| 3. Search Librarian              |")
        print("| 4. Edit Librarian                |")
        print("| 5. Remove Librarian              |")
        print("| 6. Back to Admin Menu            |")
        print("|----------------------------------|")

        choice = input("\nEnter choice: ")
        while choice < '1' or choice > "6":
            print("Invalid input!")
            choice = input("\nEnter choice: ")
        if choice == '1':
            view_librarians()  # Placeholder function
        elif choice == '2':
            add_user("librarian")  # Call sign-up function for librarian
        elif choice == '3':
            search_librarian()  # Placeholder function
        elif choice == '4':
            edit_librarian()  # Placeholder function
        elif choice == '5':
            remove_librarian()  # Placeholder function
        elif choice == '6':
            admin_menu()
            return

        # Ask user if they want to continue or exit
        continue_choice = input("Do you want to continue managing librarians? (yes/no): ").strip().lower()
        while continue_choice != "yes" and continue_choice != "no":
            print("invalid input!")
            continue_choice = input("Do you want to continue managing librarians? (yes/no): ").strip().lower()
        if continue_choice == 'no':
            admin_menu()
            return

#Admin menu
def admin_login():
    """Handles the admin login process with retry mechanism."""
    correct_username = "admin"
    correct_password = "12546"
    max_attempts = 3
    attempt_count = 0

    while attempt_count < max_attempts:
        username = input("Enter the username: ").strip()
        password = input("Enter the password: ").strip()

        if username == correct_username and password == correct_password:
            print("Login Successful")
            admin_menu()
            return
        else:
            attempt_count += 1
            if attempt_count < max_attempts:
                print(f"Login Failed. You have {max_attempts - attempt_count} attempt(s) left.")
            else:
                print("Login failed. Exiting...")
                exit()
def admin_menu():
    """Displays the admin menu and handles user choice."""
    print("\n|------------------------------------|")
    print("|-----------Admin Menu---------------|")
    print("| 1. Manage Members                  |")
    print("| 2. Manage Librarians               |")
    print("| 3. Logout                          |")
    print("|------------------------------------|")
    choice = input("Enter choice: ")
    if choice == '1':
        manage_members()
    elif choice == '2':
        manage_librarians()
    elif choice == '3':
        print("Logging out...")
        show_admin_menu()
    else:
        print("Invalid choice. Try again.")
        admin_menu()
def show_admin_menu():
    """Displays the login menu and handles user choice."""
    print("\n|------------------------------------------------|")
    print("|   Welcome to the Admin Management System     |")
    print("|------------------------------------------------|")
    print("| 1.  Admin Login                                |")
    print("| 2.  Exit                                       |")
    print("|------------------------------------------------|")
    choice = input("Enter choice: ")
    if choice == '1':
        admin_login()
    elif choice == '2':
        print("Exiting.....😔")
        exit()
    else:
        print("Invalid choice. Try again.")
        show_admin_menu()



#Creating main menu
def menu():
    print("Welcome to Brickfields KL Library")
    print("--" * 20)

    continue_choice = input("Do you want to continue browsing Brickfields KL library? (yes/no): ").strip().lower()
    while continue_choice != "yes" and continue_choice != "no":
        print("invalid input!")
        continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
    while continue_choice == "yes":
        #Centering the text
        Text1, Text2 = "1: Non-Staff", "2: Staff"
        centered_text1 = Text1.center(24)
        centered_text2 = Text2.center(20)

        print(centered_text1)
        print(centered_text2)
        print("")

        #Inputting member's choice
        choice = input("Enter the purpose of your vist (1/2): ")

        #validating choice
        while choice != "1" and choice != "2":
            choice = input("Invalid! Enter again from the 2 choices(1/2): ")

        print("--" * 20)
        if choice == "1":
            menu_member()

        #Creating menu for staff
        if choice == "2":
            #Centering new text
            Text1, Text2 = "1: Librarian", "2: System Administrator"
            centered_text1 = Text1.center(20)
            centered_text2 = Text2.center(32)

            print(centered_text1)
            print(centered_text2)
            print("")

            choice1 = input("Enter your profession: ")

             # validating choice
            while choice1 != "1" and choice1 != "2":
                choice1 = input("Invalid! Enter again from the 2 choices(1/2): ")

            if choice1 == "1":
                Librarian_menu()
            else:
                show_admin_menu()

        continue_choice = input("Do you want to continue browsing Brickfields KL library? (yes/no): ").strip().lower()
        while continue_choice != "yes" and continue_choice != "no":
            print("invalid input!")
            continue_choice = input("Do you want to continue managing members? (yes/no): ").strip().lower()
        if continue_choice == 'no':
            print("Exiting Browsing...")
            print("Opening Browsing page for next user... ")
            menu()

#System starts here
if __name__ == "__main__":
    menu()