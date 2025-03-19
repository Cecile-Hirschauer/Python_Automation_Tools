import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Ajout du répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..youtube import download_video

@pytest.fixture
def mock_yt_dlp():
    with patch('youtube.yt_dlp.YoutubeDL') as mock_ytdl:
        yield mock_ytdl

@pytest.fixture
def mock_file_dialog():
    with patch('youtube.filedialog') as mock_dialog:
        mock_dialog.askdirectory.return_value = "/chemin/test"
        yield mock_dialog

def test_download_video_success(mock_yt_dlp, tmp_path):
    # Configuration du test
    url = "https://www.youtube.com/watch?v=test123"
    
    # Exécution de la fonction
    download_video(url, str(tmp_path))
    
    # Vérifications
    mock_yt_dlp.assert_called_once()
    mock_yt_dlp.return_value.__enter__.return_value.download.assert_called_once_with([url])

def test_download_video_error(mock_yt_dlp, capfd):
    # Configuration pour simuler une erreur
    mock_yt_dlp.return_value.__enter__.return_value.download.side_effect = Exception("Erreur test")
    
    # Exécution
    download_video("https://www.youtube.com/invalid", "/chemin/invalide")
    
    # Capture et vérification de la sortie
    captured = capfd.readouterr()
    assert "Une erreur s'est produite: Erreur test" in captured.out
    assert "Type d'erreur: Exception" in captured.out

def test_download_video_with_tilde_expansion():
    with patch('youtube.yt_dlp.YoutubeDL') as mock_ytdl, \
         patch('youtube.os.path.expanduser') as mock_expanduser:
        
        # Configuration
        mock_expanduser.return_value = "/home/user/downloads"
        url = "https://www.youtube.com/watch?v=test123"
        
        # Exécution
        download_video(url, "~/downloads")
        
        # Vérifications
        mock_expanduser.assert_called_once_with("~/downloads")
        mock_ytdl.assert_called_once()

def test_download_video_options():
    with patch('youtube.yt_dlp.YoutubeDL') as mock_ytdl:
        url = "https://www.youtube.com/watch?v=test123"
        save_path = "/chemin/test"
        
        download_video(url, save_path)
        
        # Vérification des options passées à YoutubeDL
        expected_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        mock_ytdl.assert_called_once_with(expected_opts)
