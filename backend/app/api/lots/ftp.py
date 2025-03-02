from ftplib import FTP
import csv
from io import StringIO

FTP_HOST = "ftp.example.com"
FTP_USER = "username"
FTP_PASS = "password"
FTP_FILE_PATH = "/path/to/your/file.csv"

ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

file_data = StringIO()
ftp.retrlines(f"RETR {FTP_FILE_PATH}", file_data.write)

ftp.quit()

file_data.seek(0)
reader = csv.DictReader(file_data)

for row in reader:
    print(row)