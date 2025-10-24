# Log-Archive-Tool

Log Archiver — with Email Alerts and Remote Upload

🧠 Overview:

This project is an advanced command-line log archiving tool designed for Unix-based systems (like Linux or macOS). It automatically compresses and archives log files from a specified directory into a .tar.gz file, keeps a local record of archive operations, and optionally emails the user an update or uploads the archive to a remote server or cloud storage.

It’s ideal for system administrators, DevOps engineers, or developers who want to:

Keep /var/log clean,

Store backups securely, and

Get notified about archive activity automatically.

🧩 Key Features

<h3>
Command-line execution — run with log-archive <log-directory> </br>
Automatic compression — creates timestamped .tar.gz archives </br>
Logging — keeps a text log of every archive operation </br>
Email notifications — optionally emails the user a success/failure report </br>
Remote upload — can send the archive to an SFTP server or cloud service </br>
Configuration file support — credentials and settings stored securely in .env </br>
Extensible architecture — easy to add new notification or storage backends </br>
</h3>

