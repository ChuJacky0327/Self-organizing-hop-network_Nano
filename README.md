# Self-organizing-hop-network_Nano
在 Jetson Nano 中使用自組織跳點網路，實現畫面協作共享  
## Step1. Jetson Nano Update
```shell
$ sudo apt update
$ sudo apt install dkms git
$ sudo apt-get update
$ sudo apt upgrade
$ sudo apt-get dist-upgrade
$ git clone https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano.git
$ cd Self-organizing-hop-network_Nano
```
***
## Step2. Wifi dongle tp-link archer T2U plus AC600 driver install
* Jetson Nano 本身沒有網卡，由於要做**跳點網路**需要兩個網路介面，因此要再添加兩隻額外的 Wifi dongle(wlan0)、Wifi dongle(wlan1)。 
* 我的 Jetson Nano wifi配置如下圖，一個採用 tp-link 的小網卡(wlan0)、另一個採用 tp-link AC600(wlan1) ，我會將 wlan1 改為 AP model  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/jetsonNano.jpg) 
* 由於使用 AC600 這隻 Wifi dongle，因此需要進行這一步驟，若不是使用 AC600 或已有第二個 interface，可自行略過此步驟。  
* 參考來源與使用 : [https://blog.cavedu.com/2021/05/13/tp-link-archer-t2u-plus-ac600/](https://blog.cavedu.com/2021/05/13/tp-link-archer-t2u-plus-ac600/)
```shell
$ ifconfig
$ cd AC600/
$ sudo rm /var/lib/dpkg/lock-frontend 
$ sudo rm /var/lib/dpkg/lock
$ sudo dpkg -i *.deb
$ cd rtl8812au/
$ sudo make dkms_install
$ reboot
$ ifconfig
```
* ifconfig 後若有兩個 interface (wlan0)(wlan1)，即完成。如下圖所示:  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/wlan1_enable.png) 
***
## Step3. Jetson Nano AP model
將 wlan1 改成 AP model。
```shell
$ nmcli dev show wlan1
```
> 確保 wlan1 有開啟 

```shell
$ sudo apt install hostapd dnsmasq -y
$ sudo systemctl disable dnsmasq
$ sudo systemctl stop dnsmasq
$ sudo apt install gedit
$ sudo gedit /etc/NetworkManager/NetworkManager.conf
```
**將 NetworkManager.conf 裡的內容新增 :**
```
[main]
dns=dnsmasq
```

&emsp;
```shell
$ nmcli con add type wifi ifname wlan1 mode ap con-name WIFI_AP ssid pig-nano1
$ nmcli con modify WIFI_AP 802-11-wireless.band bg
$ nmcli con modify WIFI_AP 802-11-wireless.channel 1
$ nmcli con modify WIFI_AP 802-11-wireless-security.key-mgmt wpa-psk
$ nmcli con modify WIFI_AP 802-11-wireless-security.proto rsn
$ nmcli con modify WIFI_AP 802-11-wireless-security.group ccmp
$ nmcli con modify WIFI_AP 802-11-wireless-security.pairwise ccmp
$ nmcli con modify WIFI_AP 802-11-wireless-security.psk nano10327
$ nmcli con modify WIFI_AP ipv4.method shared
$ nmcli con up WIFI_AP
```
> * 修改的 interface 為 wlan1  
> * con-name 為檔案的名稱  
> * ssid 為無線網路名稱(可自行設定)  
> * 802-11-wireless-security.psk 為無線網路的密碼(可自行設定)  
### 備註 :
> 如果要換成 5G 的頻段，修改成下面這段
```shell
$ nmcli con modify WIFI_AP 802-11-wireless.band a
$ nmcli con modify WIFI_AP 802-11-wireless.channel 36
```
* 變成這樣即成功，wlan1 預設為10.X.X.X。如下圖所示:  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/wifi_ap.jpg) 


&emsp;
```shell
$ nmcli con modify WIFI_AP ipv4.addr 192.168.61.1/24
```
> * ip address 可自行設定為 192.168.xx.1  '

```shell
$ sudo gedit /etc/NetworkManager/system-connections/WIFI_AP
```
> * 可進入 WIFI_AP 看之前設定的對不對   

