import gdown
import os

def download_similarity_file():
    """Download similarity.pkl from Google Drive"""
    file_id = "YOUR_GOOGLE_DRIVE_FILE_ID"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "similarity.pkl"
    
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
        print("File downloaded successfully!")
    else:
        print("File already exists!")

if __name__ == "__main__":
    download_similarity_file()