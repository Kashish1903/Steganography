import tkinter as tk
from tkinter import filedialog
from PIL import Image

def encode():
    text = entry.get()
    cover_path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if not cover_path:
        return

    img = Image.open(cover_path)
    encoded_img = encode_text(img, text)
    encoded_img.save("encoded_image.png")
    tk.messagebox.showinfo("Success", "Text encoded successfully!")

def decode():
    stego_path = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if not stego_path:
        return

    img = Image.open(stego_path)
    decoded_text = decode_text(img)
    tk.messagebox.showinfo("Decoded Text", decoded_text)

def encode_text(img, text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    data_index = 0

    img = img.convert('RGB')
    pixels = img.load()

    for i in range(img.width):
        for j in range(img.height):
            pixel = list(pixels[i, j])
            for color_channel in range(3):
                if data_index < len(binary_text):
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_text[data_index], 2)
                    data_index += 1
                else:
                    break
            pixels[i, j] = tuple(pixel)

    return img

def decode_text(img):
    binary_text = ""
    pixels = img.load()

    for i in range(img.width):
        for j in range(img.height):
            pixel = pixels[i, j]
            for color_channel in range(3):
                binary_text += format(pixel[color_channel], '08b')[-1]

    decoded_text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    return decoded_text

# GUI setup
root = tk.Tk()
root.title("Steganography Tool")
root.configure(bg="#191970")
root.resizable(False,False)

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)
frame.configure(bg="#191970")

label = tk.Label(frame, text="Enter text to encode:")
label.grid(row=0, column=0, sticky='e')

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1, padx=5, pady=5)

encode_button = tk.Button(frame, text="Encode", command=encode)
encode_button.grid(row=1, column=0, columnspan=2, pady=10)

decode_button = tk.Button(frame, text="Decode", command=decode)
decode_button.grid(row=2, column=0, columnspan=2)

root.mainloop()
