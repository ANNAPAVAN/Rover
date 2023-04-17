from __future__ import print_function
# from dronekit import connect, VehicleMode
from dronekit import connect, VehicleMode, LocationGlobalRelative

import time
import argparse

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()
connection_string = args.connect

print("Connecting to the vehicle on", connection_string)
vehicle = connect(connection_string, wait_ready=True)

# def arm_and_takeoff():
#     while not vehicle.is_armable:
#         print("Waiting for vehicle to initialise...")
#         time.sleep(1)
#     print("Arming motors")
#     vehicle.mode = VehicleMode("GUIDED")
#     vehicle.armed = True
#     while not vehicle.armed:
#         print("Waiting for arming...")
#         time.sleep(1)
#     print("Taking off!")
#     vehicle.simple_takeoff(20)
#     while True:
#         print(" Altitude: ", vehicle.location.global_relative_frame.alt)
#         if vehicle.location.global_relative_frame.alt >= 19.5:
#             print("Target altitude reached")
#             break
#         time.sleep(1)
def arm():
    while not vehicle.is_armable:
        print("Waiting for initializing")
        time.sleep(1)
    print("Arming motors")
    vehicle.mode=VehicleMode("GUIDED")
    vehicle.armed=True
    while not vehicle.armed:
        print("Waiting for arming")
        time.sleep(1)

def move_left(distance):
    current_location = vehicle.location.global_relative_frame
    target_location = LocationGlobalRelative(current_location.lat, current_location.lon - distance, current_location.alt)
    print("Moving left")
    vehicle.simple_goto(target_location)

def move_right(distance):
    current_location = vehicle.location.global_relative_frame
    target_location = LocationGlobalRelative(current_location.lat, current_location.lon + distance, current_location.alt)
    print("Moving right")
    vehicle.simple_goto(target_location)

def move_forward(distance):
    current_location = vehicle.location.global_relative_frame
    target_location = LocationGlobalRelative(current_location.lat + distance, current_location.lon, current_location.alt)
    print("Moving forward")
    vehicle.simple_goto(target_location)

def move_backward(distance):
    current_location = vehicle.location.global_relative_frame
    target_location = LocationGlobalRelative(current_location.lat - distance, current_location.lon, current_location.alt)
    print("Moving backward")
    vehicle.simple_goto(target_location)

def disarm():
    print("Disarming...")
    vehicle.mode = VehicleMode("LAND")
    vehicle.armed = False
    while vehicle.armed:
        print("Waiting for disarm...")
        time.sleep(1)
    print("Vehicle disarmed")

while True:
    try:
        cmd = raw_input("Enter command: ")
        d = int(raw_input("Enter distance: "))
        if cmd == "arm":
            arm()
        elif cmd == "left":
            move_left(d)
        elif cmd == "right":
            move_right(d)
        elif cmd == "forward":
            move_forward(d)
        elif cmd == "backward":
            move_backward(d)
        elif cmd == "disarm":
            disarm()
            break
        else:
            print("Invalid command")
    except KeyboardInterrupt:
        disarm()
        break

