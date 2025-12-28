# There are many interesting things to look out for in this code, but some of the ones that gave me particular joy are:

# Client-Server Model
# Hashing to store sensitive information
# Complex business model
# Aggregate SQL functions
# JSON parsing
# Abstract data types
# Calling parameterized web service APIs - The token is no longer valid
# User-generated DDL scripts
# A complex data model within a database
# In the standard Python installation, you should have access to many of the imported libraries. 
# However, you will need to install mysql.connector (for database-related content), matplotlib (for mathematical and list operations), and requests (for API access).
# All libraries are free!


# These functions are recycled throughout the program. They have a very unique, narrow functionality.
# However, they are required a number of times, and hence have been predefined first.

def send_email(code, receiver_email, mycursor, db):  # -Used to send email verification codes
    # *CLIENT-SERVER MODEL* Accessing Gmail SMPTP sever to send emails. The default context of ssl validates
    # the host name and its certificates and optimizes the security of the connection 
    port = 465  # standard port for SMTP over SSL
    smtp_server = "smtp.gmail.com"  # initiate a TLS-encrypted connection
    mycursor.execute("select preference_value from preference where preference_name = 'email'")
    sender_email = mycursor.fetchall()[0][
        0]  # *SINGLE TABLE  SQL*, selects the email address used to send codes
    password = "DHINSA1210"  # When the code is distributed, an assumption is made that it is distributed in an 
    # executable file. Hence, leaving the plaintext password in the script does not cause issue. 
    message = message = """\
    Subject: Password reset code
    



    Please use the following code"""
    message = message + "\n" + str(code) + "\n if this doesn't apply to you, please ignore"
    context = ssl.create_default_context()  # create a secure SSL context
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)  # Login to email sever
            server.sendmail(sender_email, receiver_email, message)  # send message to appropriate receiver
    except smtplib.SMTPRecipientsRefused and socket.gaierror and smtplib.SMTPRecipientsRefused:
        pass
        # invalid email address is accounted for. The user will not be told they have entered an invalid user,
        # as it is common practice not to do so, preventing Bruteforce


def remove_all(window):  # Clears the screen
    for widget in window.winfo_children():  # Iterates through all widgets in the Window
        widget.destroy()  # Removes each widget in the window


def create_menu(logged_in, username, admin, db, mycursor, window):
    # The cascade bar which allows the user the ability to easily navigate the Applications features REQUIREMENT 8.3
    menu = Menu(window)
    new_menu_item = Menu(menu)
    new_menu_item.add_command(label='Menu',
                              command=lambda: initialise_window("already in", username, admin, db, mycursor, window))
    new_menu_item.add_separator()
    new_menu_item.add_command(label='Till',
                              command=lambda: till_menu(logged_in, username, admin, db, mycursor, window, None, None))
    new_menu_item.add_separator()
    if admin == 1:  # The Certain features that are only accessible by admin Users, are contained within this 
        # conditional statement. REQUIREMENT 1.2 
        new_menu_item.add_command(label='View Sales',
                                  command=lambda: view_sales(logged_in, username, admin, db, mycursor, window))
        new_menu_item.add_separator()
        new_menu_item.add_command(label='Manage Recipe',
                                  command=lambda: recipe_menu(logged_in, username, admin, db, mycursor, window))
        new_menu_item.add_separator()
        new_menu_item.add_command(label='Manage Stock',
                                  command=lambda: manage_stock(logged_in, username, admin, db, mycursor, window))
        new_menu_item.add_separator()
        new_menu_item.add_command(label='Manage Users',
                                  command=lambda: manage_users_menu(logged_in, username, admin, db, mycursor, window))
        new_menu_item.add_separator()
        new_menu_item.add_command(label='Manage Preferences',
                                  command=lambda: preference_menu(logged_in, username, admin, db, mycursor, window))
        new_menu_item.add_separator()
    new_menu_item.add_command(label='Change Password',
                              command=lambda: change_password("already in", username, admin, db, mycursor, window))
    new_menu_item.add_separator()
    new_menu_item.add_command(label='Logout',
                              command=lambda: initialise_window("relog", username, admin, db, mycursor, window))
    new_menu_item.add_separator()
    new_menu_item.add_command(label='Close Program', command=lambda: end(window, db))
    new_menu_item.add_separator()
    menu.add_cascade(label='Options', menu=new_menu_item)
    window.config(menu=menu)


def end(window, db):  # - Used to end the program, after closing all existing connections
    if db is not None:  # Before the connection to the database is made, the user may decide to close the program
        # If they do, then the variable, 'db' will currently not be assigned a value, hence be NoneType.
        db.close()  # Closes the connection to the database
    window.destroy()  # Deletes the window
    window.mainloop()  # Close the Tkinter Sequence
    quit()  # End Program


def display_logo(mycursor):  # -Used to display the company Logo. REQUIREMENT 8.5 
    mycursor.execute("select preference_value from preference where preference_name = 'file path-picture'")
    file_path = mycursor.fetchone()[0]  # Selecting the value which holds the file path of the logo from the Database
    try:
        canvas = Canvas(window, width=300, height=300, bg='blanched almond', bd=0, highlightthickness=0, relief='ridge')
        canvas.place(relx=.5, rely=.4, anchor="n")
        photo = PhotoImage(file=file_path)
        label = Label(image=photo)  # creating a canvas which allows the image to be Embedded in the existing window
        label.image = photo
        canvas.create_image(20, 20, anchor=NW, image=label.image)
    except FileNotFoundError and TclError:  # account for the possibility the filepath doesn't
        # contain a displayable image
        connection_not_found_error = Label(window, text="Logo file Not found, \nPlease Check Preferences")
        connection_not_found_error.config(bg='blanched almond')
        connection_not_found_error.config(font=("Times New Roman", 40, 'italic'))
        connection_not_found_error.place(relx=.5, rely=.4, anchor="n")


def time(clock):  # - displays the time, REQUIREMENT 8.4
    current_time = str(datetime.now().strftime("%H:%M"))  # The current time is acquired from the system clock
    clock.config(text=current_time)
    clock.after(1000, lambda: time(clock))  # *RECURSIVE ALGORITHM* -Every second the sub-routine will call
    # itself, to refresh the time. 


def initialise_window(logged_in, username, admin, db, mycursor, window):
    # The tkinter window object is created and configured to a specific size, as well as to avoid the colours green or
    # blue REQUIREMENT 8.1 The initial window serves as the home screen 
    if logged_in == "already in" or logged_in == "relog":
        remove_all(window)  # If the menu has been selected at anypoint once the user is already logged in, 
        # the screen must be cleared 
    if logged_in == "False":  # If the user is not currently, or hasn't previously logged in, then the window must be 
        # made 
        window = Tk()  # Instantiating the Tkinter Window object
        window.title("Food State Nutrition-Login")  # Indicating the user is about to be asked to login to both MYSQL
        # then 
        # their unique portal 
        window.geometry("600x600+200+200")  # Initial size of window, though resizeable
        window.configure(bg="blanched almond")
        window.resizable(0, 0)
        return window  # bring the window to the main program
    if logged_in == "relog":  # if the user has chosen to logout of their portal, then the window is wiped, and they 
        # are taken to the the login screen 
        remove_all(window)
        login(mycursor, window, logged_in, db)
    if logged_in == "True" or logged_in == "already in":  # If the menu has been selected at anypoint once the user 
        # is already logged in, then the cascade bar is created 
        remove_all(window)
        window.title("Food State Nutrition-Menu")  # Indicating the user is at the main menu
        mycursor.execute("select email from User where user_id = 1")  # *SINGLE TABLE  SQL*, selects the 
        # email for the first user 
        email = mycursor.fetchall()[0][0]
        clock = Label(window, font=('calibri', 40, 'bold'),
                      background='blanched almond')  # configure the clock label which is visable on the home screen
        clock.place(relx=.5, rely=.1, anchor="n")
        display_logo(mycursor)
        if email is not None:  # if the program has been loaded for the first time, an email must be provided for the 
            # first account 
            create_menu(logged_in, username, admin, db, mycursor, window)
            time(clock)
            title = Label(window, text="Food State Nutrition™\n        - Menu")
            title.config(bg='blanched almond')
            title.config(font=("Times New Roman", 30))
            title.place(x=70, y=125)
            username_diplay = Label(window, text="Current User is " +username)
            username_diplay.config(bg='blanched almond')
            username_diplay.config(font=("Times New Roman", 12, 'italic'))
            username_diplay.place(x=10, y=10)

            #display the current temperature in the store location
            mycursor.execute("Select preference_value from preference where preference_name = 'Current City'")
            city = mycursor.fetchone()  # *SINGLE TABLE SQL*, select the Current City of where the store is located
            city = (city[0])
            mycursor.execute("Select preference_value from preference where preference_name = 'API KEY'")
            key = mycursor.fetchone()  # *SINGLE TABLE SQL*, select the current API KEY the manager has access to
            key = (key[0])
            try:  # *CALLING PARAMETERISED WEB SERVICE API* Allowing access to the temperature data
                query = 'q=' + city;
                information = get('https://api.openweathermap.org/data/2.5/weather?' + query +
                                  '&exclude=hourly,daily,minutely&appid=' + key + '&units=metric');  # The api has 
                # parameters which will access the data for the certain city, by having access granted by the users 
                # unique key 
                weather_data = information.json();  # *PARSING JSON*
                temperature = int(round((weather_data["main"][
                    "temp"])))  # *DICTIONARY* From the data collected, access the current temperature
                mycursor.execute("select preference_value from preference where preference_name = 'Warm Day Temp'")
                temp_warm = int(mycursor.fetchone()[0]) - 1
                mycursor.execute("select preference_value from preference where preference_name = 'Cold Day Temperature'")
                temp_cold = int(mycursor.fetchone()[0]) + 1
                display = "Temperature in " + city +" is " + str(temperature)+ "°C"
                # if the day meets the warm credentials, a plus would be displayed, if the day mets the cold creentials,
                #a minus is displayed
                if temperature > temp_warm:
                    display = display + " +"
                if temperature < temp_cold:
                    display = display + " -"
                temp_display = Label(window, text=display)
                temp_display.config(bg='blanched almond')
                temp_display.config(font=("Times New Roman", 12, 'italic'))
                temp_display.place(x=400, y=10)
            except KeyError and exceptions.ConnectionError:  # In the situation where there is no internet/api access
                pass
        else:
            establish_email(logged_in, username, admin, db, mycursor, window)


def db_in(window):
    # The user will be asked to enter their mysql credentials, to access their account
    remove_all(window)
    enter_info = Label(window, text="FoodState Nutrition ™")
    enter_info.config(bg='blanched almond')
    enter_info.config(font=("Blackadder IT", 30))
    enter_info.place(x=130, y=100)
    enter_db = Label(window, text="Database Name")
    enter_db.config(bg='blanched almond')
    enter_db.config(font=("Times New Roman", 12,))
    enter_db.place(x=250, y=200)
    enter_Pw = Label(window, text="Database Password")
    enter_Pw.config(bg='blanched almond')
    enter_Pw.config(font=("Times New Roman", 12, 'italic'))
    enter_Pw.place(x=240, y=280)
    db_username = StringVar()
    username_entry = Entry(window, textvariable=db_username, text=db_username, font=('Verdana', 15),
                           bg='blanched almond')
    db_username.set("")  # Enter username
    username_entry.place(x=170, y=230)
    db_password = StringVar()
    password_entry = Entry(window, textvariable=db_password, show="*", text=db_password, font=('Verdana', 15),
                           bg='blanched almond')
    db_password.set("")  # Enter Password
    password_entry.place(x=170, y=310)
    accept_data = Button(window, text="Enter",
                         command=lambda: database_connect(db_username, db_password, window, logged_in))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=350, y=400)
    exit_button = Button(window, text="Quit", command=lambda: end(window, None))
    exit_button.config(
        bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
    exit_button.config(height=1, width=20)
    exit_button.place(x=100, y=400)


def database_connect(db_username, db_password, window, logged_in):
    # Create the Database and Cursor Object
    try:
        found = True  # variable which indicates if the connection to the database is trying to be made to an already
        # existing database 
        db_password = db_password.get()  # Returns string from STRINGVAR class
        db_username = db_username.get()  # Returns string from STRINGVAR class
        db_cursor_tuple = connect(found, db_username, db_password)  # Returns the Database and Cursor objects
        db = db_cursor_tuple[0]
        mycursor = db_cursor_tuple[1]
        login(mycursor, window, logged_in, db)  # Proceed to login to unique portal
    except mysql.connector.errors.ProgrammingError:  # if the database does not yet exist
        found = False  # variable which indicates if the connection to the database is trying to be made to a new 
        # database 
        db_cursor_tuple = connect(found, db_username, db_password)  # Returns the Database and Cursor objects
        if type(db_cursor_tuple) == tuple:  # If the connection was able to be made
            db = db_cursor_tuple[0]
            mycursor = db_cursor_tuple[1]
            initialise_database(db, mycursor, db_username, db_password)  # Create Tables within database


def connect(found, db_username, db_password):
    # Connect to the Mysql account, providing the login details are correct
    remove_all(window)
    if found:  # variable which indicates if the connection to the database is trying to be made to an 
        # already existing database 
        db = mysql.connector.connect(  # attempt to connect to database and create object
            host="localhost",
            # the host will be the computer operating the application. If access to a server is ever obtained, 
            # this can be easily changed 
            user=db_username,  # User entered username
            passwd=db_password,  # User entered password
            database="FoodStateNutritiondb"  # Name of database
        )
        mycursor = db.cursor()  # Create cursor object 
        return db, mycursor
    else:  # indicates new database must be created
        try:
            db = mysql.connector.connect(
                host="localhost",
                # the host will be the computer operating the application. If access to a server is ever obtained, 
                # this can be easily changed 
                user=db_username,  # User entered username
                passwd=db_password,  # User entered password
            )
            mycursor = db.cursor()  # Create cursor object
            return db, mycursor
        except mysql.connector.errors.ProgrammingError:  # If a connection cannot be made to the Mysql account, 
            # display an appropriate error
            connection_not_found_error = Label(window, text="No Such Database Found")
            connection_not_found_error.config(bg='blanched almond')
            connection_not_found_error.config(font=("Times New Roman", 40, 'italic'))
            connection_not_found_error.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: db_in(window))


def initialise_database(db, mycursor, db_username, db_password):
    # *USER GENERATED DDL SCRIPT* Creating the database along with the tables required. 
    mycursor.execute("CREATE DATABASE FoodStateNutritionDB")  # create the database
    found = True  # connect to an already existing database
    db_cursor_tuple = connect(found, db_username,
                              db_password)  # generate new cursor and database object specific to FoodStateNutritionDB
    db = db_cursor_tuple[0]
    mycursor = db_cursor_tuple[1]
    mycursor.execute(
        "CREATE TABLE User (user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255),active BOOLEAN ,"
        "admin BOOLEAN, k3y VARBINARY(32), salt VARBINARY(32), email VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE Sales (sales_id INT PRIMARY KEY AUTO_INCREMENT,user_id INT, FOREIGN KEY (user_id) REFERENCES "
        "User(user_id), sales_date DATE, sales_temperature INT)")
    mycursor.execute(
        "CREATE TABLE Recipe (recipe_id INT PRIMARY KEY AUTO_INCREMENT, recipe_name VARCHAR (255), recipe_price£ "
        "FLOAT, recipe_is_active BOOLEAN)")
    mycursor.execute(
        "CREATE TABLE Ingredients (ingredients_id INT PRIMARY KEY AUTO_INCREMENT, ingredients_useable BOOLEAN,"
        "ingredients_name VARCHAR(255), ingredients_remaining_g int, ingredients_price_kg FLOAT)")
    mycursor.execute(
        "CREATE TABLE Sales_Recipe_Bridge (sr_bridge_id INT PRIMARY KEY AUTO_INCREMENT, sales_id INT, FOREIGN KEY ("
        "sales_id) REFERENCES Sales(sales_id), recipe_id INT, FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),"
        "sales_price float)")
    mycursor.execute(
        "Create Table Recipe_Ingredients_Bridge (ri_bridge_id INT PRIMARY KEY AUTO_INCREMENT, ingredients_id INT, "
        "FOREIGN KEY (ingredients_id) REFERENCES Ingredients(ingredients_id), recipe_id INT, FOREIGN KEY (recipe_id) "
        "REFERENCES Recipe(recipe_id), quantity_of_ingredients_g INT)")
    mycursor.execute(
        "Create Table preference(preference_id INT PRIMARY KEY AUTO_INCREMENT, preference_name VARCHAR (255), "
        "preference_value varchar(255))")
    # *COMPLEX DATA MODEL IN DATABASE* The creation of 6 interlinked tables, as described in previously 
    # designed BY Entity Relationship Diagram
    filename = path.join(path.join(environ['USERPROFILE']),
                         'Desktop') + "//Sales_data.csv"  # Create filepath for taxation file which will be located 
    # initially on the desktop. This will make use of the path and environ modules from the OS library 
    filename_picture = path.join(path.join(environ['USERPROFILE']),
                                 'Desktop') + "//logo.png"  # Create filepath for the logo which will be located 
    # initially on the desktop. This will make use of the path and environ modules from the OS library 
    f = open(filename, "w")  # *TEXT FILE* Creating a form of plain text file, known by the acronym CSV 
    headers = "sale_id, recipe name,cashier,sale date,sale price,sale cost,sale profit\n"
    f.write(headers)  # *WRITING TO FILE* Write the relevant headers of the file, formatting it for later 
    # data entries 
    f.close()
    values = [("API KEY", "277a74884dc804db07f47f808ff06ff3"), ("Warm Day Temp", "20"), ("Cold Day Temperature", "10"),
              ("Current City", "derby"), ("Large Cup Ratio", "20"), ("Small Cup Ratio", "20"),
              ("file path-csv", filename), ("file path-picture", filename_picture),
              ("email", "foodstatenutrition@gmail.com")]
    for i in values:  # Insert default preference values, which can be later altered at the users convenience
        mycursor.execute("INSERT INTO preference(preference_name,preference_value) VALUES (%s,%s)", (i[0], i[1]))
    db.commit()  # Save all changes made to the database
    first_user = True  # The first user will have the password 101, and username admin. They will be expected to 
    # change this immediately 
    create_user("admin", "101", True, mycursor, db, first_user, None, None, window, None)


# The following routines show how the first user portal is created, as well as allowing the user a route to login to 
# their own portal, if they have the correct information. The routine to create the first user, is used later in the 
# application to create all other users after this point. Additionally in this section, the ability to change 
# passwords is present, as many of the modules used in that process, overlap here Meeting client requirement 1 


def create_user(username, password, admin, mycursor, db, first_user, current_user, current_admin, window, email):
    # *HASHING* When creating a user, the details must be hashed as explained in the design to ensure 
    # sensitive content remains safe 
    salt = urandom(32)  # Using the urandom module from the OS library, generate 32 random bytes of data
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)  # invoking the key derivation function, 
    # converting it to binary, with the salt, and iterating it 100000 times 
    users = {username: {
        'salt': salt,
        'admin': admin,
        'key': key, }}
    # *SINGLE TABLE PARAMETRISED SQL* Create new users, with parametrised credentials 
    if first_user:  # If the first user has just been created, proceed to login
        mycursor.execute("INSERT INTO User(username,active,admin,salt,k3y) VALUES (%s,%s,%s,%s,%s)",
                         (username, True, users[username]["admin"], users[username]["salt"], users[username]["key"]))
        db.commit()  # Database changes are saved
        login(mycursor, window, logged_in, db)
    else:  # If this is not the first user, return to manage user menu
        mycursor.execute("INSERT INTO User(username,active,admin,salt,k3y,email) VALUES (%s,%s,%s,%s,%s,%s)", (
            username, True, users[username]["admin"], users[username]["salt"], users[username]["key"], email))
        db.commit()  # Database changes are saved
        window.after(3000, lambda: manage_users_menu(logged_in, current_user, current_admin, db, mycursor, window))


