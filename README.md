# NetworkController - Engineer's Thesis Project

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General Info

This web application has been made as a engineer's thesis project and the main purpose of it, is to present skills and ideas obtained during studies on AGH University of Science and Technology in Cracow.
Mentioned web application has been designed to monitor, manage and configure computer local area networks.
<br>Project is splited up into three main parts:
- [Configuration](#configuration)
- [Management](#management)
- [Visualization](#visualization)  

Each of those part are explained below.

## Configuration 
The main and only purpose of this part of the project is to find, access and configure network devices with SNMPv3 protocol, specified in firstly created <i>Access Config</i> which includes parameters such as:
- Login Username
- Login Password
- Secret Password
- Subnet CIDR
- Device OS

Next part of it is a <i>SNMP Config</i> which is used to generate proper Cisco IOS configuration and apply it remotely on device(s) in order to properly use <i>Mange Section.</i> It includes parameters such as:
- Group Name
- SNMP User
- SNMP Password
- SNMP Encrypt Key
- SNMP Host
- SNMP Authentication Protocol
- SNMP Privacy Protocol
- Server Location
- Contact Details
- Enable Traps Functionality

This section includes as well two tables with created configurations for visibility.
Last part of this section is choosing of right configurations which should be applied on
network devices, scanning local network for available devices and then finally applying
mentioned SNMPv3 configurations.

## Management
This section is focused on providing details about our local area network. We can also use it to manage and configure specific devices via web-based SSH terminal session.
The first part of this section is designed with two main buttons - "Refresh List" and "Start/Stop Trap Engine" button. 
First one runs a SNMP query to all devices in our local network and then populates table with received data. 
Second button allows to monitor network by using SNMP traps (works only if "enable traps" field was marked in configure section). 
When user clicks on specific device name new fields will pop up. First field is for generating and establishing remote SSH session with chosen device. 
User can easily configure device or check it's details without using third party terminals. Second field provides device details based on system and interfaces MIBs. 
Third tab includes table which is populated with mentioned earlier SNMP traps when SNMP engine enabled.
Manage network section is a core part of this project as user is able to obtain deep details about specified network.

## Visualization
The last, but not least section of this project is focused on generating nice and user friendly, dynamic network topology with little help of initially configured LLDP protocol. 
When user clicks on chosen device new window will pop up with all neighbor(s) details.

## Technologies
Project is created with:
- Python - 3.8.1
- Django - 3.1.1
- Django Channels - 3.0.2
- Django Celery - 4.4.7
- RabbitMQ - 3.8.9
- Netmiko - 3.3.0
- Napalm - 3.2.0  
- SNMP - 3.0  
- EasySNMP - 4.4.12  
- PySNMP - 0.2.5  
- jQuery - 3.3.1  
- CSS - 2.1  
- Bootstrap - 4.3.1

## Setup
In order to properly setup and run network controller, follow below steps:  
(Checked on macOS High Sierra 10.13.6)
```
# clone to your local workspace
$ git clone https://github.com/radekska/NetworkController.git .

# create virtual environment
$ python3 -m venv <name_of_your_venv>

# activate virtual environment
$ source <name_of_your_venv>/bin/activate

# install Python 3 all dependencies
$ python3 -m pip install -r requirements.txt 

# install RabbitMQ broker for asynchronous tasks

##### For macOS #####
$ brew install rabbitmq
$ export PATH=$PATH:/usr/local/sbin

# Start server (Mac)
$ sudo rabbitmq-server -detached #-detached flag indicates the server to run in the background

# Add user settings (optional)
$ sudo rabbitmq-server -detached
$ sudo rabbitmqctl add_user myuser mypassword
$ sudo rabbitmqctl add_vhost myvhost
$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

#####################

##### For Ubuntu #####
$ apt-get install -y erlang
$ apt-get install rabbitmq-server

# Then enable and start the RabbitMQ service:
$ systemctl enable rabbitmq-server
$ systemctl start rabbitmq-server

# Check rabbitmq server status
$ systemctl status rabbitmq-server

#####################

# while message broker is running start up a Celery process
$ sudo celery -A main_app worker -l info

# finally run Network Controller 
$ python3 manage.py runserver
```
## Author
- Radosław Skałbania - [radekska](https://github.com/radekska)

