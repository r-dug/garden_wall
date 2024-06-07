import cv2
import socket
import pickle
import struct

# connect a socket to stream to the client, which will process the data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8888))
server_socket.listen(5)
print("Server is listening...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} accepted")




while True:
    run = True
    cap = cv2.VideoCapture(0)
    while run == True:
        ret, video_frame = cap.read()  # read frames from the video
        frame_data = pickle.dumps(video_frame)
        client_socket.sendall(struct.pack("Q", len(frame_data)))
        client_socket.sendall(frame_data)

        cv2.imshow('Server', video_frame)
        cv2.waitKey(100)
    if cv2.waitKey(1) == 13:
        break
cap.release()
cv2.destroyAllWindows()