def login(mycursor, window, logged_in, db):
    # A login screen for users to access their individual portals, via inputting their chosen username and password. 
    # REQUIREMENT 1.1 
    remove_all(window)
    enter_info = Label(window, text="FoodState Nutrition ™")
    enter_info.config(bg='blanched almond')
    enter_info.config(font=("Blackadder IT", 30))
    enter_info.place(x=130, y=100)
    enter_Un = Label(window, text="User Name")
    enter_Un.config(bg='blanched almond')
    enter_Un.config(font=("Times New Roman", 12, 'italic'))
    enter_Un.place(x=250, y=200)
    enter_Pw = Label(window, text="User Password")
    enter_Pw.config(bg='blanched almond')
    enter_Pw.config(font=("Times New Roman", 12, 'italic'))
    enter_Pw.place(x=240, y=280)
    username = StringVar()
    username_entry = Entry(window, textvariable=username, text=username, font=('Verdana', 15), bg='blanched almond')
    username.set("")  # Entry of username
    username_entry.place(x=170, y=230)
    password = StringVar()
    password_entry = Entry(window, textvariable=password, show="*", text=password, font=('Verdana', 15),
                           bg='blanched almond')
    password.set("")  # Entry of password
    password_entry.place(x=170, y=310)
    accept_data = Button(window, text="Enter",
                         command=lambda: check_password(username, password, mycursor, window, logged_in, db))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=350, y=400)
    exit_button = Button(window, text="Quit", command=lambda: end(window, db))
    exit_button.config(
        bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
    exit_button.config(height=1, width=20)
    exit_button.place(x=100, y=400)
    mycursor.execute("select email from User where user_id = 1")
    email = mycursor.fetchall()[0][0]  # *SINGLE TABLE  SQL*, determine if this is the first time logging 
    # in, if so, a reset email will not exist 
    if email is not None:  # if the user has an account with a recovery email set, as this is not their first time 
        # logging in, allow for password reset 
        forgot_password = Button(window, text="Forgotten Password?",
                                 command=lambda: password_reset(mycursor, window, logged_in, db))
        forgot_password.config(bg='blanched almond')
        forgot_password.config(height=1, width=20)
        forgot_password.place(x=225, y=350)


def password_reset(mycursor, window, logged_in, db):
    # The ability to reset password if forgotten REQUIREMENT 1.6
    remove_all(window)
    username = StringVar()
    enter_info = Label(window,
                       text="A Reset Code Will Be Sent To The Email \n Associated To The Account")
    enter_info.config(bg='blanched almond')
    enter_info.config(font=("Rosewood Std Regular", 20))
    enter_info.place(x=50, y=100)
    enter_Un = Label(window, text="User Name")
    enter_Un.config(bg='blanched almond')
    enter_Un.config(font=("Times New Roman", 12, 'italic'))
    enter_Un.place(x=260, y=240)
    username_entry = Entry(window, textvariable=username, text=username, font=('Verdana', 15), bg='blanched almond')
    username.set("")  # enter username of account to recover
    username_entry.place(relx=.5, rely=.5, anchor="s")
    accept_data = Button(window, text="Enter", command=lambda: enter_reset(mycursor, window, logged_in, db, username))
    accept_data.config(height=1, width=20)
    accept_data.config(bg='blanched almond')
    accept_data.place(x=350, y=400)
    exit_button = Button(window, text="Quit", command=lambda: end(window, db))
    exit_button.config(
        bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
    exit_button.config(height=1, width=20)
    exit_button.place(x=100, y=400)


def enter_reset(mycursor, window, logged_in, db, username):
    # Wait for the user to enter the verification code sent to their email, to confirm their identity
    # Continuing REQUIREMENT 1.6
    if type(username) != str:  # if the username still exists as a STRINGVAR, then return it as a string
        username = username.get()  # Returns string from STRINGVAR class
    remove_all(window)
    sql = "select email from user where username = %s and active = 1"
    mycursor.execute(sql, (username,))
    try:  # ensure a valid username was entered
        email = mycursor.fetchall()[0][0]  # *SINGLE TABLE  SQL*, select the email address associated to the
        # username, if it is still 
        # an active profile 
        if email is not None:  # If a valid email was returned from the query
            code = str(randint(100000, 999999))  # generate a 6 digit code
            send_email(code, email, mycursor, db)  # Send 6 digit code to the recovery email specified
            enter_data = Label(window, text="Email Sent to: " + email[
                                                                :3] + "*****")
            enter_data.config(bg='blanched almond')
            enter_data.config(font=("Times New Roman", 20))
            enter_data.place(x=160, y=100)
            warning = Label(window, text="(please allow a few moments)")
            warning.config(bg='blanched almond')
            warning.config(font=("Rosewood Std Regular", 10))
            warning.place(x=220, y=140)
            enter_code = Label(window,
                               text="Enter Code:")
            enter_code.config(bg='blanched almond')
            enter_code.config(font=("Times New Roman", 12, 'italic'))
            enter_code.place(x=260, y=230)
            code_entered = StringVar()
            code_entry = Entry(window, textvariable=code_entered, text=code_entered, font=('Verdana', 15),
                               bg='blanched almond')
            code_entered.set("")  # enter code here
            code_entry.place(x=170, y=260)
            accept_data = Button(window, text="Enter",
                                 command=lambda: new_password(mycursor, window, logged_in, db, username, code,
                                                              code_entered))
            accept_data.config(height=1, width=20)
            accept_data.config(bg='blanched almond')
            accept_data.place(x=350, y=350)
            resend_code = Button(window, text="Resend Code",
                                 command=lambda: enter_reset(mycursor, window, logged_in, db, username))
            resend_code.config(height=1,
                               width=20)  # *RECURSIVE ALGORITHM* -Resending the code, will call the routine
            # again
            resend_code.config(bg='blanched almond')
            resend_code.place(x=100, y=350)
            exit_button = Button(window, text="Quit", command=lambda: end(window, db))
            exit_button.config(
                bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
            exit_button.config(height=1, width=20)
            exit_button.place(x=225, y=400)
    except IndexError:  # If an invalid username is entered, the program will display a relevant error message, 
        # and return to the previous screen 
        error_message = Label(window, text="No Such User Exists")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 40, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: password_reset(mycursor, window, logged_in, db))


def new_password(mycursor, window, logged_in, db, username, code, code_entered):
    # Allow the user to enter a new password, which they mut enter twice to ensure their is no miss-entry
    # Continuing REQUIREMENT 1.6
    if code_entered is not None:  # if the code still exists as a STRINGVAR, then return it as a string
        code_entered = code_entered.get()  # Returns string from STRINGVAR class
    remove_all(window)
    if code_entered == code:  # If the code entered matches the code sent in the email, allow the user to set a new 
        # password
        enter_P = Label(window, text="New Password")
        enter_P.config(bg='blanched almond')
        enter_P.config(font=("Times New Roman", 12, 'italic'))
        enter_P.place(x=250, y=200)
        enter_PA = Label(window, text="Re-Enter New Password")
        enter_PA.config(bg='blanched almond')
        enter_PA.config(font=("Times New Roman", 12, 'italic'))
        enter_PA.place(x=220, y=280)
        enter_info = Label(window, text="Enter New Password")
        enter_info.config(bg='blanched almond')
        enter_info.config(font=("Times New Roman", 20))
        enter_info.place(x=180, y=100)
        new_password = StringVar()
        new_password_entry = Entry(window, textvariable=new_password, text=new_password, font=('Verdana', 15),
                                   bg='blanched almond', show="*")
        new_password.set("")  # enter new password
        new_password_entry.place(x=170, y=230)
        new_password_again = StringVar()
        new_password_again_entry = Entry(window, text=new_password_again, show="*", textvariable=new_password_again,
                                         font=('Verdana', 15), bg='blanched almond')
        new_password_again.set("")  # re-Enter password to confirm
        new_password_again_entry.place(x=170, y=310)
        accept_data = Button(window, text="Enter",
                             command=lambda: confirm_matching_passwords(None, username, None, new_password, db,
                                                                        mycursor, window, logged_in, True,
                                                                        new_password_again))
        accept_data.config(height=1, width=20)
        accept_data.config(bg='blanched almond')
        accept_data.place(x=350, y=400)

        exit_button = Button(window, text="Quit", command=lambda: end(window, db))
        exit_button.config(
            bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
        exit_button.config(height=1, width=20)
        exit_button.place(x=100, y=400)
    else:  # if the wrong was entered, display an error

        select_option = Label(window, text="Select An Option To Continue")
        select_option.config(bg='blanched almond')
        select_option.config(font=("Times New Roman", 12, 'italic'))
        select_option.place(x=200, y=300)

        error_message = Label(window, text="Code Entered Cannot be Verified")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 20))
        error_message.place(x=100, y=120)
        resend_button = Button(window, text="Re-Enter Code",
                               command=lambda: enter_reset(mycursor, window, logged_in, db, username))
        resend_button.config(height=1, width=20)
        resend_button.config(bg='blanched almond')
        resend_button.place(x=350, y=350)
        # Allow the user another opportunity to enter the code again
        renter_button = Button(window, text="Re-Enter Credentials",
                               command=lambda: password_reset(mycursor, window, logged_in, db))
        renter_button.config(height=1, width=20)
        renter_button.config(bg='blanched almond')
        renter_button.place(x=100, y=350)
        # Allow the user to renter their credentials, and resend a new code


def confirm_matching_passwords(admin, username, old_password, new_password_, db, mycursor, window, logged_in, forgot,
                               new_password_again):
    # A module which is used to confirm that when a new password is set, both entries of the password are identical
    new_password_again = new_password_again.get()  # Returns string from STRINGVAR class
    new_password_ = new_password_.get()  # Returns string from STRINGVAR class
    if new_password_ == new_password_again:  # If both passwords entered match:
        if not forgot:  # if the user is trying to reset a password, already knowing their old password, amend their 
            # password 
            set_new_password(admin, username, old_password, new_password_, db, mycursor, window, logged_in, forgot)
        else:  # If the user is trying to reset a password, having forgotten their old password, as identity 
            # confirmation has been done, amend their password 
            set_new_password(None, username, "empty", new_password_, db, mycursor, window, logged_in, True)
    else:  # if the code entered does not match the verification code, show an appropriate error message, and return 
        # to the previous screen 
        remove_all(window)
        do_not_match_label = Label(window, text="Passwords Do Not Match")
        do_not_match_label.config(bg='blanched almond')
        do_not_match_label.config(font=("Times New Roman", 40, 'italic'))
        do_not_match_label.place(relx=.5, rely=.4, anchor="n")
        if not forgot:  # if the user is trying to reset a password, already knowing their old password, return them 
            # to the change password feature of the application 
            window.after(3000, lambda: change_password(logged_in, username, admin, db, mycursor, window))
        else:  # If the user is trying to reset a password, having forgotten their old password, as identity 
            # confirmation has been done, allow them to retry entering a new password 
            window.after(3000, lambda: new_password(mycursor, window, logged_in, db, username, None, None))


def set_new_password(admin, username, old_password, password, db, mycursor, window, logged_in, forgot):
    # Once confirmed the current password matches that of the database, and the new password meets the standards
    # Update the userid password. REQUIREMENT 1.4/ 1.5/1.6
    # * HASHING* Password is hashed to ensure it matches the values stored in the User Table
    if not forgot:  # This module can be called to use if the user has forgotten their password, or if they are 
        # trying to change it, knowing their old password 
        old_password = old_password.get()  # Returns string from STRINGVAR class
    else:
        if type(password) != str:  # if the password still exists as a STRINGVAR, then return it as a string
            password = password.get()  # Returns string from STRINGVAR class
    remove_all(window)
    if not forgot:
        create_menu(logged_in, username, admin, db, mycursor, window)
    password_safe = False
    number = False
    for i in password:  # *  LINEAR SEARCH* through the password to look for upper case and numbers
        if 91 > ord(i) > 64:  # Is an uppercase letter present
            password_safe = True
        if 58 > ord(i) > 47:  # does the password contain a number
            number = True
    if len(password) < 8:  # does the password have 8 or more charachters
        password_safe = False
    if not password_safe != False or number == False:  # If invalid credentials are entered, display an error message, 
        # and return to previous screen 
        incorrect_password = Label(window,
                                   text="New Password Must Be:\n At least 8 Charters\n Contain An Upper Case "
                                        "Letter \n Contain A Number")
        incorrect_password.config(font=("Times New Roman", 35, 'italic'))
        incorrect_password.config(bg='blanched almond')
        incorrect_password.place(relx=.5, rely=.2, anchor="n")
        if not forgot:  # Forgotten password
            window.after(3000, lambda: change_password(logged_in, username, admin, db, mycursor, window))
        else:  # Resetting password within the program
            window.after(3000, lambda: new_password(mycursor, window, logged_in, db, username, None, None))
    else:  # if all information meets the criteria 
        password_select_query = """SELECT * FROM User WHERE username = %s"""  # sub
        mycursor.execute(password_select_query, (username,))  # *  SINGLE TABLE PARAMETRISED SQL* selects the 
        # entire record of data 
        # pertaining to the user logging in 
        details = mycursor.fetchall()  # *GROUP B RECORD* The python equivalent of a database record containing all 
        # credentials pertaining to this user 
        if len(details) > 0:
            key = details[0][4]
            salt = details[0][5]
            new_key = pbkdf2_hmac('sha256', old_password.encode('utf-8'), salt, 100000)
            if new_key == key or True == forgot:  # If the password match those within the User table
                salt = urandom(32)
                key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)  # invoking the key derivation 
                # function, converting it to binary, with the salt, and iterating it 100000 times 
                users = {username: {
                    'salt': salt,
                    'admin': admin,
                    'key': key, }}  # *GROUP B Dictionary* To store all the data for the user, before it is written 
                # to the 
                # database 
                mycursor.execute("Update User set k3y = %s, salt = %s where username = %s",
                                 (key, users[username]["salt"], username))
                db.commit()  # Database changes are saved
                incorrect_password = Label(window, text="Password successfully changed")
                incorrect_password.config(font=("Times New Roman", 20, 'italic'))
                incorrect_password.config(bg='blanched almond')
                incorrect_password.place(relx=.5, rely=.4, anchor="n")
                if not forgot:
                    window.after(3000, lambda: change_password(logged_in, username, admin, db, mycursor, window))
                else:
                    window.after(3000, lambda: login(mycursor, window, logged_in, db))
            else:  # If invalid credentials are entered, display an error message, and return to previous screen
                incorrect_password = Label(window, text="Old Password Entered Does \n Not Match Current Password")
                incorrect_password.config(font=("Times New Roman", 20, 'italic'))
                incorrect_password.config(bg='blanched almond')
                incorrect_password.place(relx=.5, rely=.4, anchor="n")
                window.after(3000, lambda: change_password(logged_in, username, admin, db, mycursor, window))


def check_password(username, password, mycursor, window, logged_in, db):
    # Continuing REQUIREMENT 1.1
    # * HASHING* Password is hashed to ensure it matches the values stored in the User Table
    remove_all(window)
    username = username.get()  # Returns string from STRINGVAR class
    password = password.get()  # Returns string from STRINGVAR class
    password_select_query = """SELECT * FROM User WHERE username = %s and active = 1"""
    mycursor.execute(password_select_query, (
        username,))  # *SINGLE TABLE PARAMETRISED SQL* selects the entire record of data pertaining to the 
    # user logging in 
    details = mycursor.fetchall()  # *RECORD* The python equivalent of a database record containing all 
    # credentials pertaining to this user 
    logged_in = "False"
    if len(details) > 0:  # To ensure a valid username was entered
        key = details[0][4]  # Locating the key in the record
        salt = details[0][5]  # Locating the salt in the record
        new_key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt,
                              100000)  # invoking the key derivation function, converting it to binary, with the 
        # salt, and iterating it 100000 times 
        if key == new_key:  # If the credentials match those within the User table, the login is successful
            logged_in = "True"
            admin = details[0][3]  # Assign an admin privilege based upon the Table Credentials
            initialise_window(logged_in, username, admin, db, mycursor, window)  # The user is brought to the main menu
    if logged_in == "False":  # If invalid credentials are entered, display an error message, and return to previous 
        # screen 
        incorrect_password = Label(window, text="Incorrect Username Or Password")
        incorrect_password.config(font=("Times New Roman", 20, 'italic'))
        incorrect_password.config(bg='blanched almond')
        incorrect_password.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: login(mycursor, window, logged_in, db))


def establish_email(logged_in, username, admin, db, mycursor, window):
    # Upon first entry into the application, an email must be assigned to the starter account, in the event the 
    # password is forgotten This email address will also act as the contact detail for the holder of the account 
    # REQUIREMENT 1.9/1.6 
    remove_all(window)
    window.title("Setup Recovery Email")
    enter_data = Label(window, text="Admin Recovery Email")
    enter_data.config(bg='blanched almond')
    enter_data.config(font=("Times New Roman", 20, 'italic'))
    enter_data.place(x=175, y=150)
    enter_data = Label(window, text="(This will be act as \n additional contact information)")
    enter_data.config(bg='blanched almond')
    enter_data.config(font=("Times New Roman", 12, 'italic'))
    enter_data.place(x=200, y=200)
    enter_here = Label(window, text="Recovery Email")
    enter_here.config(bg='blanched almond')
    enter_here.config(font=("Times New Roman", 12, 'italic'))
    enter_here.place(x=250, y=300)
    email = StringVar()
    email_entry = Entry(window, text=email, textvariable=email, font=('Verdana', 15), bg='blanched almond')
    email.set("")  # enter an email address
    email_entry.place(x=170, y=330)
    accept_data = Button(window, text="Enter",
                         command=lambda: verify_mail(logged_in, username, admin, db, mycursor, window, email, True,
                                                     None))
    accept_data.config(height=1, width=20)
    accept_data.config(bg='blanched almond')
    accept_data.place(x=350, y=450)
    exit_button = Button(window, text="Quit", command=lambda: end(window, None))
    exit_button.config(height=1, width=20)
    exit_button.config(bg='blanched almond')
    exit_button.place(x=100, y=450)


def verify_mail(logged_in, username, admin, db, mycursor, window, email, first_user, users_selectable):
    # Send a 6 digit code to the user, and request them to 
    # Continuing REQUIREMENT 1.6/1.9
    if type(
            email) != str:  # If the value of the variable choice is from the combobox, then it will have to be 
        # converted to STRING datatype 
        email = email.get()  # Returns string from STRINGVAR class
    remove_all(window)
    code = str(randint(100000, 999999))  # Randomly generate a 6-digit code
    send_email(code, email, mycursor, db)  # Send 6 digit code to the recovery email specified
    if first_user:  # If the email is being assigned to the first user, do not allow access to the cascade menu at 
        # this time 
        exit_button = Button(window, text="Quit", command=lambda: end(window, db))
        exit_button.config(
            bg='blanched almond')  # As the menu is not available at this time, a button is used to end the program
        exit_button.config(height=1, width=20)
        exit_button.place(x=100, y=400)
        back_button = Button(window, text="Re-enter email",
                             command=lambda: establish_email(logged_in, username, admin, db, mycursor, window))
    else:
        create_menu(logged_in, username, admin, db, mycursor, window)
        back_button = Button(window, text="Re-enter email",
                             command=lambda: change_email(logged_in, username, admin, db, mycursor, window,
                                                          users_selectable))
    back_button.config(bg='blanched almond')
    back_button.config(height=1, width=20)
    back_button.place(x=350, y=400)
    enter_data = Label(window, text="Email Sent to: " + email[
                                                        :3] + "*****")
    enter_data.config(bg='blanched almond')
    enter_data.config(font=("Times New Roman", 20))
    enter_data.place(x=160, y=100)
    warning = Label(window, text="(please allow a few moments)")
    warning.config(bg='blanched almond')
    warning.config(font=("Rosewood Std Regular", 10))
    warning.place(x=220, y=140)
    enter_code = Label(window,
                       text="Enter Code:")
    enter_code.config(bg='blanched almond')
    enter_code.config(font=("Times New Roman", 12, 'italic'))
    enter_code.place(x=260, y=230)
    code_entered = StringVar()
    code_entry = Entry(window, textvariable=code_entered, text=code_entered, font=('Verdana', 15), bg='blanched almond')
    code_entered.set("")  # enter verification code
    code_entry.place(x=170, y=260)
    accept_data = Button(window, text="Enter",
                         command=lambda: confirm_email(logged_in, username, admin, db, mycursor, window, email, code,
                                                       code_entered, first_user, users_selectable))
    accept_data.config(height=1, width=20)
    accept_data.config(bg='blanched almond')
    accept_data.place(x=350, y=350)
    resend_code = Button(window, text="Resend Code",
                         command=lambda: verify_mail(logged_in, username, admin, db, mycursor, window, email,
                                                     first_user, users_selectable))
    resend_code.config(height=1, width=20)  # *RECURSIVE ALGORITHM* -Resending the code, will call the routine
    # again
    resend_code.config(bg='blanched almond')
    resend_code.place(x=100, y=350)


def confirm_email(logged_in, username, admin, db, mycursor, window, email, code, code_entered, first_user,
                  users_selectable):
    # After matching the verification codes, update the email of the account in question
    # Continuing REQUIREMENT 1.6/1.9
    code_entered = code_entered.get()  # Returns string from STRINGVAR class
    remove_all(window)
    if code == code_entered:  # Ensuring the codes match
        sql = "Update User set email = %s where username = %s"  # *SINGLE TABLE PARAMETRISED SQL* updates the
        # email to the value specified, of the user specified 
        if first_user:
            mycursor.execute(sql, (email, username))
            complete_message = Label(window, text="Activation Complete")
            complete_message.config(font=("Times New Roman", 20, 'italic'))
            complete_message.config(bg='blanched almond')
            complete_message.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: initialise_window(logged_in, username, admin, db, mycursor, window))
        else:
            mycursor.execute(sql, (email, users_selectable))
            complete_message = Label(window, text="Change Successfully Made")
            window.after(3000, lambda: edit_user(logged_in, username, admin, db, mycursor, window))
            complete_message.config(font=("Times New Roman", 20, 'italic'))
            complete_message.config(bg='blanched almond')
            complete_message.place(relx=.5, rely=.4, anchor="n")
        db.commit()  # Database changes are saved
    else:  # If an invalid entry was made, display the appropriate error message and return to the previous screen
        error_message = Label(window, text="Incorrect Code, Please Try Again")
        error_message.config(font=("Times New Roman", 20, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: verify_mail(logged_in, username, admin, db, mycursor, window, email, first_user,
                                               users_selectable))


def change_password(logged_in, username, admin, db, mycursor, window):  #######
    # allowing the user to enter their old password then their proposed new password
    # REQUIREMENT 1.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - Change Password")  # Indicating the section of the application the user is operating
    enter_info = Label(window, text="Change Password")
    enter_info.config(bg='blanched almond')
    enter_info.config(font=("Times New Roman", 20))
    enter_info.place(x=200, y=100)
    enter_OP = Label(window, text="Old Password")
    enter_OP.config(bg='blanched almond')
    enter_OP.config(font=("Times New Roman", 12, 'italic'))
    enter_OP.place(x=250, y=200)
    enter_P = Label(window, text="New Password")
    enter_P.config(bg='blanched almond')
    enter_P.config(font=("Times New Roman", 12, 'italic'))
    enter_P.place(x=250, y=300)
    enter_PA = Label(window, text="Re-Enter New Password")
    enter_PA.config(bg='blanched almond')
    enter_PA.config(font=("Times New Roman", 12, 'italic'))
    enter_PA.place(x=220, y=400)
    old_password = StringVar()
    old_password_entry = Entry(window, text=old_password, show="*", textvariable=old_password,
                               font=('Verdana', 15), bg='blanched almond')
    old_password.set("")  # Enter existing password
    old_password_entry.place(x=170, y=230)
    new_password = StringVar()
    new_password_entry = Entry(window, text=new_password, show="*", textvariable=new_password,
                               font=('Verdana', 15), bg='blanched almond')
    new_password.set("")  # Enter proposed new password
    new_password_entry.place(x=170, y=330)
    new_password_again = StringVar()
    new_password_again_entry = Entry(window, text=new_password_again, show="*", textvariable=new_password_again,
                                     font=('Verdana', 15), bg='blanched almond')
    new_password_again.set("")  # Enter proposed new password again
    new_password_again_entry.place(x=170, y=430)
    accept_data = Button(window, text="Enter",
                         command=lambda: confirm_matching_passwords(admin, username, old_password, new_password, db,
                                                                    mycursor, window, logged_in, False,
                                                                    new_password_again))

    accept_data.config(height=1, width=20)
    accept_data.config(bg='blanched almond')
    accept_data.place(x=225, y=490)


# The following routines allow the user the ability to create new portals, activate and deactivate other users, 
# As well as edit the access rights of other accounts, as well as their contact information. All features are 
# reserved for admins only. Continuing client requirement 1 

def manage_users_menu(logged_in, username, admin, db, mycursor, window):
    # A menu to offer the ability for the user to make alterations to other portals REQUIREMENT 1.6/1.7/1.3/1.9/1.8
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition-Manage users")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Manage Users")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="(User Portals Can Be Assigned To Employees To Organise The Workforce)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=225)
    create = Button(window, text="Create User",
                    command=lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
    create.config(bg='blanched almond')
    create.config(height=1, width=20)
    create.place(x=225, y=300)

    edit = Button(window, text="Edit User", command=lambda: edit_user(logged_in, username, admin, db, mycursor, window))
    edit.config(bg='blanched almond')
    edit.config(height=1, width=20)
    edit.place(x=225, y=375)
    activation = Button(window, text="Control Activation",
                        command=lambda: control_activation(logged_in, username, admin, db, mycursor, window))
    activation.config(bg='blanched almond')
    activation.config(height=1, width=20)
    activation.place(x=225, y=450)
    view = Button(window, text="View", command=lambda: view_users(logged_in, username, admin, db, mycursor, window))
    # The options to either Create, Edit, view or Alter user activation are selectable
    view.config(bg='blanched almond')
    view.config(height=1, width=20)
    view.place(x=225, y=525)


def new_user_credentials(logged_in, username, admin, db, mycursor, window):
    # Allow the user to enter the details for the new portal to be created
    # CONTINUING REQUIREMENT 1.3
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition-Create new user")  # Indicating the section of the application the user is operating
    first_user = False
    select_an_option = Label(window, text="Food State Nutrition™\n        - Create Users")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=50)
    new_username = StringVar()
    new_username_entry = Entry(window, textvariable=new_username, text=new_username, font=('Verdana', 15),
                               bg='blanched almond')
    new_username.set("")  # Enter new username
    new_username_entry.place(x=175, y=200)
    user_tag = Label(window, text="New User Name")
    user_tag.config(bg='blanched almond')
    user_tag.config(font=("Times New Roman", 12, 'italic'))
    user_tag.place(x=250, y=170)
    new_password = StringVar()
    new_password_entry = Entry(window, textvariable=new_password, text=new_password, font=('Verdana', 15),
                               bg='blanched almond', show="*")
    new_password.set("")  # Enter new password
    new_password_entry.place(x=175, y=280)
    new_password_tag = Label(window, text="New Password")
    new_password_tag.config(bg='blanched almond')
    new_password_tag.config(font=("Times New Roman", 12, 'italic'))
    new_password_tag.place(x=250, y=250)
    new_password_again = StringVar()
    new_password_again_entry = Entry(window, textvariable=new_password_again, text=new_password_again,
                                     font=('Verdana', 15), bg='blanched almond', show="*")
    new_password_again.set("")  # Re-enter new password
    new_password_again_entry.place(x=175, y=360)
    new_password_again_tag = Label(window, text="Re-Enter Password")
    new_password_again_tag.config(bg='blanched almond')
    new_password_again_tag.config(font=("Times New Roman", 12, 'italic'))
    new_password_again_tag.place(x=250, y=330)
    new_email = StringVar()
    new_email_entry = Entry(window, textvariable=new_email, text=new_email, font=('Verdana', 15), bg='blanched almond')
    new_email.set("")  # Enter new email
    new_email_entry.place(x=175, y=440)
    new_email_tag = Label(window, text="New Email")
    new_email_tag.config(bg='blanched almond')
    new_email_tag.config(font=("Times New Roman", 12, 'italic'))
    new_email_tag.place(x=260, y=410)
    new_admin = IntVar()  # select whether the account to be admin or standard
    admin_user = Radiobutton(window, text='Admin', value=1, variable=new_admin)
    admin_user.config(bg='blanched almond')
    admin_user.place(x=200, y=475)
    standard_user = Radiobutton(window, text='Standard', value=0, variable=new_admin)
    standard_user.place(x=325, y=475)
    standard_user.config(bg='blanched almond')
    accept_data = Button(window, text="Enter",
                         command=lambda: usercheck(logged_in, username, admin, db, mycursor, window, new_username,
                                                   new_password, new_admin, first_user, new_email, new_password_again))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=525)


