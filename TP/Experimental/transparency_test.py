#from https://stackoverflow.com/questions/54637795/how-to-make-a-tkinter-canvas-rectangle-transparent

from tkinter import *
from PIL import Image, ImageTk

mroot = Tk()
images = []  # to hold the newly created image, clear every frame

def create_rectangle(root, canvas, x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = mroot.winfo_rgb(fill) + (alpha,)
        print(fill)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        mcanvas.create_image(x1, y1, image=images[-1], anchor='nw')
    mcanvas.create_rectangle(x1, y1, x2, y2, **kwargs)

mcanvas = Canvas(width=300, height=200)
mcanvas.pack()

# create_rectangle(50, 50, 250, 150, fill='green', alpha=.5)
# create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)

# print(len(images))

create_rectangle(mroot, mcanvas, 10, 10, 200, 100, fill='blue')

mroot.mainloop()
