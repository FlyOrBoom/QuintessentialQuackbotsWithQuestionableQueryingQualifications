# Qlassroom

A Discord.py bot that sends Google Classroom posts
straight to your server. This is designed for
students, teachers, and parents who can't or
wouldn't use the Google Classroom feed API.

## Email forwarding setup

You will need:

* A school Google account
* A spare personal Google account

1. I recommmend switching both accounts to use
Gmail's HTML View. It is much faster.
2. In the school account's Gmail settings, go to
the **Forwarding and POP/IMAP** tab.
3. Click **Add a forwarding address**. In the
pop-up window, add your spare Google account.
4. In the spare account, click the link inside
the confirmation email.
5. In the school account's **Forwarding and POP/
SNAP** tab, select **Disable forwarding** and
**Save changes**.
6. In the school account's **Filters** tab,
**Create a new Filter**. The settings are:

|      Name     |          Value        |
|      ---      |           ---         |
| From          | classroom.google.com  |
| Subject       | New                   |
| Has the words | Google Classroom      |
| Doesn't have  | private               |

7. Turn on email notifiations in Google Classroom's settings.

## Bot setup

1. Download Python3
2. `python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
3. Download the repository.
4. Create a `.env` file with `discord_token ='your Discord bot token'`.
5. Download `credentials.json` from **Enable the Gmail API** on [the quickstart page](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the). Place it in the `gmail` directory.
6. `python3 qlassroom.py`

## Configuration

During its first run, Qlassroom creates the file `config.yaml`. You can tweak the settings here even when the bot is live.

|       Name        |        Format      |                         Description                   |
|       ---         |         ---        |                             ---                       |
| channel ids       | list of ids        | List of channels the bot posts in                     |
| email pattern     | regular expression | Pattern to map emails onto embeds                     |
| email query       | Gmail query        | What query to send to Gmail                           |
| refresh interval  | number             | How many seconds between each check of Gmail          |

If you accidentally messed up `config.yaml`, delete the file. Qlassroom will automatically create a new one.
