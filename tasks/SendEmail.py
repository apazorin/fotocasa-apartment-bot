import smtplib
from tasks.ReadCSV import ReadCSV

class SendEmail: 
    def __init__(self): 
        self.email = ''
        self.passw = ''
        self.csv = ReadCSV()

    def readEmails(self):
        return self.csv.ReadEmails() 

    def run(self, message):

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.email, self.passw)
        for i in range(0,self.csv.length): 
            server.sendmail(self.email, self.csv[i], message)

        server.quit()