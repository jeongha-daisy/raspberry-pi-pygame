import socket
import RPi.GPIO as GPIO
import smbus
import time
import threading

# 서버 설정
SERVER_IP = '10.125.126.21'
EVENT_PORT = 9000       # 이벤트용 포트
JOYSTICK_PORT = 5000    # 조이스틱용 포트

# 조이스틱 설정
address = 0x48
A0 = 0x40
A1 = 0x41
bus = smbus.SMBus(1)

# GPIO 핀 설정
SHOCK_PIN = 17
BUTTON_PIN = 18
SOUND_PIN = 19
LIGHT_PIN = 27

# 소켓 선언 (초기 None)
event_client = None
joystick_client = None

# 이벤트 큐
event_queue = []

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(SHOCK_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(SOUND_PIN, GPIO.IN)

# 0.2초동안 들어온 값 없도록 하기
def stable_input(pin, target_state, duration=0.2):
    start = time.time()
    while time.time() - start < duration:
        if GPIO.input(pin) != target_state:
            return False
        time.sleep(0.01)
    return True

# 이벤트 콜백
def shock_detected(channel):
    if stable_input(SHOCK_PIN, GPIO.LOW):
        print("Shock detected")
        event_queue.append("shock")

def button_pressed(channel):
    if stable_input(BUTTON_PIN, GPIO.LOW):
        print("Button pressed")
        event_queue.append("button")

def light_detected(channel):
    if stable_input(LIGHT_PIN, GPIO.HIGH):
        print("Light detected")
        event_queue.append("light")

def sound_detected(channel):
    if stable_input(SOUND_PIN, GPIO.HIGH):
        print("Sound detected")
        event_queue.append("sound")

    
# 이벤트 감지 등록
GPIO.add_event_detect(SHOCK_PIN, GPIO.FALLING, callback=shock_detected, bouncetime=200)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)
GPIO.add_event_detect(LIGHT_PIN, GPIO.RISING, callback=light_detected, bouncetime=200)
GPIO.add_event_detect(SOUND_PIN, GPIO.RISING, callback=sound_detected, bouncetime=200)

# 소켓 연결 함수
def connect_socket(port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, port))
            print(f"Connected to port {port}")
            return s
        except Exception as e:
            print(f"Connection failed to port {port}: {e}")
            time.sleep(3)

# 이벤트 전송 스레드
def process_events():
    global event_client
    event_client = connect_socket(EVENT_PORT)

    while True:
        if event_queue:
            message = event_queue.pop(0)
            try:
                event_client.sendall(message.encode('utf-8'))
            except Exception as e:
                print("Event send error:", e)
                try:
                    event_client.close()
                except:
                    pass
                event_client = connect_socket(EVENT_PORT)
        time.sleep(0.05)

# 조이스틱 데이터 전송 스레드
def joystick_loop():
    global joystick_client
    joystick_client = connect_socket(JOYSTICK_PORT)

    while True:
        try:
            bus.write_byte(address, A0)
            time.sleep(0.01)
            value1 = bus.read_byte(address)

            bus.write_byte(address, A1)
            time.sleep(0.01)
            value2 = bus.read_byte(address)

            message = f"{value1},{value2}"
            joystick_client.sendall(message.encode('utf-8'))
            print("🎮 Joystick:", message)

        except Exception as e:
            print("Joystick error:", e)
            try:
                joystick_client.close()
            except:
                pass
            joystick_client = connect_socket(JOYSTICK_PORT)
        time.sleep(0.1)

# 스레드 시작
threading.Thread(target=process_events, daemon=True).start()
threading.Thread(target=joystick_loop, daemon=True).start()

# 메인 루프
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    if event_client:
        event_client.close()
    if joystick_client:
        joystick_client.close()