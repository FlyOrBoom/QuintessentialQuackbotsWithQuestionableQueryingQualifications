# Classroom

A Discord.py bot that sends Google Classroom posts
straight to your server. This is designed for
students, teachers, and parents who can't or
wouldn't use the Google Classroom feed API.

## Setup

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

Name | Value
| --- | --- |
From          | classroom.google.com
Subject       | New
Has the words | Google Classroom
Doesn't have  | private

7. Download the repository.
8. Run `py qlassroom.py`

### .env
* TOKEN: Discord bot token
* CHANNEL\_IDs: comma-separated string of channel ids
