import os
from ultralytics import YOLO
import torch
import cv2
import socket
import pickle
import struct
import threading
import time
# import concurrent.futures
from playsound import playsound
torch.cuda.set_device(0)
model = YOLO("yolov8s.pt")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.101', 8888))  # Replace 'server_ip_address' with the actual server IP
data = b""
payload_size = struct.calcsize("Q")
object_detected = False
detection_lock = threading.Lock()

def make_sound():
    os.system("curl http://192.168.1.101:8080/hissing")
    timer_reset()

def reset_detection_flag():
    print("timer created")
    global object_detected
    object_detected = False
    
def show_frame(label, frame):
    cv2.imshow(label, frame)

def timer_reset():
    print("time")
    time.sleep(5)
    reset_detection_flag()

def process_frame(video_frame):
    global object_detected
    results = model(video_frame)
    annotated_frame = results[0].plot()
    try:
        r = results[0]
        for i in range(0,len(r.boxes.cls)):
            cls = r.boxes.cls[i]
            conf = r.boxes.conf[i].item()
            name_idx = int(cls.item())
            name = r.names[name_idx]
            print(name, conf)
            print(object_detected)
            with detection_lock:
                if name == 'cat' and conf > 0.6 and not object_detected:
                    object_detected = True
                    t1 = threading.Thread(target=make_sound)
                    t1.start()

                    break
            t2 = threading.Thread(target=show_frame("YOLOv8 Inference", annotated_frame))
            t2.start() 
    except Exception as e:
            print(e)
    return object_detected

if __name__ == "__main__":
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        if not data:
            break
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)  # 4K buffer size
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        results = process_frame(frame)
            
        if cv2.waitKey(1) == 13:
            break
    cv2.destroyAllWindows()
