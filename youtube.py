import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog


def download_video(url, save_path):
    try:
        # Expansion du chemin avec tilde (~)
        save_path = os.path.expanduser(save_path)
        
        # Options pour yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        print(f"Tentative de téléchargement de: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Vidéo téléchargée avec succès vers {save_path}")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
        print(f"Type d'erreur: {type(e).__name__}")

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    url = input("Entrez l'URL de la vidéo YouTube: ")
    save_path = open_file_dialog()
    if not save_path:
        print("Aucun dossier sélectionné. Le téléchargement a été annulé.")
        exit()
        
    download_video(url, save_path)
