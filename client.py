import cv2
import socket
import threading
import numpy as np
import tkinter as tk
from ui import VideoChatUI

class VideoChatClient:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 클라이언트")       # ui.py 연결
        # VideoChatUI의 on_send_message 추상 메소드를 send_message_to_server로 재정의
        self.ui.on_send_message = self.send_message_to_server
        self.clients = []

        # 소켓 초기화
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 서버에 연결
        self.client_socket.connect(('localhost', 5500))

        # 웹캠 이미지 표시 시작
        self.show_frame()

        # 메세지 수신 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 클라이언트 GUI 시작
        tk.mainloop()
    def show_frame(self):
        # 처리 속도를 높이기위해 프레임 크기를 2의 21승으로 증가시킴
        received_frame_data = self.client_socket.recv(2097152)  # 최대 프레임 크기 제한
        # 서버에서 받아온 프레임의 data타입을 byte에서 numpy array로 변환
        received_frame_array = np.frombuffer(received_frame_data, dtype=np.uint8)
        # 받아온 프레임을 cv2를 이용해 이미지로 변환
        received_frame = cv2.imdecode(received_frame_array, cv2.IMREAD_COLOR)
        # 받아온 이미지 값이 None이 아닐때 이미지 출력
        if received_frame is not None:
            self.ui.show_frame(received_frame)
        # 처리 속도를 높이기 위해 after의 딜레이를 100에서 10으로 줄여줌
        self.ui.window.after(10, self.show_frame)

    def send_message_to_server(self, message):
        # 서버에 메세지 전송
        self.client_socket.send(message.encode())

    def send_message_to_clients(self, message):
        # 서버에서 전송한 메세지를 UI에 출력
        self.ui.receive_message(message)        # 클라이언트에게 받은 메세지를 UI에 표시

    def receive_message(self):
        while True:
            try:
                # 서버에서 메세지를 전송하면 받아오는 코드
                message = self.client_socket.recv(2097152).decode()
                if not message:
                    break
                self.send_message_to_clients(message)   # 서버에게 받은 메세지를 UI에 표시
            except:
                # while문에서 pass는 그냥 넘기기
                pass

if __name__ == "__main__":
    client = VideoChatClient()