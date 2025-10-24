#!/usr/bin/env python3
import os
import sys
import tarfile
import smtplib
import paramiko
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load configuration from .env (email creds, server creds, etc.)
load_dotenv()

def archive_logs(log_directory):
    if not os.path.isdir(log_directory):
        raise ValueError(f"'{log_directory}' is not a valid directory.")

    archive_dir = os.path.join(os.getcwd(), "archives")
    os.makedirs(archive_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"logs_archive_{timestamp}.tar.gz"
    archive_path = os.path.join(archive_dir, archive_name)

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(log_directory, arcname=os.path.basename(log_directory))

    log_file = os.path.join(archive_dir, "archive_log.txt")
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] Archived {log_directory} -> {archive_path}\n")

    return archive_path, log_file

def send_email_notification(subject, body):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not all([sender, password, receiver]):
        print("⚠️ Email credentials not set. Skipping email notification.")
        return

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("📧 Email notification sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def upload_to_remote_server(local_path):
    host = os.getenv("REMOTE_HOST")
    username = os.getenv("REMOTE_USER")
    password = os.getenv("REMOTE_PASS")
    remote_dir = os.getenv("REMOTE_DIR", "/backups/logs")

    if not all([host, username, password]):
        print("⚠️ Remote upload credentials not set. Skipping upload.")
        return

    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            sftp.chdir(remote_dir)
        except IOError:
            sftp.mkdir(remote_dir)
            sftp.chdir(remote_dir)

        remote_path = os.path.join(remote_dir, os.path.basename(local_path))
        sftp.put(local_path, remote_path)
        sftp.close()
        transport.close()
        print(f"🌐 Archive uploaded successfully to {host}:{remote_path}")
    except Exception as e:
        print(f"❌ Failed to upload to remote server: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: advanced_log_archive <log-directory>")
        sys.exit(1)

    log_dir = sys.argv[1]
    try:
        archive_path, log_file = archive_logs(log_dir)
        message = f"Log archive completed successfully.\n\nArchive: {archive_path}\nLog File: {log_file}"

        send_email_notification("✅ Log Archive Completed", message)
        upload_to_remote_server(archive_path)

        print("✅ Process completed successfully.")
    except Exception as e:
        error_msg = f"Log archive failed: {e}"
        print(f"❌ {error_msg}")
        send_email_notification("❌ Log Archive Failed", error_msg)
