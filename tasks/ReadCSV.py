from fileinput import close
from classes.Variable import Variable
from classes.User import User
import os
import SendEmail

PENDING = "Pending"
IN_PROGRESS = "In progress"
ERROR = "Error"
COMPLETE = "Complete"

LOGIN_FILE = "login.csv"
DATA_FILE = "data.csv"
EMAILS_FILE = "emails.csv"
PATH = "C:\\Users\\rastr\\Documents\\RPA\\fotocasa-apartment-bot\\inputs"

FILE = "data.csv"

class ReadCSV:

    def __init__(self):
        self.login_file = LOGIN_FILE
        self.data_file = DATA_FILE
        self.input_path = PATH
        self.emails_file = EMAILS_FILE
        self.sendEmail = SendEmail()

    #leer csv
    def ReadData(self):
        try:
            import csv
            variables = []
        
            os.chdir(self.input_path)
            os.getcwd()

            f = open(self.data_file)
            reader = csv.reader(f)
            i = 0

            for row in reader:
                i += 1
                if i >= 2:
                    print(f"...Procesando... fila {i}: {row}")
                    variables.append(Variable(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], \
                        row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], \
                            row[18], row[19], row[20], row[21], row[22], row[23], row[24]))
            close()
            
            return variables

        except Exception as e: 
            err = "Error al leer el archivo CSV. Compruebe no dejar ninguna columna vacía"
            print(err)
            print(f"Error: {e}")
            self.sendEmail.run(f'Fatal error: {err}')
        finally: close()
    
    def ReadLogin(self):
        try:

            import csv

            os.chdir(self.input_path)
            os.getcwd()

            f = open(self.login_file)
            reader = csv.reader(f)

            for row in reader:
                print(f"...Processing login details: {row}")
                user = User(row[0], row[1])
            return user
        except Exception as e: 
            err = "Error al leer el archivo CSV de login"
            print(err)
            print(f"Error: {e}")
            self.sendEmail.run(f'Fatal error: {err}')
        finally: close()

    def ReadEmails(self):
        try:
            import csv
            emails = []

            os.chdir(self.input_path)
            os.getcwd()

            f = open(self.emails_file)
            reader = csv.reader(f)

            for row in reader:
                print(f"...Processing emails: {row}")
                emails.append(row[0])
            print(emails)
            return emails
        except Exception as e: 
            print("Error al leer el archivo CSV de emails")
            print(f"Error: {e}")
        finally: close()
