# Bank system
import csv
import pickle as log
import datetime as dat
from time import sleep
import os,random
import pymysql as sql
users = []
cur_user = []
def date():
    dt = str(dat.datetime.now())
    months = ['Jan', 'Feb','Mar', 'Apr', 'May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day = dt[8:10]+' '
    mon = int(dt[5:7])-1
    mon = months[mon]+' '
    year = dt[0:4]
    date = day+mon+year
    return date
def clock():
    dt = str(dat.datetime.now())
    hour = dt[11:13]+' '
    ap = 'AM'
    if int(hour)>12:
        hour = int(hour)
        ap = 'PM'
        hour -= 12
        hour = str(hour)+':'
    min = dt[14:16]+' '
    clock = hour+min+ap
    return clock

# Initial connection to create sql db and tables required
logger = open("main.log",'ab')              #Starting system logger
log.dump(f"{date()}   {clock()} --- New session boot by user",logger)
log.dump("Started logging\n",logger)
try:
    con = sql.connect(
    host = 'localhost',
    user = 'root',
    password = '')
    log.dump(f'{clock()} -- Successful connection to MySQL',logger)
except sql.Error as e:
    print(f"Error encountered : {e}\nContact support team for help.")
    log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
    log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
    logger.close()
    exit()
cur = con.cursor()
try:
    cur.execute("create database if not exists Bank_db;")
    cur.execute("use Bank_db;")
    cur.execute("create table if not exists UserInfo(UsrNo int(11) PRIMARY KEY,Name varchar(25) NOT NULL,Email varchar(50) NOT NULL,Phone bigint(10) NOT NULL,Aadhar bigint(12) not null,Balance bigint(11),Transactions varchar(15) UNIQUE not null,Username varchar(20) UNIQUE not null,Password varchar(18) not null);")
    cur.execute("create table if not exists EmployeesDB(EmpNo int(11) PRIMARY KEY,Name varchar(25) NOT NULL,Email varchar(50) NOT NULL,Phone bigint(10) NOT NULL,Aadhar bigint(12) UNIQUE not null,Salary int(10) not null,Job varchar(20) not null);")
    con.commit()
except Exception as e:
    log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
    log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
    logger.close()
    print("An error has occurred. Kindly try to fix it or contact our support.\n","Error code:",e,)
cur.execute(f'select * from UserInfo')
users = []
if cur.rowcount == 0:         # Two default Admin accounts for bank usage
    log.dump(f'{clock()} !!! Default bank accounts not found. Creating 2 sample accounts',logger)
    cur.execute("insert into UserInfo values(1, 'HariRamS', 'hr2305@gmail.com', 9977553311, 123411112222, 89000, 'Trans1.csv', 'hari_2305', 'hari2305@prksh');")
    cur.execute("insert into UserInfo values(2, 'Anonymous', 'admin_@prkshbank.in', 9099099123, 111122223333, 21000, 'Trans2.csv', 'Admin_1', 'Anymos120107');")
    con.commit()
cur.execute(f'select * from UserInfo')
users = cur.fetchall()
users = list(users)
users_copy = []
for i in users:
    i = list(i)
    users_copy.append(i)
users = users_copy

employees = []
cur.execute("select * from EmployeesDB;")
if cur.rowcount == 0:             # Sample Default employees for EmployeesDB table
    log.dump(f'{clock()} !!! Default employees not found. Creating 4 sample entries in the DB',logger)
    cur.execute("insert into EmployeesDB values(1,'Jinshu','jinsu.m@gmail.com',9909112233,132322229999,20000,'Sales Marketing');")
    cur.execute("insert into EmployeesDB values(2,'Keshav','keshav@safehavendefence.com',9900000222,132333332222,10000,'Security');")
    cur.execute("insert into EmployeesDB values(3,'Sumit','sumitarora@prkshbank.com',7832139900,133232312324,50000,'IT technician');")
    cur.execute("insert into EmployeesDB values(4,'Dhyan Kanda','No mail given',8091293091,132312312325,5000,'Peon');")
    con.commit()
cur.execute("select * from EmployeesDB;")
employees = cur.fetchall()
employees = list(employees)
employees_copy = []
for j in employees:
    j = list(j)
    employees_copy.append(j)
employees = employees_copy

f = open("Trans1.csv","a",newline='')         # For existing accounts in the users DB
f.close()
f = open("Trans2.csv","a",newline='')
f.close()
con.close()
log.dump(f'{clock()} -- Initial MySQL connection closed',logger)

def sql_conn():
    try:
        con = sql.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'Bank_db')
        log.dump(f'{clock()} -- New successful connection to MySQL',logger)
    except sql.Error as e:
        log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
        log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
        print(f"Error encountered : {e}\nContact support team for help.")
        exit()
    cursor = con.cursor()
    return [con,cursor]         #Function to connect to the SQLdb. Returns the connection and cursor
