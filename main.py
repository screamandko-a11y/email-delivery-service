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