def usercheck(logged_in, username, admin, db, mycursor, window, new_username, new_password, new_admin, first_user,
              new_email, new_password_again):
    # Ensure the details enter are appropriate. The user does not already exist and the password meets the criteria
    # CONTINUING REQUIREMENT 1.3 /1.5
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if type(
            new_username) != str:  # If the value of the variable choice is from the combobox, then it will have to 
        # be converted to STRING datatype 
        new_username = new_username.get()  # Returns string from STRINGVAR class
        new_username = new_username.lower()  # set username to be lower case, to not clash with other database entries
        new_password = new_password.get()  # Returns string from STRINGVAR class
        new_email = new_email.get()  # Returns string from STRINGVAR class
        new_admin = new_admin.get()  # Returns Integer from INTVAR class
        new_password_again = new_password_again.get()  # Returns string from STRINGVAR class
    mycursor.execute("SELECT username FROM user")  # *SINGLE TABLE SQL* selects the username from User Table
    invalid = False
    for i in mycursor:  # *LINEAR SEARCH* through the users to see if an existing portal with the same 
        # username exists 
        if i[0] == new_username:
            invalid = True
    if len(new_username) > 255 or len(new_username) < 1:  # Ensure username is less than 255 charachters
        invalid = True
    if len(new_email) > 255 or len(new_email) < 1:  # ensure email is less than 255 charachters
        invalid = True
    password_safe = False
    for i in new_password:  # *LINEAR SEARCH* through the password to look for upper case and numbers
        if 91 > ord(i) > 64:  # Is an uppercase letter present
            password_safe = True
    if len(new_password) < 8:  # does the password have 8 or more charachters
        password_safe = False
    number = False
    for i in new_password:
        if 58 > ord(i) > 47:  # does the password contain a number
            number = True
    if new_password != new_password_again:
        incorrect_entry = Label(window, text="Paswords Entered Do Not Match")
        incorrect_entry.config(font=("Times New Roman", 20, 'italic'))
        incorrect_entry.config(bg='blanched almond')
        incorrect_entry.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
    elif invalid:
        already_exists = Label(window, text="One Or More Of The Entered \nCredentials Are Not Suitable")
        already_exists.config(font=("Times New Roman", 20, 'italic'))
        already_exists.config(bg='blanched almond')
        already_exists.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
    elif False == password_safe or number == False:  # If the password does not meet the criteria, display 
        # appropriate error message, return to prior screen 
        incorrect_password = Label(window,
                                   text="New Password Must Be At Least 8 Charters Long,\n Containing An Upper Case "
                                        "Letter, \n Along With A Number")
        incorrect_password.config(font=("Times New Roman", 20, 'italic'))
        incorrect_password.config(bg='blanched almond')
        incorrect_password.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
    else:
        new_code = str(randint(100000, 999999))  # Randomly generate a 6-digit code
        send_email(new_code, new_email, mycursor, db)  # Send 6 digit code to the recovery email specified
        code_entered = StringVar()
        back_button = Button(window, text="Re-enter Details",
                             command=lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
        back_button.config(bg='blanched almond')  # Allow for data to be re-Entered
        back_button.config(height=1, width=20)
        back_button.place(x=225, y=400)
        enter_data = Label(window, text="Email Sent to: " + new_email)
        enter_data.config(bg='blanched almond')
        enter_data.config(font=("Times New Roman", 20))
        enter_data.place(x=160, y=100)
        warning = Label(window, text="(please allow a few moments)")
        warning.config(bg='blanched almond')
        warning.config(font=("Rosewood Std Regular", 10))
        warning.place(x=220, y=140)
        enter_code = Label(window,
                           text="Enter Code:")
        enter_code.config(bg='blanched almond')
        enter_code.config(font=("Times New Roman", 12, 'italic'))
        enter_code.place(x=260, y=230)

        code_entered = StringVar()
        code_entry = Entry(window, textvariable=code_entered, text=code_entered, font=('Verdana', 15),
                           bg='blanched almond')
        code_entered.set("")  # enter verification code
        code_entry.place(x=170, y=260)
        accept_data = Button(window, text="Enter",
                             command=lambda: valid_email(logged_in, username, admin, db, mycursor, window, new_username,
                                                         new_password, new_admin, first_user, new_email, code_entered,
                                                         new_code))
        accept_data.config(height=1, width=20)
        accept_data.config(bg='blanched almond')
        accept_data.place(x=350, y=350)
        resend_code = Button(window, text="Resend Code",
                             command=lambda: usercheck(logged_in, username, admin, db, mycursor,
                                                       window, new_username, new_password, new_admin, first_user,
                                                       new_email, new_password))
        resend_code.config(height=1,
                           width=20)  # *RECURSIVE ALGORITHM* -Resending the code, will call the routine
        # again
        resend_code.config(bg='blanched almond')
        resend_code.place(x=100, y=350)


def valid_email(logged_in, username, admin, db, mycursor, window, new_username, new_password, new_admin, first_user,
                new_email, code, new_code):
    # Once the user has successfully verified their email, create the new user
    # CONTINUING REQUIREMENT 1.3 /1.9
    code = code.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if new_code == code:  # providing the verification code is correct, create the user
        user_created = Label(window, text="User created")
        user_created.config(font=("Times New Roman", 20, 'italic'))
        user_created.config(bg='blanched almond')
        user_created.place(relx=.5, rely=.4, anchor="n")
        create_user(new_username, new_password, new_admin, mycursor, db, first_user, username, admin, window, new_email)
    else:  # If the code is incorrect, display error message and return to previous screen
        error_message = Label(window, text="Incorrect Code, Please Try Again")
        error_message.config(font=("Times New Roman", 20, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        resend_button = Button(window, text="Re-enter code",
                               command=lambda: usercheck(logged_in, username, admin, db, mycursor, window, new_username,
                                                         new_password, new_admin, first_user,
                                                         new_email, new_password))
        renter_button = Button(window, text="Re-enter credentials",
                               command=lambda: new_user_credentials(logged_in, username, admin, db, mycursor, window))
        renter_button.config(bg='blanched almond')
        renter_button.place(relx=.3, rely=.5, anchor="n")
        resend_button.config(bg='blanched almond')
        resend_button.place(relx=.7, rely=.5, anchor="n")


def edit_user(logged_in, username, admin, db, mycursor, window):
    # Selects all available users that can be edited
    # CONTINUING REQUIREMENT 1.7/1.9
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition-Edit User")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Edit Users")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    select_user = """SELECT username FROM user where active = 1"""
    mycursor.execute(select_user)  # *SINGLE TABLE SQL* selects the usernames that are active, hence editable
    data = mycursor.fetchall()
    all_users = []
    for i in data:
        all_users.append(i[0])
    users_selectable = Combobox(window)
    users_selectable['values'] = all_users  # Select an active user to edit
    users_selectable.config(height=10, width=40)
    users_selectable.place(relx=.5, rely=.5, anchor="n")
    admin_change = Button(window, text="Access Right Changes",
                          command=lambda: admin_or_standard(logged_in, username, admin, db, mycursor, window,
                                                            users_selectable))
    # Select to amend user access rights
    email = Button(window, text="Email Change",
                   command=lambda: change_email(logged_in, username, admin, db, mycursor, window, users_selectable))
    # select to amend users email address
    admin_change.config(bg='blanched almond')
    admin_change.place(relx=.4, rely=.7, anchor="s")
    email.config(bg='blanched almond')
    email.place(relx=.6, rely=.7, anchor="s")
    info = Label(window, text="(Select From The List Below)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=200, y=250)


def change_email(logged_in, username, admin, db, mycursor, window, users_selectable):
    # Allow recovery emails to be changed, as if they are not up-to-date then then employees may lose accounts, 
    # or not be contactable CONTINUING REQUIREMENT 1.9 
    if type(
            users_selectable) != str:  # If the value of the variable choice is from the combobox, then it will have 
        # to be converted to STRING datatype 
        users_selectable = users_selectable.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT username FROM User")
    data = mycursor.fetchall()
    found = False
    for i in data:
        if i[0] == users_selectable:
            found = True
    if found == True:
        select_user = """SELECT email FROM user where username = %s"""
        mycursor.execute(select_user, (
            users_selectable,))  # *SINGLE TABLE PARAMETRISED SQL* selects the email of the user in question
        current_email = mycursor.fetchall()[0][0]
        select_an_option = Label(window, text="Food State Nutrition™\n        - Edit Email")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        display_email = Label(window, text="(Your current email: " + current_email + ")")
        display_email.config(bg='blanched almond')
        display_email.config(font=("Times New Roman", 12))
        display_email.place(x=175, y=250)
        enter_E = Label(window, text="New Email")
        enter_E.config(bg='blanched almond')
        enter_E.config(font=("Times New Roman", 12, 'italic'))
        enter_E.place(x=260, y=320)
        change_email = StringVar()
        change_label_entry = Entry(window, textvariable=change_email, text=change_email, font=('Verdana', 15),
                                   bg='blanched almond')
        change_email.set("")  # enter Email address
        change_label_entry.place(x=170, y=350)
        accept_data = Button(window, text="Accept",
                             command=lambda: verify_mail(logged_in, username, admin, db, mycursor, window, change_email,
                                                         False, users_selectable))
        accept_data.config(height=1, width=20)
        accept_data.config(bg='blanched almond')
        accept_data.place(x=320, y=450)
        back_button = Button(window, text="Reselect",
                             command=lambda: edit_user(logged_in, username, admin, db, mycursor, window))
        back_button.config(height=1, width=20)
        back_button.config(bg='blanched almond')
        back_button.place(x=120, y=450)
    else:
        error = Label(window, text="No Such User Found")
        error.config(font=("Times New Roman", 20, 'italic'))
        error.config(bg='blanched almond')
        error.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_user(logged_in, username, admin, db, mycursor, window))


def admin_or_standard(logged_in, username, admin, db, mycursor, window, users_selectable):
    # Ensure a valid username was selected, then allow user to select the privilege change they desire
    # CONTINUING REQUIREMENT 1.7
    str_user_selected = users_selectable.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT username FROM user WHERE active = 1")
    user_exists = False
    for i in mycursor:  # *LINEAR SEARCH* through the users to see if a valid username was selected
        if i[0] == str_user_selected:  # Confirms the user that has been selected to be added is a valid Selection
            user_exists = True
    if str_user_selected == username:  # DO not allow the user to make themselves a standard user
        user_exists = False
    if not user_exists:  # If an invalid username was entered, display an error message, and return to the edit user 
        # menu 
        error = Label(window, text="User Does Not Exist, Or Is Currently In Use")
        error.config(font=("Times New Roman", 20, 'italic'))
        error.config(bg='blanched almond')
        error.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_user(logged_in, username, admin, db, mycursor, window))
    else:  # If the username selection is valid, allow user to select the change they desire
        admin_fetch = """SELECT admin from User where username = %s"""  # *SINGLE TABLE PARAMETRISED SQL* 
        # selects the admin status of the selected user 
        mycursor.execute(admin_fetch, (str_user_selected,))
        admin_status = mycursor.fetchone()
        if admin_status[0] == 1:  # display the current admin status of the account
            admin_status = "Admin"
        else:
            admin_status = "Standard"

        title = Label(window, text="Food State Nutrition™\n        - Edit Access Rights")
        title.config(bg='blanched almond')
        title.config(font=("Times New Roman", 30))
        title.place(x=40, y=100)
        display_admin = Label(window,
                              text="(" + str_user_selected + " Is A " + admin_status + " User)")
        display_admin.config(bg='blanched almond')
        display_admin.config(font=("Times New Roman", 12))
        display_admin.place(x=225, y=250)
        new_admin = IntVar()  # select between changing the account to admin or standard
        admin_user = Radiobutton(window, text='Admin', value=1, variable=new_admin,
                                 font=("Times New Roman", 15, 'italic'))
        admin_user.config(bg='blanched almond')
        admin_user.place(relx=.4, rely=.6, anchor="n")
        standard_user = Radiobutton(window, text='Standard', value=0, variable=new_admin, font=("Times New Roman", 15))
        standard_user.config(bg='blanched almond')
        standard_user.place(relx=.6, rely=.6, anchor="n")
        accept_data = Button(window, text="Enter",
                             command=lambda: ammend_user(logged_in, username, admin, db, mycursor, window, new_admin,
                                                         str_user_selected, users_selectable))
        accept_data.config(bg='blanched almond')
        accept_data.config(height=1, width=20)
        accept_data.place(x=225, y=425)


def ammend_user(logged_in, username, admin, db, mycursor, window, new_admin, str_user_selected, users_selectable):
    # If a radiobutton was selected, then the changes to the portal in question will be made
    # CONTINUING REQUIREMENT 1.7
    if new_admin is not None:  # If the value of the variable choice is from the Radiobutton, then it will have to be
        # converted to Integer datatype 
        new_admin = new_admin.get()  # Returns Integer from IntVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if new_admin == 1 or new_admin == 0:  # *SINGLE TABLE PARAMETRISED SQL* if a valid radiobutton was 
        # selected, update the admin status of the user in question 
        mycursor.execute("Update User set admin = %s where username = %s ", (new_admin, str_user_selected))
        change_sucess = Label(window, text="Change Successful")
        change_sucess.config(font=("Times New Roman", 20, 'italic'))
        change_sucess.config(bg='blanched almond')
        change_sucess.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: manage_users_menu(logged_in, username, admin, db, mycursor, window))
    else:  # If a radiobutton was not selected, display an error message, and return to previous screen
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error.config(font=("Times New Roman", 20, 'italic'))
        error.config(bg='blanched almond')
        error.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: admin_or_standard(logged_in, username, admin, db, mycursor, window, users_selectable))


def control_activation(logged_in, username, admin, db, mycursor, window):
    # select to either reactivate or deactivate a user
    # CONTINUING REQUIREMENT 1.8
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - User Activation")  # Indicating the section of the application the user is operating
    title = Label(window, text="Food State Nutrition™\n        - Activation Control")
    title.config(bg='blanched almond')
    title.config(font=("Times New Roman", 30))
    title.place(x=40, y=150)
    activate = Button(window, text="Activate",
                      command=lambda: activation(logged_in, username, admin, db, mycursor, window, True))
    activate.config(height=1, width=20)
    activate.place(x=225, y=300)
    deactivate = Button(window, text="Deactivate",
                        command=lambda: activation(logged_in, username, admin, db, mycursor, window, False))
    activate.config(bg='blanched almond')  # Activate a user
    deactivate.config(bg='blanched almond')  # Deactivate a user
    deactivate.config(height=1, width=20)
    deactivate.place(x=225, y=350)

    back = Button(window, text="Back",
                  command=lambda: manage_users_menu(logged_in, username, admin, db, mycursor, window))
    back.config(bg='blanched almond')
    back.config(height=1, width=20)
    back.place(x=225, y=400)


def activation(logged_in, username, admin, db, mycursor, window, activate):
    # Based on the variable passed to the activate parameter, will show a list of all active, or deactivate users to 
    # choose from CONTINUING REQUIREMENT 1.8 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    title = Label(window, text="Food State Nutrition™\n        - Activation Control")
    title.config(bg='blanched almond')
    title.config(font=("Times New Roman", 30))
    title.place(x=40, y=150)
    if activate:
        select_an_option = Label(window, text="Please Select a user to Reactivate")
        select_user = """SELECT username FROM User WHERE username != %s and active = 0"""
        mycursor.execute(select_user, (username,))
        change = 1
    else:
        select_an_option = Label(window, text="Please Select A User To Deactivate")
        select_user = """SELECT username FROM User WHERE username != %s and active = 1"""
        mycursor.execute(select_user, (username,))
        change = 0
    all_users = []
    data = mycursor.fetchall()  # *GROUP B SINGLE TABLE PARAMETRISED SQL* selects the usernames that are 
    # deactivated/activated, but not the current user 
    for i in data:
        all_users.append(i[0])
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 12))
    select_an_option.place(x=185, y=320)
    users_selectable = Combobox(window)  # select the username of the account to make alterations to
    users_selectable['values'] = all_users
    users_selectable.place(relx=.5, rely=.6, anchor="n")
    users_selectable.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: make_activation_changes(logged_in, username, admin, db, mycursor, window,
                                                                 users_selectable, change))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=425)
    back = Button(window, text="Back",
                  command=lambda: control_activation(logged_in, username, admin, db, mycursor, window))
    back.config(bg='blanched almond')
    back.config(height=1, width=20)
    back.place(x=225, y=475)


def make_activation_changes(logged_in, username, admin, db, mycursor, window, users_selectable, active_status):
    # If a valid username is selected, then the account is activated or deactivated based on the parameter passed to 
    # active status CONTINUING REQUIREMENT 1.8 
    users_selectable = users_selectable.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT username FROM user")  # *SINGLE TABLE SQL*, select all users
    user_exists = False
    for i in mycursor:  # *LINEAR SEARCH* Ensure the user selected exists in the Table
        if i[0] == users_selectable:
            user_exists = True
    if not user_exists:  # If invalid credentials are entered, display an error message, and return to previous screen
        incorrect_username = Label(window, text="User Does Not Exist, Please Use Drop Down Icon")
        incorrect_username.config(font=("Times New Roman", 20, 'italic'))
        incorrect_username.config(bg='blanched almond')
        incorrect_username.place(relx=.5, rely=.4, anchor="n")
        if active_status == 1:  # return to correct previous screen
            window.after(3000, lambda: activation(logged_in, username, admin, db, mycursor, window, True))
        else:
            window.after(3000, lambda: activation(logged_in, username, admin, db, mycursor, window, False))
    else:  # *SINGLE TABLE PARAMETRISED SQL* amend the users activation
        mycursor.execute("UPDATE User set active = %s where username =%s", (active_status, users_selectable))
        db.commit()
        sucessful_change = Label(window, text="Change Successful")
        sucessful_change.config(font=("Times New Roman", 20, 'italic'))
        sucessful_change.config(bg='blanched almond')
        sucessful_change.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: control_activation(logged_in, username, admin, db, mycursor, window))


def view_users(logged_in, username, admin, db, mycursor, window):
    # The ability to view all usernames, with their privileges and contact email, including those deactivated
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("select username, email, admin, active from user ORDER BY active DESC")
    select_an_option = Label(window, text="Current Users")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=175, y=50)
    users = mycursor.fetchall()  # *  SINGLE TABLE SQL*, select all usernames, privileges and contact emails 
    # of users, with the deactivated accounts flagged and at the bottom 
    treeview = ttk.Treeview(window, columns=(1, 2, 3, 4), show="headings", height="5")
    style = ttk.Style(window)  # A table to display the information
    style.theme_use("clam")
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    style.configure('Treeview', rowheight=36)
    treeview.pack(side=TOP, pady=150)
    treeview.heading(1, text="Username")
    treeview.heading(2, text="Email")
    treeview.heading(3, text="Access Rights")
    treeview.heading(4, text="Active")
    # Vertical and Horizontal scrollbars to view the table fully if needed
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    scrollbar.pack(side="left", fill="y")
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    sctollbar2.pack(side='bottom', fill='x')
    for i in users:
        if i[2] == 1:  # Convert boolean SQL values into flags understandable to the user
            admin = "Admin"
        else:
            admin = "Standard"
        if i[3] == 1:
            active = "Activated"
        else:
            active = "Deactivated"
        data = [i[0], i[1], admin, active]
        treeview.insert('', 'end', values=data)


# The following section of routines comprise the Point of Service feature,satisfying fully client requirement 2. The 
# user has the ability to take orders consisting of many drinks, spanning a variety of sizes, along with the ability 
# to add or remove as many ingredients as they desire, with the cost from this added to the total bill. 

def till_menu(logged_in, username, admin, db, mycursor, window, list_ingred, order_list):
    # Select the desired recipe to place in the order REQUIREMENT 2.2
    # Only allows recipes that match all the criteria to be possibly made REQUIREMENT 2.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - Till")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Till")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="(Only Active Recipes With Active Ingredients Are Listed For Sale)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=225)
    if list_ingred is None:  # If this is the first recipe in the order, the contents of this conditional statement
        # will Select all Ingredients within the Inventory 
        mycursor.execute(
            "SELECT Ingredients.Ingredients_Name, Ingredients.Ingredients_remaining_g FROM Ingredients WHERE ((("
            "Ingredients.ingredients_useable)=1));")
        # *SINGLE TABLE SQL*, select the Quantity of all ingredients within the inventory, that are available
        # for use 
        list_ingred = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the array, 
        # containing both the ingredients name, and quantity 
    quantity = list_ingred
    list_ingred = []
    for i in quantity:  # Increase ingredient by 0.1g, this will not impact the user, as they can only operate in 
        # integer amounts. 
        value = i[
                    1] + 0.1  # The purpose is to allow a drink to be made that will use all remaining ingredients. 
        # The value will be rounded back down, removing the 0.1, 
        list_ingred.append([i[0], value])  # before the value is saved to the database
    for i in range(0, (
            len(list_ingred) - 1)):  # *LINEAR SEARCH* through the list of ingredients based on the index
        if list_ingred[i][1] < 1:  # If there is none of an ingredient in stock, then the ingredient cannot be used, 
            # hence it is 
            # removed. 
            list_ingred.pop(i)
    mycursor.execute(
        "select recipe_name from recipe where recipe_is_active = True")  # Parametrised SQL query to select all 
    # recipes which are sellable 
    recipe_names = mycursor.fetchall()
    recipes = []
    for i in recipe_names:  # Iterate through the list of recipes
        recipe_possible = True
        sql = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe " \
              "INNER JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(sql, (i[0],))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients 
        # within a recipe, as well as the quantity of the ingredient required 
        recipe_amount = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the array, 
        # containing both the ingredients name, and quantity needed to craft the recipe 
        sql = "SELECT Ingredients.Ingredients_Name FROM Recipe INNER JOIN (Ingredients INNER JOIN " \
              "Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON " \
              "Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Recipe.Recipe_Name)=%s) AND ((" \
              "Ingredients.ingredients_useable)=0)); "
        mycursor.execute(sql, (i[
                                   0],))  # Parametrised Multi-Table (3 Tables) SQL Query, selects all ingredients 
        # within the recipe which have been deactivated 
        ingredients_exists = mycursor.fetchall()
        if len(
                ingredients_exists) != 0:  # If any values exist within this array, it means one or more ingredients 
            # within the recipe have been deactivated 
            recipe_possible = False
        length = len(list_ingred)
        temp = [[k, v] for k, v in (Counter(dict(list_ingred)) - Counter(dict(recipe_amount))).items()]
        # *  DICTIONARY* Using the Counter function from collections, the lists are converted to dictionaries,
        # the keys are matched, and the quantities of the ingredients within the recipe are subtracted from the total
        # ingredients within the inventory. Any values below 0 are removed 
        if len(temp) != length:  # If any values have had to be removed from the list of ingredients, then the 
            # recipe demands a quantity of the ingredient which exceeds what it in the inventory 
            recipe_possible = False  # If all conditions are met, then the recipe can be added to a new list, 
            # of confirmed recipes which can be created 
        if recipe_possible:
            recipes.append(i[0])
    if order_list is not None:  # If drinks already exist within the order, allow the user the ability to finalise 
        # the order without adding another drink 
        submit = Button(window, text="Finalise order",
                        command=lambda: finalise_individual(logged_in, username, admin, db, mycursor, window, None,
                                                            None, None, None, None, list_ingred, order_list))
        submit.config(bg='blanched almond')
        submit.config(height=1, width=20)
        submit.place(x=225, y=425)

    info2 = Label(window, text="Beverage")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=250, y=270)
    choice = Combobox(window)
    choice['values'] = (recipes)  # select from available recipes
    choice.place(x=165, y=300)
    choice.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: select_size(logged_in, username, admin, db, mycursor, window, choice, recipes,
                                                     list_ingred, order_list))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=375)


def select_size(logged_in, username, admin, db, mycursor, window, choice, recipes, list_ingred, order_list):
    # Allows the user to select the size of drink desired REQUIREMENT 2.5
    if type(
            choice) != str:  # If the value of the variable choice is from the combobox, then it will have to be 
        # converted to STRING datatype 
        choice = choice.get()  # Returns string from STRINGVAR class
    ammendmants = []
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if recipes.count(
            choice) != 0:  # Conditional statement to confirm the selection entered is within the list of recipes
        size = StringVar()  # Both a small and medium size recipe can always be made providing they meet the criteria
        # specified prior 
        size_small = Radiobutton(window, text='Small', value="small", variable=size)
        size_small.config(bg='blanched almond')
        size_small.config(font=("Times New Roman", 20, "italic"))
        size_small.place(x=240, y=280)
        select_an_option = Label(window, text="Food State Nutrition™\n        - Select Size")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        info = Label(window, text="(The Size Of A Small And Large Compared To A Medium Is Found In Preferences)")
        info.config(bg='blanched almond')
        info.config(font=("Times New Roman", 12))
        info.place(x=75, y=225)
        size_medium = Radiobutton(window, text='Medium', value="medium", variable=size)
        size_medium.config(bg='blanched almond')
        size_medium.config(font=("Times New Roman", 20, "italic"))
        size_medium.place(x=240, y=355)
        mycursor.execute("select preference_value from preference where preference_name = 'Large Cup Ratio'")
        multiplier = mycursor.fetchone()  # *SINGLE TABLE SQL* selects the size increase of a large cup, 
        # which has been determined in the preferences 
        multiplier = (int(multiplier[
                              0]) + 100) / 100  # *SIMPLE MATHAMATICS* Converts percentage increase into a 
        # scalar multiplier 
        sql = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe " \
              "INNER JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(sql, (choice,))
        data = mycursor.fetchall()  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a 
        # recipe, as well as the quantity of the ingredient required 
        ingredients_required = []
        for i in data:
            holder = [i[0], int(ceil(i[
                                         1] * multiplier))]  # multiply each of the ingredients required by the 
            # scalar multiplier to determine the quantities needed for a large 
            ingredients_required.append(holder)
        length = len(list_ingred)
        temp = [[k, v] for k, v in (Counter(dict(list_ingred)) - Counter(dict(ingredients_required))).items()]
        # *DICTIONARY* Using the Counter function from collections, the lists are converted to dictionaries,
        # the keys are matched, and the quantities of the ingredients within the recipe are subtracted from the total
        # ingredients within the inventory. Any values below 0 are removed 
        if len(
                temp) == length:  # If any values have had to be removed from the list of ingredients, then the 
            # recipe demands a quantity of the ingredient which exceeds what it in the inventory 
            size_large = Radiobutton(window, text='Large', value="large", variable=size)
            size_large.config(bg='blanched almond')
            size_large.config(font=("Times New Roman", 20, "italic"))
            size_large.place(x=240, y=430)
        accept_data = Button(window, text="Enter",
                             command=lambda: confirm_size(logged_in, username, admin, db, mycursor, window, choice,
                                                          recipes, size, ammendmants, list_ingred, order_list))
        accept_data.config(bg='blanched almond')
        accept_data.config(height=1, width=20)
        accept_data.place(x=225, y=500)
    else:  # If an invalid recipe name was entered, display an error message, and return to previous screen
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 19, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: till_menu(logged_in, username, admin, db, mycursor, window, list_ingred, order_list))


def confirm_size(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants, list_ingred,
                 order_list):
    # CONTINUING REQUIREMENT 2.5 To confirm that a Size was selected, and to also subtract the ingredients used from 
    # the multi-dimensional array containing the ingredients 
    size = size.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    # If statement to select the relevant multiplier depending on the size of the drink
    if size == "large":
        mycursor.execute("select preference_value from preference where preference_name = 'Large Cup Ratio'")
        multiplier = mycursor.fetchone()  # *SINGLE TABLE SQL* selects the size increase of a large cup, 
        # which has been determined in the preferences 
        multiplier = (int(multiplier[
                              0]) + 100) / 100  # *SIMPLE MATHAMATICS* Converts percentage increase into a 
        # scalar multiplier 
        sql = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe " \
              "INNER JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(sql, (
            choice,))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a recipe, 
        # as well as the quantity of the ingredient required 
        data = mycursor.fetchall()  # *  MULTI DIMENSIONAL ARRAY*, With each element of the array, containing 
        # both the ingredients name, and quantity needed to craft the recipe 
        ingredients_required = []
        for i in data:
            holder = [i[0], ceil(
                i[1] * multiplier)]  # Ingredients needed are multiplied by the scalar multiplier determined by the size
            ingredients_required.append(
                holder)  # The ceil function from the math library rounds the value of the ingredients required up. 
            # As multiplication can leave values to more than 2 D.P 
    elif size == "small":
        mycursor.execute("select preference_value from preference where preference_name = 'Small Cup Ratio'")
        multiplier = mycursor.fetchone()  # *SINGLE TABLE SQL* selects the size increase of a small cup, 
        # which has been determined in the preferences 
        multiplier = (100 - int(
            multiplier[0])) / 100  # *SIMPLE MATHAMATICS* Converts percentage increase into a scalar multiplier
        sql = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe " \
              "INNER JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(sql, (
            choice,))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a recipe, 
        # as well as the quantity of the ingredient required 
        data = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the array, containing 
        # both the ingredients name, and quantity needed to craft the recipe 
        ingredients_required = []
        for i in data:
            holder = [i[0], ceil(
                i[1] * multiplier)]  # Ingredients needed are multiplied by the scalar multiplier determined by the size
            ingredients_required.append(
                holder)  # The ceil function from the math library rounds the value of the ingredients required up. 
            # As multiplication can leave values to more than 2 D.P 
    elif size == "medium":
        sql = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe " \
              "INNER JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(sql, (
            choice,))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a recipe, 
        # as well as the quantity of the ingredient required 
        multiplier = 1  # A medium size will have a multiplier of 1, as no values are increased or decreased
        ingredients_required = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the 
        # array, containing both the ingredients name, and quantity needed to craft the recipe 
    else:  # If an invalid recipe name was entered, display an error message, and return to previous screen
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: select_size(logged_in, username, admin, db, mycursor, window, choice, recipes, list_ingred,
                                         order_list))
    if size == "small" or size == "medium" or size == "large":
        list_ingred = [[k, v] for k, v in (Counter(dict(list_ingred)) - Counter(dict(ingredients_required))).items()]
        # *DICTIONARY* Using the Counter function from collections, the lists are converted to dictionaries,
        # the keys are matched, and the quantities of the ingredients within the recipe are subtracted from the total
        # ingredients within the inventory. Any values equal to 0 are removed 
        order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants,
                          multiplier, list_ingred, order_list)


