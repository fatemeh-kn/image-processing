import tkinter as tk
from tkinter import Label, Frame
from tkinter import filedialog

from PIL import Image, ImageTk
import cv2

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
# image uploader function
def imageUploader():
    global img, path
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = tk.filedialog.askopenfilename() # filetypes=fileTypes
 
    # if file is selected
    if len(path):
        img = Image.open(path)
        img = img.resize((400, 400))
        pic = ImageTk.PhotoImage(img)
 
        # re-sizing the app window in order to fit picture
        # and buttom
        app.geometry("560x300")
        label_img.config(image=pic)
        label_img.image = pic

        app.geometry("1200x800")

 
    # if no file is selected, then we are displaying below message
    else:
        print("No file is Choosen !! Please choose a file.")
        img = None

# image uploader function
def imageROI():
        image = cv2.imread(path)
        roi = cv2.selectROI("Select the area",image)
        selected_image = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        if len(selected_image)>0:
            selected_image = cv2.cvtColor(selected_image, cv2.COLOR_BGR2RGB)
            roi_image = Image.fromarray(selected_image)

        cv2.destroyAllWindows()    
        roi_image = roi_image.resize((400, 400))
        pic = ImageTk.PhotoImage(roi_image )
    
        # re-sizing the app window in order to fit picture
        # and buttom
        label_roi.config(image=pic)
        label_roi.image = pic

        # Calculate histograms for R, G, and B channels of the cropped image
        hist_r = cv2.calcHist([selected_image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([selected_image], [1], None, [256], [0, 256])
        hist_b = cv2.calcHist([selected_image], [2], None, [256], [0, 256])
        
        fig = plt.figure(figsize=(4, 4))

        # Clear the previous plots
        plt.clf()
        
        # Plot histograms
        plt.title("Histograms")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.plot(hist_r, color='r', label='R')
        plt.plot(hist_g, color='g', label='G')
        plt.plot(hist_b, color='b', label='B')
        plt.legend()
        #plt.show()

        # Create a canvas to embed the figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()

        # Create a label to hold the canvas


        # Embed the canvas in the label
        canvas.get_tk_widget().pack(in_=label_hist)

# Main method
if __name__ == "__main__":
    img = None
    # defining tkinter object
    app = tk.Tk()
 
    # setting title and basic size to our App
    app.title("Image ROI Selection and Histogram Analysis")
    app.geometry("1200x800")
 
    # adding background image
    #img = ImageTk.PhotoImage(file='/home/mok/' + 'background.png')
    #imgLabel = Label(app, image=img)
    #imgLabel.place(x=0, y=0)
 
    # adding background color to our upload button
    app.option_add("*Label*Background", "white")
    app.option_add("*Button*Background", "lightgreen")
    
    top_frame = Frame(app, width=1200, height=50, bg='grey')
    top_frame.grid(row=0, column=0, padx=10, pady=5)

    left_frame = Frame(app, width=400, height=400, bg='white')
    left_frame.grid(row=1, column=0, padx=10, pady=5)

    mid_frame = Frame(app, width=400, height=400, bg='white')
    mid_frame.grid(row=1, column=1, padx=10, pady=5)

    right_frame = Frame(app, width=400, height=400, bg='white')
    right_frame.grid(row=1, column=2, padx=10, pady=5)

    label_img = tk.Label(left_frame)
    label_img.pack()
 
    label_roi = tk.Label(mid_frame)
    label_roi.pack()

    label_hist = tk.Label(right_frame)
    label_hist.pack()



    # defining our upload buttom
    uploadButton = tk.Button(top_frame, text="Select Image", command=imageUploader).grid(row=0,  column=0,  padx=25,  pady=10,  sticky='w'+'e'+'n'+'s')
    #uploadButton.pack(side=tk.BOTTOM, padx=(50,5))

    uploadButton = tk.Button(top_frame, text="Select ROI", command=imageROI).grid(row=0,  column=1,  padx=25,  pady=10,  sticky='w'+'e'+'n'+'s')
    #uploadButton.pack(side=tk.BOTTOM, padx=(50, 5))
 
    app.mainloop()