    Запрос выполнен


This Python script is a robust, automated tool for managing and sending cold emails or newsletters via SMTP. It features built-in anti-spam measures, random content generation to ensure variety, and tracking to prevent sending duplicate emails. Key Features

    Anti-Spam Delays: Uses a configurable base sleep time (SLEEP_BASE) with random variance (SLEEP_VARIANCE) to mimic human behavior and avoid triggering spam filters.
    Duplicate Prevention: Automatically tracks sent emails in emails_sent.txt and skips them in future runs.
    Smart Rate Limiting: Processes a maximum number of emails per execution (MAX_PER_RUN) to keep your mail server reputation safe.
    Dynamic Content: Randomly assembles email bodies from multiple templates (greetings, about me, contact blocks, etc.) so each recipient receives a slightly different message.

    Deliverability Optimization: * Adds List-Unsubscribe headers.
        Generates unique Message-ID and Date headers.
        Supports DKIM signing (if dkimpy is installed).
        Sends both Plain Text and HTML versions of the message.
    Auto-Logging: Saves a copy of every successfully sent email into the sent_copies/ folder for your records.
Setup & Configuration
1. Requirements

Ensure you have Python installed. If you want to use DKIM signing, install the optional dependency:
Bash

pip install dkimpy

2. File Preparation

    emails.txt: Create this file in the same directory. Add your recipient email addresses, one per line.
    dkim_private.key: (Optional) If you are using DKIM, place your private key file here.

3. SMTP Configuration
Open main.py and update the following variables:

    SMTP_LOGIN: Email (e.g., GoDaddy/Professional Email).
    SMTP_PASSWORD: password.
    FROM_NAME: Sender name.
    MAX_PER_RUN: How many emails to send in one go (default 400).

 How it Works
    Loading: The script reads emails.txt and filters out invalid addresses.

    Filtering: It compares the list against emails_sent.txt to find only "new" recipients.
    Generation: For each recipient, it randomly picks parts of the message (Subject, Greeting, Body, Closing) to create a unique email.
    Sending: It connects via SSL (Port 465) and sends the email.
    Recording: Upon success, it adds the email to the "sent" list and saves a local text copy of the sent message.
    Cooldown: It waits for a randomized period (e.g., ~3-4 minutes) before moving to the next address.

⚠️ Important Note

This script is designed for GoDaddy Professional Email and similar SMTP services. Always ensure you are following your provider's Terms of Service regarding mass mailing to avoid account suspension. 
Project Structure

    main.py — The core script.
    emails.txt — Your target list.
    emails_sent.txt — Database of processed emails (auto-generated).
    sent_copies/ — Archive of sent messages (auto-generated).
