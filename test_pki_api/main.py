#!/usr/bin/env python3

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()


class HostInfo(BaseModel):
    host_name: str
    host_ip: str


@app.post("/host_info/")
async def host_info(host_info: HostInfo):
    host_name = host_info.host_name
    host_ip = host_info.host_ip
    bytes_host_name = host_name.encode("ascii")
    bytes_host_ip = host_ip.encode("ascii")
    base64_bytes = base64.b64encode(bytes_host_name, bytes_host_ip)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
