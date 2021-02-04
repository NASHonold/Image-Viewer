import os
from os import path
from tkinter import *
from PIL import ImageTk, Image
from resizeimage import resizeimage

#sets Folder_path to no string to allow user to set path for folder themselves
Folder_Path = ''
root = Tk()
root.title('Image Viewer')
root.iconbitmap('darkNH.ico')
window_width = 1200
window_heigth = 800
window_size = str(window_width) + 'x' +str(window_heigth) +'+350+50'

bottom_button_row = 4
image_row = 3

path_entry = Entry(root, width = int(window_width/8.5), borderwidth=5)
path_entry.grid(row=0, column=0, columnspan=3)


'''
=========================== moveForward() ========================
Method moves the picture forward in the list of images that are 
located in the designated path. This changes the global variable
of image_index. This also loops back to the beginning of list
if function is utilized on last element in the list. 
'''
def moveForward():
    global image_index
    global image_total
    global my_label
    my_label.grid_forget()
    if image_total == 0:
        button_next = Button(root, text='Next', state=DISABLED)
        button_next.grid(row=bottom_button_row, column= 1)

    if image_index == image_total -1:
        image_index = 0
    else:
        image_index += 1
    my_label = Label(image = image_list[image_index])
    my_label.grid(row=image_row,column=0, columnspan=3)

'''
=========================== moveBack() =========================
Method moves the picture backward in the list of images that are 
located in the designated path. This changes the global variable
of image_index. This also loops back to the end of list
if function is utilized on the first element in the list. 
'''
def moveBack():
    global image_index
    global image_total
    global my_label
    my_label.grid_forget()
    if image_index == 0:
        image_index = image_total -1
    else:
        image_index -= 1
    my_label = Label(image = image_list[image_index])
    my_label.grid(row=image_row,column=0, columnspan=3)

'''
========================== listDir() ===========================
Method takes a string argument that should represent a path of 
a folder that contains .jpg, .jpeg, and .png files and creates 
a list of the paths to each readable image file. 
'''

def listDir(dir):
    i_list = []
    try:
        file_names = os.listdir(dir)
        for file_name in file_names:
            print(file_name)
            file_path = os.path.abspath(os.path.join(dir, file_name))
            if file_name[-3:].lower() == 'png':
                i_list.append(file_path)
            elif file_name[-4:].lower() == 'jpeg':
                i_list.append(file_path)
            elif file_name[-3:].lower() == 'jpg':
                i_list.append(file_path)
            print(i_list)
        return i_list
    except Exception:
        return i_list


'''
=========================== createImageList() =========================
Method take the list created by listDir() and generates a list of tkinter
image objects that are dynamically resized to fit the set window size. 
'''

def createImageList(dir):
    i_list = listDir(dir)
    new_list = []
    if len(i_list) != 0:
        for i in i_list:
            this_image = Image.open(i)
            this_image = resizeimage.resize_contain(this_image, [window_width-5, window_heigth-100])
            print(len(this_image.size))
            new_list.append(ImageTk.PhotoImage(this_image))
    print(new_list)
    return new_list

'''
=========================== pathClick() =============================.
This is the command the set path button executes. This will take user input and
reformat so it is usable by the other functions, and will then validate input
and prepare window to cycle through images or to prompt for another input
if there are no image objects returned from user selected path
'''
def pathClick():
    
    global Folder_Path
    global image_index
    global image_total
    global image_list
    global my_label
    my_label.grid_forget()
    
    new_path = str(path_entry.get())
    new_path = str(new_path.replace('\\','/'))
    Folder_Path = new_path

    path_entry.delete(0, END)
    
    image_index = 0
    image_list =[]
    image_list = createImageList(Folder_Path)
    image_total = len(image_list)
    if image_total != 0:
        root.geometry(window_size)
        
        my_label = Label(image = image_list[image_index])
        my_label.grid(row=image_row, column=0, columnspan=3)

        button_next = Button(root, text = 'Next', command =moveForward, state=ACTIVE)
        button_next.grid(row=bottom_button_row, column= 1)

        button_back = Button(root, text = 'Previous', command =moveBack, state=ACTIVE)
        button_back.grid(row=bottom_button_row, column= 0)

    else:
        root.geometry("858x200" + "+500+50")
        else_label = Label(text='That path is not readable\nTry again...')
        else_label.grid(row=image_row, column=0, columnspan=3,)

        button_next = Button(root, text = 'Next', command =moveForward, state=DISABLED)
        button_next.grid(row=bottom_button_row, column= 1)

        button_back = Button(root, text = 'Previous', command =moveBack, state=DISABLED)
        button_back.grid(row=bottom_button_row, column= 0)

        
'''
Setting global variables and creating the intial image list 
'''


'''
===========================================================
This is the window set up with buttons, labels, 
and entry objects below.

'''

image_index = 0
image_list = []
image_total = len(image_list)

#setting the window size to fit with initial setup
root.geometry('858x360' + '+500+50')

#setting up all button widgets for the window
button_set_path = Button(root,width=int(window_width/15),borderwidth=3, text='Set path from Input above', command=pathClick)
button_set_path.grid(row=1, column=0, columnspan=3, )

button_quit = Button(root, text = 'Exit Program', command = root.quit)
button_quit.grid(row=bottom_button_row, column=2)

button_next = Button(root, text = 'Next', command =moveForward, state=DISABLED)
button_next.grid(row=bottom_button_row, column= 1)

button_back = Button(root, text = 'Previous', command =moveBack, state=DISABLED)
button_back.grid(row=bottom_button_row, column= 0)

#setting the default image for startup
this_image = ImageTk.PhotoImage(Image.open('nopathselected.jpg'))
my_label = Label(image = this_image)
my_label.grid(row=image_row, column=0, columnspan=3)

root.mainloop()
