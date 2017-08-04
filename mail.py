import smtplib

server = smtplib.SMTP('mail.vhsmail.vodafone.com', 25)

server.login('office@daescu.ro', 'Sugipula1@')

msg = 'this is a test email\n Yes'

server.sendmail('office@daescu.ro', 'rvdaescu@gmail.com', msg)

