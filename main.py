from pathlib import Path
import random
import time
import smtplib
import ssl
import traceback
from email.message import EmailMessage
from email.utils import formataddr, make_msgid, formatdate
from datetime import datetime

# ===== FILES =====
EMAILS_FILE = Path("emails.txt")         # list of emails, one per line
SENT_FILE = Path("emails_sent.txt")      # who has already received the email

# ===== SMTP SETTINGS FOR GODADDY PROFESSIONAL EMAIL =====
SMTP_SERVER   = "smtpout.secureserver.net"
SMTP_PORT     = 465  # SSL

# >>> BE SURE TO REPLACE WITH YOUR EMAIL AND PASSWORD <<<
SMTP_LOGIN    = "info@yourdomain.com"   # example: info@yourdomain.com
SMTP_PASSWORD = "pass"      # password for this mailbox
FROM_EMAIL    = "info@yourdomain.com"   # same address as SMTP_LOGIN
FROM_NAME     = "name"

# ===== DKIM (optional) =====
# If DKIM is already handled by GoDaddy via their SMTP, leave as None
DKIM_SELECTOR = None  # e.g.: 'default' — set the selector if you want signing from the script
DKIM_DOMAIN = None    # e.g.: 'yourdomain.com'
DKIM_PRIVATE_KEY = Path("dkim_private.key")

try:
    import dkim
except Exception:
    dkim = None

# ===== RATE LIMITS / TIMING =====
# Maximum emails per run
MAX_PER_RUN = 400
# Base pause in seconds (4 minutes)
SLEEP_BASE = 180.0
# Variation +/- in seconds
SLEEP_VARIANCE = 50.0

# ===== RANDOM CONTENT =====
INSTAGRAM_HANDLE = "instagram_handle"
YOUR_NAME = "name"

SUBJECT       = "TOPICS"

# Subject options (randomly selected when sending)
SUBJECTS = [
    "Example 1",
    "Example 2",
    "Example 3"
]



greetings = [
    "Example 1",
    "Example 2",
    "Example 3",
    
]

thanks_openers = [
    "Example 1",
    "Example 2",
    "Example 3",
]

about_me_blocks = [
    "Example 1",
    "Example 2",
    "Example 3",
]

demos_invite_blocks = [
    "Example 1",
    "Example 2",
    "Example 3",
]

contact_blocks = [
    f"Example 1 {INSTAGRAM_HANDLE}",
    f"Example 2 {INSTAGRAM_HANDLE}",
    f"Example 3 {INSTAGRAM_HANDLE}",
]


creative_stay_in_touch_blocks = [
    "Example 1",
    "Example 2",
    "Example 3",
]


closings = [
    "Example 1",
    "Example 2",
    "Example 3",
]

signature_blocks = [
    f"{YOUR_NAME}\n NAME \n",
]

def make_message(_name=None) -> str:
    greeting = random.choice(greetings)
    # combine opening, about and demos into one paragraph
    paragraph = " ".join([
        random.choice(thanks_openers),
        random.choice(about_me_blocks),
        random.choice(demos_invite_blocks),
    ])
    contact = random.choice(contact_blocks)
    creative = random.choice(creative_stay_in_touch_blocks)
    closing = random.choice(closings)
    signature = random.choice(signature_blocks)

    body = (
        f"{greeting},\n\n"
        f"{paragraph}\n\n"
        f"{contact}\n"
        f"{creative}\n\n"
        f"{closing}\n"
        f"{signature}"
    )
    return body

    # ===== LIST AND SENT RECORDS =====

def load_sent():
    if not SENT_FILE.exists():
        return set()
    with SENT_FILE.open("r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}

def append_sent(email: str):
    with SENT_FILE.open("a", encoding="utf-8") as f:
        f.write(email + "\n")

def load_emails():
    if not EMAILS_FILE.exists():
        print(f"Файл {EMAILS_FILE} не найден")
        return []
    with EMAILS_FILE.open("r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]
    # Simple filtering
    emails = [e for e in emails if "@" in e and "." in e]
    return emails