def users_info():
    vars = sql_conn()
    con = vars[0]
    cursor = vars[1]
    cursor.execute(f'select * from UserInfo')
    users = cursor.fetchall()
    users = list(users)
    users_copy = []
    for i in users:
        i = list(i)
        users_copy.append(i)
    users = users_copy
    con.close()
users_info()                #Function call to retreive current records from the sql db
def signup():
    # SQL format: UserId,Name,Email,Phone,Aadhar,Balance,Transactions,Username,Password
    trusted_domains = ['gmail.com','yahoo.com','hotmail.com','aol.com','outlook.com']
    while True:
        os.system('clear||cls')
        while True:
            try:
                name = str(input("Enter your name: "))
                if name.isalpha():
                    break
                else:
                    print("Enter your real name! (No special characters or numbers)")
            except Exception:
                print("Enter your real name! (No special characters or numbers)")        
                continue
        while True:
          index = 0
          email = input("Enter your email id: ")
          for i in range(len(email)):
            if email[i] == '@':
              index = i+1
          if email[index::] in trusted_domains:
            break
          elif email[index::] not in trusted_domains:
            print("Please enter a valid email id!")
            continue
        while True:
            aadhar = int(input("Enter your aadhar card number: "))
            if len(str(aadhar))==12:
                break
            else:
                print("Kindly enter your correct 12-digit aadhar card number.")
        while True:
            phone = int(input("Enter your phone number: "))
            if len(str(phone))==10:
                break
            else:
                print("Invalid phone number, Please try again")
        print("Are all of these details correct?")
        print(f"""Name: {name}
Phone number: {phone}
Email id: {email}
Aadhar card no: {aadhar}""")
        yn = input("(y/n): ")
        if yn=='y':
            break
        elif yn=='n':
            continue
    for i in range(3):
        print(".....")
        sleep(1)
    print("Details verified.")
    print("Choose a strong password for your account.")
    while True:
        passw = input("Password should be 8-16 characters long.\nSet password: ")
        if len(passw)<8 or len(passw)>16:
            print("Password length invalid. Try again")
            continue
        else:
            while True:
                conf = input("Confirm your password: ")
                if passw == conf:
                    break
                else:
                    print("Passwords do not match. Try again.")
                    continue
            break
    os.system('clear||cls')
    print("Loading....")
    sleep(2)
    print("Loading....")
    sleep(1)
    print("Account creating successful!")
    sleep(0.2)
    try:
        sqlcon = sql.connect(user='root',password='',database='Bank_db')
        cur = sqlcon.cursor()
        cur.execute("select * from UserInfo")
        records = cur.fetchall()
        Users = []                                  #Code to basically
        for i in records:                           #get all current usernames
            record = list(i)                        #to ensure no duplicate user
            Users.append(record[-2])                #exists.
        UserNo = len(records)+1
        while True:
            username = random.randint(100000,999999)    #New user_id creator
            if username not in Users:
                break
            else:
                continue
        print("Here are your login credentials. Save them in a secure way.")
        print(f"Username: {username}\nPassword: {passw}")
        transac = "Trans"+str(UserNo)+".csv"           #Transactions file name
        cur.execute(f"insert into UserInfo values({UserNo},'{name}','{email}',{phone},{aadhar},10000,'{transac}',{username},'{passw}')")
        log.dump(f'{clock()}  @@  New user signed up. Name:{name} - Details successfully added to SQL DB',logger)
        sqlcon.commit()
        sqlcon.close()
        print("Kindly visit our nearest branch and make the minimum deposit of Rs. 5000 only") 
        input("to start your internet banking account. Press <Enter> to return to main menu..")
        f = open(transac,"a",newline='')
        f.close()
    except sqlcon.Error as e:
        print("An error as occurred. Kindly contact our customer care for technical support")
        print(f"Error: {e}")
        log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
        log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
        logger.close()
        print("Exiting...")
        sleep(2)
        exit()
