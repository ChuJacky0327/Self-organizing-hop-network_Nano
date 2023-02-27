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
* ifconfig 後若有兩個 interface (wlan0)(wlan1)，即完成。  如下圖所示  
![image](https://github.com/ChuJacky0327/Self-organizing-hop-network_Nano/blob/main/images/wlan1_enable.png) 
