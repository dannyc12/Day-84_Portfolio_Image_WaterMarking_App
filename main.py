import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox

import PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# ------------ CONSTANTS ----------- #
WHITE = '#E8E2DB'
PEACH = '#FAB95B'
RED = '#F5564E'
BLUE = '#1A3263'


# ---- Create File Browser ------- #
def browse_files():
    global current_file
    file = filedialog.askopenfile(initialdir='/',
                                  title='Select a file',
                                  filetypes=(('Image Files',
                                              ['*.jpg*', '*.png*']),
                                             ('All files',
                                             '*.*'))
                                  )
    if file:
        # print(f"File {file.name} selected successfully")
        file_name = file.name
        load_preview(file_name)
        current_file = file_name

        # entry box for watermark text

        entry_label.config(text=f"Create your text watermark for:\n{current_file}")
        watermark_entry.config(state=NORMAL)
        create_wm_button.config(state=NORMAL)


# ---- load image from file ------ #
def load_preview(image):
    global img
    try:
        with Image.open(image) as img:
            img = img.resize((300, 300))  # resize method takes a tuple of ints
            img = ImageTk.PhotoImage(img)  # turns this into an image that tkinter can work with
            preview_label.config(image=img)
    except PIL.UnidentifiedImageError:
        messagebox.showerror('File error',
                             'Cannot identify image file. Please select another file'
                             )


# ------- Create Text Watermark from Entry ------ #
def create_watermark():
    text = str(watermark_entry.get())
    # print(f'This is your text: {text}')
    if text:
        add_watermark(current_file, text)
        # load_preview(img_to_mark)
        messagebox.showinfo('Save Successful', 'Successfully saved new image file.')
    else:
        messagebox.showinfo('Watermark Error', 'Please enter text to create a watermark.')
        # print('Please enter text')


def add_watermark(image, wm_text):
    with Image.open(image) as img_to_mark:
        img_width, img_height = img_to_mark.size
        draw = ImageDraw.Draw(img_to_mark)
        font_size = int(img_width / (len(wm_text)/2))  # use len of the wm_text to keep font size dynamic
        wm_font = ImageFont.truetype('arial.ttf', font_size)
        # coordinates for where the watermark should go
        x, y = int(img_width/2), int(img_height/2)
        draw.text((x, y), wm_text, font=wm_font, fill='#FFF', stroke_width=5, stroke_fill='#222', anchor='ms')
        # the below line converts from RGBA (A is alpha or transparency), which allows you to watermark over an
        # image that has already been watermarked (original watermark uses alpha transparency)
        img_jpg = img_to_mark.convert(mode='RGB')
        file_name = filedialog.asksaveasfile(
            filetypes=[('image file', ['*.jpg', '*.png*'])],
            defaultextension='.jpg'
        )
        file_name = file_name.name
        fn, fext = os.path.splitext(file_name)
        if fext == '.jpg' or fext == '.png':
            img_jpg.save(file_name)
        else:
            messagebox.showerror('Save Error', 'Please specify valid file extension (ie ".jpg" or ".png")')

# ------------ UI Setup ------------ #
window = Tk()
window.title('Image Watermarking')
window.config(padx=50, pady=25, bg=BLUE)
# window.geometry("1000x700")
window.geometry('+%d+%d' % (200, 10))  # this sets to open the window near screen center
canvas = Canvas(window, width=400, height=550, bg=BLUE, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=3)

# title text
title_text = tk.Label(window, text='Aqua Tag', font=('calibri', 34, 'bold'), bg=BLUE, fg=WHITE)
title_text.grid(column=1, row=0)

# logo
logo = PhotoImage(file='jet grind radio.png')
logo_label = Label(image=logo, bg=BLUE)
logo_label.image = logo
logo_label.grid(column=0, rowspan=2, row=1)

# Instructions Label
instructions = tk.Label(window, text='Select an image file from your computer to watermark', font='Raleway', bg=BLUE,
                        fg='white')
instructions.grid(columnspan=2, column=1, row=2)

# Photo Preview Window
current_file = None
with Image.open('upload.png') as img:
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(image=img)
preview_label = Label(image=img, text=f'Current File: {current_file}', width=300, height=300, bg=WHITE)
preview_label.grid(column=1, row=1, columnspan=2)


# Buttons
browse_button = Button(window, text='Browse Files', command=browse_files, bg=PEACH)
browse_button.grid(column=1, row=3)
exit_button = Button(window, text='Quit', command=window.quit, bg=PEACH)
exit_button.grid(column=2, row=3)

current_file = None

# entry box for watermark text
entry_label = Label(font=('Raleway', 14), fg='white', bg=BLUE)
entry_label.place(x=380, y=415)
watermark_entry = Entry(width=35, state=DISABLED)
watermark_entry.place(x=425, y=465)
create_wm_button = Button(window, text='Create Watermark', command=create_watermark, bg=PEACH, state=DISABLED)
create_wm_button.place(x=650, y=465)

# Start Window
window.mainloop()