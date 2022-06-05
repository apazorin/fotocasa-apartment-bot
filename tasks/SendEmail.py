import smtplib
from tasks.ReadCSV import ReadCSV

class SendEmail: 
    def __init__(self): 
        self.email = 'bot.apartment22@gmail.com'
        self.passw = 'xkarngmqiyuspujn'
        self.subject = 'Reporte de actividad de tu robot fotocasa-habitaclia'
        self.csv = ReadCSV()

    def readEmails(self):
        return self.csv.ReadEmails() 

    def run(self, message):
        emails = self.readEmails()

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.email, self.passw)

        for i in range(0, len(emails)):
            print(emails[i])
            server.sendmail(self.email, emails[i], message)
        server.quit()