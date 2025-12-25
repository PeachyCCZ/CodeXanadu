# importing required libraries 
import cv2 
import numpy as np
import os
import time as time
import random
from threading import Thread # library for implementing multi-threaded processing 

# TODO PLAYER
#from ffpyplayer.player import MediaPlayer



"""
TODO
    * change how to control the position in the video : load all video and move with get / set
    * look the behavior of memory and if the objects are correctly destroyed
    * depending on behavior with memory, change the way to destroy / reload a file
    * add keyword to change resolution on the fly

    
Load the full video and just change position randomly
Can remove the partial load
add the positional argument (newPos) as a class method

Deactivate the sound (faster withotu sound)

"""

# defining a helper class for implementing multi-threaded processing 
class videoStream :
    def __init__(self, video1, video2, video3, video4):

        # loading video filepath
        self.video1 = video1
        self.video2 = video2
        self.video3 = video3
        self.video4 = video4

        # Output resolution 
        self.outW = 640
        self.outH = 480

        # 
        self.framerate = 30

        combinedWidth = 2 * self.outW
        combinedHeight = 2 * self.outH
        self.canvas = np.zeros((combinedHeight, combinedWidth, 3), dtype=np.uint8)

        # opening video capture stream 
        self.cap1 = cv2.VideoCapture(self.video1)
        self.cap2 = cv2.VideoCapture(self.video2)
        self.cap3 = cv2.VideoCapture(self.video3)
        self.cap4 = cv2.VideoCapture(self.video4)

        # Amont of frame
        framesNb1 = self.cap1.get(cv2.CAP_PROP_FRAME_COUNT)
        framesNb2 = self.cap2.get(cv2.CAP_PROP_FRAME_COUNT)
        framesNb3 = self.cap3.get(cv2.CAP_PROP_FRAME_COUNT)
        framesNb4 = self.cap4.get(cv2.CAP_PROP_FRAME_COUNT)

        print('Amount of frame1 : {}'.format(framesNb1))

        self.cap1.set(cv2.CAP_PROP_POS_FRAMES, int(0.2 * framesNb1))
        self.cap2.set(cv2.CAP_PROP_POS_FRAMES, int(0.4 * framesNb2))
        self.cap3.set(cv2.CAP_PROP_POS_FRAMES, int(0.6 * framesNb3))
        self.cap4.set(cv2.CAP_PROP_POS_FRAMES, int(0.8 * framesNb4))

        if not self.cap1.isOpened() or not self.cap2.isOpened():
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
            
        # reading a single frame from vcap stream for initializing 
        ret1 , frame1 = self.cap1.read()
        ret2 , frame2 = self.cap2.read()
        ret3 , frame1 = self.cap3.read()
        ret4 , frame2 = self.cap4.read()

        if not ret1 or not ret2:
            print('[Exiting] No more frames to read')
            exit(0)

        # self.stopped is set to False when frames are being read from self.vcap stream 
        self.stopped = True 

        # reference to the thread for reading next available frame from input stream 
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads keep running in the background while the program is executing 
        
    # method for starting the thread for grabbing next available frame in input stream 
    def start(self):
        self.stopped = False
        self.t.start() 

    # method for reading next frame 
    def update(self):


        #delay time for 30Hz is 33ms
        delay_time = 33
        prev = 0

        while self.cap1.isOpened() and self.cap2.isOpened() and self.cap3.isOpened() and self.cap4.isOpened() :

            if self.stopped:
                break
            
            time_elapsed = time.time() - prev
            #cv2.waitKey(delay_time)

            if time_elapsed > 1./self.framerate:

                prev = time.time()

                ret1, frame1 = self.cap1.read()
                ret2, frame2 = self.cap2.read()
                ret3, frame3 = self.cap3.read()
                ret4, frame4 = self.cap4.read()

                frame1 = cv2.resize(frame1, (self.outW, self.outH))
                frame2 = cv2.resize(frame2, (self.outW, self.outH))
                frame3 = cv2.resize(frame3, (self.outW, self.outH))
                frame4 = cv2.resize(frame4, (self.outW, self.outH))

                # Combined the image
                self.canvas[:self.outH, :self.outW, :] = frame1
                self.canvas[:self.outH, self.outW:self.outW + self.outW, :] = frame2
                self.canvas[self.outH:self.outH + self.outH, :self.outW, :] = frame3
                self.canvas[self.outH:self.outH + self.outH, self.outW:self.outW + self.outW, :] = frame4

                if not ret1 or not ret2 :
                    print('[Exiting] No more frames to read')
                    self.stopped = True
                    break

        self.cap1.release()
        self.cap2.release()
        self.cap3.release()
        self.cap4.release()

    # method for returning latest read frame 
    def read(self):
        return self.canvas

    # method called to stop reading frames 
    def stop(self):
        self.stopped = True 

