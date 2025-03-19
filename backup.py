import os
import shutil
import datetime
import schedule
import time

source_dir = "/home/cecile/Images/Screenshots"
destination_dir = "/home/cecile/Bureau/Backups"

def copy_folder_to_directory(source, dest):
    today = datetime.date.today().strftime("%Y-%m-%d")
    dest_dir = os.path.join(dest, str(today))
    print(f"Copie du dossier vers {dest_dir}")

    try:
        shutil.copytree(source, dest_dir)
    except FileExistsError as e:
        print(f"Erreur lors de la copie du dossier: {e}")

schedule.every().day.at("6:00").do(lambda: copy_folder_to_directory(source_dir, destination_dir))

while True:
    schedule.run_pending()
    time.sleep(60)