def forgot_pswd():
    dat = []
    users_l = users           #Variables to store user records and stuff
    found = False
    sqll = sql_conn()
    con = sqll[0]
    cursor = sqll[1]
    while True:
        u = input("Enter username: ")
        for user in users_l:
            if user[7]==u:
                dat = user
                print("Found details!")
                found = True
                break
            elif user[7]!=u:
                print("Retrying..")
                sleep(1)
        if found:
            break
        else:
            print("Username not found. Exiting..")
            sleep(2)
            os.system('clear||cls')
            exit()             
    try:
        email = dat[2]
        phone = dat[3]
        aadhar = dat[4]
        email_inp,aadhar_inp,phone_inp='',0,0
        n1,n2,n3 = 5,5,5        #No. of tries you get to input correct credentials.
        while True:
            n1-=1               #Email verification
            email_inp = input("Enter your email: ")
            if email == email_inp:
                break
            else:
                if n1>0:
                    print("Incorrect email.",n1,"tries left.")
                    continue
                elif n1==0:
                    print("Maximum tries reached. Exiting..")
                    sleep(2)
                    os.system('clear||cls')
                    exit()
        while True:
            n2-=1               #Aadhar verification
            aadhar_inp = int(input("Enter your Aadhar id(no spaces): "))
            if aadhar == aadhar_inp:
                break
            else:
                if n2>0:
                    print("Incorrect email.",n2,"tries left.")
                    continue
                elif n2==0:
                    print("Maximum tries reached. Exiting..")
                    sleep(2)
                    os.system('clear||cls')
                    exit()
        while True:
            n3 -= 1             #Phone number verification
            phone_inp = int(input("Enter your Phone number: "))
            if phone == phone_inp:
                break
            else:
                if n3>0:
                    print("Incorrect email.",n3,"tries left.")
                    continue
                elif n3==0:
                    print("Maximum tries reached. Exiting..")
                    sleep(2)
                    os.system('clear||cls')
                    exit()
        print("Verification passed. You're password is: '"+dat[8]+"'")
        c = input("Would you like to update your password? (y/n): ")
        if c == "y":
            new_pass = ''
            while True:
                new_pass = input("Enter your new password: ")
                if len(new_pass)<8 or len(new_pass)>16:
                    print("Invalid password. Password should be 8-16 characters long")
                    continue
                elif len(new_pass)<=16 or len(new_pass)>=8:
                    break
            cursor.execute(f"update UserInfo set Password='{new_pass}' where UsrNo={dat[0]}")    
            print("Password updated successfully! Exiting now..")
            log.dump(f'{clock()} ~~ User:{u} forgot password. New password updated by user.',logger)
            sleep(3)
            os.system('clear||cls')
        else:
            print("Dont forget your password next time :)")
            log.dump(f'{clock()} ~~ User:{u} forgot password. Password was not updated.',logger)
            sleep(1)
            print("Ok, have a nice day!")
            os.system('clear||cls')
    except Exception as e:
        print("Error",e)
        log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
        log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
        logger.close()
        print("Contact our tech support team on the number: 9099096969 for help regarding this issue")
    con.commit()
    con.close()
    users_info()        #To update and fetch the updated records
def login():
    user = []
    while True:
        print("Enter username:-")
        uname = str(input(">>> "))
        print("Enter password:-")
        pass_inp = str(input(">>> "))
        found = False
        for u in users:
            if u[-2] == uname:
                found = True
                user = u
        if found:
            pass
        else:
            log.dump(f'{clock()} -- User attempted to login but couldnt',logger)
            print("User not found. Retry")
            continue
        if user[-1]==pass_inp:
            log.dump(f'{clock()} -- User logged in successfully',logger)
            print("Succesful Login!")
            break
        else:
            log.dump(f'{clock()} -- User attempted to login but couldnt',logger)
            print("Incorrect Username or password! Try signing up instead!")
            continue
    sleep(1)
    os.system('clear||cls')
    return user
def transfer_money():
    while True:
        found = False
        account = []
        print("----------------------------------------------")
        min_bal = cur_user[5]-2500             #if 2500 is min amount req
        amount = float(input("\nEnter amount to transfer: "))
        if amount > min_bal:
            print("Not enough balance!")
            continue
        elif amount <= min_bal:
            u = input("Enter the user_id to transfer to: ")
            for i in users:
                if i[-2]==u:
                    account = i
                    found = True
        if found:
            new_bal = account[5]+amount
            cur_user[5] = cur_user[5]-amount
            sqll = sql_conn()
            con = sqll[0]
            cur = sqll[1]
            cur.execute(f"update UserInfo set Balance={new_bal} where UsrNo = {account[0]};")
            cur.execute(f"update UserInfo set Balance={cur_user[5]} where UsrNo = {cur_user[0]};")
            con.commit()
            con.close()
            print("Amount transfer successful!\nReturning to main menu..")
            sleep(2)
            break
        else:
            print("Please input valid username! Ask the payee for their username.\n----------------------------------------------")
            continue
    os.system('clear||cls')
    users_info()
    f = open(cur_user[-3],'a',newline='')   #Sender update
    csvw = csv.writer(f)
    csvw.writerow([date(),clock(),f'Money transfer to {account[1]}',f'-{amount}',cur_user[5]])
    f.close()

    fr = open(account[-3],'a',newline='')   #Reciever update
    csv1 = csv.writer(fr)
    csv1.writerow([date(),clock(),f'Money recieved from {cur_user[1]}',f'+{amount}',new_bal])
    fr.close()
    log.dump(f'{clock()} $$ Money transfer to User:{account[-2]}  by  {cur_user[-2]}. Amount:{amount}',logger)