class videoStream_v2 :
    def __init__(self, videoPath, fracStart=0, frameSize = [480, 640], playSound=False):

        # loading video filepath
        self.videoPath = videoPath

        # Output resolution 
        self.outH = frameSize[0]
        self.outW = frameSize[1]

        # 
        # foo = int(self.outH * 0.025)
        # self.progressionBar = [foo, self.outH - foo, self.outW]

        # 
        self.framerate = 30

        # opening video capture stream 
        self.cap = 0
        # frameNb = total number of frame
        self.frameNb = 0
        # frameCount = current frame count
        self.frameCount = 0

        # Media player
        self.player = 0
        self.playSound = playSound

        self.initVideo(videoPath, fracStart)

        # 
        self.frame = np.zeros((self.outH, self.outW, 3), dtype=np.uint8)

        # Amont of frame
        # framesNb = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # print('Amount of frame1 : {}'.format(framesNb))
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(fracStart * framesNb))

        # 
        if not self.cap.isOpened():
            print("[Exiting]: Error accessing stream.")
            exit(0)
            
        # # reading a single frame from vcap stream for initializing 
        # ret , self.frame = self.cap.read()

        # if not ret:
        #     print('[Exiting] No more frames to read')
        #     exit(0)

        # self.stopped is set to False when frames are being read from self.vcap stream 
        self.stopped = True 

        # reference to the thread for reading next available frame from input stream 
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads keep running in the background while the program is executing

    def initVideo(self, videoPath, fracStart=0):

        # For video
        # self.cap = cv2.VideoCapture(videoPath, cv2.CAP_FFMPEG)
        self.cap = cv2.VideoCapture(videoPath)

        self.framerate = self.cap.get(cv2.CAP_PROP_FPS)
        self.frameNb = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(fracStart * self.frameNb))

        # Output resolution 
        self.cap.read()
        self.outH = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.outW = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # For sound
        video_duration = self.frameNb / self.framerate
        start_time = fracStart * video_duration
        #print('start time : {}'.format(start_time))

        if self.playSound:
            print(self.playSound)
            # self.player = MediaPlayer(videoPath)
            # time.sleep(1)
            # print(self.player)
            # self.player.seek(start_time-1.4)
        
    # method for starting the thread for grabbing next available frame in input stream 
    def start(self):
        self.stopped = False
        self.t.start() 

    # method for reading next frame 
    def update(self):

        #delay time for 30Hz is 33ms
        delay_time = 33
        prev = 0

        while self.cap.isOpened():

            if self.stopped:
                break
            
            time_elapsed = time.time() - prev
            #cv2.waitKey(delay_time)

            if time_elapsed > 1./self.framerate:

                prev = time.time()

                # Get related item to video
                ret, localFrame = self.cap.read()
                self.frameCount = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                self.frame = localFrame
                # self.frame = cv2.resize(localFrame, (self.outW, self.outH))

                # Display the progress
                foo = self.frameCount / self.frameNb * 100
                # bar = 1.3 * self.outW / 1920
                cv2.putText(self.frame, '{:04.1f}'.format(foo), 
                            (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

                # Rectangle for progression bar
                # self.frame = add_progress_bar(self.frame, self.progressionBar, foo)
                fooH1 = int(0.995 * self.outH)
                fooH2 = self.outH
                fooW1 = 0
                fooW2 = int(foo * self.outW / 100)
                self.frame[fooH1:fooH2, fooW1:fooW2] = (0, 255, 0)

                if not ret:
                    print('[Exiting] No more frames to read')
                    self.stopped = True
                    break

                # Get related item to sound
                # TODO
                if self.playSound:
                    print(self.playSound)
                    # audio_frame, val = self.player.get_frame()
                    # self.player.set_mute(not(self.playSound))

                    # if val != 'eof' and audio_frame is not None:
                    #     #audio
                    #     img, t = audio_frame

        if self.playSound:
            print(self.playSound)
            # self.player.close_player()
        self.cap.release()

    # method for returning latest read frame 
    def read(self):
        return self.frame
    
    # method called to stop reading frames 
    def stop(self):
        self.stopped = True

    def close(self):
        self.stop()
        if self.playSound:
            self.player.close_player()
        self.cap.release()

def select_random_file(folder_path, file_extension='.mp4'):
    # List all files in the given folder with the specified extension
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) 
             and f.lower().endswith(file_extension.lower())
             and not f.startswith('.')]
    
    if not files:
        raise ValueError(f"No files with extension {file_extension} found in the folder.")
    
    # Select a random file
    random_file = random.choice(files)
    return os.path.join(folder_path, random_file)

