# AstroDX Genre Collection Generator

This tool uses your device’s "levels" folder to generate `manifest.json` files for each genre, enabling better organization of your game data. It can also scan local directories on Windows, identifying folders containing a `maidata.txt` file and extracting relevant data like the title, `lv_7`, and folder name.

The generated `manifest.json` files are saved in a folder named `Collection` within the same directory as the Python script.

Due to the complexity of interfacing with Android storage, this solution is designed to work within the limitations of the device.

## Project Setup Instructions

Follow these steps to configure the environment and execute the script.

### Prerequisites

- **Windows**
  - [rclone](https://rclone.org/downloads/)
  - [WinSFP](https://winfsp.dev/rel/)
  - Python script (`main.py`)
- **Android**
  - [X-plore File Manager](https://play.google.com/store/apps/details?id=com.lonelycatgames.Xplore)
  - [Shizuku](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api)

## Steps

### 1. Install WinSFP
- Download and install **WinSFP**.

### 2. Download and Extract rclone
- Download the Intel/AMD - 64 Bit version (if on a 64-bit system).
- Setup rclone after configuring Android.

### 3. Get FTP Server for Android
- Install **X-plore File Manager** from the Play Store.
  - Note: X-plore does not have access to `android/data` by default.

### 4. Install Shizuku for Android
- Install **Shizuku** to manage privileged access to `android/data`.

### 5. Set Up Shizuku and Authorize X-plore
- Open Shizuku and follow the [guide](https://shizuku.rikka.app/guide/setup/#start-via-wireless-debugging) to set it up using wireless debugging.
- Authorize **X-plore** via Shizuku to allow access to `android/data`.
  - A prompt will appear to enable Shizuku for X-plore.
  - If missed, go to **X-plore** app permissions and manually enable Shizuku access.

### 6. Activate FTP Service on X-plore
- In X-plore, go to **Show > FTP** and activate it.
- Tap on "Server" and adjust the username and password as needed (or enable anonymous access).

### 7. Open Command Prompt (CMD) in the rclone directory
- Navigate to the rclone folder in Windows Explorer, type `cmd` in the URL bar, and hit Enter.

### 8. Configure rclone
- In the command prompt, run `rclone config`.
- Follow the on-screen instructions:
  - Name the configuration.
  - Choose FTP (option 15).
  - Input the IP address of your Android device (visible in X-plore FTP settings).
  - Enter the FTP port number (after the colon in `192.168.1.1:2222`).
  - Provide the FTP username and password.
  - Confirm all options with Enter and choose "y" when prompted.

### 9. Mount the FTP Server to a drive letter
- Run the command: `rclone mount [config name]: Z:`

### 10. Navigate to the "levels" folder and copy the path
- In Windows Explorer, go to the "levels" folder and copy its path from the URL bar.

### 11. Execute `main.py`
- Run `main.py` in the same way as rclone.
- Follow the console instructions to complete the process.
