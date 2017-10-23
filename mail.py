import smtplib
import base64

def send_mail(to_addr = 'rvdaescu@gmail.com', msg = None):
    """
    msg must contain subject \n\n + body
    """

    server = smtplib.SMTP_SSL('mail.vhsmail.vodafone.com', 465)

    server.login('office@daescu.ro', base64.decodestring('U3VnaXB1bGExQA==\n'))

    sub_msg =  'Subject: ' + msg

    msg = msg

    server.sendmail('office@daescu.ro', to_addr , sub_msg)

    server.quit()
