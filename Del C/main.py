# Install FastAPI framework
# pip3 install "fastapi[all]"
# https://fastapi.tiangolo.com/tutorial/

# uvicorn main:app --reload

import uvicorn

from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from typing import Union

from demohouse import build_demo_house
from device import Device
from sensors import *
from actuators import *

app = FastAPI()

smart_house = build_demo_house()

# http://localhost:8000/welcome/index.html
app.mount("/welcome", StaticFiles(directory="static"), name="static")


# http://localhost:8000/
@app.get("/")  # Information on the smart house
async def root():
    return {"message": "Welcome to SmartHouse Cloud REST API - Powered by FastAPI"}


@app.get("/smarthouse/floor/")  # information on all floors
async def read_floors():
    return smart_house.floors


@app.get("/smarthouse/floor/{fid}/")  # information about a floor given by fid
async def read_floor(fid: int, response: Response):
    floor = smart_house.get_floor(fid)
    if floor:
        return floor
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    return None


@app.get("/smarthouse/floor/{fid}/room/")  # information about all rooms on a given floor fid
async def read_rooms(fid: int, response: Response):
    floor = smart_house.get_floor(fid)
    if floor:
        return floor.rooms
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    return None


@app.get("/smarthouse/floor/{fid}/room/{rid}/")  # information about a specific room rid on a given floor fid
async def read_room(rid: int, fid: int, response: Response):
    floor = smart_house.get_floor(fid)
    if floor:
        room = floor.get_room(rid)
        if room:
            return room
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    return None


@app.get("/smarthouse/device/")  # information on all devices
async def read_devices():
    return smart_house.get_device_list()


@app.get("/smarthouse/device/{did}/")  # information for a given device did
async def read_device(did: int, response: Response):
    device = smart_house.get_device(did)
    if device:
        return device
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None


@app.get("/smarthouse/sensor/{did}/current/")  # get current sensor measurement for sensor did
async def read_sensor_value(did: int, response: Response):
    device = smart_house.get_device(did)
    if device and isinstance(device, Sensor):
        return {"value": device.get_current_value(), "unit": device.get_unit()}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None


@app.post("/smarthouse/sensor/{did}/current/", status_code=201)  # add measurement for sensor did
async def add_measurement(did: int, measurement: SensorMeasurement):
    device = smart_house.get_device(did)
    if device and isinstance(device, Sensor):
        device.set_current_value(float(measurement.value))
        return measurement
    else:
        return None


@app.get(
    "/smarthouse/sensor/{did}/values")  # get n latest available measurements for sensor did. If query parameter not present, then all available measurements.
async def read_specific_meas(did: int, response: Response, limit: int | None = None):
    device = smart_house.get_device(did)
    if device and isinstance(device, Sensor):
        if limit is None:
            return {"values": device.get_current_values()}
        else:
            return {"values": device.get_current_values()[0: limit]}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    return None




@app.delete("/smarthouse/sensor/{did}")  # delete oldest measurements for sensor did
async def delete_oldest_meas(did: int, response: Response):
    device = smart_house.get_device(did)
    if device and isinstance(device,Sensor):
        if len(device.get_current_values()) > 0:
            device.delete_oldest_value()
        return device.get_current_values()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None


@app.get("/smarthouse/actuator/{did}/current/")  # get current state for actuator did
async def read_current_state(did: int, response: Response):
    device = smart_house.get_device(did)
    if device and isinstance(device, Actuator):
        return {"state": device.get_current_state()}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None



@app.put("/smarthouse/actuator/{did}/current")  # update current state for actuator did
async def update_actuator_state(did: int, state: ActuatorState, response: Response):
    device = smart_house.get_device(did)

    device = smart_house.read_device(did)

    if device and device.is_actuator():
        device.set_current_state(state.state)

    return device



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8081)