def order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants, multiplier,
                      list_ingred, order_list):
    # A menu to offer the ability for the user to make alterations to the order REQUIREMENT 2.6
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Order Amendments")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)

    info = Label(window, text="Customers May Desire To Remove Or Add Ingredients To Their Beverage At Cost Price")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=25, y=225)
    add = Button(window, text="Add An Additional Product",
                 command=lambda: add_ingredient(logged_in, username, admin, db, mycursor, window, choice, recipes, size,
                                                ammendmants, multiplier, list_ingred, order_list))
    remove = Button(window, text="Remove An Existing Product",
                    command=lambda: remove_ingredient_from_order(logged_in, username, admin, db, mycursor, window,
                                                                 choice, recipes, size, ammendmants, multiplier,
                                                                 list_ingred, order_list))
    progress = Button(window, text="Progress",
                      command=lambda: finalise_individual(logged_in, username, admin, db, mycursor, window, choice,
                                                          recipes, size, ammendmants, multiplier, list_ingred,
                                                          order_list))
    # The options to either add an ingredient to a drink, remove an ingredient, or progress to the next stage
    add.config(bg='blanched almond')
    add.config(height=1, width=20)
    add.place(x=225, y=300)
    remove.config(bg='blanched almond')
    remove.config(height=1, width=21)
    remove.place(x=225, y=375)
    progress.config(bg='blanched almond')
    progress.config(height=1, width=20)
    progress.place(x=225, y=450)


def add_ingredient(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants, multiplier,
                   list_ingred, order_list):
    # CONTINUING REQUIREMENT 2.6
    # The ability is provided to add different ingredients to the recipe 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Current Inventory")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=150, y=50)
    treeview = ttk.Treeview(window, columns=(1, 2), show="headings", height="6")
    style = ttk.Style(window)  # A table to display the current ingredients in stock, and their remaining quantities
    style.theme_use("clam")
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    treeview.pack(side=TOP, pady=130)
    treeview.heading(1, text="Ingredients Name")
    treeview.heading(2, text="Quantity (KG)")
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    scrollbar.pack(side="left", fill="y")
    sctollbar2.pack(side='bottom', fill='x')
    # Vertical and Horizontal scrollbars to view the table fully if needed
    add_ingred = []
    for i in list_ingred:
        add_ingred.append(i[0])
        kg_values = round(i[1] / 1000,3)  # display the values in Kilograms
        data = [i[0], kg_values]
        treeview.insert('', 'end', values=data)
    added = Combobox(window)
    added['values'] = add_ingred  # ingredients that can be added
    added.place(x=165, y=330)
    added.config(height=10, width=40)
    info1 = Label(window, text="Ingredient")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=265, y=300)
    info1 = Label(window, text="Quantity (g)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=265, y=370)
    quantity = StringVar()
    change_label_entry = Entry(window, textvariable=quantity, text=quantity, font=('Verdana', 15), bg='blanched almond')
    quantity.set("")
    change_label_entry.place(x=170, y=400)
    accept_data = Button(window, text="Enter",
                         command=lambda: make_addition(logged_in, username, admin, db, mycursor, window, choice,
                                                       recipes, size, ammendmants, multiplier, added, quantity,
                                                       list_ingred, order_list))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=450)
    back = Button(window, text="Back",
                  command=lambda: order_ammendments(logged_in, username, admin, db, mycursor,
                                                    window, choice, recipes, size, ammendmants, multiplier,
                                                    list_ingred, order_list))
    back.config(bg='blanched almond')
    back.config(height=1, width=20)
    back.place(x=225, y=500)


def make_addition(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants, multiplier,
                  added, quantity, list_ingred, order_list):
    # CONTINUING REQUIREMENT 2.6 Confirms that a valid ingredient and quantity has been entered to add, 
    # then subtracts those values from the available ingredients. Also saves the amendment to a variable 
    quantity = quantity.get()  # Returns string from STRINGVAR class
    added = added.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    valid = False
    if quantity.isdigit():  # Confirms value entered is an integer value
        for i in list_ingred:  # *LINEAR SEARCH* through list of ingredients
            if i[0] == added:  # Confirms the ingredient that has been selected to be added is a valid Selection
                if i[1] >= int(
                        quantity):  # Confirms the amount of stock needed to add to the recipe doesn't exceed the 
                    # quantity available 
                    valid = True
    if valid:
        ammendmants.append(
            "+" + added + " " + quantity)  # The amendment is added to a variable, to be stored for later manipulation
        add_array = [[added, int(quantity)]]
        list_ingred = [[k, v] for k, v in (Counter(dict(list_ingred)) - Counter(dict(add_array))).items()]
        # *DICTIONARY* Using the Counter function from collections, the lists are converted to dictionaries,
        # the keys are matched, and the quantities of the ingredients within the recipe are subtracted from the total
        # ingredients within the inventory. Any values equal to 0 are removed 
        changes_made = Label(window, text="Changes Made")
        changes_made.config(font=("Times New Roman", 30, 'italic'))
        changes_made.config(bg='blanched almond')
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size,
                                               ammendmants, multiplier, list_ingred, order_list))
    else:  # If an invalid recipe name was entered, display an error message, and return to the order ammendments menu
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: add_ingredient(logged_in, username, admin, db, mycursor, window, choice,
                                            recipes, size, ammendmants, multiplier,
                                            list_ingred, order_list))


def remove_ingredient_from_order(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants,
                                 multiplier, list_ingred, order_list):
    # CONTINUING REQUIREMENT 2.6
    # The ability is provided to remove different ingredients to the recipe 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Remove Ingredient")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="Although An Ingredient Is Removed, The Price Will Not Be Affected")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=225)
    sql = "SELECT Ingredients.Ingredients_Name FROM Recipe INNER JOIN (Ingredients INNER JOIN " \
          "Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON " \
          "Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Recipe.Recipe_Name)=%s)); "
    mycursor.execute(sql,
                     (
                     choice,))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a recipe
    data = mycursor.fetchall()
    data_list = []
    for i in data:
        data_list.append(i[0])
    for i in ammendmants:  # *LINEAR SEARCH* to see if any ingredient changes have already been made
        if i[0] == "-":  # If any ingredients have already been removed, they will not be able to be removed twice
            remove = i[1:]
            data_list.remove(remove)
        if i[0] == "+":  # If an ingredient has been added to the drink, it can still be removed during this process
            added = i[1:]
            index = added.index(" ")
            added = added[:index]
            if data_list.count(added) == 0:
                data_list.append(added)

    info1 = Label(window, text="Ingredient")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=265, y=300)
    removed = Combobox(window)
    removed['values'] = data_list  # ingredients in the recipe that can be removed
    removed.place(x=165, y=330)
    removed.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: make_removal(logged_in, username, admin, db, mycursor, window, choice, recipes,
                                                      size, ammendmants, multiplier, removed, list_ingred, order_list))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=400)

    Back = Button(window, text="Back",
                  command=lambda: order_ammendments(logged_in, username, admin, db, mycursor,
                                                    window, choice, recipes, size, ammendmants, multiplier,
                                                    list_ingred, order_list))

    Back.config(bg='blanched almond')
    Back.config(height=1, width=20)
    Back.place(x=225, y=450)

def make_removal(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants, multiplier,
                 removed, list_ingred, order_list):
    # CONTINUING REQUIREMENT 2.6 Confirms that a valid ingredient has been entered to add, then adds those values to 
    # the available ingredients. Also saves the amendment to a variable 
    removed = removed.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    sql = "SELECT Ingredients.Ingredients_Name FROM Recipe INNER JOIN (Ingredients INNER JOIN " \
          "Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON " \
          "Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Recipe.Recipe_Name)=%s)); "
    mycursor.execute(sql,
                     (
                     choice,))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients within a recipe
    data = mycursor.fetchall()
    ingredients = []
    for i in data:
        ingredients.append(i[0])
    quantity = None
    temp = []
    for i in ammendmants:  # *LINEAR SEARCH* To collect a total list of ingredients, it is possible the 
        # ingredient to remove was added as an extra 
        if i[0] == "-":  # if it has already been removed, it cannot be removed twice
            remove = i[1:]
            temp.append(i[0])
            ingredients.remove(remove)
        if i[0] == "+":  # if the ingredient was added as an extra, it can still be removed
            added = i[1:]
            index = added.index(" ")
            added = added[:index]
            quantity = int(i[index + 1:])
            temp.append(added)
    if removed in temp:  # A conditional statement to account for if the ingredient to remove was an extra
        add_array = [removed, quantity]
        list_ingred.append(add_array)
        totals = {}
        for key, value in list_ingred:
            totals[key] = totals.get(key, 0) + value
        list_ingred = list(totals.items())
        for i in range(0, len(
                ammendmants)):  # If the ingredient to be removed, was once added to the recipe during checkout, 
            # then it removed from the amendments 
            holder = ammendmants[i][1:]
            index = holder.index(" ")
            holder = holder[:index]
            if holder == removed:
                ammendmants.pop(i)
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size,
                                               ammendmants, multiplier, list_ingred, order_list))
    elif removed in ingredients:  # a conditional statement to check if the ingredient to remove is in the recipe
        sql = "SELECT Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe INNER JOIN (Ingredients INNER " \
              "JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s) AND ((Ingredients.Ingredients_Name)=%s)); "
        mycursor.execute(sql, (choice,
                               removed))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the quantity of the
        # ingredients within a recipe 
        add_array = mycursor.fetchall()
        holder = add_array[0][
                     0] * multiplier  # The ingredient quantity in the recipe may be affected due to the size ordered
        add_array = [removed, holder]
        list_ingred.append(add_array)  # Add the newly available ingredients to the inventory available
        list_ingred = tuple(map(tuple, list_ingred))  # Convert the list to a tuple
        totals = {}
        for key, value in list_ingred:  # Any repeat keys in the tuple have their values summed, to prevent having an
            # inventory with two entities of the same ingredient 
            totals[key] = totals.get(key, 0) + value
        ammendmants.append(
            "-" + removed)  # The amendments variable is updated to indicate an ingredient has been removed
        list_ingred = list(totals.items())
        changes_made = Label(window, text="Drink Amendment Has Been Made")
        changes_made.config(font=("Times New Roman", 26, 'italic'))
        changes_made.config(bg='blanched almond')
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size,
                                               ammendmants, multiplier, list_ingred, order_list))
    else:  # If an invalid recipe name was entered, display an error message, and return to the order ammendments menu
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: order_ammendments(logged_in, username, admin, db, mycursor, window, choice, recipes, size,
                                               ammendmants, multiplier, list_ingred, order_list))


def finalise_individual(logged_in, username, admin, db, mycursor, window, choice, recipes, size, ammendmants,
                        multiplier, list_ingred, order_list):
    # At this stage of the order process, the individual drink is finalised
    # The price up to this point is displayed on screen REQUIREMENT 2.3
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if order_list is None:
        order_list = []
    if choice != None:
        sql = "Select recipe_price£ from recipe where recipe_name = %s"
        mycursor.execute(sql, (choice,))  # *SINGLE TABLE PARAMETRISED SQL*, select the price of the recipe
        price = mycursor.fetchone()
        price = round((price[0] * multiplier), 2)  # applies the scalar multiplier for the price
        for i in ammendmants:  # The amendments are iterated though to see if the price is affected
            if i[0] == "+":  # Additions to a recipe will increase the price, but removal of ingredients has no effects
                # to price 
                added = i[1:]
                index = added.index(" ")
                added = added[:index]
                quantity = int(i[index + 1:])
                sql = "Select ingredients_price_kg from ingredients where ingredients_name = %s"
                mycursor.execute(sql,
                                 (
                                 added,))  # *SINGLE TABLE PARAMETRISED SQL*, select the cost of the ingredient
                price_kg = mycursor.fetchone()
                price = price + ceil(
                    (price_kg[0] / 1000) * quantity)  # *SIMPLE MATHAMATICS* Calculates total price of drink
                # Which is the total of the listed price, plus cost of ingredient
        index = len(
            order_list) + 1  # An index is added for display purposes to allow for easy selecting of each individual 
        # recipe 
        order_list.append([index, choice, price, size, ammendmants])
    treeview = ttk.Treeview(window, columns=(1, 2, 3, 4, 5), show="headings", height="6")

    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Current Order Contents")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=120, y=50)
    style = ttk.Style(window)  # A table to display the current set of orders
    style.theme_use("clam")
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    treeview.pack(side=TOP, pady=130)
    treeview.heading(1, text="Index")
    treeview.heading(2, text="Ingredients Name")
    treeview.heading(3, text="Price £")
    treeview.heading(4, text="Size")
    treeview.heading(5, text="Amendments")
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    scrollbar.pack(side="left", fill="y")
    sctollbar2.pack(side='bottom', fill='x')
    # Vertical and Horizontal scrollbars to view the table fully if needed
    total_price = 0
    for i in order_list:
        total_price = total_price + float(i[2])  # combine the total price of all drinks in the order to this point
        string_price = (str(i[2])).split(".")  # Format the price so it is in the form £.pp
        if len(string_price[1]) < 2:
            price = string_price[0] + "." + string_price[1] + "0"
        else:
            price = string_price[0] + "." + string_price[1]
        data = [i[0], i[1], price, i[3], i[4]]
        treeview.insert('', 'end', values=data)
    try:  # Format the total price to the form £.pp 
        pennies = str(total_price).split('.')
        if len(pennies[1]) == 1:
            total_price = str(total_price) + "0"
    except IndexError:  # if all drinks have been removed from the order, the price will be Zero
        total_price = 0
    price = Label(window, text="Current Order Price: £" + str(total_price))
    total_price = float(total_price)
    price.config(bg='blanched almond')
    price.config(font=("Times New Roman", 18))
    price.place(x=175, y=300)
    another_order = Button(window, text="Add To Total Order",
                           command=lambda: till_menu(logged_in, username, admin, db, mycursor, window, list_ingred,
                                                     order_list))
    remove = Button(window, text="Remove From Total Order",
                    command=lambda: remove_item_from_order(logged_in, username, admin, db,
                           mycursor, window, choice, recipes, size, ammendmants,
                           multiplier, list_ingred, order_list))
    progress = Button(window, text="Progress",
                      command=lambda: finalise_order(logged_in, username, admin, db, mycursor, window, total_price,
                                                     list_ingred, order_list))
    # The three buttons dictate to add another drink to the order, Remove a drink from the order during the checkout 
    # process, or confirm and navigate to payment 
    another_order.config(bg='blanched almond')
    another_order.config(height=1, width=20)
    another_order.place(x=225, y=350)
    remove.config(bg='blanched almond')
    remove.config(height=1, width=20)
    remove.place(x=225, y=400)
    progress.config(bg='blanched almond')
    progress.config(height=1, width=20)
    progress.place(x=225, y=450)


def remove_item_from_order(logged_in, username, admin, db,
                           mycursor, window, choice, recipes, size, ammendmants,
                           multiplier, list_ingred, order_list):
    # Allow for a drink to be removed from the order during checkout REQUIREMENT 2.7
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Current Order Contents")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=120, y=50)
    treeview = ttk.Treeview(window, columns=(1, 2, 3, 4, 5), show="headings", height="6")
    style = ttk.Style(window)
    style.theme_use("clam")  # A table to display the current set of orders
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    treeview.pack(side=TOP, pady=130)
    treeview.heading(1, text="Index")
    treeview.heading(2, text="Ingredients_name")
    treeview.heading(3, text="Price £")
    treeview.heading(4, text="Size")
    treeview.heading(5, text="Amendments")
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    scrollbar.pack(side="left", fill="y")
    sctollbar2.pack(side='bottom', fill='x')
    # Vertical and Horizontal scrollbars to view the table fully if needed
    for i in order_list:
        treeview.insert('', 'end', values=i)
    info = Label(window, text="Each Index Corresponds To A Component Of The Order")
    info.config(bg='blanched almond')  # Select the index of the drink to remove from the order
    info.config(font=("Times New Roman", 12))
    info.place(x=125, y=300)
    index = []
    for i in order_list:
        index.append(i[0])
    removed = Combobox(window)
    removed['values'] = index  # select the index of the drink to remove
    removed.place(x=165, y=380)
    removed.config(height=10, width=40)

    info1 = Label(window, text="Index")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=265, y=350)

    accept_data = Button(window, text="Enter",
                         command=lambda: confirn_removal(logged_in, username, admin, db, mycursor, window, removed,
                                                         list_ingred, order_list))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=420)



def confirn_removal(logged_in, username, admin, db, mycursor, window, removed, list_ingred, order_list):
    # CONTINUING REQUIREMENT 2.7
    # Confirm the entry was valid, and remove it from the list of orders
    removed = removed.get()  # Returns string from STRINGVAR class
    removeable = False
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)   
    if removed.isdigit():  # The index must be a number
        removed = int(removed)
        counter = 0
        for i in order_list:  # *GROUP C LINEAR SEARCH* to find drink to be removed
            counter = counter + 1  # The position in the array of the drink to remove
            index = i[0]
            if index == removed:  # If the index value exists in the list, remove it from the list of orders
                order_list.pop(counter - 1)
                removeable = True
        if removeable:
            changes_made = Label(window, text="Drink Amendment Has Been Made")
            changes_made.config(font=("Times New Roman", 26, 'italic'))
            changes_made.config(bg='blanched almond')
            changes_made.place(relx=.5, rely=.4, anchor="n")
            window.after(3000,
                         lambda: finalise_individual(logged_in, username, admin, db, mycursor, window, None, None, None,
                                                     None, None, list_ingred, order_list))
    if removeable == False or type(
            removed) == str:  # If an invalid index was entered, display an error message, and return to previous screen
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: finalise_individual(logged_in, username, admin, db, mycursor, window, None, None, None,
                                                 None, None, list_ingred, order_list))


# The following routines are an extension of the point of service system, which is specifically focused around data 
# collection. Values such as cost of sale, temperature of sale, date of sale, and several other values are collected 
# to allow the relevant changes to be made to the CSV file, and the database to be updated where needed. Satisfying 
# requirement 3 

def finalise_order(logged_in, username, admin, db, mycursor, window, total_price, list_ingred, order_list):
    # All additional information for the sale is collected. Such as the total cost of the sale and the temperature at 
    # the time of the sale *CLIENT SERVER MODEL* The application (client) is requesting temperature data 
    # from the openweather.org server, with certain parameters such as a Unique key and Current City 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if len(order_list) == 0:  # If no items are in the order, then there is no further action needed
        error_message = Label(window, text="No order has been made")
        error_message.config(font=("Times New Roman", 26, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: till_menu(logged_in, username, admin, db, mycursor, window, None, None))
    else:
        mycursor.execute("Select preference_value from preference where preference_name = 'Current City'")
        city = mycursor.fetchone()  # *SINGLE TABLE SQL*, select the Current City of where the store is located
        city = (city[0])
        mycursor.execute("Select preference_value from preference where preference_name = 'API KEY'")
        key = mycursor.fetchone()  # *SINGLE TABLE SQL*, select the current API KEY the manager has access to
        key = (key[0])
        try:  # *  CALLING PARAMETERISED WEB SERVICE API* Allowing access to the temperature data
            query = 'q=' + city;
            information = get('https://api.openweathermap.org/data/2.5/weather?' + query +
                              '&exclude=hourly,daily,minutely&appid=' + key + '&units=metric');  # The api has 
            # parameters which will access the data for the certain city, by having access granted by the users 
            # unique key 
            weather_data = information.json();  # *PARSING JSON*
            temperature = int(round((weather_data["main"][
                "temp"])))  # *DICTIONARY* From the data collected, access the current temperature
        except KeyError and exceptions.ConnectionError:  # In the situation where there is no internet/api access
            mycursor.execute(
                "SELECT sales_temperature FROM sales where sales_temperature != 'None' ORDER BY sales_id DESC LIMIT 1")
            try:
                data = mycursor.fetchall()  # select the temperature from the last sale, and substitute it for the 
                # temperature of this sale 
                temperature = data[0][0]
            except IndexError:  # In the event no prior sales have been made, as a last resort, the temperature is 
                # given no value 
                temperature = None
            error_message = Label(window,
                                  text="Weather Request Was Invalid, Please Inform Manager And Check Internet "
                                       "Connection")
            error_message.config(font=("Times New Roman", 15, 'italic'))
            error_message.config(bg='blanched almond')
            error_message.place(relx=.5, rely=.4, anchor="n")
        current_date = date.today()  # Accessing current date from the system clock, by using the date from the 
        # datetime module 
        sql = "Select user_ID from user where username = %s"
        mycursor.execute(sql,
                         (
                         username,))  # *SINGLE TABLE PARAMETRISED SQL*, select the user who is making the sale
        user_id = mycursor.fetchone()
        user_id = (user_id[0])
        recipe_id = []
        prices = []
        cost = 0
        for i in order_list:
            sql = "select recipe_id from recipe where recipe_name = %s"
            mycursor.execute(sql, (i[1],))
            name = mycursor.fetchone()  # *SINGLE TABLE PARAMETRISED SQL*, select the recipe id's of the 
            # drinks in the sale 
            recipe_id.append(name[0])
            sql = "SELECT (Ingredients_price_kg)*(quantity_of_ingredients_g)/1000 AS Expr1 FROM Recipe INNER JOIN (" \
                  "Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
                  "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = " \
                  "Recipe_Ingredients_Bridge.Recipe_ID GROUP BY Recipe.Recipe_Name, " \
                  "Recipe_Ingredients_Bridge.quantity_of_ingredients_g, Ingredients.Ingredients_price_kg HAVING (((" \
                  "Recipe.Recipe_Name)=%s)) "
            current_cost = 0
            mycursor.execute(sql, (i[
                                       1],))  # Parametrised Multi-Table (3 Tables) SQL Query, Selects the ingredients
            # within a recipe, the quantity of the ingredient in that recipe, as well as its cost per kg, 
            # then multiplies the values to find the cost of the serving in the recipe 
            data = mycursor.fetchall()
            for x in data:  # total all the costs for each component in the recipe
                current_cost = x[0] + current_cost
            if i[3] == "small":  # Account for the cost alterations based on size
                mycursor.execute("select preference_value from preference where preference_name = 'Small Cup Ratio'")
                multiplier = mycursor.fetchone()  # *SINGLE TABLE SQL* selects the size increase of a small 
                # cup, which has been determined in the preferences 
                multiplier = (100 - int(multiplier[
                                            0])) / 100  # *SIMPLE MATHAMATICS* Converts percentage increase 
                # into a scalar multiplier 
            elif i[3] == "large":
                mycursor.execute("select preference_value from preference where preference_name = 'Large Cup Ratio'")
                multiplier = mycursor.fetchone()  # *SINGLE TABLE SQL* selects the size increase of a large 
                # cup, which has been determined in the preferences 
                multiplier = (int(multiplier[
                                      0]) + 100) / 100  # *SIMPLE MATHEMATICS* Converts percentage increase 
                # into a scalar multiplier 
            else:
                multiplier = 1
            current_cost = current_cost * multiplier  # Account for the cost alterations based on size
            alteration = i[4]  # select the dimension of the array that contains the alterations
            for y in alteration:  # iterate through the list of alterations
                if y[0] == "-":  # If an ingredient was removed, then the cost is decreased
                    ingredient = y[1:]
                    sql = "SELECT (Ingredients_price_kg)*(quantity_of_ingredients_g)/1000 AS Expr1 FROM Recipe INNER " \
                          "JOIN (Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
                          "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = " \
                          "Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Ingredients.Ingredients_Name)=%s) AND ((" \
                          "Recipe.Recipe_Name)=%s)); "
                    mycursor.execute(sql, (ingredient, i[1]))
                    data = mycursor.fetchone()  # Parametrised Multi-Table (3 Tables) SQL Query,  Selects the 
                    # ingredient removed, the quantity of the ingredient that was removed, as well as its cost per 
                    # kg, then multiplies the values over 1000 to find the cost of the serving in the recipe 
                    current_cost = current_cost - (data[0] * multiplier)  # reflect the cost decrease
                if y[0] == "+":  # If an ingredient was added, then the cost is increased
                    added = y[1:]
                    index = added.index(" ")
                    added = added[:index]
                    quantity = int(y[index + 1:])
                    sql = "SELECT ((Ingredients_price_kg)*%s)/1000 AS Expr1 FROM Ingredients WHERE (((" \
                          "Ingredients.Ingredients_Name)=%s)); "
                    mycursor.execute(sql, (quantity,
                                           added))  # Parametrised Multi-Table (3 Tables) SQL Query,  Selects the 
                    # ingredient added, the quantity of the ingredient that was added, as well as its cost per kg, 
                    # then multiplies the values over 1000 to find the cost of the serving in the recipe 
                    data = mycursor.fetchone()
                    current_cost = current_cost + (data[0] * multiplier)  # reflect the cost decrease
            cost = cost + current_cost
            cost = round(cost, 2)  # round the totals to get the value to 2dp, the format for sterling
        complete_transaction(logged_in, username, admin, db, mycursor, window, total_price, total_price, cost,
                             recipe_id, user_id, temperature, current_date, order_list, list_ingred)  # ,order_list)


def complete_transaction(logged_in, username, admin, db, mycursor, window, total_price, working_total, cost, recipe_id,
                         user_id, temperature, current_date, order_list, list_ingred):
    # Allows for payment to be tendered, displaying the amount outstanding for the purchase to be complete REQUIREMENT 2.3
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Change")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="(Once Full Payment Has Been Tendered, The Transaction Is Recorded)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=225)
    pennies = str(total_price).split('.')
    if len(pennies[1]) == 1:  # Format the total price to the form £.pp 
        total_price = str(total_price) + "0"

    display = Label(window, text="Total Owed Is £" + str(total_price))
    total_price = float(total_price)
    display.config(bg='blanched almond')
    display.config(font=("Times New Roman", 12))
    display.place(x=225, y=300)
    quantity = StringVar()
    change_label_entry = Entry(window, textvariable=quantity, text=quantity, font=('Verdana', 15), bg='blanched almond')
    quantity.set("")
    change_label_entry.place(x=170, y=370)
    info = Label(window, text="Tendered")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12, "italic"))
    info.place(x=260, y=340)
    accept_data = Button(window, text="Enter",
                         command=lambda: confrim_payment(logged_in, username, admin, db, mycursor, window, total_price,
                                                         working_total, cost, recipe_id, user_id, temperature,
                                                         current_date, quantity, order_list, list_ingred))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=415)

