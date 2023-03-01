import cv2, socket, numpy, pickle    # Import Modules

# AF_INET refers to the address of family of ip4v
# SOCK_DGRAM means connection oriented UDP protocol
s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)  # Gives UDP protocol to follow
ip="192.168.61.1"   # Server public IP
port=2323             # Server Port Number to identify the process that needs to recieve or send packets
s.bind((ip,port))     # Bind the IP:port to connect 
s.settimeout(2)
i = 0
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('result.mp4', fourcc, 20.0, (320,  240))
# In order to iterate over block of code as long as test expression is true
while True:
    try:
        i = i+1
        x=s.recvfrom(100000000)    # Recieve byte code sent by client using recvfrom
        clientip = x[1][0]         # x[1][0] in this client details stored,x[0][0] Client message Stored
        data=x[0]                  # Data sent by client
        data=pickle.loads(data)    # All byte code is converted to Numpy Code 
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)  # Decode 
        cv2.imshow('my pic', data) # Show Video/Stream
        print(data)
        #out.write(data)
	cv2.imwrite('imgs/'+str(i)+'.jpg', data)
        if cv2.waitKey(10) == 13:  # Press Enter then window will close
            break
    except:
        print("receive frame is over")
        print("save video")
        break
#out.release()
cv2.destroyAllWindows()        # Close all windows

import os  
img = cv2.imread('imgs/1.jpg') 
print('ok')
size = (img.shape[1],img.shape[0]) 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
videoWrite = cv2.VideoWriter('results.mp4',fourcc,20,size)
files = os.listdir('imgs/') 
out_num = len(files) 
print(out_num)
for i in range(1, out_num+1): 
	fileName = "imgs/"+str(i)+'.jpg' 
	img = cv2.imread(fileName) 
	videoWrite.write(img)
videoWrite.release()
