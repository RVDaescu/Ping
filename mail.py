import smtplib

def send_mail(to_addr = 'rvdaescu@gmail.com', msg = None)

    server = smtplib.SMTP('mail.vhsmail.vodafone.com', 25)

    server.login('office@daescu.ro', 'Sugipula1@')

    msg = msg

    server.sendmail('office@daescu.ro', to_addr , msg)

