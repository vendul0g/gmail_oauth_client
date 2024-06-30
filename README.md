# Gmail OAuth Client for IMAP and SMTP

This repository provides a comprehensive guide and tools for setting up OAuth2 authentication for both IMAP and SMTP connections with Gmail, using Python. Whether you need to send emails via SMTP or read emails via IMAP in your automated end-to-end tests or scripts, this project has got you covered. It's built upon Google's authentication libraries and further simplifies the process with an additional layer, making it easy to integrate Gmail OAuth2 authentication into your projects.

## About The Project

The project is divided into two main parts: one for SMTP Email sending using Google Gmail OAuth2, and another for setting up Google OAuth2 authentication for IMAP connections with Gmail. It is ideal for those looking to integrate Gmail's sending and receiving email functionalities securely in their Python applications.

## Getting Started

### Google Gmail API Setup:

To use OAuth2 for Gmail SMTP and IMAP, follow these initial setup steps:

1. **Google Cloud Platform Account:** A Google Cloud Platform account is required.
2. **Enable the Gmail API:** Go to the [Enabled APIs and services](https://console.cloud.google.com/apis/dashboard) page and enable the Gmail API.
3. **Configure OAuth Consent Screen** (left panel): Add the scope 'https://mail.google.com/' to match the SCOPES used in the Python code. Also add your email as Test users.
4. **Create OAuth 2.0 Client ID:** Navigate to [Credentials](https://console.cloud.google.com/apis/credentials), click "+ Create Credentials", and select "OAuth Client ID".
5. **Download Credentials:** Download the client secret file and rename it to `credentials.json` in the project directory.


## Usage

### Installing
I recommend use python environments to manage the package installation to use the project

So install `pipenv` with:
```
pip install pipenv
```

> If the above command does not work, try installing directly with apt:
> ```
> sudo apt install pipenv
> ```

Now install in the project folder the `requirements.txt` with `pipenv`:
```
pipenv install
```

Now launch the environment shell to execute the python script
```
pipenv shell
```

> Note that it will appear the name of the project between `()` in your prompt, that means the environment is correctly working.

### Setup and run

1. Create a folder named `oauth_credentials`
2. Download the `credentials.json` file from the *Google Cloud Console* and save it into the `oauth_credentials` folder.
3. Create a file `.env` where you have to initialize the envar `USER_EMAIL` with you own email
```
#.env file
USER_EMAIL="mymail@email.com"
```
4. Run the script
```
python gmail_oauth_client.py
```

## Modifying the behavior
If you read the [code](./gmail_oauth_client.py), easily you will get what is doing and how to modify the behavior of the program. Adapt it to your requirements.


## SMTP and IMAP usage

### SMTP Email Sending

Refer to the SMTP setup part for sending emails using Gmail with OAuth2 authentication, in the [python script](./gmail_oauth_client.py).

### IMAP Email Reading

Once you have the token file, you can authenticate IMAP connections to read emails from Gmail using functions provided by Pyioga.

```python
import pyioga
from imap_tools import MailBox, AND

username = "user@gmail.com"
access_token = pyioga.get_access_token("token.json")
with MailBox('imap.gmail.com').xoauth2(username, access_token) as mailbox:
    for msg in mailbox.fetch():
        print(msg.date, msg.subject, len(msg.text or msg.html))
```

`pyioga.get_access_token` ensures you receive a valid token, raising an exception otherwise.

## Conclusion

This repository offers a streamlined approach to integrating Gmail OAuth2 authentication for both sending and receiving emails in your Python projects. By following the outlined steps, you can securely set up SMTP and IMAP functionalities with Gmail.

Remember to keep your credentials secure and follow best practices for managing OAuth tokens and application secrets.

## Bibliography
- [IMAP OAuth](https://github.com/mbroton/pyioga/blob/main/README.md)
- [SMTP OAuth](https://github.com/zamyen/smtp_oauth_python_gmail/blob/main/main.py)
