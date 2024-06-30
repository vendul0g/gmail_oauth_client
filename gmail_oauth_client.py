#!/usr/bin/env python3
import os
import sys
import logging
import time
import smtplib
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
from imap_tools import MailBox
import pyioga
from dotenv import load_dotenv


# This variables set the configuration for the email client
# Now there are here but they should be in a .env file
# Specifically private information like the email, as i hav done with the SMTP_EMAIL
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SCOPES = ["https://mail.google.com/"]
logging.basicConfig(level=logging.INFO)

load_dotenv()
SMTP_EMAIL = os.getenv("SMTP_EMAIL")

# Setup the key files
TOKEN_FILE = "./oauth_credentials/token.json"
CREDENTIALS_FILE = "./oauth_credentials/credentials.json"

def check_credential_file() -> bool:
    '''
    Function to check if the credential file exists
    '''
    if not os.path.exists(CREDENTIALS_FILE):
        print("[!] Credential file not found. Exiting...")
        return False
    return True

def authenticate_and_get_token() -> str:
    '''
    Function to authenticate and get the token if the token.json file is not found
    '''
    # Check if the credential file exists
    if not check_credential_file():
        sys.exit(1)

    # Authenticate and get the token
    creds = None
    try:
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
                with open(TOKEN_FILE, "w", encoding='utf-8') as token:
                    token.write(creds.to_json())
    except RefreshError as e:
        logging.error("RefreshError: %s. Re-authenticating.", e)
        # Re-initiate the authentication flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding='utf-8') as token:
            token.write(creds.to_json())

    return creds.token if creds else None


def send_email(recipient, subject, content):
    '''
    Function to send email to the recipient
    :param recipient: Email address of the recipient
    :param subject: Subject of the email
    :param content: Content of the email
    '''
    token = authenticate_and_get_token()
    if not token:
        logging.error("Failed to obtain a valid token. Email not sent.")
        return False

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.starttls()
    auth_string = (
        b"user="
        + bytes(SMTP_EMAIL, "ascii")
        + b"\1auth=Bearer "
        + token.encode()
        + b"\1\1"
    )
    session.docmd("AUTH", "XOAUTH2 " + (base64.b64encode(auth_string)).decode("ascii"))
    headers = f"From: {SMTP_EMAIL}\r\nTo: {recipient}\r\nSubject: {subject}\r\n\r\n"
    session.sendmail(SMTP_EMAIL, recipient, headers + content)
    session.quit()


def main():
    '''
    Main function
    '''
    # Setup the key files
    username = SMTP_EMAIL
    if not os.path.exists(TOKEN_FILE):
        print("[-] token.json file not found. Authenticating...")
        authenticate_and_get_token()
        
    access_token = pyioga.get_access_token(TOKEN_FILE)

    # Loop receiving and sending emails
    while True:
        with MailBox(IMAP_SERVER).xoauth2(username, access_token) as mailbox:
            for msg in mailbox.fetch():
                print(
                    f"---- New email received ----\nFrom: {msg.from_}\nSubject: {msg.subject}\n----------------------------"
                )
                if msg.subject == "Hello":
                    send_email(msg.from_, "Re: " + msg.subject, f"Hello {msg.from_}")
                    print(f"Answered to {msg.from_}\n")

                mailbox.delete(msg.uid)
        time.sleep(30)


if __name__ == "__main__":
    main()
