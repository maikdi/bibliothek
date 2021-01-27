# bibliothek
A 3rd Semester Group Finals Project

This project demonstrates the integration of database (via SQLite3) and UI (via TKinter) using a Service layer 

## Installation
Most of the libraries and modules used in this project are built-in from Python it self (such as tkinter, os, sys, configparser,datetime)
For the testing we used the pytest framework. 

Installed by typing in the terminal
```
python -m pip install pytest
```
For the database we used the sqlite3 module


Installed by typing in the terminal
```
python -m pip install sqlite3
```
## Usage
 
**Executing the Program**
Can be launched via IDE or by typing in the terminal with commands below.
```
python -m nbibliothek_v1 
#launches program with it's default database and language
```

You can specify the database with -db:url=
```
python -m nbibliothek_v1 -db:url=xxxx\xxxx.db 
```
You can initialize the .db file with -db:init=true or -db:init=false
```
python -m nbibliothek_v1 -db:init=true/false
```
To get report on the 5 most popular books borrowed 
```
python -m nbibliothek_v1 - apps:report
```

We implemented Factory Method to change the program's language which can be executed with:

```
python -m nbibliothek_v2 -lang=EN #default language is -lang=IN
```

## Project Team
[Elson Prima Roulsie Sutrisno](https://github.com/esutrisno94) 

[Michael David](https://github.com/maikdi/)

## Special Thanks
[Sanga Lawalata](https://github.com/slawalata) Our Professor and main reason why were able to finish this 3rd Semester Project

