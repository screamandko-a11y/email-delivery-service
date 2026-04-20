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