# new position in fraction
def newPosRel(videoStream, fracNewPos):
    # Get various information
    videoPath = videoStream.videoPath
    frameCount = videoStream.frameCount
    frameNb = videoStream.frameNb

    #New
    videoStream.close()

    # Define new position
    foo = (1 + fracNewPos) * frameCount / frameNb

    #Debug
    # print('frameCount {} / new frameCount {:.3f} / frameNb {}'.format(frameCount, foo, frameNb))

    # Usual stuff to check
    if (foo > 0) and (foo < 1) :
        print('skip forward {}'.format(foo))
        newVideoStream = videoStream_v2(videoPath, foo, [outH, outW])
    else:
        print('no skip')

    return newVideoStream

# Function to add a progress bar
def add_progress_bar(myImage, progressionBar, progress_percentage):
    
    # Height of the progress bar (percentage of the height of the image)
    bar_height = progressionBar[0]
    
    # Position the bar at the bottom of the image
    bar_y_position = progressionBar[1]  

    # Width of the progress bar is the width of the image
    bar_width = progressionBar[2]
    
    # Create a blank (black) bar image
    bar_image = np.zeros((bar_height, bar_width, 3), dtype=np.uint8)
    
    # Calculate the width of the progress fill
    progress_fill_width = int((progress_percentage / 100) * bar_width)
    
    # Fill the bar with green color to indicate progress
    cv2.rectangle(bar_image, (0, 0), (progress_fill_width, bar_height), (0, 255, 0), -1)
    
    # Combine the original image and the progress bar
    final_image = np.vstack((myImage, bar_image))

    return final_image


# new position in fraction
def newPosAbs(videoStream, fracNewPos):
    # Get various information
    videoPath = videoStream.videoPath
    frameCount = videoStream.frameCount
    frameNb = videoStream.frameNb

    #Debug
    # print('frameCount {} / new frameCount {:.3f} / frameNb {}'.format(frameCount, foo, frameNb))

    #new
    videoStream.close()

    # Usual stuff to check
    if (fracNewPos > 0) and (fracNewPos < 1) :
        # print('skip forward {}'.format(foo))
        newVideoStream = videoStream_v2(videoPath, fracNewPos, [outH, outW])
    else:
        print('no skip')

    return newVideoStream

