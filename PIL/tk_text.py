from PIL import ImageTk, Image, ImageEnhance
import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import os
import pytesseract
import pyperclip
import urllib.request

bg = 'orange' ; fg = "#4f4646" ; button_bg = "#ffb303" ; abg = '#806b71'
afg = '#3b2e70' ; fnt = 'gisha' ; fnt_size = '12'
hi = '1' #buttons height;
wid = '21' #buttons width

def image_mani01(filename):
    PIL.Image.open(filename).convert('RGB').save(r"image01.jpg")
    img = PIL.Image.open("image01.jpg")
    width, height = img.size
    #resize do not help here so it is the same hight and width no multiply - width*2 for example
    newsize = (width*2, height*2)
    rezised_img = img.resize(newsize)
    lst=[]
    img_bw = rezised_img.convert("L")
    im1 = img_bw.save(r"bw.png")

def image_mani02(filename):
    PIL.Image.open(filename).convert('RGB').save(r"image01.jpg")
    img = PIL.Image.open("image01.jpg")
    img_data = img.getdata()

    lst=[]
    for i in img_data:
        lst.append(i[0]*0.7+i[1]*1.8+i[2]*0.2)
        #lst.append(i[0]*0.299+i[1]*0.587+i[2]*0.114) ### Rec. 609-7 weights
        #lst.append(i[0]*0.2125+i[1]*0.7174+i[2]*0.0721) ### Rec. 709-6 weights

    new_img = PIL.Image.new("L", img.size)
    new_img.putdata(lst)

    im1 = new_img.save(r"bw.png")

def image_to_text(filename, choice):
    if choice == 1:
        image_mani01(filename)
    else:
        image_mani02(filename)
    custom_config = r'-l eng --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    global text01
    text01 = (pytesseract.image_to_string(r"bw.png", config=custom_config))
    print_text(text01)
    pyperclip.copy(text01)

def heb_text(filename, choice):
    if choice == 1:
        image_mani01(filename)
    else:
        image_mani02(filename)
    custom_config = r'-l eng+heb --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    global text01
    text01 = (pytesseract.image_to_string(r"bw.png", config=custom_config))
    print_text(text01)
    pyperclip.copy(text01)

def select_file():
    global filename
    filename = fd.askopenfilename()
    showImage(image_resize(filename), "left_frame")


def clear_frame():
    for widgets in left_frame.winfo_children():
        widgets.destroy()


def showImage(filename, where="left_frame"):
    clear_frame()
    img = ImageTk.PhotoImage(PIL.Image.open(image_resize(filename)))
    if where == "left_frame":
        label = Label(left_frame, image = img)
    else:
        pass
    label.image = img
    label.grid(row = 0, column = 0)

def rotate_img(filename):
    image_mani01(filename)

    img = PIL.Image.open("bw.png")
    angle = (rotate_e.get())
    rot = img.rotate(int(angle))
    rot.save(r"r.jpg")
#    rot.show()
    showImage("r.jpg")

def image_url():
    img_url  = url_e.get()
    print(img_url)
    with urllib.request.urlopen(img_url) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
    img = PIL.Image.open('temp.jpg')
    showImage('temp.jpg')


def print_text(text01):
    text_widget = Text(right_frame)
    text_widget.insert( "1.0", text01)
    text_widget.grid(row = 0, column = 0)

def image_resize(filename):
    basewidth = 250
    img = PIL.Image.open(filename)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), resample=PIL.Image.BICUBIC)
    img.save('resized_image.png')
    return 'resized_image.png'

def save_text():
    with open("text.txt", "w", encoding='utf8') as f:
        f.write(text01)

def on_closing():
    try:
        os.remove("bw.png")
        os.remove("resized_image.png")
        os.remove("image01.jpg")
        root.destroy()
        print ("See you soon!")
    except:
        print ("See you soon!")
        root.destroy()

filename = "text03.png"


root = Tk()
root.configure(bg="orange")
root.title("Remove Image Background")
top_frame = Frame(root)
top_frame.grid(row = 2, column = 0, columnspan = 4)
top_frame.configure(bg = bg)

mani_frame = Frame(root)
mani_frame.grid(row = 1, column = 0, columnspan = 4)
mani_frame.configure(bg = bg)

left_frame = Frame(root)
left_frame.grid(row = 0, column = 0, padx = "3", pady = "3")
img = ImageTk.PhotoImage(PIL.Image.open(before_img))
label = Label(left_frame, image = img)
label.image = img
label.grid(row = 0, column = 0, padx = "3", pady = "3")

right_frame = Frame(root)
right_frame.grid(row = 0, column = 1, padx = "3", pady = "3")

label.grid(row = 0, column = 0, padx = "3", pady = "3")


open_button = Button(top_frame,text='Open Image', font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=select_file)
open_button.grid(row = 1, column = 0, padx = "3", pady = "5")

rm_bg_button = Button(top_frame, text='Image to Text',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=lambda:image_to_text(filename, 1))
rm_bg_button.grid(row = 1, column = 1, padx = "3", pady = "5")

try_this_button = Button(top_frame, text='Try This',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=lambda:image_to_text(filename, 2))
try_this_button.grid(row = 1, column = 2, padx = "3", pady = "5")

heb_text_button = Button(top_frame, text='Hebrew Text?',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=lambda:heb_text(filename, 1))
heb_text_button.grid(row = 1, column = 3, padx = "3", pady = "5")

rotate_l = Label(mani_frame, text = "Rotate by %:", font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg)
rotate_l.grid(row = 0, column = 0,  padx = "3", pady = "5")

rotate_e = Entry(mani_frame, width = "10", font=(fnt,fnt_size), fg=fg, bg=button_bg)
rotate_e.grid(row = 0, column = 1, padx = "3", pady = "5")

rotate_b = Button(mani_frame, text = "Rotate", font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda: rotate_img(filename))
rotate_b.grid(row = 0, column = 2, padx = "3", pady = "5")

url_l= Label(mani_frame, text = "Enter Image URL",  font=(fnt,fnt_size), fg=fg, bg=button_bg)
url_l.grid(row = 0, column = 3,  padx = "3", pady = "5")

url_e = Entry(mani_frame, width = "25",  font=(fnt,fnt_size), fg=fg, bg=button_bg)
url_e.grid(row = 0, column = 4,  padx = "3", pady = "5")

url_b = Button(mani_frame, width = "10", text = "get image", font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, command=lambda: image_url())
url_b.grid(row = 0, column = 5,  padx = "3", pady = "5")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
