import smtplib
import os
import glob
import sys
import Adafruit_DHT
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


__version__ = '0.1'
__author__ = '@Iban Marco@'

def get_pictures():
    files = glob.glob("/var/lib/motion/*jpg")
    files.sort(key=os.path.getmtime)
    files.reverse()

    my_picts = []

    for zz in range(0, 51, 10):
        my_picts.append(files[zz])

    return my_picts

def send_gmail(temperature, humidity, my_picts):
    recipients = [RECIPIENTS_EMAILS_IDs]
    sender_email_id = SENDER_EMAIL_ID
    sender_pwd = PASSWORD
    my_humidity = "Humidity is {}".format(humidity)

    if temperature >= 23:
        my_temperature = "[Patrick]: Temperature HIGH: {0}°C".format(temperature)
    elif temperature <= 19:
        my_temperature = "[Patrick]: Temperature LOW: {0}i°C".format(temperature)
    else:
        my_temperature = "[Patrick]: Temperature OK: {0}°C".format(temperature)

    for recipient in range(len(recipients)):
        subject = my_temperature
        message = my_humidity
        msg = MIMEMultipart()
        msg['From'] = sender_email_id
        msg['To'] = recipients[recipient]
        msg['Subject'] = my_temperature

        msg.attach(MIMEText(message, 'plain'))

        for pict in my_picts:
            filename = os.path.basename(pict)
            attachment = open(pict, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email_id, sender_pwd)
        text = msg.as_string()
        server.sendmail(sender_email_id, recipients[recipient], text)
        server.quit()

def main():
    sensor = 22
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    temperature = round(temperature, 2)
    humidity = round(humidity, 2)

    my_picts = get_pictures()
    send_gmail(temperature, humidity, my_picts)

if __name__ =="__main__":
    main()
