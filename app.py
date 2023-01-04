# Importing Necessary Libraries
from pyexpat import model
import string
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from turtle import color
from PIL import Image, ImageTk
import numpy
import numpy as np
import detect
import eye_color
import predict

# Loading the Model
# from keras.models import load_model
# model = load_model('models//bald_classifity.h5')
# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Eye Colour, Bald and Child Detection')
top.configure(background='#CDCDCD')

# Initializing the Labels (1 for age and 1 for Sex)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

# Definig Detect fuction which detects the age and gender of the person in image using the model


# def Detect(file_path):
#     global label_packed
#     image = Image.open(file_path)
#     image = image.resize((48, 48))
#     image = numpy.expand_dims(image, axis=0)
#     image = np.array(image)
#     image = np.delete(image, 0, 1)
#     image = np.resize(image, (48, 48, 3))
#     print(image.shape)
#     image = np.array([image])/255
#     pred = model.predict(image)
#     age = int(np.round(pred[1][0]))
#     print("Predicted Age is " + str(age))

def Detect(file_path):
    # img=Image.open(file_path)
    # print(detect.age(file_path))
    # print(predict.bald(file_path))
    # print(eye_color.eye_color(file_path))
    age = detect.age(file_path)
    bald = predict.bald(file_path)
    eye = eye_color.eye_color(file_path)
    print(type(age))
    child = ['15-20', '25-32', '38-43', '48-53', '60-100']
    if age in child:
        x = 'adult'
    else:
        x = 'child'
    res = []
    res.append(eye)
    res.append(x)
    res.append(bald)
    print(res)
    result = ' '.join(res)
    label1.configure(foreground="#011638", text=result)


# Defining Show_detect button function


def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image",
                      command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156",
                       foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Definig Upload Image Function


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(
            ((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)
    except:
        pass


upload = Button(top, text="Upload an Image",
                command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white',
                 font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Eye Color, Bald And child Detection",
                pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()
top.mainloop()
