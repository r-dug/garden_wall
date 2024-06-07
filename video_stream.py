import cv2
import time
from ultralytics import YOLO
import torch
from playsound import playsound

torch.cuda.set_device(0)
model = YOLO("yolov8s.pt")


cat_count = 0
bird_count = 0 
all_count = 0
run = True
while True:
    time.sleep(1/2)
    run = True
    cap = cv2.VideoCapture(0)
    while run == True:
        # cv2.waitKey(50)
        result, video_frame = cap.read()  # read frames from the video
        print(result)
        results = model(video_frame)


        annotated_frame = results[0].plot()
        try:
            r = results[0]
            # print(r.names)            
            for i in range(0,5):
                cls = r.boxes.cls[i]
                conf = r.boxes.conf[i].item()
                name_idx = int(cls.item())
                name = r.names[name_idx]
                print(name, conf)
                if name == 'cell phone' and conf > 0.6:
                    
                    run = False
                
            cv2.imshow("YOLOv8 Inference", annotated_frame)
        except Exception as e:
            print(e)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.waitKey(500)
    playsound('getoffyerphone.mp3')
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cv2.waitKey(0)
cv2.destroyAllWindows()
