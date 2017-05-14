from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import os
import traceback
from threading import Thread
import numpy as np
import proxsens as p
import base64
import StartMapping as smap
import subprocess
import time

PORT_NUMBER = 8080

USERS_DICT = {"admin": "admin"}
USERS_IP = []
THREADS = []


def createScript():
    print("In createScript.")
    try:
        os.system("raspivid -n -ih -t 0 -rot 0 -w 1280 -h 720 -fps 30 -b 1000000 -o - | nc -lkv4 5001 &")
        print("Done")
    except:
        print("Falied To Save GotBlock File...")
        print(traceback.format_exc())


def login(path, ip):
    global USERS_IP
    print("In Login()")
    try:
        userName = path[path.index("?") + 6:path.index("&")]
        password = path[path.index("&") + 6:]
    except:
        return False

    print("user: " + userName)
    print("pass: " + password)
    if userName in USERS_DICT:
        if password == USERS_DICT[userName]:
            USERS_IP.append(ip)
            return True
        else:
            return False
    else:
        return False


def getMap():
    stringMap=""
    map=np.load('Grid.npy')
    stringMap+=str(len(map))+":"+str(len(map[0]))+"?"
    for x in range(len(map)):
        for y in range(len(map[0])):
            tempStr=''
            if map[x][y]==p.status.unexplored:
                tempStr="0"
            elif map[x][y]==p.status.block:
                tempStr="1"
            else:
                tempStr="2"
            stringMap+=tempStr
        stringMap+=":"
    print(stringMap)
    return stringMap

def moveLeft():
    p.turnleft()


def moveRight():
    p.turnright()


def moveForward():
    p.moveForward()


def stopCamera():
    for t in THREADS:
        if t.getName() == "Camera":
            pass


def savePoints(path):
    try:
        pointsList = []
        pointString = path[path.index("?") + 1:]

        while ":" in pointString:
            pointString = pointString[pointString.index(":") + 1:]
            x = int(pointString[:pointString.index(",")])
            y = int(pointString[pointString.index(",")+1:pointString.index("~")])
            pointsList.append((x, y))

        np.save("points", pointsList)
        return True
    except:
        return False


def getPoint():
    try:
        points = np.load("points.npy")
        msg=""
        for item in points:
            msg=msg+":"+str(item[0])+','+str(item[1])+'~'
        return msg
    except:
        return "False"



import picamera


def startPatrol():
    points = np.load("points.npy")
    counter = 0
    for point in points:
        point = tuple(point)
        smap.goToPoint(point)
        for x in range(4):
            with picamera.PiCamera() as camera:
                camera.resolution = (1024, 768)
                camera.capture('/patrolPics/pic{}.jpg'.format(str(counter)))
            p.turnleft()
            counter += 1





class myHandler(BaseHTTPRequestHandler):
    global THREADS

    def do_GET(self):
        print("Path-->" + str(self.path))

        if "/main" in self.path:
            t = Thread(target=createScript(), name="Camera")
            THREADS.append(t)
            msg="ok"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        elif "/Login" in self.path:
            if login(self.path, self.client_address[0]) is True:
                msg = "ok" 
            else:
                msg = "no" 
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        elif "Left" in self.path:
            moveLeft()
            self.wfile.write("ok".encode())
            return
        elif "Right" in self.path:
            moveRight()
            self.wfile.write("ok".encode())
            return
        elif "Forward" in self.path:
            moveForward()
            self.wfile.write("ok".encode())
            return
        elif "Map" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            map=getMap()
            self.wfile.write(map.encode())
            return
        elif "savpoints" in self.path:
            msg= "true" if savePoints(self.path) is True else "false"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        elif "getpoints" in self.path:
            msg=getPoint()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(msg.encode())
            return
        elif "patrol" in self.path:
            startPatrol()
            return
        elif "getPicInfo" in self.path:
            import os.path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #filePath = str(os.getcwd())+'/patrolPics'
            #num_files = len([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            points = np.load("points.npy")
            self.wfile.write((str(len(points)*4)+'3').encode())
            return
        elif "getPic" in self.path:
            import os.path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            filePath = str(os.getcwd()) + '/patrolPics/pic' + str(self.path.split("Pic")[1]) +'.jpg'
            imageFile = open(filePath, "rb")
            imageBase64Str = str(base64.b64encode(imageFile.read()))[2:-1]
            self.wfile.write(imageBase64Str.encode())
            #self.wfile.write(filePath.encode())
            return


        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype = 'image/png'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                print("TEST STATIC FILE PATH ", curdir + sep + "serverApp" + self.path)
                print(mimetype)

                if "image" in mimetype:
                    f = open(curdir + sep + "serverApp" + sep + self.path, "rb")
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return
                else:
                    f = open(curdir + sep + "serverApp" + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                resStr = f.read()
                bytes = str.encode(str(resStr))
                self.wfile.write(bytes)
                f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)
    print(str(server.server_address))
    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
