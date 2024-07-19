
import os
import base64
import logging
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://mail.google.com/']

def get_gmail_service():
    creds = None
    token_path = '/code/app/token.json'
    credentials_path = '/code/app/credentials.json'

    # Check if the token file exists and load credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or obtain new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Failed to refresh credentials: {e}")
                creds = None
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logger.error(f"Failed to obtain credentials: {e}")
                return None
        # Save the new credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        logger.error(f'An error occurred: {error}')
        return None

def send_email(subject: str, recipient: str, body: str):
    service = get_gmail_service()
    if not service:
        logger.error('Failed to create Gmail service.')
        return

    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}

    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        logger.info(f'Message Id: {sent_message["id"]}')
    except HttpError as error:
        logger.error(f'An error occurred: {error}')

# Uncomment the following block to test the script directly
# if __name__ == "__main__":
#     send_email(
#         'Test Subject',
#         'recipient@example.com',
#         'This is the body of the email.'
#     )
