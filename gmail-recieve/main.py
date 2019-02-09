# coding=utf-8
import email
import imaplib
import collections

email_structure = collections.namedtuple(
    ('email_structure'), ['id', 'sender', 'subject', 'body'])

GMAIL_LOGIN = "xxx@gmail.com"
GMAIL_PASSWORD = "yyyy+"
GMAIL_SERVER = "imap.gmail.com"


def get_message_body(email_message):
    for part in email_message.walk():
        if part.get_content_type() in ["text/plain", "text/html"]:
            body = part.get_payload(decode=True)
            return body


# https://codehandbook.org/how-to-read-email-from-gmail-using-python/
# http://www.vineetdhanawat.com/blog/2012/06/how-to-extract-email-gmail-contents-as-text-using-imaplib-via-imap-in-python-3/
def read_email_from_gmail(*, server, login, password, limit=2):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    limit_counter = 0
    for i in range(latest_email_id, first_email_id, -1):
        limit_counter += 1
        if limit_counter > limit:
            return

        email_id = str(i)
        typ, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        yield email_structure(
            id=email_id,
            subject=email_message['subject'],
            body=get_message_body(email_message),
            sender=email_message['from']
        )

def delete_email_from_gmail(*, server, login, password, limit=1):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    limit_counter = 0
    for i in range(latest_email_id, first_email_id, -1):
        limit_counter += 1
        if limit_counter > limit:
            break
        mail.store(str(i), '+FLAGS', '\\Deleted')

    mail.expunge()
    mail.close()
    mail.logout()

if __name__ == '__main__':
    for message_data in read_email_from_gmail(server=GMAIL_SERVER,
                                              login=GMAIL_LOGIN, password=GMAIL_PASSWORD):
        print(message_data.id, message_data.subject)
    delete_email_from_gmail(server=GMAIL_SERVER,
                                              login=GMAIL_LOGIN, password=GMAIL_PASSWORD)
