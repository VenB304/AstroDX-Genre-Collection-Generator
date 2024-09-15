# AstroDX Genre Collection Generator
- Uses your current levels folder from your device to create the manifest.json files for each genre
- This can also be used for local files in your Windows, it only looks for folders that had "maidata.txt" and takes note of the title, lv_7, and folder name


# Project Setup Instructions

Follow these steps to configure the environment and execute the script.

## Prerequisites

- Windows
  - [rclone](https://rclone.org/downloads/)
  - [WinSFP](https://winfsp.dev/rel/)
  - Python script (`main.py`)
- Android
  - [X-plore File Manager](https://play.google.com/store/apps/details?id=com.lonelycatgames.Xplore)
  - [Shizuku](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api)

## Steps

### 1. Install WinSFP
- Download and install **WinSFP**.

### 2. Download and Extract rclone
- You will most likely be on 64 bit so download Intel/AMD - 64 Bit
- We will setup rclone after setting up android

### 3. Get FTP Server for Android
- You can use **X-plore File Manager** from the Play Store.
  - On its own it does not have access to `android/data`

### 4. Install Shizuku for Android
- Install **Shizuku** to manage privileged access for `android/data`.

### 5. Set Up Shizuku and Authorize X-plore
- Open Shizuku and follow the instructions to set it up. See [this](https://shizuku.rikka.app/guide/setup/#start-via-wireless-debugging) and use Start via Wireless Debugging
- Authorize **X-plore** via Shizuku to allow access to the `android/data` directory.
  - A Prompt will show up if you want to allow **X-plore** to use Shizuku
  - If you missed the prompt you can probably try and manually enable this by going into the App information of **X-plore**, go into Permissions, then Additional Permissions you know the rest

### 6. Activate FTP Service on X-plore
- In X-plore, go to **Show > FTP**. and activate it
- Press FTP to bring down its options, Tap on where it says "Server" 
- Tap on Authentication and change username and password if you want, you can also enable Anonymous Access.

### 7. Open Command Prompt (CMD) at the path of rclone
- You can do this by going into the folder of rclone in windows explorer, tap on the url bar, type in cmd and enter

### 8. Configure rclone
- Upon the cmd loading up, type in the command "rclone config"
- Follow on console instructions
> name
> 15 (FTP)
> 192.168.x.x (you are most like within the same network of you device and your PC, the ip address of your device is most likely listed on the ftp server app)
> username
> port number (the number after the colon in 192.168.1.1:2222)
> password
> enter
> enter
> enter
> y

### 9. Mount FTP Server to a drive letter
> rclone mount [the name of the configuration you did in step 8]: Z:

### 10. Navigate to the "levels" folder and copy path
- When you are at the levels folder, you can copy the path by pressing the url bar of the FIle Explorer

### 11. Execute main.py like how you did for rclone
- run main.py
- Follow on console instructions



