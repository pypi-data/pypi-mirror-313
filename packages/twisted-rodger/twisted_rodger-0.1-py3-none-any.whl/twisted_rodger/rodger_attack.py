import webbrowser
import os

def main():
    image_path = os.path.abspath('image.png')
    if not os.path.isfile(image_path):
        print("Error: image.png not found.")
        return
    file_url = f'file:///{image_path}'
    for _ in range(50):
        webbrowser.open(file_url, new=1)
    print("Opened 50 rodger images. hahaha")
