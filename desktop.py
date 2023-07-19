#!/usr/bin/env python3

import tkinter as tk

def close_interface(event):
    root.destroy()

root = tk.Tk()
root.title("Logo Interface")
root.attributes('-fullscreen', True)  # Set full screen

# Add your logo image path below
logo_image_path = "static/images/Sirrl_v.png"
logo_image = tk.PhotoImage(file=logo_image_path)

# Create a label for the logo image
logo_label = tk.Label(root, image=logo_image)
logo_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the image

root.bind("<Double-Button-1>", close_interface)
root.mainloop()
