from ftplib import FTP
import csv
from io import StringIO

# Данные для подключения к FTP
FTP_HOST = "ftp.example.com"
FTP_USER = "username"
FTP_PASS = "password"
FTP_FILE_PATH = "/path/to/your/file.csv"

# Подключение к FTP
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

# Загрузка файла в память
file_data = StringIO()
ftp.retrlines(f"RETR {FTP_FILE_PATH}", file_data.write)

# Закрытие соединения
ftp.quit()

# Обработка CSV-файла
file_data.seek(0)  # Перемещаем указатель в начало файла
reader = csv.DictReader(file_data)

for row in reader:
    print(row)  # Здесь можно сохранять данные в базу данных