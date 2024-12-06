# twisted_rodger/rodger.py
import webbrowser
import os

def rodger():
    """Prints the 'rodger' message."""
    print("i like distracting twisted rodger")

def rodger_attack():
    """Opens 50 browser windows displaying 'image.png'."""
    image_path = os.path.abspath('image.png')
    
    if not os.path.isfile(image_path):
        print("Error: image.png not found.")
        return

    file_url = f'file:///{image_path}'

    # Open 50 browser windows with the image
    for _ in range(50):
        webbrowser.open(file_url, new=1)

    print("Opened 50 browser windows with image.png.")

def shrimp(value1, value2):
	image_path = os.path.abspath('wasted.png')
	mape = os.path.abspath('Twisted_Poppy_chasing_Boxten.png')
	file_url = f'file:///{image_path}'
	boxten-x-poppy-img = f'file:///{mape}'
	if value1 = "goob" and value2 = "methamorphine":
		for _ in range(50):
			webbrowser.open(file_url, new=1)
	else:
		webbrowser.open(boxten-x-poppy-img, new=1)

def hate(sth):
	messagebox.showerror("IHATE Panel", "I HATE {sth}")
