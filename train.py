import tkinter as tk
import cv2, os
import csv
import numpy as np
# Python image library adds support for opening, manipulating, and saving many different image file formats
from PIL import ImageTk,Image
import pandas as pd
import datetime
import time
# smtplib module defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.
import smtplib
# We will deal with the MIME message type, which is able to combine HTML and plain text.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

window = tk.Tk()
# helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

#dialog_title = 'QUIT'
#dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

# window.geometry('1280x720')
window.configure(background='#b3b3ff')

# window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



message = tk.Label(window, text="Face Recognition Based Attendance System", bg="#3d3d5c", fg="white", width=50,
                   height=3, font=('poppins', 30, 'bold underline'))

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID", width=20, height=2, fg="#00004d", bg="white", font=('poppins', 15, ' bold '))
lbl.place(x=400, y=200)

txt = tk.Entry(window, width=20, bg="white", fg="#00004d", font=('times', 15, '  '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="#00004d", bg="white", height=2, font=('poppins', 15, ' bold '))
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window, width=20, bg="white", fg="#00004d", font=('poppins', 15, '  '))
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Notification : ", width=20, fg="#00004d", bg="white", height=2,
                font=('poppins', 15, ' bold '))
lbl3.place(x=400, y=600)

message = tk.Label(window, text="", bg="white", fg="#00004d", width=40, height=1, activebackground="white",
                   font=('poppins', 15, '  '))
message.place(x=700, y=615)

lbl4 = tk.Label(window, text="Enter subject", width=20, fg="#00004d", bg="white", height=2, font=('poppins', 15, ' bold '))
lbl4.place(x=400, y=400)

txt3 = tk.Entry(window, width=30, bg="white", fg="#00004d", font=('poppins', 15, '  '))
txt3.place(x=700, y=415)


lbl3 = tk.Label(window, text="Enter Email id : ", width=20, fg="#00004d", bg="white", height=2,
                font=('poppins', 15, 'bold'))
lbl3.place(x=400, y=500)

message2 = tk.Entry(window, width=30, bg="white", fg="#00004d", font=('poppins', 15, '  '))
message2.place(x=700, y=515)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        ''' Haar Cascade is a machine learning-based approach where a lot of positive and negative images are used to
        train the classifier. 
        So how this works is they are huge individual .xml files with a lot of feature sets and each xml
        corresponds to a very specific type of use case.
        '''
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            #converting image into gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)# frame,scalefactor,minimum neighbours
            #print(faces)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captu#00004d face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 60
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
#        message.configure(text= res)
        TrainImages()
    else:
        if not is_number(Id):
            res = "Enter Numeric Id"
            message.configure(text= res)
        elif not name.isalpha():
            res = "Enter Alphabetic Name"
            message.configure(text= res)

       


def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #harcascadePath = "haarcascade_frontalface_default.xml"
    #detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Saved Successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df = pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name','Subject', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    sub =(txt3.get())
    email_sender=(message2.get())
    if sub and email_sender:
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            sub =(txt3.get())
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if (conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    tt = str(Id) + "-" + aa
                    attendance.loc[len(attendance)] = [Id, aa,sub, date, timeStamp]

                else:
                    Id = 'Unknown'
                    tt = str(Id)
                if (conf > 75):
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
                cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            cv2.imshow('im', im)
            if (cv2.waitKey(1) == ord('q')):
                break
        sub = (txt3.get())
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName ="C:\Face Attendance\Attendance\\"+ sub+" "+ date+"_"+Hour+"-"+Minute+"-"+Second + ".csv"
       
        attendance.to_csv(fileName, index=False)
        cam.release()
        cv2.destroyAllWindows()

       

        email_user = 'abc@gmail.com'
        email_password = 'your_email_password'
        email_send = email_sender
       
        subject = 'Attendance of '+sub
       
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject
       
        body = 'Hereby is the attached attendance sheet of '+sub +" subject."
        msg.attach(MIMEText(body, 'plain'))
        filename ="C:\Face Attendance\Attendance\\"+ sub+" "+date+"_"+Hour+"-"+Minute+"-"+Second + ".csv"
        #filename = "Attendance" + date+"_"+Hour+"-"+Minute+"-"+Second + ".csv"
        attachment = open(filename, 'rb')
       
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)
       
        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
       
        server.sendmail(email_user, email_send, text)
        server.quit()
    else:
        res = "Enter Subject Name and Email-Id"
        message.configure(text=res)


clearButton = tk.Button(window, text="Clear", command=clear, fg="#00004d", bg="#e6e6e6", width=20, height=1,
                        activebackground="#00004d", font=('poppins', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="#00004d", bg="#e6e6e6", width=20, height=1,
                         activebackground="#00004d", font=('poppins', 15, ' bold '))
clearButton2.place(x=950, y=300)
takeImg = tk.Button(window, text="Register User", command=TakeImages, fg="#00004d", bg="#e6e6e6", width=20, height=2,
                    activebackground="#00004d", font=('poppins', 15, ' bold '))
takeImg.place(x=350, y=700)
#trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="#00004d", bg="#e6e6e6", width=20, height=2,
#                     activebackground="#00004d", font=('poppins', 15, ' bold '))
#trainImg.place(x=500, y=700)
trackImg = tk.Button(window, text="Attendance", command=TrackImages, fg="#00004d", bg="#e6e6e6", width=20, height=2,
                     activebackground="#00004d", font=('poppins', 15, ' bold '))
trackImg.place(x=675, y=700)
quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="#00004d", bg="#e6e6e6", width=20, height=2,
                       activebackground="#00004d", font=('poppins', 15, ' bold '))
quitWindow.place(x=1000, y=700)

window.mainloop()
