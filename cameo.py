import cv2
import filters
from managers import WindowManager, CaptureManager
import time

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager ('Cameo',self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0, cv2.CAP_DSHOW),self._windowManager, True)
   
   
        
    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:

            self._captureManager.enterFrame()
            
            frame = self._captureManager.frame

            # TODO: filter frame
            
            


 
            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    def collectSample(self, baseFilename, numPics):
            count = 0
            while(count < 20):
                self._captureManager.enterFrame()
                if self._captureManager.frame is not None and self._captureManager.faces is not None:
                    count +=1
                    
                    filename = f"sample_photo_{count}.pgm"
                    self._captureManager.writeImage(filename)

                    


                self._captureManager.exitFrame() 
                self._windowManager.processEvents()
                time.sleep(1) 

    def onKeypress(self, keycode):
        """ Handle a keypress.
        space -> Take a screenshot
        tab -> Start/stop recording a screencast.
        escape -> Quit.
        """
        if keycode == 32: #space
            self._captureManager.writeImage('screenshot.png')

        elif keycode == 9: #tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
                    'screencast.avi'
                )
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: #escape
            self._windowManager.destroyWindow()
        elif keycode == ord('q'): #q
            self.collectSample('photo', 20) 

if __name__=="main":
    Cameo().run



