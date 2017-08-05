import smtplib
import base64

def send_mail(to_addr = 'rvdaescu@gmail.com', msg = None):

    server = smtplib.SMTP_SSL('mail.vhsmail.vodafone.com', 465)

    server.login('office@daescu.ro', base64.decodestring('U3VnaXB1bGExQA==\n'))

    msg =  'Subject: TEST \n\n Mail from Office'

    msg = msg

    server.sendmail('office@daescu.ro', to_addr , msg)

    server.quit()