```shell
$ sudo systemctl restart NetworkManager 
$ ifconfig
```
> * restart NetworkManager 讓更改生效 
> * ifconfig 後若有更改成你設定的參數，即成功。如下圖所示:  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/wlan1_AP.png)
***
## Step4. Ping Test
手機連上 Jetson Nano 的 AP 網路，去看配到的 ipaddress，用 Jetson Nano 去 ping，若能 ping 到就代表成功。  
```shell
$ ping 192.168.61.208
```
***
## Step5. OpenCV and yolov4-tiny install
* 因為本專案是進行影像畫面的共享傳輸，因此需要安裝 OpenCV和darknet。
* 使用 yolov4-tiny 辨識與儲存影片
```shell
$ git clone https://github.com/AlexeyAB/darknet
$ sudo apt-get install build-essential libpcre3-dev libssl-dev libopencv-dev
```
* 先檢查 Jetson Nano 的 cuda 有沒有開啟
```shell
$ nvcc -V
```
> 若有顯示即有，若沒顯示要做以下步驟，把環境變數加進去
```shell
$ sudo gedit ~/.bashrc
```
**在 bashrc 內容新增 :**
```
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
```shell
$ sudo reboot
```
> 在測一次```  $ nvcc -V ``` 看有沒有成功

&emsp;
```shell
$ cd darknet/
$ sudo gedit Makefile 
```
**在 Makefile 內容修改 :**
```
GPU=1
CUDNN=1
CUDNN_HALF=1
OPENCV=1
```
```shell
$ make
```
> 如果 ``` make ``` 出現錯誤，Makefile:185: recipe for target 'obj/network_kernels.o' failed，則做以下步驟，之後從新make:
```shell
$ sudo gedit src/network_kernels.cu
```
**在 network_kernels 內容修改 :**
```
ctrl+F查找關鍵詞cudaStreamCaptureModeGlobal，把這個參數刪掉(含前面的逗號) 
```
```shell
$ make clean
$ make
```

&emsp;
### 檢查攝影機有沒有接到 :
```shell
$ ls /dev/video*
```  
### 測試 yolov4-tiny 辨識照片 :
```shell
$ ./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights data/person.jpg
```
### 將辨識結果存成 mp4 檔 :
```shell
$ ./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights test.mp4 -out_filename test_yolo.mp4
```
***

## Step6. TensorRT 進行 yolo 辨識推論加速
* 使用 TensorRT 進行推論加速，讓 yolo 的辨識 FPS 更快。  
* 所執行的程式，當辨識到人時且一段時間後，會將辨識影片儲存下來。  
```shell
$ cd Self-organizing-hop-network_Nano
$ bash install_protobuf-3.8.0.sh
$ pip3 install onnx==1.4.1
$ ./install_pycuda.sh
$ cd plugins/
$ make -j4
```
### 備註 :  
> 1. 若編譯失敗需要重新編譯的話，下 ``` $ make clean ```，在 ``` $ make -j4 ```。  
> 2. 上面執行的過程，需要 1~2 個小時的時間。
&emsp;  
* 請自先訓練完 darknet 的 weights，以得到 **.weights** 和 **.cfg** 檔
* 將 **.weights** 和 **.cfg** 檔放入```/Self-organizing-hop-network_Nano/yolo```裡，並修改檔名(檔名最後要是數字，為輸入的大小)
```shell
$ cd ..
$ cd yolo/
$ python3 yolo_to_onnx.py -c 80 -m yolov4-tiny-416
$ python3 onnx_to_tensorrt.py -c 80 -m yolov4-tiny-416
$ cd ..
```
> * 透過 yolo_to_onnx.py 轉成 onnx 檔  
> * 透過 onnx_to_tensorrt.py 轉成 trt 檔  
> * (80 為 classes 的數量)
&emsp;  
### 接上攝影機後，透過 TensorRT 執行辨識，並將辨識到人後將辨識影片存下來 :
```shell
$ python3 trt_yolo.py --usb 0 -c 80 -m yolov4-tiny-416
```

***
## Step7. RTMP install
* 因為本專案是進行影像畫面的共享傳輸，因此需要安裝 RTMP 串流協定。
* 需安裝 nginx-1.16.0 和 ffmpeg。
```shell
$ git clone https://github.com/arut/nginx-rtmp-module.git
$ wget http://nginx.org/download/nginx-1.16.0.tar.gz
$ tar zxvf nginx-1.16.0.tar.gz 
$ sudo apt-get install build-essential libpcre3 libpcre3-dev libssl-dev libopencv-dev 
$ cd nginx-1.16.0/
$ ./configure --add-module=../nginx-rtmp-module
$ make
$ sudo make install
$ sudo gedit /usr/local/nginx/conf/nginx.conf
```
**將 nginx.conf 裡的內容新增下段**
```
rtmp {
	server {
		listen 1935;
		ping 30s;
		notify_method get;
		application rtmp {
			live on;
		}
	}
     }
