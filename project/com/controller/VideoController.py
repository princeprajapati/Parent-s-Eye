import os
import random
import smtplib
import threading
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
import dlib
from flask import request, redirect, render_template, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.VideoVO import VideoVO

faceCascade = cv2.CascadeClassifier('project/static/adminResources/modelDump/haarcascade_frontalface_default.xml')

UPLOAD_FOLDER = 'project/static/adminResources/outputVideo/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The deisred outputVideo width and height
capture_duration = 20


@app.route('/user/loadVideo', methods=['GET'])
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addVideo.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# We are not doing really face recognition
def doRecognizePerson(faceNames, fid):
    time.sleep(2)
    faceNames[fid] = "Person " + str(fid)


@app.route('/user/insertVideo', methods=['GET'])
def userInsertVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            uploadDate = str(datetime.now().date())
            uploadTime = datetime.now().strftime('%H:%M:%S')

            random_number = random.randint(1, 1000)

            videoOutputFileName = "output_" + str(random_number) + ".webm"
            videoOutputFilePath = app.config['UPLOAD_FOLDER']

            outputVideo = videoOutputFilePath + videoOutputFileName

            capture = cv2.VideoCapture(r"F:\projectworkspace\project\static\adminResources\inputVideo\input_1.mp4")

            fourcc = cv2.VideoWriter_fourcc(*'VP80')
            out = cv2.VideoWriter(outputVideo, fourcc, capture_duration, (640, 480))

            # Create two opencv named windows
            cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

            # Position the windows next to eachother
            cv2.moveWindow("base-image", 0, 100)
            cv2.moveWindow("result-image", 400, 100)

            # Start the window thread for the two windows we are using
            cv2.startWindowThread()

            # The color of the rectangle we draw around the face
            rectangleColor = (0, 165, 255)

            # variables holding the current frame number and the current faceid
            frameCounter = 0
            currentFaceID = 0

            # Variables holding the correlation trackers and the name per faceid
            faceTrackers = {}
            faceNames = {}

            try:
                while True:
                    # Retrieve the latest image from the webcam
                    rc, fullSizeBaseImage = capture.read()

                    # Resize the image to 320x240
                    baseImage = cv2.resize(fullSizeBaseImage, (320, 240))

                    # Result image is the image we will show the user, which is a
                    # combination of the original image from the webcam and the
                    # overlayed rectangle for the largest face
                    resultImage = baseImage.copy()

                    # STEPS:
                    # * Update
                    #
                    #
                    # all trackers and remove the ones that are not
                    #   relevant anymore
                    # * Every 10 frames:
                    #       + Use face detection on the current frame and look
                    #         for faces.
                    #       + For each found face, check if centerpoint is within



                    #         existing tracked box. If so, nothing to do
                    #       + If centerpoint is NOT in existing tracked box, then
                    #         we add a new tracker with a new face-id


                    # Increase the framecounter
                    frameCounter += 1

                    # Update all the trackers and remove the ones for which the update
                    # indicated the quality was not good enough
                    fidsToDelete = []
                    for fid in faceTrackers.keys():
                        trackingQuality = faceTrackers[fid].update(baseImage)

                        # If the tracking quality is good enough, we must delete
                        # this tracker
                        if trackingQuality < 7:
                            fidsToDelete.append(fid)

                    for fid in fidsToDelete:
                        print("Removing fid " + str(fid) + " from list of trackers")
                        faceTrackers.pop(fid, None)

                    # Every 10 frames, we will have to determine which faces
                    # are present in the frame
                    if (frameCounter % 10) == 0:

                        # For the face detection, we need to make use of a gray
                        # colored image so we will convert the baseImage to a
                        # gray-based image
                        gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                        # Now use the haar cascade detector to find all faces
                        # in the image
                        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

                        # Loop over all faces and check if the area for this
                        # face is the largest so far
                        # We need to convert it to int here because of the
                        # requirement of the dlib tracker. If we omit the cast to
                        # int here, you will get cast errors since the detector
                        # returns numpy.int32 and the tracker requires an int
                        matchedFid = None
                        for (_x, _y, _w, _h) in faces:
                            x = int(_x)
                            y = int(_y)
                            w = int(_w)
                            h = int(_h)

                            # calculate the centerpoint
                            x_bar = x + 0.5 * w
                            y_bar = y + 0.5 * h

                            # Variable holding information which faceid we
                            # matched with


                            # Now loop over all the trackers and check if the
                            # centerpoint of the face is within the box of a
                            # tracker
                            for fid in faceTrackers.keys():
                                tracked_position = faceTrackers[fid].get_position()

                                t_x = int(tracked_position.left())
                                t_y = int(tracked_position.top())
                                t_w = int(tracked_position.width())
                                t_h = int(tracked_position.height())

                                # calculate the centerpoint
                                t_x_bar = t_x + 0.5 * t_w
                                t_y_bar = t_y + 0.5 * t_h

                                # check if the centerpoint of the face is within the
                                # rectangleof a tracker region. Also, the centerpoint
                                # of the tracker region must be within the region
                                # detected as a face. If both of these conditions hold
                                # we have a match
                                if ((t_x <= x_bar <= (t_x + t_w)) and
                                        (t_y <= y_bar <= (t_y + t_h)) and
                                        (x <= t_x_bar <= (x + w)) and
                                        (y <= t_y_bar <= (y + h))):
                                    matchedFid = fid

                            # If no matched fid, then we have to create a new tracker
                            if matchedFid is None:
                                print("Creating new tracker " + str(currentFaceID))

                                start_time = time.time()
                                minutes = 0

                                # Create and store the tracker
                                tracker = dlib.correlation_tracker()
                                tracker.start_track(baseImage,
                                                    dlib.rectangle(x - 10,
                                                                   y - 20,
                                                                   x + w + 10,
                                                                   y + h + 20))

                                faceTrackers[currentFaceID] = tracker

                                # Start a new thread that is used to simulate
                                # face recognition. This is not yet implemented in this
                                # version :)
                                t = threading.Thread(target=doRecognizePerson,
                                                     args=(faceNames, currentFaceID))
                                t.start()

                                # Increase the currentFaceID counter
                                currentFaceID += 1

                    # Now loop over all the trackers we have and draw the rectangle
                    # around the detected faces. If we 'know' the name for this person
                    # (i.e. the recognition thread is finished), we print the name
                    # of the person, otherwise the message indicating we are detecting
                    # the name of the person
                    for fid in faceTrackers.keys():
                        tracked_position = faceTrackers[fid].get_position()

                        t_x = int(tracked_position.left())
                        t_y = int(tracked_position.top())
                        t_w = int(tracked_position.width())
                        t_h = int(tracked_position.height())

                        cv2.rectangle(resultImage, (t_x, t_y),
                                      (t_x + t_w, t_y + t_h),
                                      rectangleColor, 2)

                        if fid in faceNames.keys():
                            cv2.putText(resultImage, faceNames[fid],
                                        (int(t_x + t_w / 2), int(t_y)),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255), 2)
                        else:
                            cv2.putText(resultImage, "Detecting...",
                                        (int(t_x + t_w / 2), int(t_y)),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255), 2)

                        for fid in faceTrackers.keys():
                            print("fid>>>>>>>", fid)

                            ffid = faceTrackers[fid]
                            seconds = int(time.time() - start_time) - minutes * 60
                            print(seconds)
                            if ffid is not None and seconds == capture_duration:
                                print(seconds)
                                sender = "pythondemodonotreply@gmail.com"

                                receiver = session['session_loginUsername']

                                currentDate = datetime.now().date()
                                currentTime = datetime.now().strftime('%H:%M:%S')

                                body = 'Your child is watching t.v continue:  \nDate:{}\nTime:{}'.format(currentDate,
                                                                                                         currentTime)

                                msg = MIMEMultipart()

                                msg['From'] = sender

                                msg['To'] = receiver

                                msg['Subject'] = "DETECTION"

                                msg.attach(MIMEText(body, 'plain'))
                                # To change the payload into encoded form
                                server = smtplib.SMTP('smtp.gmail.com', 587)

                                server.starttls()

                                server.login(sender, "qazwsxedcrfvtgb1234567890")

                                text = msg.as_string()

                                server.sendmail(sender, receiver, text)

                                server.quit()
                                break
                    # Since we want to show something larger on the screen than the
                    # original 320x240, we resize the image again
                    #
                    # Note that it would also be possible to keep the large version
                    # of the baseimage and make the result image a copy of this large
                    # base image and use the scaling factor to draw the rectangle
                    # at the right coordinates.
                    largeResult = cv2.resize(resultImage, (640, 480), interpolation=cv2.INTER_AREA)

                    out.write(largeResult)

                    # Finally, we want to show the images on the screen
                    cv2.imshow("base-image", baseImage)
                    cv2.imshow("result-image", largeResult)

                    # Check if a key was pressed and if it was Q, then break
                    # from the infinite loop
                    pressedKey = cv2.waitKey(2)
                    if pressedKey == ord('q'):
                        break

                capture.release()
                out.release()
                cv2.destroyAllWindows()

            # To ensure we can also deal with the user pressing Ctrl-C in the console
            # we have to check for the KeyboardInterrupt exception and break out of
            # the main loop
            except KeyboardInterrupt as e:
                pass

            videoVO.videoOutputFileName = videoOutputFileName
            videoVO.videoOutputFilePath = videoOutputFilePath.replace('project','..')
            videoVO.videoUploadDate = uploadDate
            videoVO.videoUploadTime = uploadTime
            videoVO.video_LoginId = session['session_loginId']

            videoDAO.insertVideo(videoVO)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewVideo', methods=['GET'])
def userViewVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoVO.video_LoginId = session['session_loginId']

            videoVOList = videoDAO.viewVideo(videoVO)

            print("______________", videoVOList)

            return render_template('user/viewVideo.html', videoVOList=videoVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteVideo', methods=['GET'])
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()

            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')

            videoVO.videoId = videoId

            videoList = videoDAO.deleteVideo(videoVO)

            path = videoList.videoOutputFilePath.replace("..", "project") + videoList.videoOutputFileName

            os.remove(path)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDetection', methods=['GET'])
def adminViewDetection():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()

            videoVOList = videoDAO.adminViewVideo()

            return render_template('admin/viewDetection.html',videoVOList=videoVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)