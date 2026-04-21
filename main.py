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

    # ===== SENDING EMAIL =====

def send_email(to_email: str, body_text: str):
    msg = EmailMessage()
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = to_email
    # Choose a random subject from the list and remove trailing question mark (if any)
    subj = random.choice(SUBJECTS)
    if subj.strip().endswith('?'):
        subj = subj.rstrip('?').strip()
    msg["Subject"] = subj
    # Reply/Reply-To header
    msg["Reply-To"] = FROM_EMAIL
    # For mailings: clear unsubscribe link (helps deliverability)
    msg["List-Unsubscribe"] = f"<mailto:{FROM_EMAIL}>"
    # Add Date and Message-ID
    msg["Date"] = formatdate(localtime=True)
    try:
        msg["Message-ID"] = make_msgid(domain=FROM_EMAIL.split("@", 1)[1])
    except Exception:
        msg["Message-ID"] = make_msgid()

    plain = body_text
    html = body_text.replace("\n", "<br>")

    # Set explicit quoted-printable encoding for text parts
    msg.set_content(plain, subtype="plain", charset="utf-8", cte="quoted-printable")
    msg.add_alternative(html, subtype="html", charset="utf-8", cte="quoted-printable")

     # SSL connection (port 465)
    context = ssl.create_default_context()
    local_hostname = FROM_EMAIL.split("@", 1)[1]
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, local_hostname=local_hostname) as server:
        # EHLO/HELO will contain your domain — improves trust
        server.login(SMTP_LOGIN, SMTP_PASSWORD)

        sent_ok = False
        # If DKIM is configured and dkimpy is available, sign the message
        if dkim and DKIM_SELECTOR and DKIM_DOMAIN and DKIM_PRIVATE_KEY.exists():
            unsigned = msg.as_bytes(policy=msg.policy.clone(max_line_length=998))
            priv = DKIM_PRIVATE_KEY.read_bytes()
            try:
                signature = dkim.sign(unsigned, DKIM_SELECTOR.encode(), DKIM_DOMAIN.encode(), priv,
                                      include_headers=[b"From", b"To", b"Subject", b"Date", b"Message-ID"])
                # dkim.sign returns the DKIM-Signature header (bytes). Prepend the signature to the original and send raw bytes
                signed_message = signature + unsigned
                server.sendmail(FROM_EMAIL, [to_email], signed_message)
                sent_ok = True
            except Exception:
                # If signing fails — log and send without signature
                traceback.print_exc()

        else:
            # Send the usual way
            server.send_message(msg, from_addr=FROM_EMAIL, to_addrs=[to_email])
            sent_ok = True

        # If the email was sent — save a copy to a separate file
        if sent_ok:
            try:
                copies_dir = Path("sent_copies")
                copies_dir.mkdir(exist_ok=True)
                ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
                safe_to = to_email.replace('@', '_at_').replace('.', '_')
                filename = copies_dir / f"{ts}_{safe_to}.txt"
                with filename.open('w', encoding='utf-8') as f:
                    f.write(f"To: {to_email}\n")
                    f.write(f"From: {FROM_EMAIL}\n")
                    f.write(f"Subject: {msg.get('Subject')}\n")
                    f.write(f"Date: {msg.get('Date')}\n")
                    f.write(f"Message-ID: {msg.get('Message-ID')}\n\n")
                    f.write("--- Plain text ---\n")
                    f.write(plain + "\n\n")
                    f.write("--- HTML ---\n")
                    f.write(html + "\n")
            except Exception:
                traceback.print_exc()
# ===== MAIN LOOP =====

def main():
    emails_all = load_emails()
    if not emails_all:
        print("There are no valid emails in the file — nothing to send")
        return

    sent = load_sent()
    to_send = [e for e in emails_all if e not in sent]

    if not to_send:
        print("There is no one to send emails to — all emails are already in emails_sent.txt")
        return

    # Limit per run
    if len(to_send) > MAX_PER_RUN:
        print(f"Warning: {len(to_send)} addresses to send — limiting to {MAX_PER_RUN} per run")
        to_send = to_send[:MAX_PER_RUN]

    print(f"Total addresses: {len(emails_all)}; to send in this run: {len(to_send)}")

    for i, email in enumerate(to_send, start=1):
        print(f"[{i}/{len(to_send)}] Sending -> {email}")
        sent_success = False

        try:
            message_text = make_message()
            send_email(email, message_text)
            print("  successfully sent")
            append_sent(email)
            sent_success = True

        except Exception:
            print("  Error while sending:")
            traceback.print_exc()

        if not sent_success:
            print("  sending failed, we proceed to the next one without waiting.")
            continue

        # pause SLEEP_BASE ± SLEEP_VARIANCE
        offset = random.uniform(-SLEEP_VARIANCE, SLEEP_VARIANCE)
        sleep_seconds = max(1.0, SLEEP_BASE + offset)
        print(f"  waiting {int(sleep_seconds)} sec. (≈{int(SLEEP_BASE/60)} min ±{int(SLEEP_VARIANCE)} sec)")
        time.sleep(sleep_seconds)

    print("All available emails have been processed.")

if __name__ == "__main__":
    main()