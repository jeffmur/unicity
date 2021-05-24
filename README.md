# 490-demo
Date : Spring 2021

Author : Jeffrey Murray Jr

Purpose: Demonstrate how to pre-process and calculate unicity test

--- 
## Tools 
- Pipenv for Python enviornment 
- Python3 
- Libraries can be found in requirements.txt


## Using Pipenv
``` bash 
$ sudo apt-get install python3-pip                  # For Debian/Ubuntu 
$ sudo apt-get install pipenv  
```

## Download from Github
``` bash
$ git clone https://github.com/jeffmur/unicity.git  # for https clone
$ cd unicity/                                       # Enter directory before next step!
```

## Set-up Enviornment 
``` bash 
$ pipenv shell                                      # creates new env or loads existing env in directory 
$ which pip                                         # ensure you are in virtual env 
$ pip install -r requirements.txt                   # Recursving install dependencies 
```

## Organization 
---
### Data Directory: 
geoLife/ : already pre-processed

split_by_month.py : script to generate user_by_month/ 

geoLife/user_by_month/ : Each User ID is a directory containing each month of location records YEAR_MONTH.csv

I recommend using sample.csv for resource-constrained devices. ( less than 4 processors )

### Notebooks: 
Using Jupyter Notebooks for easy to read & simplicity 

Contains lib/ 
- Function Calls for retriving data
- Algorithms to analyze data 
- Unicity Test

### geo_cluster
Data visualization with Follium 

---

