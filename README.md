# Terminal keylogger

This is a terminal application that provides a keylogging feature. It records the time spend, the keystrokes quantity and the typing speed. Additionally, you can look at your statistics for available dates by using extra flags.
1. [Setup](#setup)
   1. [Clone repository](#1-clone-repository)
   2. [Create a virtual environment](#2-create-a-virtual-environment)
2. [Functionality](#functionality)
   1. [Start menu](#1-start-menu)
   2. [Recording](#2-recording)
   3. [Record statistics](#3-record-statistics)
   4. [View statistics for another days](#4-view-statistics-for-another-days)
   5. [Help message](#5-help-message)
3. [Bash script](#bash-script)
4. [Configuring](#configuring)

<a id=""></a>
## Setup
An application requires `python 3.10.4`, can be a higher version.

<a id="clone-repository"></a>
### 1. Clone repository
```
$ git clone https://github.com/BorisPlaton/keylogger.git
$ cd keylogger
```
<a id="virtual"></a>
### 2. Create a virtual environment
```
$ sudo apt update && sudo apt install virtualenv
$ virtualenv --python=3.10.4 venv
$ ./venv/bin/activate
$ pip install -r requirements.txt
```
<a id="functionality"></a>
## Functionality
<a id="start-menu"></a>
### 1. Start menu
To run the program you have to write the following:
```
$ cd src
$ ./main.py
```
This will print:
```
Menu:
 `F1` Start recording
 `F2` Exit
```
- `F1` - Start recording process
- `F2` - Exit from the program

You can change these buttons in `configuration.base_settings` module.
<a id="recording"></a>
### 2. Recording
If you press `F1` you will start the recording process. Program will notify you by printing following message:
```
01:18, recording started:
 `F1` Stop
```
The message has time when you started recording and button to stop it.
<a id="record-statistics"></a>
### 3. Record statistics
If you press `F1` program will view your summary keylogging statistic and for last session:
```
Summary statistics:
  - Time passed: 0:52:24
  - Keystrokes: 4239 times
  - Typing speed: ≈80.74 key/min
Last session:
  - Started at: 28 July, 00:36
  - Ended in: 28 July, 00:55
  - Time passed: 0:19:38
  - Keystrokes: 1189 times
  - Typing speed: ≈60.52 key/min
```
<a id="view-statistics"></a>
### 4. View statistics for another days
If you want to show statistics for a specific day, you can write the following command:
```
$ ./main.py -r
28 July, 2022:
- Time passed: 0:30:15
- Keystrokes: 2119 times
- Typing speed: 70.05 key/min
```
Without arguments, it shows current day statistics. Let's pass the date:
```
$ ./main.py -r 2022-07-27
27 July, 2022:
- Time passed: 0:34:33
- Keystrokes: 2145 times
- Typing speed: 62.08 key/min
```
You can change the input date format if you change the value of the `INPUT_DATE` key in the `configuration.base_settings.DATA_FORMATS` dict.
If you want to see a list of statistics rather than a summary data, you can pass the `-s` or `--separate` flag.
```
$ ./main.py -r -s

1. 01 August, 2022:
- Time range: 00:39 - 00:39
- Time passed: 0:00:08
- Keystrokes: 0 times
- Typing speed: 0.0 key/min

2. 01 August, 2022:
- Time range: 00:42 - 00:42
- Time passed: 0:00:00
- Keystrokes: 0 times
- Typing speed: 0.0 key/min

3. 01 August, 2022:
- Time range: 01:29 - 01:29
- Time passed: 0:00:03
- Keystrokes: 0 times
- Typing speed: 0.0 key/min

4. 01 August, 2022:
- Time range: 01:36 - 01:36
- Time passed: 0:00:02
- Keystrokes: 6 times
- Typing speed: 123.13 key/min
```
With another date:
```
$ ./main.py -r 2022-07-27 -s

1. 27 July, 2022:
- Time range: 01:00 - 01:01
- Time passed: 0:00:06
- Keystrokes: 11 times
- Typing speed: 102.36 key/min

2. 27 July, 2022:
- Time range: 01:01 - 01:35
- Time passed: 0:34:26
- Keystrokes: 2134 times
- Typing speed: 61.95 key/min
```
<a id="help-message"></a>
### 5. Help message
Type `-h` or `--help` flag to view the help message:
```
$ ./main -h
$ ./main --help
```
<a name="bash-script"></a>
## Bash script
The project has a bash script - `keylog`, that allows you to run the program from anywhere in your filesystem. To add this script to your `PATH` write:
```
$ ls
keylog  README.md  requirements.txt  setup.cfg  src  venv
$ sudo ln -s $(pwd)/keylog /usr/local/bin/
```
Now you can write `keylog` and start the script:
```
$ cd /
$ keylog
Creating a virtual environment. Wait.

Menu:
 `F1` Start recording
 `F2` Exit
```
If you don't have a `venv` folder this script will create it. It will output the text above, so you can understand what is going on. If you do have a virtual environment it will run a program as a default.
<a name="configuring"></a>
## Configuring
You can change appearance of messages in the `configuration.base_settings` module. Also, you can bind different buttons to start, stop and exit from the program.
