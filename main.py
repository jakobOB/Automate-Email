from string import Template
import smtplib
import os
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
FILES = ['test.pdf']                            # Add more files if you want to


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    greetings = []
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            greetings.append(a_contact.split(', ')[0])
            names.append(a_contact.split(', ')[1])
            emails.append(a_contact.split(', ')[2])
    return greetings, names, emails


def main():
    greetings, names, emails = get_contacts('Files/contacts.txt')
    message_template = read_template('Files/message.txt')

    try:
        with smtplib.SMTP_SSL(host=SMTP_SERVER, port=SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            for greeting, name, email in zip(greetings, names, emails):
                msg = MIMEMultipart()

                name = '' if "NONE" in name else name

                message = message_template.substitute(GREETING=" ".join([greeting, name]))

                msg['From'] = EMAIL_ADDRESS
                msg['To'] = email
                msg['Subject'] = ""                          # Add a subject here

                msg.attach(MIMEText(message, 'plain'))

                for file in FILES:
                    with open('Files/' + file, "rb") as f:
                        part = MIMEApplication(f.read(), Name=basename(file))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
                    msg.attach(part)

                smtp.send_message(msg)
                print("Email sent to: {}".format(email))
                del msg
        print("Emails Successfully send!")
    except:
        print("Something went wrong!")


if __name__ == "__main__":
    main()
