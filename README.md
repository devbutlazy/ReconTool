# ReconTool

A tool to get information about a webhost (like ip, subdomain, dir, etc.) 

# Important Information
- **Currently not mantained, as authors are no longer engaged in "gray affairs"**
- **There might be some shity-code, as the code was originally written almost 9 month ago and hasn't been rewritten yet**
- [Author](https://github.com/devbutlazy/GTokenChecker) author: [LazyDev](https://github.com/devbutlazy) and .inferno

# Features 

- **Get all information about the host service**
- **Enormous txt file with different subdomains and dirs for search**
- **Convenient GUI to control the proccess**
- **Secured, and fast**

# Installation

`1` Download python from [python.org](https://python.org)  
`2` Clone this repository  
```
git clone https://github.com/devbutlazy/ReconTool
```
`3` Go to`cmd.exe` and type `cd <PROJECT_PATH>`  
`4` Type `pip install -r requirements.txt` to install required packages  
`5` Configure censys - [Guide](https://support.censys.io/hc/en-us/articles/360056141971-Censys-Search-Python-Library)  
`6` Run the program
```
python main.py -t https://target_domain.com
```

# TODO

- [x] Subdomains search
- [x] Directories search
- [x] Get host information at programm start
- [ ] Store the already checked info in .cache files, to make the proccess faster
- [ ] Get CMS (Content Management Service) for all subdomains
- [ ] Rewrite the code to follow MyPy, Pylint rules

    
### License: GNU GPL 3