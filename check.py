import dns.resolver
import re
import sys
import smtplib
import threading

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']                     
lock = threading.Lock()
                                                                            def read_emails(filename):
    try:
        file = open(filename, 'r')
        emails = [line.strip() for line in file]
        file.close()
        return emails
    except FileNotFoundError:
        print(f"File '{filename}' not found.")                                      return []

def write_to_file(filename, email):
    with lock:
        file = open(filename, 'a')
        file.write(email + "\n")
        file.close()

def check_email(email):
    # Validate email syntax
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        print("Invalid email format")
        write_to_file("invalid.txt", email)
        return

    # Extract domain
    domain = email.split('@')[1]

    try:
        # Perform DNS lookup
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_records = [mx.to_text().split()[1] for mx in mx_records]

        # Check MX records
        if mx_records:
            # Check SMTP connectivity
            for mx in mx_records:
                try:
                    server = smtplib.SMTP(mx, 25, timeout=5)
                    server.helo()
                    server.mail('pogininjas@gmail.com')
                    response = server.rcpt(email)
                    server.quit()

                    if response[0] == 250:
                        print(f"\033[92m{email} is deliverable\033[0m")
                        write_to_file("valid.txt", email)
                        return
                    else:
                        print(f"\033[91m{email} is not deliverable\033[0m")
                        write_to_file("invalid.txt", email)
                        return
                except smtplib.SMTPException as e:
                    print(f"SMTP error: {e}")
        else:
            print("No MX records found. Checking A records...")
            a_records = dns.resolver.resolve(domain, 'A')
            a_records = [a.to_text() for a in a_records]
            if a_records:
                print("A records found:")
                for a in a_records:
                    print(a)
            else:
                print("No A records found")
    except dns.resolver.NoAnswer:
        print("No MX or A records found")

    write_to_file("invalid.txt", email)

# Test the function
if __name__ == "__main__":
    print("email validator")
    emails = read_emails("emails.txt")
    threads = []

    def thread_func(email):
        check_email(email)

    for email in emails:
        thread = threading.Thread(target=thread_func, args=(email,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
