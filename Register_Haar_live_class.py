# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

class Reg:
    def __init__(self,UserName,Pass):
        self.UserName = UserName
        self.Pass = Pass

        self.f = open("/home/pi/Desktop/finished_project/passfile.pickle", "rb")
        self.PassFileData = pickle.load(self.f)

        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        self.data = pickle.loads(open("/home/pi/Desktop/finished_project/encodings.pickle", "rb").read())
        self.detector = cv2.CascadeClassifier("a1.xml")

    def Check(self):
        if self.UserName in self.PassFileData:
            return 1            

    def Start(self):

        self.knownEncodings = [] #type: List[str]
        self.knownNames = []  #type: List[str]
        self.imgnum = 13
        self.fpsnum = 150



        # initialize the video stream and allow the camera sensor to warm up
        #vs = VideoStream(src=0).start()
        self.vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        # start the FPS counter
        self.fps = FPS().start()

        # loop over frames from the video file stream
        while self.imgnum > 0:
            
            self.fpsnum = self.fpsnum -1
            
            if self.fpsnum == 0:
                # stop the timer and display FPS information
                self.fps.stop()

                # do a bit of cleanup
                cv2.destroyAllWindows()
                self.vs.stop()
                return 2

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

            if self.imgnum > 10:
                self.imgnum = self.imgnum - 1
                continue

            # loop over the facial embeddings
            for self.encoding in self.encodings:
                    
                    # attempt to match each face in the input image to our known
                    # encodings
                self.knownEncodings.append(self.encoding)
                self.knownNames.append(self.UserName)
                self.imgnum = self.imgnum - 1
                self.fpsnum = 150

            # display the image to our screen
            cv2.imshow("Frame", self.frame)
            self.key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if self.key == ord("q"):
                
                # stop the timer and display FPS information
                self.fps.stop()

                # do a bit of cleanup
                cv2.destroyAllWindows()
                self.vs.stop()
                return 0

            # update the FPS counter
            self.fps.update()

        # stop the timer and display FPS information
        self.fps.stop()

        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.vs.stop()

        if "encodings" in self.data:
            self.data["encodings"].extend(self.knownEncodings)
            self.data["names"].extend(self.knownNames)
        else:
            self.data = {"encodings": self.knownEncodings, "names": self.knownNames}

        self.e = open("/home/pi/Desktop/finished_project/encodings.pickle", "wb")
        self.e.write(pickle.dumps(self.data))
        self.e.close()

        self.PassFileData[self.UserName] = self.Pass
        self.pf = open("/home/pi/Desktop/finished_project/passfile.pickle", "wb")
        self.pf.write(pickle.dumps(self.PassFileData))
        self.pf.close()
        return 1