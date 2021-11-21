# BUAA Gateway Login

Automatically login to BUAA-WiFi gateway by using Firefox and Selenium, especially useful for device without GUI like Raspberry Pi, etc.

## How to use

Before you can use this tool, Firefox has to be installed and added in `PATH`.

Then you just need to clone this repo, and execute the shell script.

Detailed steps are below:

1. clone this repo

   ```bash
   git clone https://github.com/badcodebuilder/buaagwlogin.git --depth=1
   ```

2. edit the config file and run the shell script

   ```bash
   cd buaagwlogin
   touch config.json && vim config.json
   ./run.sh
   ```
   
# TODO

1. Store account information securely or directly get password from input.
2. Flow usage alert and auto-disconnection