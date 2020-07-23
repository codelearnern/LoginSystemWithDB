import sqlite3 #For database
import hashlib #For hashing
import binascii
import os

conn = sqlite3.connect("account.db") #Connecting to database(if not connected, it will be created.)
 
def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

ifAccount = input("Do you already have an account? ")

if ifAccount.lower() == "yes":
    c = conn.cursor() #To actually do SQL commands
    c.execute("SELECT * FROM accounts")

    unameOrEmail = input("Please enter your username or email: ")
    pwdLogin = input("Please enter your password: ")

    data = c.fetchall()[0] #To access the account stored in the database

    if unameOrEmail in data:
        if verify_password(data[2], pwdLogin): #Check if password stored in database in unhashed form is same as password entered
            print("You're logged in!")
        else:
            print("Your account was not found, please enter correct credentials or signup if you don't already have an account.")
    else:
        print("Your account was not found, please enter correct credentials or signup if you don't already have an account.")
elif ifAccount.lower() == "no":
    try:
        c = conn.cursor() #To actually do SQL commands

        c.execute("""CREATE TABLE accounts(
            username text,
            email text,
            password text
        )""") #Creating table
        conn.commit()

        print("Alright then, signup process has started.")

        uname = input("What do you want your username to be: ")
        email = input("What is your email: ")
        pwd = input("What do you want your password to be: ")

        c.execute("""INSERT INTO accounts VALUES (?, ?, ?)""", (uname, email, hash_password(pwd))) #Insert in the username, email, and password for the account

        conn.commit()
        conn.close()

        print("Account created, to login, run the program again.")
    except:
        print("You actually already have an account, sign in with your credentials.")
    
else:
    print("You have to say yes or no.")