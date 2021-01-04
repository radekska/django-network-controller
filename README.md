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
Last part of this section is to choosing right configurations which should be applied on
network devices, scanning local network for available devices and then finally applying
mentioned SNMPv3 configurations.