import json
import smtplib
from email.message import EmailMessage
from google.cloud import firestore
from google.cloud import secretmanager
import os

def invite_users(data, context):

    db = firestore.Client()
    path = context.resource.split('documents/')[-1]
    doc_ref = db.document(path)
    client = secretmanager.SecretManagerServiceClient()
    sender = client.access_secret_version(request={"name": f"projects/{os.environ.get('PROJECT_ID')}/secrets/SMTP_EMAIL/versions/1"}).payload.data.decode("UTF-8")
    password = client.access_secret_version(request={"name": f"projects/{os.environ.get('PROJECT_ID')}/secrets/SMTP_PASSWORD/versions/1"}).payload.data.decode("UTF-8")
    invitee_email = data['value']['fields']['inviteeEmail']['stringValue']
    inviter_email = data['value']['fields']['inviterEmail']['stringValue']
    message = EmailMessage()
    message['From'] = sender
    message['Subject'] = 'Invitation to join Demand-Driven Marketplace Application'
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, password)
    message['To'] = invitee_email
    message.set_content(
        f"You have been invited by {inviter_email} to join Demand-Driven Marketplace Application.\nClick on link to join now: http://localhost:3000/signup")
    s.sendmail(sender, invitee_email, message.as_string())
    doc_ref.update(
        {
            'sent': True
        }
    )
    s.quit()