def deposit_money():
    d = float(input("Enter amount to deposit: "))
    print("----------------------------------------------")
    print("We have booked your reservation at the nearest Bank. Please go there and make your deposit. Thank you")
    print("----------------------------------------------")
    # Imagine user goes to bank to make the deposit
    log.dump(f'{clock()} $$ Rupees {d} deposited by {cur_user[-2]} to self',logger)
    new_bal = cur_user[5]+d
    sqll = sql_conn()
    con = sqll[0]
    cur = sqll[1]
    cur.execute(f'update UserInfo set Balance = {new_bal} where UsrNo = {cur_user[0]};')
    con.commit()
    con.close()
    cur_user[5] = new_bal
    f = open(cur_user[-3],'a',newline='')
    csvw = csv.writer(f)
    csvw.writerow([date(),clock(),'Deposit by self',f'+{d}',new_bal])
    f.close()
    sleep(5)
    os.system('clear||cls')
def fixed_deposit():
    print("Fixed deposit can only be applied offline. \n Check your interest below:")
    print("----------------------------------------------")
    print("We offer 2.4%"+" interest per month\n")
    fd = 0
    while True:
        fd = float(input("Enter the principal amount: "))
        bal = cur_user[5]-2500
        if bal>=fd:
            break
        else:
            print("Not enough balance!")
            continue
    print("How many years would you like to deposit for?")
    n = int(input(">>> "))
    nt = float(12*n)
    interest = (1+(0.024/12))**nt
    f = fd*interest
    print("Calculating...")
    sleep(1)
    print("You will be receiving",f,"Rs. after the tenure.")
    input("Press <Enter> to return to main menu..")
    os.system('clear||cls')
def logo():
    os.system('clear||cls')
    print("===============================================================================================")
    print("                     ██████╗░██████╗░  ██████╗░░█████╗░███╗░░██╗██╗░░██╗")
    sleep(0.1)
    print("                     ██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗████╗░██║██║░██╔╝")
    sleep(0.1)
    print("                     ██████╔╝██████╔╝  ██████╦╝███████║██╔██╗██║█████═╝░")
    sleep(0.1)
    print("                     ██╔═══╝░██╔══██╗  ██╔══██╗██╔══██║██║╚████║██╔═██╗░")
    sleep(0.1)
    print("                     ██║░░░░░██║░░██║  ██████╦╝██║░░██║██║░╚███║██║░╚██╗")
    sleep(0.1)
    print("                     ╚═╝░░░░░╚═╝░░╚═╝  ╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝")
    print("                                                                                     By HariRam")
    print("                                                                                     Class 12th")
    print("                                                                Prakash Higher Secondary School")
    sleep(0.1)
    print("===============================================================================================\n")
    print("Welcome!")

