# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
#from tkinter import messagebox
import face_recognition
import imutils
import pickle
import time
import cv2
# construct the argument parser and parse the arguments

class Rec:
    def __init__(self,UserName,Pass):
        self.UserName = UserName
        self.Pass = Pass

        self.f = open("/home/pi/Desktop/finished_project/passfile.pickle", "rb")
        self.PassFileData = pickle.load(self.f)

        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        self.data = pickle.loads(open("/home/pi/Desktop/finished_project/encodings.pickle", "rb").read())
        self.detector = cv2.CascadeClassifier("a1.xml")

    def CheckPass(self):
        if self.UserName == "" or self.Pass == "":
            return 1
        elif self.UserName in self.PassFileData and self.Pass != self.PassFileData[self.UserName]:
            return 2
        else:
            return 0

    def Start(self):            
        
        self.trynum = 10
        self.checknum = 3
        self.fpsnum = 150
        # initialize the video stream and allow the camera sensor to warm up
        #vs = VideoStream(src=0).start()
        self.vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        # start the FPS counter
        self.fps = FPS().start()

        # loop over frames from the video file stream
        while self.trynum > 0:
            
            self.fpsnum = self.fpsnum -1
            if self.fpsnum == 0:
                self.close()
                return 3
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=250)
            
            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            # detect faces in the grayscale frame
            self.rects = self.detector.detectMultiScale(self.gray, scaleFactor=1.1, 
                    minNeighbors=5, minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE)

            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            self.boxes = [(y, x + w, y + h, x) for (x, y, w, h) in self.rects]

            # compute the facial embeddings for each face bounding box
            self.encodings = face_recognition.face_encodings(self.rgb, self.boxes)
            self.names = [] #type: List[str]

            # loop over the facial embeddings
            for self.encoding in self.encodings:
                
                # attempt to match each face in the input image to our known
                # encodings
                self.matches = face_recognition.compare_faces(self.data["encodings"],self.encoding)
                self.name = "Unknown"
                self.trynum -= 1

                # check to see if we have found a match
                if True in self.matches:
                    
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    self.matchedIdxs = [i for (i, b) in enumerate(self.matches) if b]
                    self.counts = {} # type: Dict

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    #faceacc = {}
                    for i in self.matchedIdxs:
                        
                        self.name = self.data["names"][i]
                        self.counts[self.name] = self.counts.get(self.name, 0) + 1
                        #faceacc[name] = face_recognition.face_distance(data["encodings"],encoding) + faeacc.get(name, 0)

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    self.name = max(self.counts, key=self.counts.get)
                    #accurecy = faceacc[name]/counts[name]
                    self.fpsnum = 150
                    if self.PassFileData[self.name] == self.Pass and self.name == self.UserName:
                        
                        if self.checknum is 0:
                            self.close()
                            return 1
                        else:
                            self.checknum -= 1
                    else:
                        self.name = "Unknown"
                        if self.checknum is 6:
                            self.close()
                            return 0
                        else:
                            self.checknum += 1
                        
                                
                self.names.append(self.name)
          

            # loop over the recognized faces
            for ((top, right, bottom, left), self.name) in zip(self.boxes, self.names):
                
                # draw the predicted face name on the image
                cv2.rectangle(self.frame, (left, top), (right, bottom),
                        (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(self.frame, self.name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

            # display the image to our screen
            cv2.imshow("Frame", self.frame)
            self.key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if self.key == ord("q"):
                self.close()
                return 2

            # update the FPS counter
            self.fps.update()
        self.close()
        return 0
        
    def close(self):
        # stop the timer and display FPS information
        self.fps.stop()

        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.vs.stop()