def confrim_payment(logged_in, username, admin, db, mycursor, window, total_price, working_total, cost, recipe_id,
                    user_id, temperature, current_date, quantity, order_list, list_ingred):
    # Ensure a valid sterling amount is entered, accept tendered amoount
    quantity = quantity.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    accept = False
    if quantity.replace('.', '', 1).isdigit():  # confirms the string is a valid sterling value
        quantity = float(quantity)
        if round(quantity, 2) == quantity:
            accept = True
    if accept:
        total_price = round(total_price - quantity, 2)  # subtracts amoount payed from the amount outstanding
        if total_price > 0:  # if the full payment has not been made, loop back to the previous routine until it has been
            complete_transaction(logged_in, username, admin, db, mycursor, window, total_price, working_total, cost,
                                 recipe_id, user_id, temperature, current_date, order_list, list_ingred)
        elif total_price <= 0:
            confrim_change(logged_in, username, admin, db, mycursor, window, total_price, working_total, cost,
                           recipe_id, user_id, temperature, current_date, order_list, list_ingred)
    if not accept:
        error_message = Label(window, text="Please Enter In The Form ££.pp")
        error_message.config(font=("Times New Roman", 20, 'italic'))
        error_message.config(bg='blanched almond')
        error_message.place(relx=.5, rely=.4, anchor="n")

        # If an invalid recipe name was entered, display an error message, and return to previous screen
        window.after(3000, lambda: complete_transaction(logged_in, username, admin, db, mycursor, window, total_price,
                                                        working_total, cost, recipe_id, user_id, temperature,
                                                        current_date, order_list, list_ingred))


def confrim_change(logged_in, username, admin, db, mycursor, window, total_price, working_total, cost, recipe_id,
                   user_id, temperature, current_date, order_list, list_ingred):
    # Calculation of change, if need. REQUIREMENT 2.3
    if total_price == 0:
        update_db(logged_in, username, admin, db, mycursor, window, working_total, cost, recipe_id, user_id,
                  temperature, current_date, order_list, list_ingred)
    if total_price < 0:  # Format the total price to the form £.pp 
        total_price = total_price * -1
        pennies = str(total_price).split('.')
        if len(pennies[1]) == 1:
            total_price = str(total_price) + "0"
        select_an_option = Label(window, text="Food State Nutrition™\n        - Return Change")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        info = Label(window, text="Proceed To Prepare the Customers Order")
        info.config(bg='blanched almond')
        info.config(font=("Times New Roman", 12))
        info.place(x=150, y=275)
        return_value = Label(window, text="Please Return The Amount Of £" + str(total_price) + " To The Customer")
        total_price = float(total_price)
        return_value.config(bg='blanched almond')
        return_value.config(font=("Times New Roman", 12))
        return_value.place(x=125, y=225)
        total_price = 0
        accept_data = Button(window, text="Returned",
                             command=lambda: confrim_change(logged_in, username, admin, db, mycursor, window,
                                                            total_price, working_total, cost, recipe_id, user_id,
                                                            temperature, current_date, order_list, list_ingred))
        accept_data.config(bg='blanched almond')
        accept_data.config(height=2, width=40)
        accept_data.place(x=150, y=350)


def update_db(logged_in, username, admin, db, mycursor, window, total_price, cost, recipe_id, user_id, temperature,
              current_date, order_list, list_ingred):
    # The transaction will update the database in the appropriate manner. Recording details of the sale and the 
    # ingredients consumed. REQUIREMENT 3.1 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    prices = []
    for i in order_list:
        prices.append(i[2])
    mycursor.execute("SELECT ingredients_name, ingredients_remaining_g from Ingredients where ingredients_useable = 1")
    # *SINGLE TABLE PARAMETRISED SQL*, select the name and Quantity of all ingredients within the inventory, 
    # that are available for use 
    data = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the array, containing both
    # the ingredeinets name, and quantity 
    list_ingred_names = []
    for i in list_ingred:  # Inserts all ingredients names into an array which are remaining after the sale has taken
        # place 
        list_ingred_names.append(i[0])
    ingredients = []
    for i in data:  # Inserts all ingredients names into an array which exist in the database
        ingredients.append(i[0])
    for i in ingredients:
        if list_ingred_names.count(
                i) == 0:  # if there is a value in the list of database ingredients, that is no longer in the 
            # available after the transaction, it means that it has been used entirely 
            data = [i,
                    0]  # This value is inserted back into the ingredients array, but with the value 0, as it has 
            # been entirely used 
            list_ingred.append(data)
    for i in list_ingred:
        name = i[0]
        quantity = round(i[1])  # Round the quantity of each ingredient down, to equate for the 0.1 added prior
        mycursor.execute("Update Ingredients set ingredients_remaining_g = %s where ingredients_name = %s",
                         (quantity, name))  # *SINGLE TABLE PARAMETRISED SQL* Update ingredients Table
    mycursor.execute("INSERT INTO Sales(user_id,sales_date,sales_temperature) VALUES (%s,%s,%s)",
                     (
                     user_id, current_date, temperature))  # *SINGLE TABLE PARAMETRISED SQL* update sales Table
    mycursor.execute(
        "SELECT sales_id FROM sales ORDER BY sales_id DESC LIMIT 1")  # *SINGLE TABLE SQL* select sales Id 
    # from the sale that has just been made 
    sales_id = mycursor.fetchall()
    for i in range(0, len(recipe_id)):  # insert all sales into the sales recipe bridge
        mycursor.execute("INSERT INTO Sales_Recipe_Bridge(sales_id,recipe_id,sales_price) VALUES (%s,%s,%s)",
                         (sales_id[0][0], recipe_id[i], prices[i]))
    db.commit()  # Save changes to the database
    update_csv(logged_in, username, admin, db, mycursor, window, total_price, sales_id[0], cost, recipe_id)


def update_csv(logged_in, username, admin, db, mycursor, window, total_price, sales_id, cost, recipe_id):
    # A log of the translation will be recorded for taxation purposes in a format the client has requested (
    # CSV).REQUIREMENT 3.2 
    mycursor.execute("select preference_value from preference where preference_name = 'file path-csv'")
    file_path = mycursor.fetchone()  # *SINGLE TABLE SQL*, select the user decided filepath for the where 
    # the CSV is located 
    profit = str(total_price - cost)  # profit calculation
    current_date = date.today()  # The date of sale using the date module from datetime library
    current_date = current_date.strftime("%d %b %Y")
    current_date = (str(current_date)).replace("-", " ")  # format the date into the british standard of date/month/year
    recipe_name = ""
    for i in recipe_id:
        sql = "select recipe_name from recipe where recipe_id = %s"
        mycursor.execute(sql, (i,))  # *SINGLE TABLE PARAMETRISED SQL*, select the names involved in the sale
        name = mycursor.fetchone()
        recipe_name = recipe_name + " " + name[0]
    try:
        f = open(file_path[0], "a")  # *WRITING TO FILE* input data of the sale into the sales data file
        f.write(str(sales_id[0]) + "," + recipe_name + "," + username + "," + current_date + "," + str(
            total_price) + "," + str(cost) + "," + str(profit) + "\n")
        f.close()
        complete = Label(window, text="Sale Complete")
        complete.config(bg='blanched almond')
        complete.config(font=("Times New Roman", 40, 'italic'))
        complete.place(relx=.5, rely=.5, anchor="n")
    except FileNotFoundError and PermissionError:  # if the file has been deleted, or is currently open so not accessible
        try:  # attempt to create a new file on the desktop with the information
            filename = path.join(path.join(environ['USERPROFILE']), 'Desktop') + "//recordable_sales_data.csv"
            f = open(filename, "w")
            headers = "sale_id, recipe name,cashier,sale date,sale price,sale cost,sale profit\n"
            f.write(headers)
            f.write(str(sales_id[0]) + "," + recipe_name + "," + username + "," + current_date + "," + str(
                total_price) + "," + str(cost) + "," + str(profit) + "\n")
            f.close()
            error_message = Label(window, text="Could Not Find File, Please Check File Preferences\n Second File Made")
            error_message.config(font=("Times New Roman", 20, 'italic'))
            error_message.config(bg='blanched almond')
            error_message.place(relx=.5, rely=.4, anchor="n")
        except PermissionError:  # if the new file has already been made, as is currently open also, then the warning
            # message is displayed 
            error_message = Label(window, text="File Could Not Be Opened As It Is Already Open")
            error_message.config(bg='blanched almond')
            error_message.config(font=("Times New Roman", 18, 'italic'))
            error_message.place(relx=.5, rely=.5, anchor="n")
    window.after(3000, lambda: till_menu(logged_in, username, admin, db, mycursor, window, None, None))


# The following collection of modules is designed to fulfill client requirement 4. The ability to add stock to the 
# inventory, is coupled with the ability to to edit the details of the items manually. Particular ingredients can be 
# removed and re-added for use at any time, while all active ingredients can be seen in the viewing section. All 
# features are reserved exclusively for admin users 

def manage_stock(logged_in, username, admin, db, mycursor, window):
    # A menu to offer the ability for the user to select, view, edit or see restock prediction dates
    # REQUIREMENT 4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - Manage Stock")
    select_an_option = Label(window, text="Food State Nutrition™\n        - Manage Stock")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="(The Individual Components Of A Recipe Can Be Manipulated To Create The Ideal Beverage)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=5, y=225)
    add = Button(window, text="Add stock", command=lambda: add_stock(logged_in, username, admin, db, mycursor, window))
    add.config(bg='blanched almond')
    add.config(height=1, width=20)
    add.place(x=225, y=300)
    edit = Button(window, text="Edit stock",
                  command=lambda: edit_stock(logged_in, username, admin, db, mycursor, window))
    edit.config(bg='blanched almond')
    edit.config(height=1, width=20)
    edit.place(x=225, y=375)
    view = Button(window, text="view stock",
                  command=lambda: view_stock(logged_in, username, admin, db, mycursor, window))
    view.config(bg='blanched almond')
    view.config(height=1, width=20)
    view.place(x=225, y=525)
    predict_dates = Button(window, text="Date Prediction",
                           command=lambda: predict_data(logged_in, username, admin, db, mycursor, window, None, None,
                                                        None))
    predict_dates.config(bg='blanched almond')
    predict_dates.config(height=1, width=20)
    predict_dates.place(x=225, y=450)
    # The user selects to Add, edit, view or see predicted date of restock


def add_stock(logged_in, username, admin, db, mycursor, window):
    # The ability to enter new stock purchases (name,quantity, price) #REQUIMRENT 4.2
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - Add Stock")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Add Stock")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    mycursor.execute("SELECT ingredients_name FROM Ingredients Where ingredients_useable = 1")
    data = mycursor.fetchall()  # *SINGLE TABLE SQL*, selects all ingredients within the inventory, that are 
    # available for use 
    data.sort()
    ingredients_selectable = Combobox(window)
    all_ingredients = []
    for i in data:
        all_ingredients.append(i[0])
    ingredients_selectable['values'] = (
        all_ingredients)  # select the ingredient to add quantity to, if it already exists   
    ingredients_selectable.set("")
    ingredients_selectable.place(x=165, y=320)
    ingredients_selectable.config(height=10, width=40)
    info4 = Label(window, text="(When Ordering Recipe Components, Input Information Below To Update The Inventory)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=25, y=250)
    info2 = Label(window, text="Ingredient Name")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=240, y=290)
    info1 = Label(window, text="Total Quantity of Ingredient Item (Kg)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=185, y=370)
    quanitity_in_kg = StringVar()
    quanitity_in_kg_entry = Entry(window, textvariable=quanitity_in_kg, text=quanitity_in_kg, font=('Verdana', 15),
                                  bg='blanched almond')
    quanitity_in_kg.set("")  # Enter the quantity in Kg of stock purchased 
    quanitity_in_kg_entry.place(x=170, y=400)
    info = Label(window, text="Total Price of Ingredient Item (£)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12, "italic"))
    info.place(x=195, y=470)
    price_payed = StringVar()
    price_payed_entry = Entry(window, textvariable=price_payed, text=price_payed, font=('Verdana', 15),
                              bg='blanched almond')
    price_payed.set("")  # Enter the price which was payed for the amount of the ingredient in question
    price_payed_entry.place(x=170, y=500)
    accept = Button(window, text="Enter",
                    command=lambda: clarify_stock_details(logged_in, username, admin, db, mycursor, window, price_payed,
                                                          ingredients_selectable, quanitity_in_kg))
    accept.config(bg='blanched almond')
    accept.config(height=1, width=20)
    accept.place(x=225, y=550)


def clarify_stock_details(logged_in, username, admin, db, mycursor, window, price_payed, ingredients_selectable,
                          quanitity_in_kg):
    # Confirm the information entered is in the correct format
    # CONTINUING REQUIREMENT 4.2
    ingredients_selectable = ingredients_selectable.get()  # Returns string from STRINGVAR class
    ingredients_selectable = ingredients_selectable.lower()  # All database entries are required to be in the lowercase
    quanitity_in_kg = quanitity_in_kg.get()  # Returns string from STRINGVAR class
    price_payed = price_payed.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if quanitity_in_kg.replace('.', '', 1).isdigit() != True or price_payed.replace('.', '',
                                                                                    1).isdigit() != True or ingredients_selectable == "Select ingredient":
        # If the user has failed to enter numerical values in the spaces provided, or they've chosen to not enter an 
        # ingredient name, display a relevant error message Return to the previous screen        
        error_message = Label(window, text="Invalid Format Of Values Entered")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 30, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: add_stock(logged_in, username, admin, db, mycursor, window))
    else:
        quanitity_in_grams = float(
            quanitity_in_kg) * 1000  # convert the Kg amount into g, as the database uses the unit g
        ingredients_exists = False
        mycursor.execute(
            "SELECT ingredients_name FROM Ingredients")  # *SINGLE TABLE SQL*, selects all ingredients 
        # within the inventory 
        for i in mycursor:
            if i[0] == ingredients_selectable:  # checks if an ingredient with the same name already exists
                ingredients_exists = True
        if ingredients_exists:
            create = False
            update_ingredients(logged_in, username, admin, db, mycursor, window, price_payed, ingredients_selectable,
                               quanitity_in_grams, create)
        else:
            create = True
            update_ingredients(logged_in, username, admin, db, mycursor, window, price_payed, ingredients_selectable,
                               quanitity_in_grams, create)


def update_ingredients(logged_in, username, admin, db, mycursor, window, price_payed, ingredients_selectable,
                       quanitity_in_grams, create):
    # Adds the entry to the inventory. If a new ingredient has been entered, a new DB entry is made, 
    # else the existing entry has its values updates CONTINUING REQUIREMENT 4.2 
    if create:
        try:  # *SIMPLE MATHEMATICS* For new inventory items, calculate the price per kilogram
            price_per_kg = float(price_payed) / ((float(quanitity_in_grams)) / 1000)
        except ZeroDivisionError:
            price_per_kg = 0  # If the quantity in grams entered was 0, and the user is creating a DB value for later
            # use, then the current price is £0.00 
        mycursor.execute(
            "INSERT INTO Ingredients(ingredients_name,ingredients_useable,ingredients_remaining_g,"
            "ingredients_price_kg) VALUES (%s,%s,%s,%s)",
            # Insert the inventory item into the DB
            (ingredients_selectable, True, quanitity_in_grams, price_per_kg))
    if not create:
        ingredients_select = "SELECT * FROM Ingredients WHERE ingredients_name = %s"
        mycursor.execute(ingredients_select, (
            ingredients_selectable,))  # *SINGLE TABLE PARAMETRISED SQL* selects the entire record of data 
        # pertaining to the ingredient entered 
        record = mycursor.fetchone()  # *GROUP B RECORD* The python equivalent of a database record containing all 
        # credentials pertaining to the ingredient 
        new_ingredients_remaining = int(
            float(record[3]) + float(quanitity_in_grams))  # Calculate the new quantity of ingredients remaining
        new_price_per_kg = (1000 / new_ingredients_remaining) * (
            (float(price_payed) + ((float(record[3]) / 1000) * record[4])))
        # *RANGE OF MATHEMATICAL CALCULATIONS* To calculate the new price per Kg
        mycursor.execute(
            "Update Ingredients set ingredients_remaining_g = %s, ingredients_price_kg = %s where ingredients_name = %s",
            (int(new_ingredients_remaining), float(new_price_per_kg), str(ingredients_selectable)))
        # *SINGLE TABLE PARAMETRISED SQL* Update the inventory item in the DB
    db.commit()  # Save changes made to the database
    changes_made = Label(window, text="Inventory Has Been Updated")
    changes_made.config(bg='blanched almond')
    changes_made.config(font=("Times New Roman", 30, 'italic'))
    changes_made.place(relx=.5, rely=.4, anchor="n")
    window.after(3000, lambda: manage_stock(logged_in, username, admin, db, mycursor, window))


def edit_stock(logged_in, username, admin, db, mycursor, window):
    # The user has the ability to remove or re-add stock items, or additionally edit their properties REQUIREMENT 4.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - Edit stock")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Edit Stock")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info4 = Label(window, text="(Stock Items can be Deactivated, Reactivated or Amended)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=125, y=250)
    delete = Button(window, text="Deactivate",
                    command=lambda: activation_stock(logged_in, username, admin, db, mycursor, window, False))
    delete.config(bg='blanched almond')
    delete.config(height=1, width=20)
    delete.place(x=225, y=400)
    recreate = Button(window, text="Reactivate",
                      command=lambda: activation_stock(logged_in, username, admin, db, mycursor, window, True))
    recreate.config(bg='blanched almond')
    recreate.config(height=1, width=20)
    recreate.place(x=225, y=325)

    amend = Button(window, text="Amend", command=lambda: amend_stock(logged_in, username, admin, db, mycursor, window))
    # the user selects to alter an ingredients active status, or change the price, name, or quantity of it
    amend.config(bg='blanched almond')
    amend.config(height=1, width=20)
    amend.place(x=225, y=475)


def activation_stock(logged_in, username, admin, db, mycursor, window, option):
    # Allow the user to select the ingredient they wish to alter the activation of
    # CONTINUING REQUIREMENT 4.4
    if option == True:
        choice = "Reactivate"
    if option == False:
        choice = "Deactivate"
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition -Stock Activation")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - " + choice + " Stock")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info4 = Label(window, text="(Only Active Stock Items Can Form Recipe Components To Be Sold)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=85, y=250)
    info3 = Label(window, text="Ingredient Name")
    info3.config(bg='blanched almond')
    info3.config(font=("Times New Roman", 12, "italic"))
    info3.place(x=240, y=320)
    select_query = "SELECT ingredients_name FROM Ingredients where ingredients_useable != %s ORDER BY ingredients_name"
    mycursor.execute(select_query, (
        option,))  # *SINGLE TABLE PARAMETRISED SQL*, selects all ingredients within the inventory, that can
    # be changed 
    data = mycursor.fetchall()
    names = []
    for i in data:
        names.append(i[0])
    ingredients = Combobox(window)
    ingredients['values'] = names  # Select the ingredient to amend
    ingredients.place(x=165, y=350)
    ingredients.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: check_ingred_details(logged_in, username, admin, db, mycursor, window,
                                                              ingredients, option))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=400)
    back = Button(window, text="Back",
                  command=lambda: edit_stock(logged_in, username, admin, db, mycursor, window))
    back.config(bg='blanched almond')
    back.config(height=1, width=20)
    back.place(x=225, y=475)


def check_ingred_details(logged_in, username, admin, db, mycursor, window, ingredients, activate):
    # After confirming a valid ingredient was selected, the relevant changes are made
    # CONTINUING REQUIREMENT 4.4
    ingredients_selectable = ingredients.get()  # Returns string from STRINGVAR class
    ingredients_selectable = ingredients_selectable.lower()  # All database entries are required to be in the lowercase
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute(
        "SELECT ingredients_name FROM Ingredients")  # *SINGLE TABLE SQL*, selects all ingredients within 
    # the inventory 
    ingredients_exists = False
    for i in mycursor:  # *LINEAR SEARCH* through the list of ingredients, determining if a valid ingredient
        # was selected 
        if i[0] == ingredients_selectable:
            ingredients_exists = True
    if ingredients_exists:  # *SINGLE TABLE PARAMETRISED SQL* Change the ingredients activate status as desired 
        mycursor.execute("Update ingredients set ingredients_useable = %s where ingredients_name = %s",
                         (activate, ingredients_selectable))
        db.commit()
        changes_made = Label(window, text="Alterations Have Been Made")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 35, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_stock(logged_in, username, admin, db, mycursor, window))
    else:  # an invalid ingredient was entered, an error message is shown, and the user is returned to the previous 
        # screen 
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again.")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 19, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: activation_stock(logged_in, username, admin, db, mycursor, window, activate))


def amend_stock(logged_in, username, admin, db, mycursor, window):
    # The user selects the ingredient to alter, as well as the field and new value they wish to input into that field
    # CONTINUING REQUIREMENT 4.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - Amend stock")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Amend Stock")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info4 = Label(window, text="(The Name, Quantity And Price Per Kg Of A Stock Item Can Be Edited)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=85, y=250)
    mycursor.execute(
        "SELECT ingredients_name FROM Ingredients where ingredients_useable = True ORDER BY ingredients_name")
    data = mycursor.fetchall()  # *SINGLE TABLE SQL*, selects all ingredients within the inventory, that are 
    # available for use 
    names = []
    for i in data:
        names.append(i[0])
    ingredients = Combobox(window)
    ingredients['values'] = names  # select the ingredient to amend
    ingredients.set("")
    ingredients.place(x=165, y=325)
    ingredients.config(height=10, width=40)
    info = Label(window, text="Ingredient Name")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12, "italic"))
    info.place(x=250, y=295)
    info1 = Label(window, text="Characteristic")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=250, y=370)
    select = Combobox(window)
    select['values'] = ("name", "quantity", "price per kg")  # select the field to amend
    select.set("")
    select.place(x=165, y=400)
    select.config(height=10, width=40)
    info1 = Label(window, text="New Value")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=262, y=445)
    change = StringVar()
    Change_label_entry = Entry(window, textvariable=change, text=change, font=('Verdana', 15), bg='blanched almond')
    change.set("")  # enter the new value the user would like to replace the selected category with
    Change_label_entry.place(x=170, y=475)
    accept_data = Button(window, text="Enter",
                         command=lambda: clarify_data(logged_in, username, admin, db, mycursor, window, ingredients,
                                                      select, change))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=550)


def clarify_data(logged_in, username, admin, db, mycursor, window, ingredients, select, change):
    # ensure all the information inputted is in the requested format, if so, the database is updated
    # CONTINUING REQUIREMENT 4.4
    ingredients_selectable = ingredients.get()  # Returns string from STRINGVAR class
    change = change.get()  # Returns string from STRINGVAR class
    select = select.get()  # Returns string from STRINGVAR class
    if select == "name":
        change = change.lower()  # All database entries are required to be in the lowercase
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute(
        "SELECT ingredients_name FROM Ingredients where ingredients_useable = True ORDER BY ingredients_name")
    ingredients_exists = False  # *SINGLE TABLE SQL*, selects all ingredients within the inventory, that are 
    # available for use 
    proper_unit = False
    for i in mycursor:  # *LINEAR SEARCH* through the database ingredient names to ensure the ingredient exists
        if i[0] == ingredients_selectable:
            ingredients_exists = True
    if not ingredients_exists:  # If an invalid ingredient was entered, an error message is displayed, and the user 
        # is returned to the previous screen 
        error_message = Label(window, text="Please Select A Valid Ingredient")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 30, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: amend_stock(logged_in, username, admin, db, mycursor, window))
    duplicate = False
    if select == "name" and change.replace('.', '', 1).isdigit() == False:
        # If the user has opted to choose an ingredient name, ensure the value is not a number but a series of letters
        mycursor.execute("SELECT ingredients_name FROM Ingredients")
        # *SINGLE TABLE SQL*, selects all ingredients within the inventory
        for i in mycursor:  # *LINEAR SEARCH* through the database ingredient names to ensure the name is 
            # not already in use 
            if i[0] == change:
                duplicate = True
        proper_unit = True
        field = "1"
        change = str(change)
    if select == "quantity" and change.isdigit() == True:
        # If the user wishes to change the quantity in stock of an ingredient, the new value's unit must be numerical 
        proper_unit = True
        change = int(change)
        field = "2"
    if select == "price per kg" and change.replace('.', '', 1).isdigit() == True:
        # If the user wishes to change the price per Kg of an ingredient, the new value's unit must be numerical 
        proper_unit = True
        change = float(change)
        field = "3"
    if proper_unit == True and ingredients_exists == True and duplicate == False:
        # If all the information was correctly entered by the user, update the database
        # *SINGLE TABLE PARAMETRISED SQL* The relevant SQL Query is chosen to update the appropriate field
        try:
            if field == "1":
                select_query = "Update ingredients set ingredients_name = %s WHERE ingredients_name =%s"
            if field == "2":
                select_query = "Update ingredients set ingredients_remaining_g = %s WHERE ingredients_name =%s"
            if field == "3":
                select_query = "Update ingredients set ingredients_price_kg = %s WHERE ingredients_name =%s"
            mycursor.execute(select_query, (change, ingredients_selectable))
            db.commit()  # save changes to the database
            changes_made = Label(window, text="Change Complete")
            changes_made.config(bg='blanched almond')
            changes_made.config(font=("Times New Roman", 30, 'italic'))
            changes_made.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: edit_stock(logged_in, username, admin, db, mycursor, window))
        except mysql.connector.errors.DataError:
            duplicate = True
    if proper_unit == False and ingredients_exists == True or duplicate == True:
        # If the values inputted do not match the format requested by the database, display an appropriate error 
        # message and revert to previous screen 
        error_message = Label(window,
                              text="Please Follow The Instructions Carefully, And Try Again. \nAll Recipe Names Must "
                                   "Be Unique")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 19, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: amend_stock(logged_in, username, admin, db, mycursor, window))


