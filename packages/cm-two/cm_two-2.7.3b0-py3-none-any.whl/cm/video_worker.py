from __future__ import print_function
import subprocess
import platform
import time
import traceback
import uuid
from imutils.video import VideoStream
from PIL import Image, ImageDraw
from PIL import ImageTk
import tkinter as tki
import threading
import os
import imutils
import cv2
from cm.configs import settings
import socket


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)),
                (w - rad, h - rad))
    im.putalpha(alpha)
    return im


class PhotoBoothApp:
    def __init__(self, url, outputPath, root, canvas,
                 width=300, height=300,
                 pos_x=500, pos_y=500, zoomed_x=1000, zoomed_y=1000,
                 zoomed_video_width=1000, zoomed_video_height=700,
                 root_zoom_callback_func=None,
                 root_hide_callback_func=None,
                 cam_type=None):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.url = url
        host = url.split("@")[1].split("/")[0]
        self.ip = host.split(":")[0]
        self.port = int(host.split(":")[1])
        self.zoomed = False
        self.cam_type = cam_type
        self.zoomed_video_width = zoomed_video_width
        self.zoomed_video_height = zoomed_video_height
        self.outputPath = outputPath
        self.root_zoom_callback_func = root_zoom_callback_func
        self.root_hide_callback_funct = root_hide_callback_func
        self.frame = None
        self.can_show = False
        self.can_zoom = True
        self.thread = None
        self.stopEvent = None
        self.image = None
        self.zoomed_x = zoomed_x
        self.zoomed_y = zoomed_y
        # initialize the root window and image panel
        self.root = root
        self.init_x, self.init_y = pos_x, pos_y
        self.place_x, self.place_y = pos_x, pos_y
        self.init_video_width, self.init_video_height = width, height
        self.video_width, self.video_height = width, height
        self.panel = None
        self.canvas = canvas
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.ping = self.ping_ok(self.ip, self.port)
        threading.Thread(target=self.get_image_loop).start()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        if self.ping:
            self.vs = VideoStream(url).start()


    def ping_ok(self, ip, port=554, timeout=2) -> bool:
        """ping server"""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
        except OSError as error:
            return False
        else:
            s.close()
            return True


    def get_image_loop(self):
        while not self.stopEvent.is_set():
            if not self.ping:
                self.image = self.get_image_not_available()
                time.sleep(2)
            else:
                self.image = self.get_image_from_camera()

    def get_image_not_available(self):
        image = Image.open(
            os.path.join(settings.IMGS_DIR, "camera_is_not_available.png"))
        return image

    def get_image_from_camera(self):
        while not self.stopEvent.is_set():
            # grab the frame from the video stream and resize it to
            # have a maximum width of 300 pixels
            #if error_count > 5:
            #    return
            try:
                self.frame = self.vs.read()
            except:
                self.vs = VideoStream(self.url).start()
                print(self.url, "\nSOME ERROR")
                print(traceback.format_exc())
                continue
            try:
                self.frame = imutils.resize(self.frame,
                                            width=self.video_width,
                                            height=self.video_height)
                error_count = 0
            except AttributeError:
                #error_count += 1
                #print(self.url, "\nATTR ERROR")
                continue
            # OpenCV represents images in BGR order; however PIL
            # represents images in RGB order, so we need to swap
            # the channels, then convert to PIL and ImageTk format
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image_prev = Image.fromarray(image)
            image = add_corners(image_prev, 15)
            return image

    def stop_video(self):
        self.can_show = False

    def play_video(self):
        self.can_show = True

    def reconnection_logic(self):
        ping = self.ping_ok(self.ip, self.port)
        if ping:
            try:
                self.vs = VideoStream(self.url).start()
                return True
            except:
                pass

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading]
        boo = []
        tags = ['foo']
        #count = 0
        while not self.stopEvent.is_set():
            #print(self.image)
            if not self.image:
                continue
            try:
                # keep looping over frames until we are instructed to stop
                tag = str(uuid.uuid4())
                #count += 1
                #tag = str(count)
                image = ImageTk.PhotoImage(self.image)
                if self.can_show:
                    img = self.canvas.create_image(self.place_x, self.place_y,
                                                   image=image, tag=tag)
                    self.canvas.tag_bind(img, '<Button-1>', self.img_callback)
                boo.append(image)
                prev_tag = tags[-1]
                tags.remove(prev_tag)
                self.canvas.delete(prev_tag)
                tags.append(tag)
                time.sleep(0.1)
                if len(boo) > 6:
                    #boo = [image, ]
                    boo = boo[-2:]
                    tags = tags[-2:]
                #if count > 100:
                #    count = 0
            except (RuntimeError) as e:
                print("[INFO] caught a RuntimeError")

    def set_new_params(self, x=None, y=None, width=None, height=None):
        if width:
            self.video_width = width
        if height:
            self.video_height = height
        if x:
            self.place_x = x
        if y:
            self.place_y = y

    #def set_default_params(self):

    def hide_callback(self, root_calback=True):
        self.video_width = self.init_video_width
        self.video_height = self.init_video_height
        self.place_x = self.init_x
        self.place_y = self.init_y
        self.can_show = True
        if self.root_hide_callback_funct and root_calback:
            self.root_hide_callback_funct(self.cam_type)
            self.zoomed = False

    def zoom_callback(self, root_calback=True):
        self.video_width = self.zoomed_video_width
        self.video_height = self.zoomed_video_height
        self.place_x = self.zoomed_x
        self.place_y = self.zoomed_y
        self.can_show = True
        if self.root_zoom_callback_func and root_calback:
            self.root_zoom_callback_func(self.cam_type)
        self.zoomed = True

    def img_callback(self, *args):
        if not self.can_zoom or not self.ping:
            return
        self.can_show = False
        if self.zoomed:
            self.hide_callback()
        else:
            self.zoom_callback()

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


def start_video_stream(root, canvas, xpos, ypos, v_width, v_height,
                       cam_login, cam_pass, cam_ip, zoomed_x, zoomed_y,
                       zoomed_video_width, zoomed_video_height,
                       cam_type=None,
                       cam_port=554,
                       zoom_callback_func=None, hide_callback_func=None):
    url = f"rtsp://{cam_login}:{cam_pass}@{cam_ip}:{cam_port}/Streaming/Channels/102"
    inst = PhotoBoothApp(url, "output", root=root, canvas=canvas, width=v_width,
                         height=v_height, pos_x=xpos, pos_y=ypos,
                         zoomed_x=zoomed_x,
                         zoomed_y=zoomed_y,
                         root_zoom_callback_func=zoom_callback_func,
                         root_hide_callback_func=hide_callback_func,
                         cam_type=cam_type,
                         zoomed_video_width=zoomed_video_width,
                         zoomed_video_height=zoomed_video_height)
    return inst
