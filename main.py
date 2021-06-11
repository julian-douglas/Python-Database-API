#Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27) 
#[Clang 6.0 (clang-600.0.57)] on darwin
#Type "help", "copyright", "credits" or "license()" for more information.
import sqlite3

conn = sqlite3.connect("EmployeeUoB")

# Define DBOperation class to manage all data into the database. 
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = "create table EmployeeUoB (employeeID INTEGER primary key, empTitle Text, forename TEXT, surname TEXT,email Text,salary float NOT NULL)" #this is the one I used. Command to create a table with six columns.

  sql_create_table = "create table if not exists EmployeeUoB (employeeID INTEGER primary key, empTitle Text, forename TEXT, surname TEXT,email Text,salary float NOT NULL)" #I was going to add 'AUTOINCREMENT' to employeeID, but I couldn't get it to automatically increment the user ID so I just left it off.

  sql_insert = ("insert into EmployeeUoB values (?, ?, ?, ?, ?,?)") #insert function
  #user inputs all values
  sql_select_all = "select * from EmployeeUoB" #select all
  sql_search = "select * from EmployeeUoB where employeeID = ?" #mark scheme asks to search data by employee ID 
  sql_update_data = "update EmployeeUoB set (empTitle, forename, surname, email, salary) = (?,?,?,?,?) where employeeID = ?" #unclear what I was meant to update here, so I just allowed the user to update anything, searching by employee ID.
  sql_delete_data = ("delete from EmployeeUoB where employeeID = (?)") #there was a comment in this template that mentioned deleting data by employee ID.
  sql_drop_table = "drop table if exists EmployeeUoB" #this was already in the template (I think), unless I added it in.
  sql_higher_sal = ("select * from EmployeeUoB where salary >= ?") #my optional function was to select employees who have a salary over a specified amount.

 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("EmployeeUoB")
      self.cur = self.conn.cursor()
      #self.cur.execute(self.sql_create_table)
      #I edited this out so that it runs create table below
     

      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close() 

  def get_connection(self):
    self.conn = sqlite3.connect("EmployeeUoB")
    self.cur = self.conn.cursor()

  def create_table(self): #create table
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table_firsttime) #Run the command using SQL code. I wanted to use create_table, but because I added 'if not exists', no error message was produced. 
      self.conn.commit() #store the changes to the system
      print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self): #insert data, enter a column one by one
    print("Add a record")
    print()
    try:
      self.get_connection()
      
      emp = Employee()
      emp.set_employee_id(int(input("Enter Employee ID: "))) #I was going to take this off so that the programme automatically incremented employee ID but I couldn't get it to work.
      #If the user tries to input a number that is not an integer or a number that is already taken, the programme produces an error message.

      #now to add my own
      #allow the user the input each column for a record
      emp.set_employee_title(input("Enter Employee Title: "))

      emp.set_forename(input("Enter Employee's First Name: "))

      emp.set_surname(input("Enter Employee's Surname: "))

      emp.set_email(input("Enter Employee's Email Address: "))

      emp.set_salary(float(input("Enter Employee's Salary: ")))
      

      self.cur.execute(self.sql_insert,list(str(emp).split("\n"))) #use the sql_insert function above to append the record to the database

      self.conn.commit() #commit results (save the data that has entered into the database)
      print()
      print("Data inserted successfully")#allow the user to know that they have successfully inserted data
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all) #call the function defined above
      results = self.cur.fetchall()
      col_names = ['Employee ID', 'Title', 'Forename', 'Surname', 'Email', 'Salary'] #to make the output look cool, I did this and below. We did it a different way in CW2 (by specifying .header on, .mode column etc) however as this is Python and not SQL, I couldn't get this to work. I tried self.cur.execute() but it would not work.It may look strange the first time you run it; I designed my programme to be used full screen so please stretch the black screen so it fits the full screen. 
      
      
      if len(results) >0: #show the records
        print('All records shown below')
        print()
        
        print("{:12} {:6} {:15} {:15} {:40} {:10}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4],col_names[5])) #Long character count of 40: this is to take into account long email addresses.

        for row in results:
          print("{:<12} {:<6} {:<15} {:<15} {:<40} {:<10}".format(row[0], row[1], row[2], row[3], row[4], row[5]))

        
      else:
        print ("No records found")
      self.conn.commit()


    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
      

  def search_data(self): #search data by employee ID
    print("Search for a record")
    print()
    try:
      self.get_connection()
      employeeID = input("Enter Employee ID: ") #search by employee ID as per the requirements
      self.cur.execute(self.sql_search, (employeeID,)) #put a comma next to employeeID to fix the binding issue
      

      result = self.cur.fetchall() #get all the records that match with that ID. should only return one.
      
      col_names = ['Employee ID', 'Title', 'Forename', 'Surname', 'Email', 'Salary']
      if len(result) >0:
        print("Result shown below")
        print()
        
        print("{:12} {:6} {:15} {:15} {:40} {:10}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4],col_names[5]))

        for row in result:
          print("{:<12} {:<6} {:<15} {:<15} {:<40} {:<10}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
      else:
        print("No record exists for Employee ID", employeeID)
            

      #no need to commit anything here, as the database is not being updated.

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  def update_data(self):
    print("Update a record")
    print() #here I allowed the user to update every column in the record
    try:
      self.get_connection()
      employeeID = input("Enter Employee ID: ")
      title = input("Enter new title: ")
      forename = input("Enter new first name: ")
      surname = input("Enter new surname: ")
      email = input("Enter new email address: ")
      salary = input("Enter new salary: ")
      self.cur.execute(self.sql_update_data, (title, forename, surname, email, salary, employeeID)) #call the function above
      result = self.cur.rowcount #get the number of records changed
      print()
      if result == 1:
        print("1 row updated.")

      elif result > 1:
        print(result, "rows updated.")
      else:
        print("No record exists for Employee ID", employeeID)
      self.conn.commit() #a record will have changed, so needs to be committed

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Define Delete_data method to delete data from the table. The user will need to input the employee id to delete the corrosponding record. 
  def delete_data(self):
    print("Delete a record")
    print()
    try:
      self.get_connection()
      employeeID = input("Enter Employee ID: ")
      self.cur.execute(self.sql_delete_data, (employeeID,))
      result = self.cur.rowcount #get the number of records deleted (should only be one, as they are deleting records that match a primary key)
      self.conn.commit() #update the database
      print()
      if result == 1:
        print("1 record deleted.")
      elif result > 1:
        print(result, "records deleted.")

      else:
        print("No record exists for Employee ID", employeeID)

    except Exception as e:
      print(e)
    finally: 
      self.conn.close()
      
  def higher_salary(self):
#my optional function was to return a list of employees who have a salary higher than what the user puts in.
    try:
      self.get_connection()
      salary = input("Salary higher than?: ") #user inputs a salary
      print()
      
      self.cur.execute(self.sql_higher_sal, (salary,))
      results = self.cur.fetchall()
      col_names = ['Employee ID', 'Title', 'Forename', 'Surname', 'Email', 'Salary']
      

      
      print("Records with salaries higher than £", salary, ":", sep='')
      print()


      if len(results) >=1:
        print(len(results), "record(s) found.")
        print()
        
        print("{:12} {:6} {:15} {:15} {:40} {:10}".format(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4],col_names[5]))

        for row in results:
          #print(row[0], row[1])
          print("{:<12} {:<6} {:<15} {:<15} {:<40} {:<10}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
          
          
      else:
        print("No records found.")
      
      
      
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary
  
  def get_employee_id(self):
    return self.employeeId

  def get_employee_title(self):
    return self.empTitle
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# The main function will parse arguments. 
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
  #create a menu
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data from EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data some records")
  print (" 6. Delete data some records")
  print (" 7. Return employees with higher salaries than input")
  print (" 8. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7: #I added my function here
    db_ops.higher_salary()
  elif __choose_menu == 8:
    exit(0)
  else:
    print ("Invalid Choice")