def view_stock(logged_in, username, admin, db, mycursor, window):
    # To view all current stock available in reserve. Including the name, quantity and price payed per kg REQUIREMENT
    # 4.1 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - View Stock")  # Indicating the section of the application the user is operating
    treeview = ttk.Treeview(window, columns=(1, 2, 3), show="headings", height="5")
    style = ttk.Style(window)  # A table to display the current ingredients in stock
    style.theme_use("clam")
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    treeview.pack(side=TOP, pady=130)
    treeview.heading(1, text="Ingredients name")
    treeview.heading(2, text="Ingredients Remaining (kg)")
    treeview.heading(3, text="Ingredients Price (£/kg)")
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    # Vertical and Horizontal scrollbars to view the table fully if needed
    scrollbar.pack(side="left", fill="y")
    sctollbar2.pack(side='bottom', fill='x')
    mycursor.execute(
        "SELECT ingredients_name, ingredients_remaining_g, ingredients_price_kg FROM Ingredients Where "
        "ingredients_useable = 1 ORDER BY ingredients_name")
    # *SINGLE TABLE  SQL*, selects all active ingredients within the inventory, the price and quantity
    rows = mycursor.fetchall()  # *MULTI DIMENSIONAL ARRAY*, With each element of the array, containing both
    # the ingredients name, quantity and price per KG 
    for i in rows:
        new_quantity = i[1] / 1000  # quantity in KG
        new_price = (str(round(i[2], 2))).split(".")
        if len(new_price[1]) < 2:
            new_price = new_price[0] + "." + new_price[1] + "0"  # format the price into the accepted form (££.pp)
        else:
            new_price = new_price[0] + "." + new_price[1]
        data = [i[0], new_quantity, new_price]
        treeview.insert('', 'end', values=data)
    select_an_option = Label(window, text="Current Inventory")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=150, y=50)


# The following routines makeup the prediction algorithm. The routines are looped, going through different processes,
# to calculate a set of dates. For every ingredient in the inventory, one loop is performed, providing the 
# ingredients has been sold within a recipe. REQUIREMENT 4.3 

def predict_data(logged_in, username, admin, db, mycursor, window, ingredients_collected, ingredients_remaining,
                 predictions):
    # collect the sales data for the prediction, and display this data, once it has undergone the needed processes 
    # REQUIREMENT 4.3 *  COMPLEX BUSINESS MODEL* A prediction algorithm which takes sales data and makes 
    # forecasts based on several variables 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if predictions is None:  # if this is the loop through the set of routines, create relevant variables
        window.title(
            "Food State Nutrition - Predict restock")  # Indicating the section of the application the user is operating
        mycursor.execute(
            "SELECT ingredients_name FROM Ingredients where ingredients_useable = True ORDER BY ingredients_name")
        names = mycursor.fetchall()  # *  SINGLE TABLE  SQL* Select the ingredients name of active ingredients
        ingredients_remaining = []
        ingredients_collected = []
        predictions = []
        for i in names:
            ingredients_remaining.append(i[0])
    if len(ingredients_remaining) != 0:  # Providing that there are still ingredient dates to predict. Everytime the
        # set of modules loop, the next element in the list will receive a prediction date 
        sql = 'SELECT Sum(Recipe_Ingredients_Bridge.quantity_of_ingredients_g) AS SumQuantity_of_ingredients_g FROM ' \
              'Sales INNER JOIN ((Recipe INNER JOIN (IngredientS INNER JOIN Recipe_Ingredients_Bridge ON ' \
              'IngredientS.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = ' \
              'Recipe_Ingredients_Bridge.Recipe_ID) INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = ' \
              'Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY ' \
              'Sales.Sales_Date, IngredientS.Ingredients_Name, Sales.Sales_Date HAVING (((' \
              'IngredientS.Ingredients_Name)=%s)) ORDER BY Sales.Sales_Date DESC limit 28; '
        mycursor.execute(sql, (ingredients_remaining[
                                   0],))  # *  AGGREGATE SQL FUNCTIONS* The sales of an ingredient each day are
        # 'summed' for the last 28 days. These values are selected from 5 Interlinked tables 
        data = mycursor.fetchall()
        sales_average = []
        if len(data) != 0:
            for i in data:
                sales_average.append(
                    int(i[0]))  # *  SINGLE TABLE  SQL* Select the ingredients name of active ingredients
            mycursor.execute("Select preference_value from preference where preference_name = 'Cold Day Temperature'")
            cold_temp = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the cold temperature value from 
            # the preference table 
            sql = 'SELECT Sum(Recipe_Ingredients_Bridge.quantity_of_ingredients_g) AS SumQuantity_of_ingredients_g ' \
                  'FROM Sales INNER JOIN ((Recipe INNER JOIN (IngredientS INNER JOIN Recipe_Ingredients_Bridge ON ' \
                  'IngredientS.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = ' \
                  'Recipe_Ingredients_Bridge.Recipe_ID) INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = ' \
                  'Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY ' \
                  'Sales.Sales_Date, Sales.Sales_Date, IngredientS.Ingredients_Name HAVING (((Avg(' \
                  'Sales.sales_temperature))<%s) AND ((IngredientS.Ingredients_Name)=%s)) ORDER BY Sales.Sales_Date ' \
                  'DESC limit 7; '
            mycursor.execute(sql, (int(cold_temp[0]) + 1, ingredients_remaining[0]), )
            data = mycursor.fetchall()  # *  AGGREGATE SQL FUNCTIONS* The sales of an ingredient, on days where
            # the 'average' temperature is equal to, or below that specified, are 'summed' for the last 7 
            # criteria-meeting days. These values are selected from 5 Interlinked tables 
            sales_cold = []
            for i in data:
                try:
                    i = str(i[0])
                    sales_cold.append(int(i))
                except IndexError:
                    sales_cold = sales_average  # If minimal cold days have passed, then it will take the values of 
                    # the average day, and not have any additional impact on the prediction 
            if len(sales_cold) < 2:
                sales_cold = sales_average
            mycursor.execute("Select preference_value from preference where preference_name = 'Warm Day Temp'")
            warm_temp = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the warm temperature value from 
            # the preference table 
            sql = 'SELECT Sum(Recipe_Ingredients_Bridge.quantity_of_ingredients_g) AS SumOfquantity_of_ingredients_g ' \
                  'FROM Sales INNER JOIN ((Recipe INNER JOIN (IngredientS INNER JOIN Recipe_Ingredients_Bridge ON ' \
                  'IngredientS.Ingredients_ID = Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = ' \
                  'Recipe_Ingredients_Bridge.Recipe_ID) INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = ' \
                  'Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY ' \
                  'Sales.Sales_Date, Sales.Sales_Date, IngredientS.Ingredients_Name HAVING (((Avg(' \
                  'Sales.sales_temperature))>%s) AND ((IngredientS.Ingredients_Name)=%s)) ORDER BY Sales.Sales_Date ' \
                  'DESC limit 7; '
            # *  AGGREGATE SQL FUNCTIONS* The sales of an ingredient, on days where the 'average' temperature 
            # is equal to, or above that specified, are 'summed' for the last 7 criteria-meeting days. These values 
            # are selected from 5 Interlinked tables 
            mycursor.execute(sql, (int(warm_temp[0]) - 1, ingredients_remaining[0]), )
            data = mycursor.fetchall()
            sales_warm = []
            for i in data:
                try:
                    sales_warm.append(int(i[0]))
                except IndexError:
                    sales_warm = sales_average
            if len(sales_warm) < 2:
                sales_warm = sales_average  # If minimal warm days have passed, then the values are taken from the 
                # average, and not have any additional impact on the prediction 
            counter = 0
            dates = []
            sales_weekend = []
            current_date = date.today()  # The current date using the date module from datetime library
            while counter < 8:  # Indefinite iteration, which will select the dates of the last 8 weekend days
                current_date = current_date - timedelta(
                    days=1)  # Going back a day using the timedelta module from the datetime library
                day_of_week = current_date.weekday()  # finding the day of the week of the date in question
                if day_of_week == 5 or day_of_week == 6:  # The fifth and 6th day of the week, indexing from 0, 
                    # are classified as weekends 
                    counter = counter + 1
                    dates.append(current_date)
            for i in dates:
                sql = 'SELECT Sum(Recipe_Ingredients_Bridge.quantity_of_ingredients_g) AS ' \
                      'SumOfquantity_of_ingredients_g FROM Sales INNER JOIN ((Recipe INNER JOIN (IngredientS INNER ' \
                      'JOIN Recipe_Ingredients_Bridge ON IngredientS.Ingredients_ID = ' \
                      'Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = ' \
                      'Recipe_Ingredients_Bridge.Recipe_ID) INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = ' \
                      'Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY ' \
                      'Sales.Sales_Date, IngredientS.Ingredients_Name HAVING (((Sales.Sales_Date)=%s) AND ((' \
                      'IngredientS.Ingredients_Name)=%s)) ORDER BY Sales.Sales_Date DESC; '
                mycursor.execute(sql, (i, ingredients_remaining[0]), )
                data = mycursor.fetchall()  # *  AGGREGATE SQL FUNCTIONS* From the last four weekends, the sum 
                # of the sales on those days are calculated and returned 
                try:
                    sales_weekend.append(int(data[0][0]))
                except IndexError:
                    sales_weekend = sales_average
            if len(sales_weekend) < 2:
                sales_warm = sales_weekend  # If minimal sales have been made over the last 4 weekends, then the 
                # values are taken from the average, and not have any additional impact on the prediction 
            master_list = [sales_average, sales_warm, sales_cold,
                           sales_weekend]  # *  MULTI DIMENSIONAL ARRAY*, which contains all the sales data 
            # needed for the prediction to be made 
            cleanse(logged_in, username, admin, db, mycursor, window, master_list, ingredients_collected,
                    ingredients_remaining, predictions)
        else:  # If no sales have been made of the ingredient, then there is insufficient data to make any predictions
            values = [ingredients_remaining[0], "N/A"]
            ingredients_collected.append(ingredients_remaining[0])
            ingredients_remaining.pop(0)
            predictions.append(values)
            predict_data(logged_in, username, admin, db, mycursor, window, ingredients_collected, ingredients_remaining,
                         predictions)
    elif len(
            ingredients_remaining) == 0:  # Once all ingredients have received prediction dates, they can be displayed
        # in a table 
        treeview = ttk.Treeview(window, columns=(1, 2), show="headings", height="5")
        style = ttk.Style(window)  # A table to display the current ingredients in stock
        style.theme_use("clam")
        style.configure('Treeview', rowheight=36)
        style.configure("Treeview", background="blanched almond",
                        fieldbackground="blanched almond", foreground="black")
        treeview.pack(side=TOP, pady=130)
        treeview.heading(1, text="Ingredients name")
        treeview.heading(2, text="Date")
        scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
        sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
        scrollbar.pack(side="left", fill="y")
        sctollbar2.pack(side='bottom', fill='x')
        # Vertical and Horizontal scrollbars to view the table fully if needed
        scrollbar.pack()
        for i in predictions:
            treeview.insert('', 'end', values=i)
        select_an_option = Label(window, text="Inventory Restock Predictions")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=65, y=50)


def cleanse(logged_in, username, admin, db, mycursor, window, master_list, ingredients_collected, ingredients_remaining,
            predictions):
    # The data is cleansed using the Z-Value. Any value +- 1.4 standard deviations from the mean is removed
    # *  COMPLEX MATHEMATICS* Z-Value calculation
    # CONTINUING REQUIREMENT 4.3
    for i in range(0, len(master_list)):  # cleanse all data, from all temperatures and weekdays
        mean = sum(master_list[i]) / len(master_list[i])  # calculation of μ
        standard_deviation = 0
        for element in master_list[i]:  # Iterate through each day of sales data
            element = (element - mean) ** 2  # for each value, the distance from the mean is squared
            standard_deviation = standard_deviation + element  # the values are totalled
        standard_deviation = (standard_deviation / len(
            master_list[i])) ** 0.5  # square-rooted, to give the final value of σ
        for index in master_list[i]:
            try:
                if (index - mean) / standard_deviation > 1.4 or (
                        index - mean) / standard_deviation < -1.4:  # if the value is above or below 1.4 standard 
                    # deviations of the mean 
                    master_list[i] = list(filter(index.__ne__, master_list[i]))  # remove it from the list 
            except ZeroDivisionError:  # If as a product of coincidence, the standard deviation is 0, then this must 
                # be accounted for 
                pass
    gradient(logged_in, username, admin, db, mycursor, window, master_list, ingredients_collected,
             ingredients_remaining, predictions)


def gradient(logged_in, username, admin, db, mycursor, window, master_list, ingredients_collected,
             ingredients_remaining, predictions):
    # The average change between data entries is calculated to see a trend. This is done for all 4 sales data 
    # classifications, to obtain 4 trends CONTINUING REQUIREMENT 4.3 
    master_gradients = []
    for i in range(0, len(master_list)):
        increase = 0
        mean_increase = 0
        for element in range(0, (len(master_list[i]) - 1)):
            increase = increase + (master_list[i][element + 1] - master_list[i][
                element])  # calculate and total the difference between each value  
            mean_increase = increase / len(master_list[i])  # Calculate the average distance between each value
        master_gradients.append(mean_increase)  # final gradient value
    temperature(logged_in, username, admin, db, mycursor, window, master_list, master_gradients, ingredients_collected,
                ingredients_remaining, predictions)


def temperature(logged_in, username, admin, db, mycursor, window, master_list, master_gradients, ingredients_collected,
                ingredients_remaining, predictions):
    # A list of temperatures of the upcoming days is calculated. Depending on the API membership the user has, 
    # will dictate how many days of future data is accessible * /B CLIENT SERVER MODEL* The application ( 
    # client) is requesting temperature data from the pinfeather.org server, with certain parameters such as a Unique
    # key and Current City CONTINUING REQUIREMENT 4.3 
    mycursor.execute("Select preference_value from preference where preference_name = 'API KEY'")
    key = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the API KEY value from the preference table
    key = (key[0])
    units = "metric"  # Unit of temperature data is to be returned in
    exclude = "current,minutely,hourly"  # data that is to be excluded as it is not needed. Excluding data makes the 
    # API call more efficient 
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?exclude=' + exclude + '&appid=' + key + '&units=' + units
    mycursor.execute("Select preference_value from preference where preference_name = 'Current City'")
    city = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the Current City from the preference table
    city = (city[0])
    api_call = api_call + "&q=" + city
    try:
        json_data = get(api_call).json()  # *  PARSING JSON*
        all_temps = []
        for item in json_data['list']:
            all_temps.append(item['main'][
                                 'temp'])  # *  DICTIONARY* From the data collected, append as many data 
            # entries as the key allows, in three hour increments 
        current_time = datetime.now().hour  # The current hour of the day using the datetime module from datetime 
        # library 
        first_temp = 11 - (current_time // 3)  # Find the midday temperature of the following day
        final_temps = []
        for i in range(first_temp, len(all_temps) - 8,
                       8):  # iterate through 24 hour intervals to find the following midday temperatures
            final_temps.append(all_temps[
                                   i])  # *  QUEUE* The list will function as a queue, as the first temperature
            # in, will be the first to be required, iterating through the list. FIFO 
    except KeyError and exceptions.ConnectionError:  # In the situation where there is no internet/api access, 
        # temperature will not be accounted for in the prediction 
        final_temps = []
    prediction(logged_in, username, admin, db, mycursor, window, master_list, master_gradients, final_temps,
               ingredients_collected, ingredients_remaining, predictions)


def prediction(logged_in, username, admin, db, mycursor, window, master_list, master_gradients, temperatures,
               ingredients_collected, ingredients_remaining, predictions):
    # With the sales data, and the forecast, the gradient trend is followed and mapped onto future days, 
    # accounting for any available future temperatures, and weekends, to calculate an estimation of restocking 
    # CONTINUING REQUIREMENT 4.3 
    sql = 'select ingredients_remaining_g from ingredients where ingredients_name = %s'
    mycursor.execute(sql, (ingredients_remaining[
                               0],))  # *  SINGLE TABLE PARAMETRISED SQL* Select the ingredients remaining of 
    # the ingredients in question 
    grams_remaining = mycursor.fetchone()
    mycursor.execute("Select preference_value from preference where preference_name = 'Warm Day Temp'")
    warm = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the warm temperature value from the preference 
    # table 
    mycursor.execute("Select preference_value from preference where preference_name = 'Cold Day Temperature'")
    cold = mycursor.fetchone()  # *  SINGLE TABLE  SQL* Select the cold temperature value from the preference 
    # table 
    d4te = date.today()  # The current date using the date module from datetime library
    pointer = 0  # creating the pointer which will indicate the front of the queue
    grams_remaining = grams_remaining[0]
    final_gradient = 0
    while grams_remaining > 0:  # Iterate until the stock becomes depleted, hence the date which will signify a restock
        d4te = d4te + timedelta(days=1)  # Going forward a day using the timedelta module from the datetime library
        upper_limit = d4te + timedelta(days=(6 - d4te.weekday()))
        lower_limit = d4te + timedelta(days=(5 - d4te.weekday()))
        if d4te >= lower_limit <= upper_limit:  # Determine if the date is a weekend
            weekend = True
        else:
            weekend = False
        if pointer < (len(
                temperatures)):  # if the pointer is still in range of the list, then the temperate variable can 
            # still be incorporated 
            if temperatures[pointer] >= int(warm[0][
                                                0]):  # if the temperature classifies the upcoming day as warm, 
                # find the average of the warm and overall gradients 
                final_gradient = (master_gradients[0] + master_gradients[1]) / 2
            if temperatures[pointer] >= int(cold[0][
                                                0]):  # if the temperature classifies the upcoming day as cold, 
                # find the average of the cold and overall gradients 
                final_gradient = (master_gradients[0] + master_gradients[2]) / 2
        pointer = pointer + 1
        if weekend:  # if the day of the week classifies as a weekend, find the average of the weekend and overall 
            # gradients 
            final_gradient = (master_gradients[0] + master_gradients[3]) / 2
        grams_remaining = grams_remaining - (final_gradient + master_list[0][
            -1])  # reduce the amount of grams in inventory based on how many grams are predicted to be used in the day
    d4te = d4te.strftime("%d %b %Y")  # Format the date to the british standard
    values = [ingredients_remaining[0], d4te]
    ingredients_collected.append(ingredients_remaining[0])  # Store the data for display
    ingredients_remaining.pop(0)  # Remove the ingredient from the list of ingredients to be predicted
    predictions.append(values)
    predict_data(logged_in, username, admin, db, mycursor, window, ingredients_collected, ingredients_remaining,
                 predictions)


# The following routines comprise the recipe section of the program. Here the abilities for the user to create 
# recipes based on their inventory is available, along with having the functionality to manipulate the ingredients 
# quantities, as well as defining the price, after becoming aware of the recipe's total cost. This will also allow 
# for profit to be calculated. Individual recipe's can be altered (price + quantity of ingredients) and removed from 
# the menu, to be re-added at a later date. Meeting Client Requirement 5 

def recipe_menu(logged_in, username, admin, db, mycursor, window):
    # Allow the user to view, edit or edit a recipe REQUIREMENT 5
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - Manage Recipe")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Manage Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info4 = Label(window, text="(Recipes Are Built From Active Ingredients To Be Sold)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=150, y=250)
    create = Button(window, text="Create Recipe",
                    command=lambda: create_recipe(logged_in, username, admin, db, mycursor, window))
    create.config(bg='blanched almond')
    create.config(height=1, width=20)
    create.place(x=225, y=300)
    edit = Button(window, text="Edit Recipe",
                  command=lambda: edit_recipe(logged_in, username, admin, db, mycursor, window))
    edit.config(bg='blanched almond')
    edit.config(height=1, width=20)
    edit.place(x=225, y=375)
    view = Button(window, text="View Recipe",
                  command=lambda: view_recipe(logged_in, username, admin, db, mycursor, window))
    view.config(bg='blanched almond')
    view.config(height=1, width=20)
    view.place(x=225, y=450)
    # Allow the user to select a choice from a display for buttons


def create_recipe(logged_in, username, admin, db, mycursor, window):
    # The user can create new recipes, which can be added to the menu for purchase REQUIREMENT 5.1
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Create Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info4 = Label(window, text="(This Recipe Information Can Be Changed At Any Time)")
    info4.config(bg='blanched almond')
    info4.config(font=("Times New Roman", 12))
    info4.place(x=125, y=250)
    info = Label(window, text="Recipe Name")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12, "italic"))
    info.place(x=250, y=320)
    info2 = Label(window, text="Recipe Price (Medium)")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=225, y=420)
    name = StringVar()
    name_label_entry = Entry(window, textvariable=name, text=name, font=('Verdana', 15), bg='blanched almond')
    name.set("")  # Enter the name of the recipe to create
    name_label_entry.place(x=170, y=350)
    name_label_entry.config(bg='blanched almond')
    price = StringVar()
    price_label_entry = Entry(window, textvariable=price, text=price, font=('Verdana', 15), bg='blanched almond')
    price.set("")  # enter the price of the recipe to create, this is the price for a medium, 
    # the variations are calculated later 
    price_label_entry.place(x=170, y=450)
    price_label_entry.config(bg='blanched almond')
    accept_data = Button(window, text="Enter",
                         command=lambda: name_price_recipe(logged_in, username, admin, db, mycursor, window, name,
                                                           price))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=525)


def name_price_recipe(logged_in, username, admin, db, mycursor, window, name, price):
    # ensure the recipe name and price are valid inputs  CONTINUING REQUIREMENT 5.1
    name = name.get()  # Returns string from STRINGVAR class
    name = name.lower()  # All names are to be in lowercase
    price = price.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT recipe_name FROM recipe")
    # *  SINGLE TABLE  SQL* Selects the names of all existing recipes
    issue = False
    for i in mycursor:  # if the recipe name already exists, a recipe of the same name cannot be created
        if i[0] == name:
            issue = True
    if len(name) > 255:  # If the name is over 255 characters, this will be rejected due to the datatype constraints
        issue = True
    if issue == False and price.replace('.', '',
                                        1).isdigit() == True:  # if the inputs were
        # valid, proceed to create the recipe 
        ingredients_list = []
        build_recipe(logged_in, username, admin, db, mycursor, window, name, ingredients_list, price)
    else:  # if the inputs were invalid, request the user re enter them, after an appropriate error message
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: create_recipe(logged_in, username, admin, db, mycursor, window))


def build_recipe(logged_in, username, admin, db, mycursor, window, name, ingredients_list, price):
    # The user will select an ingredient, as well as the quantity of that ingredient to add to the smoothie 
    # CONTINUING REQUIREMENT 5.1 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Create Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="(Once Entered, Recipe Components Cannot Be Changed, Only Quantities)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=75, y=250)
    mycursor.execute(
        "SELECT ingredients_name FROM Ingredients where ingredients_useable = True ORDER BY ingredients_name")
    names = mycursor.fetchall()  # *  SINGLE TABLE  SQL* Selects the names of all ingredients, that have been 
    # marked available for selection
    ingredients = Combobox(window)
    ingredients['values'] = names  # allow the user to select from an easy dropdown menu of ingredients 
    ingredients.place(x=165, y=325)
    ingredients.config(height=10, width=40)
    info2 = Label(window, text="Quantity Of Ingredient (g)")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=210, y=420)
    quantity = StringVar()
    quantity_label_entry = Entry(window, textvariable=quantity, text=quantity, font=('Verdana', 15),
                                 bg='blanched almond')
    quantity.set("")  # Enter quantity in grams of the ingredient
    quantity_label_entry.place(x=170, y=450)
    info3 = Label(window, text="Ingredient Name")
    info3.config(bg='blanched almond')
    info3.config(font=("Times New Roman", 12, "italic"))
    info3.place(x=230, y=295)
    accept_data = Button(window, text="Enter",
                         command=lambda: clarify_ingredients(logged_in, username, admin, db, mycursor, window, name,
                                                             quantity, ingredients, ingredients_list, price))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=525)


def clarify_ingredients(logged_in, username, admin, db, mycursor, window, name, quantity, ingredients, ingredients_list,
                        price):
    # Confirm the ingredient names and quantities are valid CONTINUING REQUIREMENT 5.1
    ingredients = ingredients.get()  # Returns string from STRINGVAR class
    quantity = quantity.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    ingredients_exists = False
    mycursor.execute("SELECT ingredients_name FROM Ingredients where ingredients_useable = True")
    # *  SINGLE TABLE  SQL* Selects the names of all ingredients, that have been marked available for selection
    for i in mycursor:  # iterate through all ingredients in the database to ensure the name entered in valid
        if i[0] == ingredients:
            ingredients_exists = True
    if price.replace('.', '',1).isdigit() == True == False or ingredients_exists == False:
        # If any of the inputs are invalid, display an 
        # error message and return to the previous screen 
        changes_made = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 18, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: build_recipe(logged_in, username, admin, db, mycursor, window, name, ingredients_list,
                                          price))
    else:  # if the inputs are valid, append them to a multidimensional array which will contain the names and 
        # quantities of ingredients 
        entry = [ingredients, float(quantity)]
        ingredients_list.append(entry)  # *  MULTI DIMENSIONAL ARRAY*
        select_an_option = Label(window, text="Food State Nutrition™\n        - Create Recipe")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        question = Label(window, text="Do you wish to add another ingredient?")
        question.config(bg='blanched almond')
        question.config(font=("Times New Roman", 12))
        question.place(x=160, y=200)
        # allow the user to decide to add additional ingredients, repeating the several previous sub-routines, 
        # or confirm they are happy to finalise the recipe\\\ 
        yes = Button(window, text="  YES  ",
                     command=lambda: build_recipe(logged_in, username, admin, db, mycursor, window, name,
                                                  ingredients_list, price))

        yes.config(bg='blanched almond')
        yes.config(height=1, width=20)
        yes.place(x=100, y=240)
        no = Button(window, text="  NO  ",
                    command=lambda: finalise_recipe(logged_in, username, admin, db, mycursor, window, name, price,
                                                    ingredients_list))

        no.config(bg='blanched almond')
        no.config(height=1, width=20)
        no.place(x=300, y=240)
        treeview = ttk.Treeview(window, columns=(1, 2), show="headings", height="8")
        style = ttk.Style(window)  # A table to display the information
        style.theme_use("clam")
        style.configure('Treeview', rowheight=20)
        style.configure("Treeview", background="blanched almond",
                        fieldbackground="blanched almond", foreground="black")
        treeview.place(x=100, y=300)
        treeview.heading(1, text="Ingredient Name")
        treeview.heading(2, text="Quantity (g)")
        scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
        sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
        scrollbar.pack(side="left", fill="y")
        sctollbar2.pack(side='bottom', fill='x')
        # Vertical and Horizontal scrollbars to view the table fully if needed
        for i in ingredients_list:
            treeview.insert('', 'end', values=i)


