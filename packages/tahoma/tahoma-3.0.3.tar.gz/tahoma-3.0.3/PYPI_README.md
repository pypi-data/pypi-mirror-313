# tahoma
[UP TO DATE] This is a very easy API for controlling Somfy Tahoma's devices written in Python3, thanks to the pyoverkiz API.
You just need a three-word input to control a device.
It was created with Tahoma but can also works with Somfy Connectivity Kit, Connexoon, Cozytouch


![Somfy](https://www.voletsdusud.com/wp-content/uploads/2018/04/logo-tahoma.jpg)




# Install the main package :


Install tahoma :

#########################################

On the next version of Python and Linux you will need to install in this way (using virtual env) :

```
sudo apt install pipx
pipx install tahoma
```
To update tahoma to the latest version :
`pipx upgrade tahoma`

If tahoma has been installed in ~/.local/bin you will need to add this file to the PATH : ~/.local/bin (if it's not already done) :

`sudo echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc`

[How to create a PATH on Linux ?](https://linuxize.com/post/how-to-add-directory-to-path-in-linux/)

#########################################

Normal way to install on Linux :

```
python3 -m pip install -U tahoma
```


#########################################

For Windows users :

Open a terminal (Powershell) as administrator (Win+X and A) and type this command :

```
python3 -m pip install -U tahoma
```
Then search tahoma.exe and add the folder named 'scripts' (which contain tahoma.exe)  to the PATH of Windows or simply copy tahoma.exe wherever you want and add the destination folder to the PATH of Windows.
[How to create a PATH on Windows ?](https://www.computerhope.com/issues/ch000549.htm)



# Configure :


It's very easy to configure, there are just two commands to execute once for all the first time :

All is explained in tahoma --help and tahoma --info


1. Specify your Somfy-connect login's info and choose the Somfy server :

Open a terminal and type :
- `tahoma --config` or `tahoma -c`

For Windows users : (Go to the folder of tahoma.exe and open a terminal if tahoma.exe is not in the PATH of Windows) :
- `.\tahoma -c`
or
- C:\foler\of\tahoma\tahoma.exe -c


2. Configure the API and get the list of your personal Somfy's devices :

Open a terminal and type :
- `tahoma --getlist` or `tahoma -g`

For Windows users : Go to the folder of tahoma.exe and open a terminal if tahoma.exe is not in the PATH of Windows) :
- `.\tahoma -g`
or
- C:\foler\of\tahoma\tahoma.exe -g

3. And now, you are ready to use tahoma :


# Usage : 
`python3 tahoma.py [ACTION] [CATEGORY] [NAME]`


For instance : `tahoma open shutter kitchen` or `tahoma ouvrir volet cuisine`

- You can also close a shutter or a sunscreen to a specific level. For example, to close to 25%, you can use the commands : `tahoma 25 shutter kitchen` or `tahoma 25 sunscreen kitchen`. Please note that this feature only works with IO protocols and not with RTS.

- As name you can use a unic word like `bath` or the full name with `[""]` like `["bath 1st floor"]`

- You can also run many commands during the same process without restarting tahoma :

For instance : `tahoma arm alarm garden open shutter ["room 6"] confort heater dining off plug office 25 sunscreen kitchen launch scene morning`

- There is also a wait functionality with `wait for <SECOND(S)>` or `sleep for <SECOND(S)>` or `attendre pendant <SECOND(S)>` :

For instance : `tahoma open shutter kitchen wait for 20 close shutter kitchen`

- You can also wait for a specific time with `wait for <HOUR:MINUTE>` (24-hour format)

For instance : `tahoma wait for 13:32 open shutten kitchen`

- Since it is impossible to stop an RTS device, there is the possibility to cancel the immediate preceding command (without affecting a 'wait for <SECONDS>' command). To do this you can use the command 'cancel last action' or 'annuler precedente commande' just after a command that opens or closes an RTS device.

For example :

`tahoma open shutter kitchen wait for 2 cancel last action` : It will stop the kitchen shutter after 2 seconds

`tahoma open shutter kitchen open shutter room6 cancel last action` : It will only stop the room6 shutter

Examples :
Here are some example commands :

- tahoma open shutter kitchen
- tahoma 25 sunscreen Velux3 (You can close a shutter or a sunscreen to a specifique level. Here it will close to 25% )
- tahoma get sensor ["Luminance sensor garden"] (You can use the full name of the device with `["<NAME>"]` )
- tahoma get sensor door (You will receive all the informations about all the sensors with the name `door` in the house in one time)
- tahoma get sensor ["Front door"] 
- tahoma on plug office
- tahoma on light ["kitchen light"]
- tahoma off spotalarm spot
- tahoma open shutter ["room 6"]
- tahoma toggle plug kitchen (For IO devices only)
- tahoma arm alarm garden
- tahoma confort heater dining
- tahoma get sensor ['heater dining room']
- tahoma launch scene morning
- tahoma wait for 13:32 open shutten kitchen
- tahoma arm alarm garden wait for 10 open shutter room6 sleep for 7 confort heater dining off plug office 25 sunscreen kitchen launch scene morning get sensor ['heater dining room']
- tahoma comfort heater dining wait for 3 get sensor ["Heater dining room"]
- tahoma open shutter kitchen open shutter room6 wait for 2 cancel last action (It will stop the room6 shutter after 2 seconds)
- tahoma open shutter kitchen --local (It will override default API set in `tahoma -c` with the `--local` argument for using the local API (For Tahoma hubs only))
- tahoma open shutter kitchen --username mail@address.com --password password --remote (You can provide the username and password with arguments to override the logins stored. This is useful if you have more than one Tahoma box)
- tahoma my shutter kitchen --token 2343d8c7f23dd5f328de --pin 1234-1234-1234 --local (It will use the local API (for Tahoma hubs only) with the pin and token arguments. This is useful if you have more than one Tahoma box)
- tahoma manual heater kitchen wait for 2 19 heater kitchen --server atlantic_cozytouch --username cozytouch_username --password cozytouch_password --remote (For some atlantic_cozytouch heaters, it is possible to use other ACTIONS than comfort, eco, off...with auto, manual, standby, prog, NUMBER. As a Cozytouch hub is not compatible with the local API, you can add the `--remote` argument. In this example tahoma will change the heater's mode to manual and will give the ability to modify the temperature to 19°C using the cloud API)

Special note:

If you want to use the local API for Tahoma hubs only, you will need to activate developer mode (www.somfy.com > My Account > Activate developer mode).
The local API allows controlling some devices without a cloud connection for Tahoma hubs only.
The local API is only compatible with some devices (shutters, sunscreens, heaters).
You can configure the local API with the `tahoma -c` command or override the default API set in `tahoma -c` with the `--local` or `--remote` argument


# But first you need to retrieve your PERSONALS commands :


## Get a list of all possibles [ACTIONS] for each [CATEGORIES] : 

Open a terminal and type :
- `tahoma --list-actions` or `tahoma -la`

or

- `tahoma --list-actions-french` or `tahoma -laf`
 
 
 
## Get a list of availables [CATEGORIES] :

Open a terminal and type :
- `tahoma --list-categories` or `tahoma -lc`

or 

- `tahoma --list-categories-french` or `tahoma -lcf`



## Get the [NAMES] you have given to your personal devices in the Somfy's App :

Open a terminal and type :
- `tahoma --list-names` or `tahoma -ln`

or

- `tahoma --list-names-french` or `tahoma -lnf`



Enjoy !  For more info `tahoma -h` or `tahoma -i` 




# Create a PATH to tahoma :


If you have installed tahoma without the `sudo` command on Linux you will need to create a PATH for starting tahoma with the `tahoma` command.

Indead, to be able to run tahoma directly in the terminal, without going to the source package, you should add the tahoma's folder to the PATH :

On Linux, it can be permanently done by executing : `sudo gedit ~/.bashrc` and adding, at the end of the document, this line :

`export PATH=$PATH:/place/of/the/folder/tahoma`



If you want to temporarily test it before, you can just execute this command in the terminal : 

`export PATH=$PATH:/place/of/the/folder/tahoma` 

It will be restored on the next reboot.



By doing this, instead of taping `python3 '/place/of/the/folder/tahoma/tahoma.py open shutter kitchen'`,

 you will be able to directly tape in the terminal : `tahoma open shutter kitchen`.


Then execute tahoma just like this : `tahoma arm alarm garden close shutter room6 confort heater dining off plug office 25 sunscreen kitchen launch scene morning` and that's all !






For :

Somfy Connectivity Kit

Somfy Connexoon IO

Somfy Connexoon RTS

Somfy TaHoma

Somfy TaHoma Beecon

Somfy TaHoma Switch

Thermor Cozytouch

And more...


Supported devices :

Alarm
Shutter
Plug
Heater
Sensors
Scenes
and more if you ask me on github : 

[@pzim-devdata GitHub Pages](https://github.com/pzim-devdata/tahoma/issues)












<p align="center" width="100%">
    <img width="33%" src="https://avatars.githubusercontent.com/u/52496172?v=4"> 
</p>

------------------------------------------------------------------

- [Licence](https://github.com/pzim-devdata/DATA-developer/raw/master/LICENSE)
MIT License Copyright (c) 2023 pzim-devdata

------------------------------------------------------------------

Created by @pzim-devdata - feel free to contact me!