# __main__
while True:
    log.dump(f'{clock()} @@ New session started successfully',logger)
    users_info()                    #Calling funcit
    logo()
    print("Sign up today and get higher interest rates!            *T&C applies\nAlready a user? Login")
    ls = int(input("Choose an option:\n1.Login\n2.Signup\n3.Forgot password\n4.Exit\n> "))
    if ls == 1:
        cur_user = login()
    elif ls == 2:
        signup()
        continue
    elif ls == 3:
        forgot_pswd()
    elif ls == 4:
        print("Have a nice day!")
        sleep(3)
        os.system('clear||cls')
        log.dump(f"{clock()} -- User exits session",logger)
        log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
        logger.close()
        exit()
    elif ls == 29892:                           #Secret input for admin login page
        admins = ['Admin_1','hari_2305']
        cur_user = login()
        if cur_user[-2] in admins:
            log.dump(f'{clock()} ## New admin login by {cur_user[-2]}',logger)
            while True:
                try:
                    conn = sql.connect(host='localhost',user='root',password='',database='Bank_db')
                    log.dump(f"{clock()} -- Successful connection to EmployeeDB",logger)
                except Exception as e:
                    print(f"Error encountered : {e}\nContact support team for help.")
                    log.dump(f'{clock()} -- Error {e} encountered. Exited program',logger)
                    log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
                    logger.close()
                    exit()
                cursor = conn.cursor()
                cursor.execute('select * from EmployeesDB;')
                employees = cursor.fetchall()
                employees = list(employees)
                emp_copy = []
                for i in employees:
                    emp_copy.append(list(i))
                employees = emp_copy
                logo()
                print("Today:",date(),'\t','Time:',clock())
                print("Welcome Admin",cur_user[1])
                print("Menu:\n1.View BMS log\n2.View Employees \n3.Edit employees\n4.Logout")
                inp = int(input("Select an option: "))
                if inp == 1:
                    os.system('clear||cls')
                    log_view = open("main.log","rb")
                    try:
                        while True:
                            print(log.load(log_view))
                    except EOFError:
                        pass
                    input("Press <Enter> to go back to menu")
                elif inp == 2:
                    print("[EmpNo,Name,Email,Phone,Aadhar,Salary,Job]")
                    for i in employees:
                        print(i)
                    print("------------------------------------------------------------------------------------------------------------")
                    input("Press <Enter> to continue")

                elif inp == 3:
                    ch = int(input("1.Add employee\n2.Delete employee\n>>> "))
                    if ch == 1:
                        while True:
                            nm = input("Enter employee's name: ")
                            em = input("Enter employee's email: ")
                            phn = int(input("Enter employee's phone: "))
                            adh = int(input("Enter employee's aadhar: "))
                            slr = int(input("Enter employee's salary: "))
                            job = input("Enter employee's job: ")
                            print("Are all these details correct?")
                            print(f"Name: {nm}")
                            print(f"Email: {em}")
                            print(f"Phone: {phn}")
                            print(f"Aadhar: {adh}")
                            print(f"Salary: {slr}")
                            print(f"Job: {job}")
                            yn = input("(y/n): ")
                            if yn == 'y':
                                num = len(employees)
                                num+=1
                                cursor.execute(f'insert into EmployeesDB values({num},{nm},{em},{phn},{adh},{slr},{job});')
                                conn.commit()
                                log.dump(f"{clock()} -- Admin added new employee {nm} to DB",logger)
                                break
                    elif ch == 2:
                        while True:
                            emp_del = int(input("Enter the record no to delete: "))
                            print("Do you want to delete this record?\n",employees[emp_del-1])
                            yn = input("(y/n): ")
                            if yn == 'y':
                                log.dump(f"{clock()} -- Admin deleted employee no: {emp_del} from DB",logger)
                                cursor.execute(f'delete from EmployeesDB where EmpNo={emp_del};')
                                conn.commit()
                                break
                    else:
                        print("Invalid choice. Returning to main menu")
                        sleep(3)
                elif inp == 4:
                    print("Now logging out. Please wait..")
                    log.dump(f"{clock()} ## Admin logged off.",logger)
                    log.dump(f'======================= END OF LOG FOR THIS SESSION =======================',logger)
                    logger.close()
                    sleep(3)
                    conn.close()
                    exit()
    else:
        print("Enter a valid option please!")
        sleep(3)
        continue
    os.system('clear||cls')
    while True:
        try:
            os.system('clear||cls')
            logo()
            print("Today:",date(),'\t','Time:',clock())
            print("Available actions:\n1. Transfer money\n2. Deposit money\n3. View account statement\n4. Make a Fixed Deposit(FD)\n5. Logout")
            ch = int(input("Input action: "))
            if ch == 1:
                transfer_money()
            elif ch == 2:
                deposit_money()
            elif ch == 3:
                f = open(cur_user[-3],'r')
                stmt = csv.reader(f)
                print(['Date','Time','Description','Amount','New balance'])
                for line in stmt:
                    print(line)
                print("-------------------------------------------------------------------------------------")
                log.dump(f'{clock()} ~~ User {cur_user[-2]} requested Account Statement',logger)
                input("Press <Enter> to return to main menu")
            elif ch == 4:
                log.dump(f'{clock()} $$ User {cur_user[-2]} made new Fixed Deposit',logger)
                fixed_deposit()
            elif ch == 5:
                print("Now logging out. Please wait..")
                log.dump(f'{clock()} -- User {cur_user[-2]} logged out',logger)
                sleep(3)
                break
        except Exception as e:
            log.dump(f"{clock()} !! Unexpected action by user. Ignoring..",logger)
            continue
