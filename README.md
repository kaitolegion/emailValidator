# Overview
This email validator is written by python3 made with full of <3 purpose is to checks the validity of the existing email addresses by performing DNS lookups and SMTP connectivity tests. It uses multi-threading to speed up the validation process.

# Main Components
Email Reader: The code reads a list of email addresses from a file named ```"emails.txt"```.

DNS lookup to check for MX records.
SMTP connectivity test to check if the email address is deliverable.

File Saved: valid email addresses to two separate files: ```"valid.txt"``` and ```"invalid.txt"```.

Multi-Threading: The code uses multi-threading to speed up the validation process. Each email address is validated in a separate thread.

# Usage

Command following:
```bash
git clone https://github.com/kaitolegion/emailValidator
cd emailValidator
python3 -m pip install dnspython
python3 check.py
```
