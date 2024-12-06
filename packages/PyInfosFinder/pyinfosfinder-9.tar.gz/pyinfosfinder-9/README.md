# PyMalWare - Info Stealer Toolkit

**Note**: The use of this toolkit for malicious purposes, such as unauthorized access to systems, stealing information, or causing harm to others, is **illegal** and **unethical**. This repository is provided for educational purposes only, and the code should not be used for any harmful activity.

## Description

`PyMalWare` is a Python-based malware/info-stealer toolkit that collects a variety of system and user information, including:

- **IP address**
- **Geolocation**
- **Hardware details (CPU, GPU, RAM, etc.)**
- **System configuration**
- **Battery and uptime status**
  
The collected data can be sent to an external server or saved locally for further analysis.

This toolkit is a demonstration of how data can be extracted from a system, and it can be useful for security researchers and penetration testers who are interested in understanding how malicious software works.

## Features

- **IP Address**: Retrieves the public IP of the system.
- **Hardware ID (HWID)**: Fetches unique hardware identifiers.
- **Geolocation**: Uses the public IP to get location data (latitude, longitude, etc.).
- **System Information**: Gathers information on the system's CPU, GPU, RAM, OS, and more.
- **Battery and Uptime**: Provides battery status and system uptime.
- **And other usefull things like:**

- **Cookie Stealer**: put all the password with user and url in a txt file called "data.txt" in the temp folder, the function will return the path of the file, so you can delete it after uploading it to a discord webhook / a server
- **Discord Token Finder**: returns all the detected tokens on the user's machine
- 

## Installation

To use the toolkit, clone this repository and install the required dependencies:

```bash
git clone https://github.com/your-username/PyMalWare.git
cd PyMalWare
pip install -r requirements.txt
```

## Ethical Considerations

WARNING: This code is a demonstration of how malicious software works, and it should never be used for malicious purposes. Using this code to steal personal information, spy on users, or damage systems is illegal and unethical.

If you are interested in learning about cybersecurity or ethical hacking, always ensure that you have explicit permission from the system owner and follow legal guidelines.
Legal and Ethical Hacking Practices

If you're interested in improving your understanding of security and ethical hacking, here are some responsible activities you can engage in:

    Penetration testing (with explicit permission)
    Capture the flag (CTF) challenges
    Security research on public systems

Always use your skills in a responsible, ethical, and legal manner.