# Mouse callback function to get the position of a point
def get_mouse_position(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_LBUTTONDOWN:  # Check if the left mouse button was clicked
        mouse_x, mouse_y = x, y
        #print(f"Mouse position: ({x}, {y})")

def resolutionSelection(myRes):
    if myRes == 0:
        outW = 640
        outH = 480
    elif myRes == 1:
        outW = 1280
        outH = 720
    elif myRes == 2:
        outW = 1920
        outH = 1080
    return [outH, outW]

# def startSound(videoObject, fracStart, additionalDealy = 0):
#     myMusic = MediaPlayer(videoObject.videoPath)
#     video_duration = videoObject.frameNb / videoObject.framerate
#     start_time = fracStart * video_duration
#     time.sleep(1)
#     myMusic.seek(start_time + additionalDealy)

#     return myMusic

if __name__ == "__main__":

    # # initializing and starting multi-threaded webcam capture input stream 
    # vid1 = os.path.join('D:\Test', 'test1.mp4')
    # vid2 = os.path.join('D:\Test', 'test2.mp4')
    # vid3 = os.path.join('D:\Test', 'test3.mp4')
    # vid4 = os.path.join('D:\Test', 'test4.mp4')

    # video_stream = videoStream(vid1, vid2, vid3, vid4)
    # video_stream.start()

    # # processing frames in input stream
    # num_frames_processed = 0 
    # start = time.time()
    # while True :
    #     if video_stream.stopped:
    #         break
    #     else :
    #         frame = video_stream.read() 

    #     # adding a delay for simulating time taken for processing a frame 
    #     delay = 0.03 # delay value in seconds. so, delay=1 is equivalent to 1 second 
    #     time.sleep(delay) 
    #     num_frames_processed += 1 

    #     cv2.imshow('frame' , frame)
    #     key = cv2.waitKey(1)
    #     if key == ord('q'):
    #         break
    # end = time.time()
    # video_stream.stop() # stop the webcam stream 

    # # printing time elapsed and fps 
    # elapsed = end-start
    # fps = num_frames_processed/elapsed 
    # print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(fps, elapsed, num_frames_processed))

    # # closing all windows 
    # cv2.destroyAllWindows()

    # initializing and starting multi-threaded webcam capture input stream 
    # vid1 = os.path.join(r'D:\Test', 'test1.mp4')
    # vid2 = os.path.join(r'D:\Test', 'test2.mp4')
    # vid3 = os.path.join(r'D:\Test', 'test3.mp4')
    # vid4 = os.path.join(r'D:\Test', 'test4.mp4')

    # folder
    myFolder = r'F:\# Videos B'

    # Setup 640x480 // 1920x1080 // 720 x 480
    res = 1
    outH, outW = resolutionSelection(res)

    videoList = []
    for iL in range(4):
        videoList.append(select_random_file(myFolder))
        # videoList.append(videoStream_v2(select_random_file(myFolder), random.uniform(0, 0.9), [outH, outW]))

    foo = random.uniform(0, 0.9)
    videoS1 = videoStream_v2(videoList[0], foo, [outH, outW])
    videoS2 = videoStream_v2(videoList[1], random.uniform(0, 0.9), [outH, outW])
    videoS3 = videoStream_v2(videoList[2], random.uniform(0, 0.9), [outH, outW])
    videoS4 = videoStream_v2(videoList[3], random.uniform(0, 0.9), [outH, outW])

    # musicS1 = MediaPlayer(videoS1.videoPath)
    # video_duration = videoS1.frameNb / videoS1.framerate
    # start_time = foo * video_duration
    # time.sleep(1)
    # musicS1.seek(start_time)
    myAddDelay = 0.5
    # musicS1 = startSound(videoS1, foo, myAddDelay)

    print('debug')
    print('\tSound S1 {} S2 {} S3 {} S4 {}'.format(videoS1.playSound, videoS2.playSound, videoS3.playSound, videoS4.playSound))

    videoS1.start()
    videoS2.start()
    videoS3.start()
    videoS4.start()

    print('\tSound S1 {} S2 {} S3 {} S4 {}'.format(videoS1.playSound, videoS2.playSound, videoS3.playSound, videoS4.playSound))

    # Progression step
    stepProg = 0.05

    # get frame rate
    print('FPS1 {:.0f} FPS2 {:.0f} FPS3 {:.0f} FPS4 {:.0f}'.format(videoS1.framerate, videoS2.framerate, videoS3.framerate, videoS4.framerate))

    # Construction
    combinedWidth = 2 * outW
    combinedHeight = 2 * outH
    canvas = np.zeros((combinedHeight, combinedWidth, 3), dtype=np.uint8)

    # processing frames in input stream
    num_frames_processed = 0 
    start = time.time()

    # Global variables to store positions
    mouse_x, mouse_y = -1, -1

    while True :

        outH, outW = resolutionSelection(res)

        combinedWidth = 2 * outW
        combinedHeight = 2 * outH
        canvas = np.zeros((combinedHeight, combinedWidth, 3), dtype=np.uint8)

        if videoS1.stopped:
            frame1 = np.zeros((outH, outW, 3), dtype=np.uint8)
        elif videoS2.stopped:
            frame2 = np.zeros((outH, outW, 3), dtype=np.uint8)
        elif videoS3.stopped:
            frame3 = np.zeros((outH, outW, 3), dtype=np.uint8)
        elif videoS4.stopped:
            frame4 = np.zeros((outH, outW, 3), dtype=np.uint8)
        else :
            frame1 = videoS1.read()
            frame2 = videoS2.read() 
            frame3 = videoS3.read() 
            frame4 = videoS4.read()
        
        canvas[:outH, :outW, :] = cv2.resize(frame1, (outW, outH))
        canvas[:outH, outW:outW + outW, :] = cv2.resize(frame2, (outW, outH))
        canvas[outH:outH + outH, :outW, :] = cv2.resize(frame3, (outW, outH))
        canvas[outH:outH + outH, outW:outW + outW, :] = cv2.resize(frame4, (outW, outH))

        # canvas[:outH, :outW, :] = frame1
        # canvas[:outH, outW:outW + outW, :] = frame2
        # canvas[outH:outH + outH, :outW, :] = frame3
        # canvas[outH:outH + outH, outW:outW + outW, :] = frame4

        # audio_frame, val = musicS1.get_frame()
        # # self.player.set_mute(not(self.playSound))
        # if val != 'eof' and audio_frame is not None:
        #     #audio
        #     img, t = audio_frame

        # adding a delay for simulating time taken for processing a frame 
        delay = 0.01 # delay value in seconds. so, delay=1 is equivalent to 1 second 
        time.sleep(delay) 
        num_frames_processed += 1 

        # Display the video
        cv2.imshow('frame' , canvas)

        # If I want to play with mouse position, I need to define the position of window
        # opencv has no built-in position but can force positio of image
        #cv2.moveWindow('frame', 20, 20)

        # Set the mouse callback function to the window
        cv2.setMouseCallback('frame', get_mouse_position)

        # Value for mouse position
        #print('Mouse position: {} x {}'.format(mouse_x, mouse_y))

        # Randomize the streams
        if 0 < mouse_y < outH / 2:
            print(mouse_x)
            if 0 < mouse_x < 100:
                if res == 2:
                    res = 0
                else:
                    res+=1

            if 100 < mouse_x < outW :
                print('1 : {} x {}'.format(mouse_x, mouse_y))
                videoS1.close()
                fracStart = random.uniform(0, 0.9)
                videoS1 = videoStream_v2(select_random_file(myFolder),
                                        fracStart, [outH, outW])
                # musicS1.close_player()
                # musicS1 = startSound(videoS1, fracStart, myAddDelay)
                
                videoS1.start()

            if outW < mouse_x < 2*outW :
                print('2 : {} x {}'.format(mouse_x, mouse_y))
                videoS2.close()
                videoS2 = videoStream_v2(select_random_file(myFolder),
                                        random.uniform(0, 0.9), [outH, outW])
                videoS2.start()

        if outH < mouse_y < 3 * outH / 2:
            if 0 < mouse_x < outW :
                print('3 : {} x {}'.format(mouse_x, mouse_y))
                videoS3.close()

                videoS3 = videoStream_v2(select_random_file(myFolder),
                                        random.uniform(0, 0.9), [outH, outW])
                videoS3.start()

            if outW < mouse_x < 2*outW:
                print('4 : {} x {}'.format(mouse_x, mouse_y))
                videoS4.close()

                videoS4 = videoStream_v2(select_random_file(myFolder),
                                        random.uniform(0, 0.9), [outH, outW])
                videoS4.start()

        # Control the video stream positions
        if outH /2 < mouse_y < outH:
            if 0 < mouse_x < outW :
                print('1bis : {} x {}'.format(mouse_x, mouse_y))

                fracS = mouse_x / outW
                print(fracS)
                
                videoS1 = newPosAbs(videoS1, fracS)

                # musicS1.close_player()
                # musicS1 = startSound(videoS1, fracS, myAddDelay)

                videoS1.start()
                # videoS1.newPositionAbs(fracS)
                
            if outW < mouse_x < 2*outW :
                print('2bis : {} x {}'.format(mouse_x, mouse_y))

                fracS = (mouse_x - outW) / outW
                print(fracS)
                videoS2 = newPosAbs(videoS2, fracS)
                videoS2.start()

        if 3*outH /2 < mouse_y < 2 * outH:
            if 0 < mouse_x < outW :
                print('3bis : {} x {}'.format(mouse_x, mouse_y))

                fracS = mouse_x / outW
                print(fracS)
                videoS3 = newPosAbs(videoS3, fracS)
                videoS3.start()

            if outW < mouse_x < 2*outW:
                print('4bis : {} x {}'.format(mouse_x, mouse_y))

                fracS = (mouse_x - outW) / outW
                print(fracS)
                videoS4 = newPosAbs(videoS4, fracS)
                videoS4.start()

        # Reinit mouse_x and mouse_y
        mouse_x = -1
        mouse_y = -1


        key = cv2.waitKey(1)
        
        # Close 
        if key == ord('q'):
            break

        # control stream : a z e r & é " '
        # Refresh streams
        if key == ord('&'):
            videoS1 = videoStream_v2(select_random_file(myFolder),
                                      random.uniform(0, 0.9), [outH, outW])
            videoS1.start()
        if key == ord('é'):
            videoS2 = videoStream_v2(select_random_file(myFolder),
                                      random.uniform(0, 0.9), [outH, outW])
            videoS2.start()
        if key == ord('"'):
            videoS3 = videoStream_v2(select_random_file(myFolder),
                                      random.uniform(0, 0.9), [outH, outW])
            videoS3.start()    
        if key == ord('\''):
            videoS4 = videoStream_v2(select_random_file(myFolder),
                                      random.uniform(0, 0.9), [outH, outW])
            videoS4.start()

        # Control position of stream 1
        if key == ord('a'):
            videoS1 = newPosRel(videoS1, stepProg)
            videoS1.start()
        if key == ord('A'):
            videoS1 = newPosRel(videoS1, -stepProg)
            videoS1.start()
        
        # Control position of stream 2
        if key == ord('z'):
            videoS2 = newPosRel(videoS2, stepProg)
            videoS2.start()
        if key == ord('Z'):
            videoS2 = newPosRel(videoS2, -stepProg)
            videoS2.start()

        # Control position of stream 3
        if key == ord('e'):
            videoS3 = newPosRel(videoS3, stepProg)
            videoS3.start()
        if key == ord('E'):
            videoS3 = newPosRel(videoS3, -stepProg)
            videoS3.start()

        # Control position of stream 4
        if key == ord('r'):
            videoS4 = newPosRel(videoS4, stepProg)
            videoS4.start()
        if key == ord('R'):
            videoS4 = newPosRel(videoS4, -stepProg)
            videoS4.start()

    end = time.time()

    # Stop all processes
    videoS1.stop()
    videoS2.stop()
    videoS3.stop()
    videoS4.stop()

    # printing time elapsed and fps 
    elapsed = end-start
    fps = num_frames_processed/elapsed 
    print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(fps, elapsed, num_frames_processed))

    # closing all windows 
    cv2.destroyAllWindows()