def finalise_recipe(logged_in, username, admin, db, mycursor, window, name, price, ingredients_list):
    # Finalising the recipe creation process, writing it to the database. CONTINUING REQUIREMENT 5.1
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    ingredients = tuple(
        map(tuple, ingredients_list))  # create a tuple containing the ingredients and their quantities in the recipe
    totals = {}  # *GROUP B Dictionary* a dictionary is created so the ingredients quantities can be summed on their 
    # keys 
    for key, value in ingredients:  # All ingredients must be summed if they share the same key, this is to ensure a 
        # recipe doesnt reference the same ingredient twice 
        totals[key] = totals.get(key, 0) + value
    keys = list(totals.keys())  # create a separate list of all the ingredients names 
    values = list(totals.values())  # create a separate list of all the ingredients quantities
    mycursor.execute("INSERT INTO Recipe(recipe_name, recipe_price£, recipe_is_active) VALUES (%s,%s,%s)",
                     (name, price, True))
    # *  SINGLE TABLE PARAMETRISED SQL* Create new recipe, based on user entered credentials
    db.commit()  # save changes to the database
    select_query = "SELECT recipe_id FROM recipe where recipe_name=%s"
    mycursor.execute(select_query, (
        name,))  # *  SINGLE TABLE PARAMETRISED SQL* Selects the recipe id of the recipe just created
    record = mycursor.fetchone()
    identification_r = (int(record[0]))  # create a variable to store a recipe ID
    for i in range(0, len(keys)):  # Iterate for every item in the list of ingredients
        select_query = "SELECT ingredients_id FROM ingredients where ingredients_name=%s"
        mycursor.execute(select_query, (
            keys[
                i],))  # *  SINGLE TABLE PARAMETRISED SQL* select the ingredients Id from the item in the recipe
        record = mycursor.fetchone()
        identification_i = (int(record[0]))  # create a variable to store a ingredients  ID
        mycursor.execute(
            "Insert INTO Recipe_Ingredients_Bridge (ingredients_id, recipe_id, quantity_of_ingredients_g) VALUES (%s,"
            "%s,%s)",
            (identification_i, identification_r, values[
                i]))  # *  SINGLE TABLE PARAMETRISED SQL* #write to the bridgeable the ingredient and its 
        # quantity that is to be in the recipe 
    db.commit()  # save changes to the database
    changes_made = Label(window, text="Recipe Has Been Created")
    changes_made.config(bg='blanched almond')
    changes_made.config(font=("Times New Roman", 18, 'italic'))
    changes_made.place(relx=.5, rely=.4, anchor="n")
    window.after(3000, lambda: create_recipe(logged_in, username, admin, db, mycursor, window))


def edit_recipe(logged_in, username, admin, db, mycursor, window):
    # The user has the functionality to edit recipes after their creation REQUIREMENT 5.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Edit Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="(Recipes Name, Price, And Ingredient Quantity Can All Be Edited)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=100, y=250)
    # The user is to select whether they are deactivating, reactivating, or amending a recipe
    delete = Button(window, text="Deactivate",
                    command=lambda: activation_recipe(logged_in, username, admin, db, mycursor, window, False))
    delete.config(bg='blanched almond')
    delete.config(height=1, width=20)
    delete.place(x=225, y=375)
    recreate = Button(window, text="Reactivate",
                      command=lambda: activation_recipe(logged_in, username, admin, db, mycursor, window, True))
    recreate.config(bg='blanched almond')
    recreate.config(height=1, width=20)
    recreate.place(x=225, y=300)
    amend = Button(window, text="Amend", command=lambda: amend_recipe(logged_in, username, admin, db, mycursor, window))
    amend.config(bg='blanched almond')
    amend.config(height=1, width=20)
    amend.place(x=225, y=450)


def activation_recipe(logged_in, username, admin, db, mycursor, window, option):
    # Allow the user to reactivate or deactivate recipes already in existence. This moves them onto, or off the menu 
    # REQUIREMENT 5.3 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if option == True:
        word = "Reactivate"
    if option == False:
        word = "Deactivate"
    select_an_option = Label(window, text="Food State Nutrition™\n        - " + word + " Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="(Only Active Recipes Can Be Sold To The Public)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=150, y=250)
    select_query = "SELECT recipe_name FROM recipe where recipe_is_active != %s ORDER BY recipe_name"
    mycursor.execute(select_query, (
        option,))  # *  SINGLE TABLE PARAMETRISED SQL* Selects all active or deactivate recipes based on the 
    # users choice prior 
    data = mycursor.fetchall()
    names = []
    for i in data:
        names.append(i[0])
    recipe = Combobox(window)
    recipe['values'] = names  # A simple dropdown menu to allow the user to choose a recipe
    recipe.place(relx=.5, rely=.5, anchor="n")
    recipe.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: check_recipe_details(logged_in, username, admin, db, mycursor, window, recipe,
                                                              option))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=400)
    back = Button(window, text="Back",
                  command=lambda: edit_recipe(logged_in, username, admin, db, mycursor, window))
    back.config(bg='blanched almond')
    back.config(height=1, width=20)
    back.place(x=225, y=450)


def check_recipe_details(logged_in, username, admin, db, mycursor, window, recipe, option):
    # Confirm the recipe that has been selected is a valid input CONTINUING REQUIREMENT 5.3
    recipe_selectable = recipe.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute(
        "SELECT recipe_name FROM recipe")  # *  SINGLE TABLE SQL* selects recipe names from recipe table
    recipe_exists = False
    for i in mycursor:  # iterate through all recipe names to ensure one matches the given input
        if i[0] == recipe_selectable:
            recipe_exists = True
    if recipe_exists:  # *  SINGLE TABLE PARAMETRISED SQL* #if the recipe entered is valid, make the 
        # relevant changes 
        mycursor.execute("Update recipe set recipe_is_active = %s where recipe_name = %s", (option, recipe_selectable))
        db.commit()  # save changes to the database
        changes_made = Label(window, text="Changes Made")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 30, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        
        window.after(3000, lambda: edit_recipe(logged_in, username, admin, db, mycursor, window))
    else:  # if the recipe name was invalid, return to the previous screen and allow the user to renter
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: activation_recipe(logged_in, username, admin, db, mycursor, window, option))


def amend_recipe(logged_in, username, admin, db, mycursor, window):
    # The user is able to enter the name of the recipe, and the part of it they want to change CONTINUING REQUIREMENT
    # 5.4 
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - manage recipe")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - Amend Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="(Recipes Name, Price, And Ingredient Quantity Can All Be Edited)")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=100, y=250)
    mycursor.execute("SELECT recipe_name FROM recipe where recipe_is_active = True ORDER BY recipe_name")
    data = mycursor.fetchall()  # *  SINGLE TABLE SQL* select all recipes that are active
    names = []
    for i in data:
        names.append(i[0])
    info2 = Label(window, text="Recipe Name")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=250, y=295)
    recipe = Combobox(window)
    recipe['values'] = names  # allow the user to select a recipe from a simple dropdown box
    recipe.set("")
    recipe.place(x=165, y=325)
    recipe.config(height=10, width=40)
    info3 = Label(window, text="Recipe Feature")
    info3.config(bg='blanched almond')
    info3.config(font=("Times New Roman", 12, "italic"))
    info3.place(x=250, y=370)
    select = Combobox(window)
    select['values'] = ("Name", "Price", "Ingredients Quantity")  # allow the user to select the field to alter
    select.set("")
    select.place(x=165, y=400)
    select.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: clarify_inputs_recipe_changes(logged_in, username, admin, db, mycursor, window,
                                                                       recipe, select))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=500)


def clarify_inputs_recipe_changes(logged_in, username, admin, db, mycursor, window, recipe, select):
    # Ensure the inputs the user has entered are valid CONTINUING REQUIREMENT 5.4
    recipe_selectable = recipe.get()  # Returns string from STRINGVAR class
    select = select.get()  # Returns string from STRINGVAR class
    if select == "Name":  # if the user has decided to change the name, ensure the input is in lower case, 
        # as all recipes are 
        recipe_selectable = recipe_selectable.lower()
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT recipe_name FROM recipe where recipe_is_active = True ORDER BY recipe_name")
    recipe_exists = False  # *  SINGLE TABLE SQL* select all recipes that are active
    proper_unit = False
    for i in mycursor:  # iterate through all recipes available to ensure the input matches a valid entry
        if i[0] == recipe_selectable:
            recipe_exists = True
    if not recipe_exists:  # if the recipe does not exist, return to the previous screen to request valid inputs
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: amend_recipe(logged_in, username, admin, db, mycursor, window))
    elif select == "Ingredients Quantity":  # The user has chosen to amend the ingredients within the recipe
        details_to_change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable)
    elif select == "Name":  # The user has chosen to amend the name of the recipe
        detials_to_change_n_p(logged_in, username, admin, db, mycursor, window, recipe_selectable, select)
    elif select == "Price":  # The user has chosen to amend the price of the recipe
        detials_to_change_n_p(logged_in, username, admin, db, mycursor, window, recipe_selectable, select)
    else:  # if no valid input was given, return to the previous screen an d request one
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: amend_recipe(logged_in, username, admin, db, mycursor, window))


def details_to_change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable):
    # The user selects the ingredient within the recipe they desire to change CONTINUING REQUIREMENT 5.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_query = "SELECT Ingredients.Ingredients_Name FROM Recipe INNER JOIN (Ingredients INNER JOIN " \
                   "Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
                   "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = " \
                   "Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Recipe.Recipe_Name)=%s)); "
    mycursor.execute(select_query, (
        recipe_selectable,))  # Parametrised Multi-Table (3 Tables) SQL Query, selects all ingredients within the 
    # given recipe 
    ingredients_to_select = mycursor.fetchall()
    select_an_option = Label(window, text="Food State Nutrition™\n        - Amend Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="Select The Ingredient To Be Edited")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=200, y=250)
    ingredients_selectable = Combobox(window)
    ingredients_selectable['values'] = (
        ingredients_to_select)  # allow the user to select an ingredient from a simple dropdown menu
    ingredients_selectable.place(x=165, y=330)
    ingredients_selectable.config(height=10, width=40)
    info3 = Label(window, text="Ingredient Name")
    info3.config(bg='blanched almond')
    info3.config(font=("Times New Roman", 12, "italic"))
    info3.place(x=250, y=300)
    accept_data = Button(window, text="Enter",
                         command=lambda: clarify_and_change_i(logged_in, username, admin, db, mycursor, window,
                                                              recipe_selectable, ingredients_selectable,
                                                              ingredients_to_select))
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=380)
    accept_data.config(bg='blanched almond')
    back = Button(window, text="Back",
                  command=lambda: amend_recipe(logged_in, username, admin, db, mycursor, window))
    back.config(height=1, width=20)
    back.place(x=225, y=450)
    back.config(bg='blanched almond')


def clarify_and_change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable, ingredients_selectable,
                         ingredients_to_select):
    # Ensure the ingredient entered is a valid input CONTINUING REQUIREMENT 5.4
    if type(ingredients_selectable) != str:  # if the variables are still STRINGVAR, Convert them to strings
        ingredients_selectable = ingredients_selectable.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    ingredients_exists = False
    for i in ingredients_to_select:  # iterate through the list of ingredients to ensure an input that matches a data
        # entry was given 
        if i[0] == ingredients_selectable:
            ingredients_exists = True
    if ingredients_exists:
        sql = "SELECT Recipe_Ingredients_Bridge.quantity_of_ingredients_g FROM Recipe INNER JOIN (IngredientS INNER " \
              "JOIN Recipe_Ingredients_Bridge ON IngredientS.Ingredients_ID = " \
              "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = Recipe_Ingredients_Bridge.Recipe_ID " \
              "WHERE (((Recipe.Recipe_Name)=%s) AND ((IngredientS.Ingredients_Name)=%s)); "
        mycursor.execute(sql, (recipe_selectable,
                               ingredients_selectable), )  # Parametrised Multi-Table (3 Tables) SQL Query, selects 
        # the quantity of the ingredient in the recipe currently 
        display_current_quanitty = mycursor.fetchone()
        select_an_option = Label(window, text="Food State Nutrition™\n        - Amend Recipe")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        info1 = Label(window, text="Please Enter The New Quantity Current Quantity: " + str(
            display_current_quanitty[0]) + "g")  # displays to the user the current quanity in the recipe
        info1.config(bg='blanched almond')
        info1.config(font=("Times New Roman", 12))
        info1.place(x=125, y=250)
        info2 = Label(window, text="New Value (g)")
        info2.config(bg='blanched almond')
        info2.config(font=("Times New Roman", 12, "italic"))
        info2.place(x=260, y=320)
        change = StringVar()
        change_label_entry = Entry(window, textvariable=change, text=change, font=('Verdana', 15), bg='blanched almond')
        change.set("")  # Enter new ingredients quantity
        change_label_entry.place(x=170, y=350)
        accept_data = Button(window, text="Enter",
                             command=lambda: change_i(logged_in, username, admin, db, mycursor, window,
                                                      recipe_selectable, ingredients_selectable, change,
                                                      ingredients_to_select))
        accept_data.config(bg='blanched almond')
        accept_data.config(height=1, width=20)
        accept_data.place(x=225, y=450)
    if not ingredients_exists:  # if an invalid ingredient was entered, return to the previous screen to request an
        # ingredient to amend 
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: details_to_change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable))


def change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable, ingredients_selectable, change,
             ingredients_to_select):
    # Make the changes to the ingredient in the recipe CONTINUING REQUIREMENT 5.4
    change = change.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if change.isdigit():  # Ensuring the quantity entered is an integer value
        change = int(change)
        select_query = "SELECT recipe_id FROM recipe where recipe_name=%s"
        mycursor.execute(select_query, (
            recipe_selectable,))  # *  SINGLE TABLE PARAMETRISED SQL* select recipe Id of the recipe given
        r_id = mycursor.fetchone()[0]
        select_query = "SELECT ingredients_id FROM Ingredients where ingredients_name=%s"  # *  SINGLE TABLE 
        # PARAMETRISED SQL* select ingredient Id of the ingredient given 
        mycursor.execute(select_query, (ingredients_selectable,))
        i_id = mycursor.fetchone()[0]
        mycursor.execute(
            "Update Recipe_Ingredients_Bridge set quantity_of_ingredients_g = %s where ingredients_id = %s and "
            "recipe_id = %s",
            (change, i_id,
             r_id))  # *  SINGLE TABLE PARAMETRISED SQL* update the ingredient quantity within the given recipe
        db.commit()  # save changes to the database
        changes_made = Label(window, text="Changes Made")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 30, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: amend_recipe(logged_in, username, admin, db, mycursor, window))
    else:  # if an invalid quantity was given, return to the previous screen and request a valid input
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: clarify_and_change_i(logged_in, username, admin, db, mycursor, window, recipe_selectable,
                                                  ingredients_selectable, ingredients_to_select))


def detials_to_change_n_p(logged_in, username, admin, db, mycursor, window, recipe_selectable, select):
    # Allow the user to change the name or price, depending on their choice CONTINUING REQUIREMENT 5.4
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Amend Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="What Would You Like To Change The " + select + " Of The Recipe To?")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=100, y=250)
    info1 = Label(window, text="New Value")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=265, y=320)
    change = StringVar()
    change_label_entry = Entry(window, textvariable=change, text=change, font=('Verdana', 15), bg='blanched almond')
    change.set("")  # Enter the new value of the given field
    change_label_entry.place(x=170, y=350)
    accept_data = Button(window, text="Enter",
                         command=lambda: clarify_and_change_n_p(logged_in, username, admin, db, mycursor, window,
                                                                recipe_selectable, select, change))
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=430)
    accept_data.config(bg='blanched almond')


def clarify_and_change_n_p(logged_in, username, admin, db, mycursor, window, recipe_selectable, select, change):
    # Ensure the inputs given were valid CONTINUING REQUIREMENT 5.4
    change = change.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    possible = True
    if select == "Name" and change.replace('.', '', 1).isdigit() == False:  # Ensure the recipe is not a float/integer
        select_query = "Update recipe set recipe_name = %s WHERE recipe_name =%s"
        mycursor.execute("SELECT recipe_name FROM recipe")
        for i in mycursor:  # iterate through all recipes to ensure the name is not already given to another recipe
            if i[0] == change:
                possible = False
        if len(change) > 255 and len(change) > 0:  # Names must be below 255 charachters, given the database constraints
            possible = False
    if select == "Price" and change.replace('.', '',
                                            1).isdigit() == True:  # if the price is to be changed, ensure a float/integer was entered
        select_query = "Update recipe set recipe_price£ = %s WHERE recipe_name =%s"
        possible = True
    if possible:  # given all inputs are valid
        mycursor.execute(select_query, (
            change, recipe_selectable))  # *  SINGLE TABLE PARAMETRISED SQL* Update the name/price of the recipe
        db.commit()  # Returns string from STRINGVAR class
        changes_made = Label(window, text="The Alterations Have Been Made")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 18, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_recipe(logged_in, username, admin, db, mycursor, window))
    if not possible:  # if the inputs were invalid, request them to be reentered on the previous screen                           
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000,
                     lambda: detials_to_change_n_p(logged_in, username, admin, db, mycursor, window, recipe_selectable,
                                                   select))


def view_recipe(logged_in, username, admin, db, mycursor, window):
    # Allow the user to view individual recipes, and their relevant information REQUIREMENT 5.5
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - view recipe")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - View Recipe")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info1 = Label(window, text="When Viewing A Recipe, You Can Observe All Components And Their Information")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12))
    info1.place(x=50, y=250)
    mycursor.execute("SELECT recipe_name FROM recipe where recipe_is_active = True ORDER BY recipe_name")
    data = mycursor.fetchall()  # *  SINGLE TABLE SQL* Select all recipes that are active
    names = []
    for i in data:
        names.append(i[0])
    recipe = Combobox(window)
    recipe['values'] = names  # allow the user to select a recipe from a dropdown menu
    recipe.place(x=165, y=360)
    recipe.config(height=10, width=40)
    info2 = Label(window, text="Recipe Name")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=250, y=330)
    accept_data = Button(window, text="Enter",
                         command=lambda: recipe_to_view_info(logged_in, username, admin, db, mycursor, window, recipe))
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=430)
    accept_data.config(bg='blanched almond')


def recipe_to_view_info(logged_in, username, admin, db, mycursor, window, recipe):
    # providing the user has selected a valid recipe, display the recipe CONTINUING REQUIREMENT 5.5
    recipe = recipe.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    mycursor.execute("SELECT recipe_name FROM recipe where recipe_is_active = True ORDER BY recipe_name")
    recipe_exists = False  # *  SINGLE TABLE SQL* selects all recipe names
    for i in mycursor:  # ensure the recipe name matches that of a data entry
        if i[0] == recipe:
            recipe_exists = True
    if not recipe_exists:  # if the 
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: view_recipe(logged_in, username, admin, db, mycursor, window))
    if recipe_exists:
        select_query = "SELECT (Ingredients_price_kg)*(quantity_of_ingredients_g)/1000 AS Expr1 FROM Recipe INNER " \
                       "JOIN (" \
                       "Ingredients INNER JOIN Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
                       "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = " \
                       "Recipe_Ingredients_Bridge.Recipe_ID GROUP BY Recipe.Recipe_Name, " \
                       "Recipe_Ingredients_Bridge.quantity_of_ingredients_g, Ingredients.Ingredients_price_kg HAVING " \
                       "(((" \
                       "Recipe.Recipe_Name)=%s)); "
        mycursor.execute(select_query, (
            recipe,))  # Parametrised Multi-Table (3 Tables) SQL Query, selects the calculated cost of the recipe 
        # REQUIREMENT 5.2 
        data = mycursor.fetchall()
        total = 0
        for i in data:
            total = total + i[0]
        sql = "select recipe_price£ from recipe where recipe_name = %s"
        mycursor.execute(sql, (recipe,))  # *  SINGLE TABLE SQL* selects the price of the recipe
        price = str(mycursor.fetchall()[0][0])
        pennies = price.split('.')
        if len(pennies[1]) == 1:  # format the price correctly
            price = price + "0"
        elif len(pennies[1]) > 1:
            price = pennies[0] + "." + str(round(int(pennies[1]), -2))
        total = str(round(total, 2))
        pennies = total.split('.')
        if len(pennies[1]) == 1:
            total = total + "0"
        if total == "0.00":
            total = "0.01"
        display = Label(window, text=" Name: " + recipe + " \n Price: £" + price + " \n Cost: £" + total)
        display.config(bg='blanched almond')
        display.config(font=("Times New Roman", 20))
        display.place(x=215, y=400)
        select_an_option = Label(window, text="Recipe View")
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=200, y=40)
        select_query = "SELECT Ingredients.Ingredients_Name, Recipe_Ingredients_Bridge.quantity_of_ingredients_g, " \
                       "Ingredients.Ingredients_price_kg FROM Recipe INNER JOIN (Ingredients INNER JOIN " \
                       "Recipe_Ingredients_Bridge ON Ingredients.Ingredients_ID = " \
                       "Recipe_Ingredients_Bridge.Ingredients_ID) ON Recipe.Recipe_ID = " \
                       "Recipe_Ingredients_Bridge.Recipe_ID WHERE (((Recipe.Recipe_Name)=%s)); "
        mycursor.execute(select_query, (
            recipe,))  # Parametrised Multi-Table (3 Tables) SQL Query, selects the ingredients and their quantities 
        # within the recipe 
        data = mycursor.fetchall()

        treeview = ttk.Treeview(window, columns=(1, 2, 3), show="headings", height="5")
        style = ttk.Style(window)  # A table to display the recipe information
        style.theme_use("clam")
        style.configure('Treeview', rowheight=36)
        style.configure("Treeview", background="blanched almond",
                        fieldbackground="blanched almond", foreground="black")
        treeview.pack(side=TOP, pady=170)
        treeview.heading(1, text="Ingredients Name")
        treeview.heading(2, text="Quantity(g)")
        treeview.heading(3, text="Price Per Kg")
        scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
        sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
        scrollbar.pack(side="left", fill="y")
        sctollbar2.pack(side='bottom', fill='x')
        # Vertical and Horizontal scrollbars to view the table fully if needed
        scrollbar.pack()
        for i in data:
            x = (i[2])
            x = ceil((x) * 100) / 100.0
            q = [i[0], i[1], x]
            treeview.insert('', 'end', values=q)


# The following routines allow the user to view their sales history, graphically. A start date is given, which from 
# that date, to present day, a graph is displayed showing the data of sales. This feature is greater extended as the 
# user has the functionality to select certain variables that will show them trends of more niche data. These 
# features include the sales of individual drinks, hot and cold days, weekend's etc. REQUIREMENT 6 

def view_sales(logged_in, username, admin, db, mycursor, window):
    # The user is to enter a start date, and type of data they want to observe REQUIREMENT 6.1/6.3
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title("Food State Nutrition - View Sales")  # Indicating the section of the application the user is operating
    select_an_option = Label(window, text="Food State Nutrition™\n        - View Sales")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="Revenue Is Plotted Over Time Accounting For Multiple Different Variables")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=250)
    info1 = Label(window, text="Variable")
    info1.config(bg='blanched almond')
    info1.config(font=("Times New Roman", 12, "italic"))
    info1.place(x=275, y=330)
    info2 = Label(window, text="Start Date (dd/mm/yy)")
    info2.config(bg='blanched almond')
    info2.config(font=("Times New Roman", 12, "italic"))
    info2.place(x=225, y=400)
    choice = Combobox(window)
    choice['values'] = (
        ['User', 'Warm', 'Cold', 'Recipe', 'Overall'])  # select the type of data to view REQUIREMENT 6.3
    choice.place(x=175, y=360)
    choice.config(height=10, width=40)
    d4te = StringVar()
    change_label_entry = Entry(window, textvariable=d4te, text=d4te, font=('Verdana', 15), bg='blanched almond')
    d4te.set("")  # Enter Date
    change_label_entry.place(x=170, y=430)
    accept_data = Button(window, text="Enter",
                         command=lambda: collecting_data_to_view(logged_in, username, admin, db, mycursor, window,
                                                                 choice, d4te))
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=500)
    accept_data.config(bg='blanched almond')




