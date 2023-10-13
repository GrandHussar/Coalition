# Create a file called managers. py
# This file should contain the code below:
import cv2
import numpy
import time
import filters
from PIL import Image


n = 21

face_cascade =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade =cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
       



        self._capture = capture
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
        self.faces = None

        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
        self._startTime = None
        self._framesElapsed = float(0)
        self._fpsEstimate = None

        n = 21

    @property
    
    def channel (self):
        return self._channel
        
    @channel.setter
    def channel(self,value):
        if self._channel != value:
           self._channel = value
           self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:

            _, self._frame = self._capture.retrieve()
            
  
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None
    
    def enterFrame(self):
        """ Capture the next frame, if any."""

    
    # First, we will check if any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        
        if self._capture is not None:
           self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """Draw to the window. Write to Files. Release the frame."""
    
    #Check whether any grabbed frame is retrievable
    #The getter may retrieve and cache the frame.
        if self.frame is None:
            self.enteredFrame = False
            return
        
    #Update the FPS estimate and related variables.
        if self._framesElapsed==0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Draw to the window , if any.
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                
                mirroredFrame = numpy.fliplr(self._frame.copy()).astype(numpy.uint8)
                gray = cv2.cvtColor(mirroredFrame, cv2.COLOR_BGR2GRAY)
                self.faces = face_cascade.detectMultiScale(gray,1.3,5,0,(20,20))
                for (x,y,w,h) in self.faces:
                    img = cv2.rectangle(mirroredFrame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray,1.3, 5, 0, (20, 20))
                    smile = smile_cascade.detectMultiScale(roi_gray,1.3,5,0,(40,40))
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(img[y:y+h, x:x+w],(ex,ey),(ex+ew,ey+eh),
                        (0,255,0),2)
                    for (sx,sy,sw,sh) in smile:
                        cv2.rectangle(img[y:y+h, x:x+w],(sx,sy),(sx+sw,sy+sh),
                        (0,0,255),2)
        
                self.previewWindowManager.show(mirroredFrame)
                


                
                
                
                

                
            else:
                OnlyFrame = self._frame.copy().astype(numpy.uint8)
                
                gray = cv2.cvtColor(OnlyFrame, cv2.COLOR_BGR2GRAY)
                self.faces = face_cascade.detectMultiScale(gray,1.3,5,0,(20,20))
                for (x,y,w,h) in self.faces:
                    img = cv2.rectangle(OnlyFrame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray,1.3, 5, 0, (19, 20))
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(img[y:y+h, x:x+w],(ex,ey),(ex+ew,ey+eh),
                        (0,255,0),2)
                self.previewWindowManager.show(OnlyFrame)

                
        #Write to the image file, if any.
        if self.isWritingImage:
            OnlyFrame = self._frame.copy().astype(numpy.uint8)
            gray = cv2.cvtColor(OnlyFrame, cv2.COLOR_BGR2GRAY)
            self.faces = face_cascade.detectMultiScale(gray,1.3,5,0,(20,20))
            if self.faces is not None:
                for (x,y,w,h) in self.faces:
                    img = cv2.rectangle(OnlyFrame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray,1.3, 5, 0, (19, 20))
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(img[y:y+h, x:x+w],(ex,ey),(ex+ew,ey+eh),
                        (0,255,0),2)
                    if y is not None:
                        cropped_image = gray[y:y+h, x:x+w]
                        new_image = cv2.resize(cropped_image, (200,200), interpolation = cv2.INTER_AREA)
                
            

                    
                    cv2.imwrite(self._imageFilename, new_image)
            self._imageFilename = None
        
        #Write to the video file, if any.
        self._writeVideoFrame()

        #Release the frame
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        """Write the next exited frame to an image file."""
        self._imageFilename = filename

    def startWritingVideo(self,filename,encoding = cv2.VideoWriter_fourcc('I','4','2','0')):
        """Start Writing exited frames to a video file"""
        self._videoFilename = filename
        self._videoEncoding = encoding
    
    def stopWriting(self):
        """Stop Writing exited frames to a video file."""
        self._videoFilename= None
        self._videoEncoding= None
        self._videoWrite = None
    
    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._framesElapsed < 20:
                    #Wait until more frames elapse so that the estimate
                    # is more stable
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

                    
            self._videoWriter = cv2.VideoWriter(self._videoFilename,
                                                self._videoEncoding,
                                                fps, size)
        self._videoWriter.write(self.frame)


                                        

class WindowManager(object):
    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False
        
    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self,frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
    
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
        # Discard any non-ASCII info encoded by GTK
            keycode &= 0xFF
            self.keypressCallback(keycode)



        