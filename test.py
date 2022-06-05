import smtplib

email = 'bot.apartment22@gmail.com'
passw = 'xkarngmqiyuspujn'

contact = ''
message = 'Ey! te quiero guapo xxx'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(email, passw)
server.sendmail(email, contact, message)

server.quit()