def collecting_data_to_view(logged_in, username, admin, db, mycursor, window, choice, d4te):
    # The data that is to be graphed, is collected at this stage CONTINUING REQUIREMENT 6.3
    if type(choice) != str:  # if the variables are still STRINGVAR, Convert them to strings
        choice = choice.get()  # Returns string from STRINGVAR class
        d4te = d4te.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    try:
        d4te = datetime.strptime(d4te, "%d/%m/%Y")  # convert the date string to the datetime variable
        d4te = str(d4te)[0: str(d4te).index(" ")]  # Format the date
        if choice == 'Warm' or choice == 'Cold':  # if the user has chosen to observe data on warm or cold days
            if choice == "Warm":  # if the user has chosen to observe warm days
                mycursor.execute("select preference_value from preference where preference_name = 'Warm Day Temp'")
                temp = str(int(
                    mycursor.fetchone()[0]) - 1)  # *  SINGLE TABLE SQL* selects the warm temperature preference
                sql = "SELECT Sales.Sales_Date FROM Sales GROUP BY Sales.Sales_Date HAVING (((Sales.Sales_Date)>%s) " \
                      "AND ((Avg(Sales.sales_temperature))>%s))ORDER BY Sales.Sales_Date ASC; "
                mycursor.execute(sql, (d4te,
                                       temp))  # *  AGGREGATE SQL FUNCTIONS* Selects the dates of sales where 
                # the average temperature was above or equal to that desired 
                dates = mycursor.fetchall()
            elif choice == "Cold":  # if the user has chosen to observe cold days
                mycursor.execute(
                    "select preference_value from preference where preference_name = 'Cold Day Temperature'")
                temp = str(int(
                    mycursor.fetchone()[0]) + 1)  # *  SINGLE TABLE SQL* selects the cold temperature preference
                sql = "SELECT Sales.Sales_Date FROM Sales GROUP BY Sales.Sales_Date HAVING (((Sales.Sales_Date)>%s) " \
                      "AND ((Avg(Sales.sales_temperature))<%s))ORDER BY Sales.Sales_Date ASC; "
                mycursor.execute(sql, (d4te,
                                       temp))  # *  AGGREGATE SQL FUNCTIONS* Selects the dates of sales where 
                # the average temperature was below or equal to that desired 
                dates = mycursor.fetchall()
            sql = "SELECT Sum(Sales_Recipe_Bridge.sales_price) AS SumOfsales_price, Sales.Sales_Date FROM Sales INNER " \
                  "JOIN (Recipe INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = Sales_Recipe_Bridge.Recipe_ID) " \
                  "ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY Sales.Sales_Date, Format(sales_date," \
                  "'dd') HAVING (((Sales.Sales_Date)=%s)) ORDER BY Format(sales_date,'dd') DESC; "
            plottable = []  # *  MULTI DIMENSIONAL ARRAY*, holds the data to be displayed
            for i in dates:
                mycursor.execute(sql, (i[
                                           0],))  # *  AGGREGATE SQL FUNCTIONS* selects the sum of the revenue 
                # of the days where the average temperature meets the condition 
                holder = mycursor.fetchall()
                plottable.append(holder[0])  # append the information to the list to be plotted
            if len(plottable) > 1:  # if more than two data entries exist, graph the data
                graph(logged_in, username, admin, db, mycursor, window, choice, d4te, None, plottable)
            else:  # if less than two data entries exist, then their cannot be a graph, hence display an error and 
                # return to previous screen 
                error_message = Label(window, text="Two Or More Days Of Data Are Needed For Graphing")
                error_message.config(bg='blanched almond')
                error_message.config(font=("Times New Roman", 18, 'italic'))
                error_message.place(relx=.5, rely=.4, anchor="n")
                window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))
        elif choice == 'Overall':  # if the user chooses to observe all data within the two periods
            sql = "SELECT Sum(Sales_Recipe_Bridge.sales_price) AS SumOfsales_price, Sales.Sales_Date FROM Sales INNER " \
                  "JOIN (Recipe INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = Sales_Recipe_Bridge.Recipe_ID) " \
                  "ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID GROUP BY Sales.Sales_Date, Format(sales_date," \
                  "'dd') HAVING (((Sales.Sales_Date)>%s)) ORDER BY Format(sales_date,'dd') ASC; "
            mycursor.execute(sql, (
                d4te,))  # *  AGGREGATE SQL FUNCTIONS* selects the sum of the revenue of the days between the 
            # dates 
            plottable = mycursor.fetchall()
            if len(plottable) > 1:  # if more than two data entries exist, graph the data
                graph(logged_in, username, admin, db, mycursor, window, choice, d4te, None, plottable)
            else:  # if less than two data entries exist, then their cannot be a graph, hence display an error and 
                # return to previous screen 
                error_message = Label(window, text="Two Or More Days Of Data Of Needed For Graphing")
                error_message.config(bg='blanched almond')
                error_message.config(font=("Times New Roman", 18, 'italic'))
                error_message.place(relx=.5, rely=.4, anchor="n")
                window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))
        elif choice == 'Recipe' or choice == 'User':  # if the user chooses to observe all data made by certain 
            # cashiers or from certain recipes 
            if choice == 'Recipe':  # if the user has chosen to observe sales based on recipes
                mycursor.execute("select recipe_name from recipe where recipe_is_active =1")
                data = mycursor.fetchall()  # *  SINGLE TABLE SQL* selects the recipe names
                options = []
                for i in data:
                    options.append(i[0])
            if choice == 'User':  # if the user has chosen to observe sales based on recipes
                mycursor.execute("select username from user where active =1")  #
                data = mycursor.fetchall()  # *  SINGLE TABLE SQL* selects the user names
                options = []
                for i in data:
                    options.append(i[0])
            select_an_option = Label(window, text="Food State Nutrition™\n        - View Sales")
            select_an_option.config(bg='blanched almond')
            select_an_option.config(font=("Times New Roman", 30))
            select_an_option.place(x=40, y=100)
            info = Label(window, text="Select A " + choice + " That Will Be Graphically Represented")
            info.config(bg='blanched almond')
            info.config(font=("Times New Roman", 12))
            info.place(x=150, y=220)
            info1 = Label(window, text=choice)
            info1.config(bg='blanched almond')
            info1.config(font=("Times New Roman", 13, "italic"))
            info1.place(x=275, y=270)
            selection = Combobox(window)
            selection['values'] = options  # Allow the user to select the username or recipe name they desire
            selection.place(x=175, y=300)
            selection.config(height=10, width=40)
            accept_data = Button(window, text="Enter",
                                 command=lambda: clarify_data_to_view(logged_in, username, admin, db, mycursor, window,
                                                                      choice, d4te, selection, options))
            accept_data.config(bg='blanched almond')
            accept_data.config(height=1, width=20)
            accept_data.place(x=225, y=360)
            back = Button(window, text="Back",
                          command=lambda: view_sales(logged_in, username, admin, db, mycursor, window))
            back.config(bg='blanched almond')
            back.config(height=1, width=20)
            back.place(x=225, y=410)

        else:  # if an invalid option was selected, return to prior screen, request a valid input
            error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
            error_message.config(bg='blanched almond')
            error_message.config(font=("Times New Roman", 18, 'italic'))
            error_message.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))
    except ValueError:  # if an invalid date was entered, return to prior screen, request a valid input
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))


def clarify_data_to_view(logged_in, username, admin, db, mycursor, window, choice, d4te, selection, options):
    # The data that is to be graphed, is collected at this stage CONTINUING REQUIREMENT 6.3
    selection = selection.get()  # Returns string from STRINGVAR class
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if selection in options:  # if a valid recipe or username was selected
        if choice == 'Recipe':  # if the user has chosen to observe sales based on recipes
            sql = "SELECT Sum(Sales_Recipe_Bridge.sales_price) AS SumOfsales_price, Sales.Sales_Date FROM User INNER " \
                  "JOIN (Sales INNER JOIN (Recipe INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = " \
                  "Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID) ON User.User_ID = " \
                  "Sales.User_ID GROUP BY Sales.Sales_Date, Format(sales_date,'dd'), Recipe.Recipe_Name HAVING (((" \
                  "Sales.Sales_Date)>%s) AND ((Recipe.Recipe_Name)=%s)) ORDER BY Sales.Sales_Date DESC , " \
                  "Format(sales_date,'dd') DESC; "
        if choice == 'User':  # if the user has chosen to observe sales based on recipes
            sql = "SELECT Sum(Sales_Recipe_Bridge.sales_price) AS SumOfsales_price, Sales.Sales_Date FROM User INNER " \
                  "JOIN (Sales INNER JOIN (Recipe INNER JOIN Sales_Recipe_Bridge ON Recipe.Recipe_ID = " \
                  "Sales_Recipe_Bridge.Recipe_ID) ON Sales.Sales_ID = Sales_Recipe_Bridge.Sales_ID) ON User.User_ID = " \
                  "Sales.User_ID GROUP BY Sales.Sales_Date, Format(sales_date,'dd'), User.Username HAVING (((" \
                  "Sales.Sales_Date)>%s) AND ((User.Username)=%s)) ORDER BY Sales.Sales_Date DESC , " \
                  "Format(sales_date,'dd') DESC; "
        mycursor.execute(sql, (d4te,
                               selection))  # *  AGGREGATE SQL FUNCTIONS* selects the sales date, and sum of 
        # revenue from the day, of all sales that meet the condition 
        plottable = mycursor.fetchall()  # *  MULTI DIMENSIONAL ARRAY*, holds the data to be displayed
        plottable.reverse()
        if len(plottable) > 1:  # if more than two data entries exist, graph the data
            graph(logged_in, username, admin, db, mycursor, window, choice, d4te, None, plottable)
        else:  # if less than two data entries exist, then their cannot be a graph, hence display an error and 
            # return to previous screen
            error_message = Label(window, text="Two Or More Days Of Data of Needed For Graphing")
            error_message.config(bg='blanched almond')
            error_message.config(font=("Times New Roman", 18, 'italic'))
            error_message.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))
    else:  # if an invalid selection was made, that does not match an entry in the database, return to previous 
        # screen, request input 
        error_message = Label(window, text="Please Follow The Instructions Carefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 18, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: view_sales(logged_in, username, admin, db, mycursor, window))


def graph(logged_in, username, admin, db, mycursor, window, choice, d4te, selection, plottable):
    # The graph is plotted, allowing the user to observe trends and save the graph image for later use REQUIREMENT 6.1/2
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    x_values = []
    y_values = []
    for i in plottable:  # create arrays to store both x and y values for the graph
        x_values.append(i[1])
        y_values.append(i[0])
    str_dates = []
    for i in range(0, len(x_values)):  # convert the dates into string datatype, for better viewing
        value = ((str(x_values[i])).replace("-", " ")[6:]).split()
        value = value[1] + " " + value[0]
        str_dates.append(value)
    x_values = str_dates
    fig = figure(figsize=(6, 6), dpi=100)  # create the graph for the display of data
    fig.patch.set_facecolor('wheat')
    ax = fig.add_subplot(111)
    xlabel("Dates")  # label the axis
    ylabel("Gross (£)")  # label the axis
    if len(
            x_values) > 9:  # find 9 regular intervals of data, if the data is too large, so the graph is not so 
        # condensed the axis are not viewable 
        length = len(x_values) // 9
        new_x = []
        new_y = []
        for i in range(length, len(x_values) - 1, length):
            new_x.append(x_values[i])
            new_y.append(y_values[i])
            plot(new_x, new_y)  # plot the data on the graph
    else:
        plot(x_values, y_values)  # plot the data on the graph
    canvas = FigureCanvasTkAgg(fig, master=window)  # create a canvas embedded in the window the place the graph
    canvas.draw()
    canvas.get_tk_widget().place(relx=.5, rely=.5, anchor="n")
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)  # Toolbar allows for graph manipulation, zooming, saving of graphical 
    # image etc 
    toolbar.place(relx=.5, rely=.0, anchor="n")
    canvas.get_tk_widget().pack()
    display = Label(window, text=" A Graph To Show The Sales Since " + d4te + " \n Condition: " + choice)
    display.config(bg='wheat')
    display.place(relx=.5, rely=.1, anchor="n")


# The purpose of the following routines is to allow the user complete control over the preferences of the program. 
# This means they have full control to customise certain features, such as cup sizes, temperatures, or the location 
# of the business. The program functionality can also be improved, if the user opts to purchase a premium API KEY, 
# for better weather predictions, thus improving the prediction algorithm. 

def preference_menu(logged_in, username, admin, db, mycursor, window):
    # Allow the user to select either to edit or view the preferences REQUIREMENT 7.1/2
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    window.title(
        "Food State Nutrition - Manage Preferences")  # Indicating the section of the application the user is operating

    select_an_option = Label(window, text="Food State Nutrition™\n        - Manage Preferences")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=10, y=100)
    info = Label(window, text="(Preferences Are Features That Help Tailor The Application To Your Needs)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=75, y=250)
    # allow the user to select between editing or viewing preferences
    edit = Button(window, text="Edit Preferences",
                  command=lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))
    edit.config(bg='blanched almond')
    edit.config(height=2, width=40)
    edit.place(x=150, y=300)
    view = Button(window, text="View Preferences",
                  command=lambda: view_preferences(logged_in, username, admin, db, mycursor, window))
    view.config(bg='blanched almond')
    view.config(height=2, width=40)
    view.place(x=150, y=400)


def edit_preference_menu(logged_in, username, admin, db, mycursor, window):
    # The user selects the preference to edit CONTINUING REQUIREMENT 7.2
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Food State Nutrition™\n        - Edit Preferences")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=40, y=100)
    info = Label(window, text="(Select From The List Below)")
    info.config(bg='blanched almond')
    info.config(font=("Times New Roman", 12))
    info.place(x=200, y=250)
    mycursor.execute(
        "Select preference_name from preference")  # *  SINGLE TABLE SQL* selects the preference names
    data = mycursor.fetchall()
    names = []
    for i in data:
        names.append(i[0])
    choice = Combobox(window)
    names.pop()
    choice['values'] = names  # A dropdown menu to choose which preference to amend
    choice.place(relx=.5, rely=.5, anchor="n")
    choice.config(height=10, width=40)
    accept_data = Button(window, text="Enter",
                         command=lambda: confirn_valid_preference(logged_in, username, admin, db, mycursor, window,
                                                                  choice))
    accept_data.config(bg='blanched almond')
    accept_data.config(height=1, width=20)
    accept_data.place(x=225, y=450)


def confirn_valid_preference(logged_in, username, admin, db, mycursor, window, choice):
    # confirm the user has entered a valid preference title to amend CONTINUING REQUIREMENT 7.2
    if type(choice) != str:  # if the selection still exists in a STRINGVAR
        preference = choice.get()  # Returns string from STRINGVAR class
    else:
        preference = choice
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    if preference == "API KEY" or preference == "Warm Day Temp" or preference == "Cold Day Temperature" or \
            preference == "Current City" or preference == "Large Cup Ratio" or preference == "Small Cup Ratio":
        # if the user has entered a preference that is not a filepath
        select_an_option = Label(window, text="Food State Nutrition™\n        - Edit " + preference)
        select_an_option.config(bg='blanched almond')
        select_an_option.config(font=("Times New Roman", 30))
        select_an_option.place(x=40, y=100)
        info = Label(window, text="Enter New Value")
        info.config(font=("Times New Roman", 12))
        info.config(bg='blanched almond')
        info.place(x=250, y=270)
        change = StringVar()
        change_label_entry = Entry(window, textvariable=change, text=change, font=('Verdana', 15), bg='blanched almond')
        change.set("")  # enter new preference value here
        change_label_entry.place(x=170, y=300)
        accept_data = Button(window, text="Enter",
                             command=lambda: confirm_valid_change(logged_in, username, admin, db, mycursor, window,
                                                                  preference, change))
        accept_data.config(bg='blanched almond')
        accept_data.config(height=1, width=20)
        accept_data.place(x=350, y=400)
        backwards = Button(window, text="Back",
                           command=lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))
        backwards.config(bg='blanched almond')
        backwards.config(height=1, width=20)
        backwards.place(x=100, y=400)
    elif preference == "file path-csv":  # if the user wants to alter the sales data csv path
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(('csv files', 'csv'),))
        # open the file dialog (file explorer) only showing csv files. If the user has moved the csv file, 
        # they simply select the location of the new file 
        changes_made = Label(window, text="File selected: " + filename)
        changes_made.place(relx=.5, rely=.4, anchor="n")
        confirm_valid_change(logged_in, username, admin, db, mycursor, window, preference, filename)
    elif preference == "file path-picture":  # if the user wants to alter the logo path
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
        # open the file dialog (file explorer). The user can select a new picture, or if they have moved the picture,
        # reselect its path 
        changes_made = Label(window, text="File selected: " + filename)
        changes_made.place(relx=.5, rely=.4, anchor="n")
        confirm_valid_change(logged_in, username, admin, db, mycursor, window, preference, filename)
    else:  # if no valid preference was selected, display an error and return to the previous screen
        error_message = Label(window, text="Please Follow The Instructions\nCarefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 35, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))


def confirm_valid_change(logged_in, username, admin, db, mycursor, window, preference, change):
    # Dependant on the users choice, update the relevant preference, with the desired new content CONTINUING 
    # REQUIREMENT 7.2 
    if type(change) != str:  # if the option to change is a STRINGVAR, alter it to a string
        change = change.get()  # if the selection still exists in a STRINGVAR
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    sucess = False
    if preference == "file path-csv":  # if the user has desired to change the filepath of the cav
        if change != "":  # providing they have selected a file
            with open(change,
                      newline='') as f:  # open the csv file. read the first line, if all headings are correct, 
                # only then can data be written to it 
                read = reader(f)
                row1 = next(read)
            if row1 == ['sale_id', ' recipe name', 'cashier', 'sale date', 'sale price', 'sale cost', 'sale profit']:
                sucess = True
    if preference == "file path-picture":  # if the user has desired to change the filepath of the cav
        if change != "":  # providing they have selected a file
            try:  # attempt to open the file and see if it is an embeddable image with the correct filetype (jpeg etc)
                photo = PhotoImage(file=change)
                label = Label(image=photo)
                sucess = True
                label.image = photo
            except TclError:  # if the file is not an embeddable imagine, then return an error
                sucess = False
    if preference == "API KEY":  # if the user has desired to change the API KEY 
        try:
            mycursor.execute("Select preference_value from preference where preference_name = 'Current City'")
            city = mycursor.fetchone()  # *  SINGLE TABLE SQL* selects the business's Current City
            city = (city[0])
            query = 'q=' + city;  # *  CALLING PARAMETERISED WEB SERVICE API* attempting to connect to api 
            # with new key 
            information = get('https://api.openweathermap.org/data/2.5/weather?' + query +
                              '&exclude=hourly,daily,minutely&appid=' + change + '&units=metric');  # The api has 
            # parameters which will access the data for the certain city, by having access granted by the users 
            # unique key 
            weather_data = information.json();  # *  PARSING JSON*
            temperature = float(weather_data["main"][
                                    "temp"])  # *  DICTIONARY* From the data collected, access the current 
            # temperature 
            sucess = True
        except KeyError:  # if no connection can be made, then the API KEY is invalid
            sucess = False
    if preference == "Current City":  # if the user has desired to change the Current City
        try:
            mycursor.execute("Select preference_value from preference where preference_name = 'API KEY'")
            key = mycursor.fetchone()
            key = (key[0])
            query = 'q=' + change;  # *  CALLING PARAMETERISED WEB SERVICE API* attempting to connect to api 
            # with new key 
            information = get('https://api.openweathermap.org/data/2.5/weather?' + query +
                              '&exclude=hourly,daily,minutely&appid=' + key + '&units=metric');  # The api has 
            # parameters which will access the data for the certain city, by having access granted by the users 
            # unique key 
            weather_data = information.json();  # *  PARSING JSON*
            temperature = float(weather_data["main"][
                                    "temp"])  # *  DICTIONARY* From the data collected, access the current 
            # temperature 
            sucess = True
        except KeyError:  # if no connection can be made, then the city is invalid
            sucess = False
    if preference == "Large Cup Ratio":  # if the user has desired to change the Large Cup Ratio
        if change.isdigit():  # if they have entered an integer, then the input is valid
            sucess = True
    if preference == "Small Cup Ratio":  # if the user has desired to change the Large Cup Ratio
        if change.isdigit():  # if they have entered an integer, then the input is valid
            if int(change) < 100:  # The small cup must be within 100, a 100% or over decrease removes the entire drink
                sucess = True
    if preference == "Warm Day Temp":  # if the user has desired to change the warm day temperature
        if change.isdigit():  # the temperature must be an integer
            mycursor.execute("Select preference_value from preference where preference_name = 'Cold Day Temperature'")
            cold = mycursor.fetchone()  # *  SINGLE TABLE SQL* selects the cold day temperature
            cold = cold[0]
            if int(cold) < int(change):  # ensure the warm day, will be greater than the cold day
                sucess = True
    if preference == "Cold Day Temperature":  # if the user has desired to change the cold day temperature
        if change[0] == "-" and change[
                                1:].isdigit() == True or change.isdigit() == True:  # the temperature input must be 
            # an integer 
            mycursor.execute("Select preference_value from preference where preference_name = 'Warm Day Temp'")
            warm = mycursor.fetchone()  # *  SINGLE TABLE SQL* selects the warm day temperature
            warm = warm[0]
            if int(warm) > int(change):  # ensure the warm day, will be greater than the cold day
                sucess = True
    if sucess == False and preference == "file path-csv":  # if the filepath selected was incorrect, display an 
        # error message
        changes_made = Label(window, text="File Path Or \n File Format Is Invalid")
        changes_made.config(bg='blanched almond')
        changes_made.config(font=("Times New Roman", 40, 'italic'))
        changes_made.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))
    elif not sucess:  # if the input was incorrect, return to the previous screen
        error_message = Label(window, text="Please Follow The Instructions\nCarefully, And Try Again")
        error_message.config(bg='blanched almond')
        error_message.config(font=("Times New Roman", 35, 'italic'))
        error_message.place(relx=.5, rely=.4, anchor="n")
        window.after(3000, lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))
    else:
        try:
            select_query = "Update preference set preference_value = %s WHERE preference_name =%s"
            mycursor.execute(select_query, (change, preference))  # *  SINGLE TABLE SQL* update the preference
            db.commit()
            changes_made = Label(window, text="Update Was Successful")
            changes_made.config(bg='blanched almond')
            changes_made.config(font=("Times New Roman", 40, 'italic'))
            changes_made.place(relx=.5, rely=.4, anchor="n")
            window.after(3000, lambda: edit_preference_menu(logged_in, username, admin, db, mycursor, window))
        except mysql.connector.errors.DataError:  # if the entry was greater than 255 charters, display an error 
            # and return ot the previous screen 
            changes_made = Label(window, text="Entry Must Be Under 255 Characters")
            changes_made.config(bg='blanched almond')
            changes_made.config(font=("Times New Roman", 40, 'italic'))
            changes_made.place(relx=.5, rely=.4, anchor="n")
            window.after(3000,
                         lambda: confirn_valid_preference(logged_in, username, admin, db, mycursor, window, preference))


def view_preferences(logged_in, username, admin, db, mycursor, window):
    # Allow the user to view their current preferences CONTINUING REQUIREMENT 7.1
    remove_all(window)
    create_menu(logged_in, username, admin, db, mycursor, window)
    select_an_option = Label(window, text="Current Preferences")
    select_an_option.config(bg='blanched almond')
    select_an_option.config(font=("Times New Roman", 30))
    select_an_option.place(x=150, y=50)
    mycursor.execute("Select preference_name, preference_value from preference")
    data = mycursor.fetchall()  # *  SINGLE TABLE SQL* select the preference names and values from the 
    # preference table 
    treeview = ttk.Treeview(window, columns=(1, 2), show="headings", height="8")
    style = ttk.Style(window)  # A table to display the information
    style.theme_use("clam")
    style.configure('Treeview', rowheight=36)
    style.configure("Treeview", background="blanched almond",
                    fieldbackground="blanched almond", foreground="black")
    treeview.pack(side=TOP, pady=130)
    treeview.heading(1, text="Preference")
    treeview.heading(2, text="Value")
    scrollbar = ttk.Scrollbar(orient="vertical", command=treeview.yview)
    sctollbar2 = ttk.Scrollbar(orient="horizontal", command=treeview.xview)
    scrollbar.pack(side="left", fill="y")
    sctollbar2.pack(side='bottom', fill='x')
    # Vertical and Horizontal scrollbars to view the table fully if needed
    counter = 0
    for i in data:  # format the data into the appropriate forms
        counter = counter + 1
        if counter == 2 or counter == 3:
            data = [i[0], i[1] + " degrees"]
            treeview.insert('', 'end', values=data)
        elif counter == 5:
            data = [i[0], "+" + i[1] + "%"]
            treeview.insert('', 'end', values=data)
        elif counter == 6:
            data = [i[0], "-" + i[1] + "%"]
            treeview.insert('', 'end', values=data)
        elif counter == 9:
            pass
        else:
            treeview.insert('', 'end', values=i)


# Although majority of the program functions within highly modularised code, the window is created from the main 
# program. Additionally, all modules are checked to be functional, to ensure no abrupt crashes occur, while the user 
# is operating the application 

try:
    from tkinter import *  # attempt to import the TKINTER module. This allows for dropdown menu's, buttons, 
    # and custom background colour REQUIREMENT 8.1
    modules_exist = True
    logged_in = "False"
    window = initialise_window(logged_in, None, None, None, None, None)  # create the graphics window
except ImportError:  # if the graphics window cannot be made, a message is printed in the idle indicating the 
    # relevant graphics package is missing 
    modules_exist = False
    print("The Graphics Module Tkinter Is Missing. Please Install To Continue")
try:  # all modules are imported briefly to ensure they are all installed, before the program exists
    import mysql.connector
    from tkinter import filedialog
    from tkinter import ttk
    from tkinter import font
    from random import randint
    from tkinter import TclError
    from datetime import timedelta, date, datetime
    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    from matplotlib.pyplot import (figure, xlabel, ylabel, plot)
    from tkinter.ttk import Combobox
    from hashlib import pbkdf2_hmac
    from os import (path, environ, urandom)
    from csv import reader
    from requests import get, exceptions
    from math import ceil
    from collections import Counter
    import smtplib, ssl
    import socket
except ImportError as error:  # if any modules are missing, the program cannot run, hence display an appropriate 
    # error message 
    modules_not_found_error = Label(window, text="One Or More Of The Modules \nRequired, Are Not Installed")
    modules_not_found_error.config(bg='blanched almond')
    modules_not_found_error.config(font=("Times New Roman", 30))
    modules_not_found_error.place(relx=.5, rely=.3, anchor="n")
    view = Button(window, text="Quit",
                  command=lambda: (window.destroy(), quit()))
    view.config(bg='blanched almond')
    view.config(height=2, width=40)
    view.place(x=150, y=400)
    modules_exist = False
if modules_exist:  # if all modules exist, begin to sign into the database
    db_in(window)
