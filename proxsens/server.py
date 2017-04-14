from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import os
import cgi
import json
import subprocess
import traceback
import datetime
import requests
import time

PORT_NUMBER = 8080

USERS_DICT = {"admin": "admin"}


def createScript(ip):
    try:
        gotBlocked = ' #!/bin/bash \n clear \n raspivid -n -t 0 -rot 0 -w 960 -h 720 -fps 30 -b 6000000 -o - | gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=' + str(
            ip) + ' port=5000'
        filePath = str(os.path.dirname(os.path.abspath(__file__))) + "/" + "data.sh"
        with open(filePath, 'w') as outfile:
            outfile.write(gotBlocked)
        print("Data Has Been Saved")
        os.system("chmod +x data.sh")
        os.system("./data.sh")
        print("Done")
    except:
        print("Falied To Save GotBlock File...")
        print(traceback.format_exc())


def login(path):
    print("In Login(")
    try:
        userName = path[path.index("?") + 6:path.index("&")]
        password = path[path.index("&") + 6:]
    except:
        return False

    print("user: "+userName)
    print("pass: "+password)
    if userName in USERS_DICT:
        if password == USERS_DICT[userName]:
            return True
        else:
            return False
    else:
        return False


class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        print("Path-->" + str(self.path))

        if "/main" in self.path:
            createScript(self.client_address[0])
        elif "/Login" in self.path:
            if login(self.path) is True:
                msg = "ok"
            else:
                msg = "notok"
            js = {"res": msg}
            self.send_response(200)
            self.wfile.write(json.dumps(js))
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
