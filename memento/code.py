import wifi
import time
import board
import busio
import digitalio
import sys
import espcamera as camera
import socketpool
import adafruit_requests

print(sys.version)
print("zomg its aliiiive")
print(board.board_id)

print("wifi enabled:", wifi.radio.enabled)
print("ip:", wifi.radio.ipv4_address)
print("ssid:", wifi.radio.ap_info.ssid if wifi.radio.ap_info else None)

WEBHOOK_URL = "http://homeassistant.local:8123/api/webhook/memento_camera"

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)

def post_jpeg(jpg_bytes):
    boundary = "----mementoBoundary"
    headers = {"Content-Type": "multipart/form-data; boundary=%s" % boundary}
    preamble = (
        "--%s\r\n"
        'Content-Disposition: form-data; name="image"; filename="snap.jpg"\r\n'
        "Content-Type: image/jpeg\r\n\r\n"
    ) % boundary
    epilogue = "\r\n--%s--\r\n" % boundary
    body = preamble.encode("utf-8") + jpg_bytes + epilogue.encode("utf-8")
    resp = requests.post(WEBHOOK_URL, data=body, headers=headers)
    print("POST status:", resp.status_code)
    resp.close()

pir = digitalio.DigitalInOut(board.A0)
pir.direction = digitalio.Direction.INPUT

cheese = digitalio.DigitalInOut(board.BUTTON)
cheese.direction = digitalio.Direction.INPUT
cheese.pull = digitalio.Pull.UP

i2c = busio.I2C(board.SCL, board.SDA)

cam = camera.Camera(
    i2c=i2c,
    data_pins=(
        board.CAMERA_DATA2,
        board.CAMERA_DATA3,
        board.CAMERA_DATA4,
        board.CAMERA_DATA5,
        board.CAMERA_DATA6,
        board.CAMERA_DATA7,
        board.CAMERA_DATA8,
        board.CAMERA_DATA9,
    ),
    pixel_clock_pin=board.CAMERA_PCLK,
    external_clock_pin=board.CAMERA_XCLK,
    vsync_pin=board.CAMERA_VSYNC,
    href_pin=board.CAMERA_HREF,
    powerdown_pin=board.CAMERA_PWDN,
    reset_pin=board.CAMERA_RESET,
    pixel_format=camera.PixelFormat.JPEG,
    frame_size=camera.FrameSize.QVGA,
)

print("waiting for action...")

# with open("/writetest.txt", "w") as f: f.write("ok")

last = cheese.value

while True:
    now = cheese.value
    if last and not now:
        jpg = cam.take(1)
        print("say cheese 🧀")
        if jpg:
            post_jpeg(jpg)
    last = now
    """
    print(pir.value)
    if pir.value:
        jpg = cam.take(1)
        print("bytes:", len(jpg))
        # with open("/test.jpg", "wb") as f:
            # f.write(jpg)
    """

    time.sleep(0.05)
