#!/usr/bin/env python3
import os
import sys
import logging
import time
import smtplib
import base64
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
from imap_tools import MailBox
from dotenv import load_dotenv
import pyioga

load_dotenv()
logging.basicConfig(level=logging.INFO)

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SCOPES = ["https://mail.google.com/"]
USER_EMAIL = os.getenv("USER_EMAIL")
TOKEN_FILE = "./oauth_credentials/token.json"
CREDENTIALS_FILE = "./oauth_credentials/credentials.json"


class CredentialManager:
    """
    Manages the OAuth credentials for the email client.
    """

    def __init__(self, credentials_file: str, token_file: str):
        self.credentials_file = credentials_file
        self.token_file = token_file

    def check_credential_file(self) -> bool:
        """
        Check if the credential file exists.

        :return: True if credential file exists, False otherwise.
        """
        if not os.path.exists(self.credentials_file):
            print("[!] Credential file not found. Exiting...")
            return False
        return True

    def authenticate_and_get_token(self) -> Optional[str]:
        """
        Authenticate and get the token if the token.json file is not found.

        :return: The OAuth token if authentication is successful, None otherwise.
        """
        if not self.check_credential_file():
            sys.exit(1)

        creds = None
        try:
            if os.path.exists(self.token_file):
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    with open(self.token_file, "w", encoding='utf-8') as token:
                        token.write(creds.to_json())
        except RefreshError as e:
            logging.error("RefreshError: %s. Re-authenticating.", e)
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(self.token_file, "w", encoding='utf-8') as token:
                token.write(creds.to_json())

        return creds.token if creds else None


class EmailClient:
    """
    Handles email sending operations.
    """

    def __init__(self, smtp_server: str, smtp_port: int, email_address: str, credential_manager: CredentialManager):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.credential_manager = credential_manager

    def send_email(self, recipient: str, subject: str, content: str) -> bool:
        """
        Send an email to the specified recipient.

        :param recipient: Email address of the recipient.
        :param subject: Subject of the email.
        :param content: Content of the email.
        :return: True if email is sent successfully, False otherwise.
        """
        token = self.credential_manager.authenticate_and_get_token()
        if not token:
            logging.error("Failed to obtain a valid token. Email not sent.")
            return False

        try:
            session = smtplib.SMTP(self.smtp_server, self.smtp_port)
            session.starttls()
            auth_string = (
                b"user="
                + bytes(self.email_address, "ascii")
                + b"\1auth=Bearer "
                + token.encode()
                + b"\1\1"
            )
            session.docmd("AUTH", "XOAUTH2 " + (base64.b64encode(auth_string)).decode("ascii"))
            headers = f"From: {self.email_address}\r\nTo: {recipient}\r\nSubject: {subject}\r\n\r\n"
            session.sendmail(self.email_address, recipient, headers + content)
            session.quit()
            return True
        except Exception as e:
            logging.error("Failed to send email: %s", e)
            return False


class EmailProcessor:
    """
    Processes incoming emails.
    """

    def __init__(self, imap_server: str, email_address: str, credential_manager: CredentialManager):
        self.imap_server = imap_server
        self.email_address = email_address
        self.credential_manager = credential_manager

    def process_emails(self, email_client: EmailClient):
        """
        Process and respond to incoming emails.

        :param email_client: An instance of EmailClient to send responses.
        """
        while True:
            access_token = pyioga.get_access_token(TOKEN_FILE)
            with MailBox(self.imap_server).xoauth2(self.email_address, access_token) as mailbox:
                for msg in mailbox.fetch():
                    print(f"---- New email received ----\nFrom: {msg.from_}\nSubject: {msg.subject}\n----------------------------")
                    if msg.subject == "Hello":
                        email_client.send_email(msg.from_, "Re: " + msg.subject, f"Hello {msg.from_}")
                        print(f"Answered to {msg.from_}\n")

                    mailbox.delete(msg.uid)
            time.sleep(30)


def main():
    """
    Main function to initialize and run the email processing system.
    """
    credential_manager = CredentialManager(CREDENTIALS_FILE, TOKEN_FILE)
    email_client = EmailClient(SMTP_SERVER, SMTP_PORT, USER_EMAIL, credential_manager)
    email_processor = EmailProcessor(IMAP_SERVER, USER_EMAIL, credential_manager)

    if not os.path.exists(TOKEN_FILE):
        print("[-] token.json file not found. Authenticating...")
        credential_manager.authenticate_and_get_token()

    email_processor.process_emails(email_client)


if __name__ == "__main__":
    main()
