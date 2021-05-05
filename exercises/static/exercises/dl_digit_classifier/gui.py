import json
import cv2
import base64
import threading
import time
from datetime import datetime
from websocket_server import WebsocketServer

import logging


# Graphical User Interface Class
class GUI:
    # Initialization function
    # The actual initialization
    def __init__(self, host, console, hal):
        t = threading.Thread(target=self.run_server)

        self.payload = {'image': '', 'shape': [], 'text_buffer': ''}
        self.server = None
        self.client = None

        self.host = host

        # Image variables
        self.image_to_be_shown = None
        self.digit_to_be_shown = None
        self.image_to_be_shown_updated = False
        self.image_show_lock = threading.Lock()

        self.acknowledge = False
        self.acknowledge_lock = threading.Lock()

        # Take the console object to set the same websocket and client
        self.console = console
        self.hal = hal
        t.start()

    # Explicit initialization function
    # Class method, so user can call it without instantiation
    @classmethod
    def initGUI(cls, host, console):
        # self.payload = {'image': '', 'shape': []}
        new_instance = cls(host, console)
        return new_instance

    # Function to prepare image payload
    # Encodes the image as a JSON string and sends through the WS
    def payloadImage(self):
        self.image_show_lock.acquire()
        image_to_be_shown_updated = self.image_to_be_shown_updated
        image_to_be_shown = self.image_to_be_shown
        digit_to_be_shown = self.digit_to_be_shown
        self.image_show_lock.release()

        image = image_to_be_shown
        payload = {'image': '', 'shape': '', 'digit': ''}

        if (image_to_be_shown_updated == False):
            return payload

        shape = image.shape
        frame = cv2.imencode('.JPEG', image)[1]
        encoded_image = base64.b64encode(frame)

        payload['image'] = encoded_image.decode('utf-8')
        payload['shape'] = shape
        payload['digit'] = digit_to_be_shown

        self.image_show_lock.acquire()
        self.image_to_be_shown_updated = False
        self.image_show_lock.release()

        return payload

    # Function for student to call
    def showResult(self, image, digit):
        self.image_show_lock.acquire()
        self.image_to_be_shown = image
        self.digit_to_be_shown = digit
        self.image_to_be_shown_updated = True
        self.image_show_lock.release()

    # Function to get the client
    # Called when a new client is received
    def get_client(self, client, server):
        self.client = client
        self.console.set_websocket(self.server, self.client)

    # Function to get value of Acknowledge
    def get_acknowledge(self):
        self.acknowledge_lock.acquire()
        acknowledge = self.acknowledge
        self.acknowledge_lock.release()

        return acknowledge

    # Function to get value of Acknowledge
    def set_acknowledge(self, value):
        self.acknowledge_lock.acquire()
        self.acknowledge = value
        self.acknowledge_lock.release()

    # Update the gui
    def update_gui(self):
        # Payload Image Message
        payload = self.payloadImage()
        self.payload["image"] = json.dumps(payload)

        # Payload Console Messages
        message_buffer = self.console.get_text_to_be_displayed()
        self.payload["text_buffer"] = json.dumps(message_buffer)

        message = "#gui" + json.dumps(self.payload)
        self.server.send_message(self.client, message)

    # Function to read the message from websocket
    # Gets called when there is an incoming message from the client
    def get_message(self, client, server, message):
        # Acknowledge Message for GUI Thread
        if (message[:4] == "#ack"):
            self.set_acknowledge(True)

        # Message for Console
        elif (message[:4] == "#con"):
            self.console.prompt(message)

    # Activate the server
    def run_server(self):
        self.server = WebsocketServer(port=2303, host=self.host)
        self.server.set_fn_new_client(self.get_client)
        self.server.set_fn_message_received(self.get_message)
        self.server.run_forever()


# This class decouples the user thread
# and the GUI update thread
class ThreadGUI(threading.Thread):
    def __init__(self, gui):
        self.gui = gui
        # Time variables
        self.time_cycle = 80
        self.ideal_cycle = 90
        self.iteration_counter = 0

    # Function to start the execution of threads
    def start(self):
        self.measure_thread = threading.Thread(target=self.measure_thread)
        self.thread = threading.Thread(target=self.run)

        self.measure_thread.start()
        self.thread.start()

        print("GUI Thread Started!")

    # The measuring thread to measure frequency
    def measure_thread(self):
        while (self.gui.client == None):
            pass

        previous_time = datetime.now()
        while (True):
            # Sleep for 2 seconds
            time.sleep(2)

            # Measure the current time and subtract from previous time to get real time interval
            current_time = datetime.now()
            dt = current_time - previous_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            previous_time = current_time

            # Get the time period
            try:
                # Division by zero
                self.ideal_cycle = ms / self.iteration_counter
            except:
                self.ideal_cycle = 0

            # Reset the counter
            self.iteration_counter = 0

    def run(self):
        while (self.gui.client == None):
            pass

        while (True):
            start_time = datetime.now()
            self.gui.update_gui()
            acknowledge_message = self.gui.get_acknowledge()

            while (acknowledge_message == False):
                acknowledge_message = self.gui.get_acknowledge()

            self.gui.set_acknowledge(False)

            finish_time = datetime.now()
            self.iteration_counter = self.iteration_counter + 1

            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            if (ms < self.time_cycle):
                time.sleep((self.time_cycle - ms) / 1000.0)
