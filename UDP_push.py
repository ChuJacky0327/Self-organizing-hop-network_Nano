import cv2, socket, pickle, os    # Import Modules

# AF_INET refers to the address of family of ip4v
# SOCK_DGRAM means connection oriented UDP protocol
s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)  # Gives UDP protocol to follow
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000) # setSockoptTo open two protocols,SOL_SOCKET: Request applies to socket layer.
serverip="192.168.61.1"       # Server public IP
serverport=2323                # Server Port Number to identify the process that needs to recieve or send packets

cap = cv2.VideoCapture('result.mp4')       # Start Streaming video, will return video from your first webcam

# In order to iterate over block of code as long as test expression is true
while True:
    try:
        ret,frame = cap.read()      # Start Capturing a images/video
        cv2.imshow('frame', frame) # Show Video/Stream
        ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY),30])  # ret will returns whether connected or not, Encode image from image to Buffer code(like [123,123,432....])
        x_as_bytes = pickle.dumps(buffer,protocol = 2)       # Convert normal buffer Code(like [123,123,432....]) to Byte code(like b"\x00lOCI\xf6\xd4...")
        s.sendto(x_as_bytes,(serverip , serverport)) # Converted byte code is sending to server(serverip:serverport)
        if cv2.waitKey(10) == 13:    # Press Enter then window will close
            break
    except:
        print('break')
        break
#s.sendto(b'send',(serverip , serverport))                 
print('OK')   
# Destroy all Windows/close
cv2.destroyAllWindows() 
cap.release()