```
```shell
$ sudo /usr/local/nginx/sbin/nginx
$ sudo apt install -y ffmpeg
$ sudo apt install python3-dev
$ sudo pip3 install --upgrade pip
$ pip3 install -U opencv-python
```
### 備註 :  
> 1. Jetson Nano 開機時，要下```sudo /usr/local/nginx/sbin/nginx```，啟動 nginx 服務。
> 2. 在網頁輸入```localhost```，即可得知 nginx 有無啟動。
> 3. 因為我的 Nano 的映像檔很舊，所以有保留 python2.7 的版本，若```  pip3 install -U opencv-python ```安裝後有 core dump 問題為 numpy 版本為1.19.5的關係。解法為降 numpy 的版本，先```  pip3 uninstall numpy ```，在 ```  pip3 install  ```
***
## Step8. Test and Demo
* 本章節是進行最後的測試與 Demo。  
* 由於本專案會配合 Raspberry Pi 進行開發，因此會分成三個小節執行說明。  
* 我在做 Jetson Nano 的跳點專案開發時，遇到了一些問題，詳細會在各小節內說明，並附上目前的解決方法。  
##### 備註 :
>  我的 Jetson Nano python 版本為 2.7，Raspberry Pi python 版本為 3.6。

&emsp;
### 8.1 Jetson Nano 利用自組織跳點網路傳送影像給 Raspberry Pi :  
* 影像在 Jetson Nano 身上，所以 Jetson Nano 為 client 端，Raspberry Pi 為 server 端。
* Raspberry Pi 開啟 AP，Jetson Nano 的 STA 連上 Raspberry Pi 的 AP，形成自組織的跳點網路。  
#### client 端(Jetson Nano) :
```shell
$ python Nano_push.py
```
#### server 端(Raspberry Pi) :
```shell
$ python3 Nano_pull.py
```
##### 備註 :
> 1.即完成透過 RTMP 進行影像傳輸。  
> 2.傳輸的影像為 Step5 的 yolov4-tiny 辨識結果，可自行更改。  
> 3.要自行更改連到的 ip address，每個人設定的會不一樣，(我的為192.168.53.6)。  

&emsp;
### 8.2  Raspberry Pi 利用自組織跳點網路傳送影像給 Jetson Nano :
* 影像在 Raspberry Pi 身上，所以 Raspberry Pi 為 client 端，Jetson Nano 為 server 端。
* Jetson Nano 開啟 AP，Raspberry Pi 的 STA 連上 Jetson Nano 的 AP，形成自組織的跳點網路。  
##### 備註 :
> * Jetson Nano AP(192.168.61.1)，Raspberry Pi STA(192.168.61.93)。  
> * 這邊發現有 Bug，透過 RTMP 無法連上 Jetson Nano 所分享出去的 AP(192.168.61.93)，連線會被拒絕，因此無法使用 RTMP 傳送影像。  

***
#### Ping test for Raspberry Pi STA:
```shell
$ ping 192.168.61.93
```
> 可看出其實是 ping 的到的，代表 AP 所分享出去的網路是可以連接的。

***
#### 改用 iperf3 測試 :
```shell
$ sudo apt-get install iperf3
```
#### iperf3 for TCP packet: 
* 要打封包測試 192.168.61.93 是否可以連通。所以 Raspberry Pi 為 server 端，Jetson Nano 為 client 端。
#### server 端(Raspberry Pi) :
```shell
$ iperf3 -s
```
#### client 端(Jetson Nano) :
```shell
$ iperf3 -c 192.168.61.93 -t 30 
```
*  iperf3 結果:  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/Nano_AP_iperf3_tcp.png)
> 經過測試發現 TCP 的連接被阻擋掉了，無法接收到封包，因此換 UDP 試試。 
 
***
#### iperf3 for UDP packet: 
* 要打封包測試 192.168.61.93 是否可以連通。所以 Raspberry Pi 為 server 端，Jetson Nano 為 client 端。
#### server 端(Raspberry Pi) :
```shell
$ iperf3 -s
```
#### client 端(Jetson Nano) :
```shell
$ iperf3 -c 192.168.61.93 -t 30 -u -b 0
```
*  iperf3 結果:  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/Nano_AP_iperf3_udp.png)
> 經過測試發現 UDP 的封包是可以傳送到的，因此改用 UDP 的影像串流方法 (socket)。  

***
* 使用 socket 進行自組織跳點網路影像傳送:
#### client 端(Raspberry Pi) :
```shell
$ python3 UDP_push.py
```
#### server 端(Jetson Nano) :
```shell
$ python UDP_pull.py
```
##### 備註 :
> * 要自行更改連到的 ip address，每個人設定的會不一樣。  
> * UDP socket 推送，經實驗後得知，推流的話都可以推到任何的ip address，拉流只能拉自己 ifconfig 看的到的 ip address，因此 UDP socket 改送(192.168.61.1)。  
> * 由於我的 Jetson Nano python 版本為 2.7，Raspberry Pi python 版本為 3.6，因此在用到 pickle 時要補上 protocol = 2，不然 python 3.X 的資料無法傳給 python2.X。   

&emsp;
### 8.3 Jetson Nano 利用自組織跳點網路傳送影像給 Jetson Nano :
* 同 7.2 一樣的問題，解法與 7.2 一樣，可自行往 7.2 小節去看。
* 使用 socket 進行自組織跳點網路影像傳送:
#### client 端(Raspberry Pi) :
```shell
$ python3 UDP_push.py
```
#### server 端(Jetson Nano) :
```shell
$ python UDP_pull.py
```
> 即完成自組織跳點網路的影像傳送_Nano版







