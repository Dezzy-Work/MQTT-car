import socket
import pygame, random

from paho.mqtt import client as mqtt_client
from config.config import *

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

def connect_mqtt(): #Connecting to mqtt server
    def on_connect(rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.connect(broker, port)

    return client

global client

def run():
    global client

    client = connect_mqtt()
    client.loop_start()

def publish(client, msg, topic):

    client.publish(topic, msg)

# information
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set screen width and height (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()

pygame.joystick.init()

textPrint = TextPrint()

run()

# -------- Main program loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    screen.fill(WHITE)
    textPrint.reset()

    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):

            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            global client
            if i == 0:


                if round(axis) == -1:

                    publish(client, 60, "robot/rotate")
                    print('send')
                elif round(axis) == 1:

                    publish(client, 120, "robot/rotate")
                    print('send')


            if i == 5:
                if axis != -1:
                        publish(client, 1, "robot/forward")
                else:
                    publish(client, 1, "robot/stop")

            if i == 4:
                if axis != -0.0078125:

                    if round(axis) == 1:

                        publish(client, 1, "robot/backward")
                        print('send')



        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
            if i == 0:
                if button == 1:
                    publish(client, 1, "robot/stop")
            if i == 1:
                if button == 1:
                    publish(client, 90, "robot/rotate")
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()



    pygame.display.flip()

    # Limit to 20 FPS.
    clock.tick(20)

pygame.quit()
