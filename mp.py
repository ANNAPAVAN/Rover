
# dronekit-sitl copter
# python mp.py --connect 127.0.0.1:14551
# mavproxy.exe --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551
# 
from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()
connection_string = args.connect

print("Connecting to vehicle on: ", connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(target_altitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached!")
            break
        time.sleep(1)


arm_and_takeoff(10)

print("Setting airspeed to 7 m/s")
vehicle.airspeed = 7

print("Going towards first point for 30 seconds...")
point1 = LocationGlobalRelative(15.5057, 80.0499, 10)
vehicle.simple_goto(point1)

time.sleep(30)

print("Returning to launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
vehicle.close()
