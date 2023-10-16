import cv2
import socket
import threading
import tkinter as tk
from ui import VideoChatUI


class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")      # ui.py 연결
        # VideoChatUI의 on_send_message 추상 메소드를 send_message_to_clients로 재정의
        self.ui.on_send_message = self.send_message_to_clients
        # 클라이언트를 초기화, 클라이언트의 정보를 저장하는 변수
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 소켓 열기
        self.server_socket.bind(('0.0.0.0', 5500))
        self.server_socket.listen(5)

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        # 서버에 영상 표출함
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        # 클라이언트에 메세지 전송
        for client in self.clients:
            client.send(message.encode())
        # 서버 UI에도 메세지 표시
        self.ui.receive_message(message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message)        # 서버에서 받은 메세지를 UI에 표시
        self.send_message_to_clients(message)   # 받은 메세지를 다른 클라이언트들에게 전송


    def send_webcam(self):
        while True:
            # 카메라의 프레임 읽어오기
            ret, frame = self.cap.read()
            if not ret:
                continue
            # 이미지의 rgb 값을 bgr로 변환하여 처리
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # 이미지의 60%의 퀄리티의 jpg로 변환후 인코딩
            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            # 이미지를 byte로 변환
            encoded_frame = encoded_frame.tobytes()
            # 각 클라이언트마다 전송
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            # 서버 UI에도 비디오 화면 표시
            self.show_frame(frame)

    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        while True:
            try:
                # 클라이언트에서 보내는 메세지 받아오기
                message = client_socket.recv(1024).decode()
                if not message:
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                self.send_message_to_server(message)    # 클라이언트에서 받은 메세지를 서버로 전송
            except:
                pass

    def receive_clients(self):
        # 클라이언트와 연결후 클라이언트 마다 스레드 생성
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.daemon = True
            client_handler.start()


if __name__ == "__main__":
    server = VideoChatServer()