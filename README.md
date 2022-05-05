# MFThunter
Hunt through MFT files with CSV format

### Description
MFThunter.py is used to hunt through bunch of MFT files in CSV format in an attempt to spot quick anamolies, the script currently has 2 hunt methods:

1. Calcualte similiraty between two execuatable names (levenshtein distance) to spot if a malicious exe/process is mirroring a legitmate one Ex: (svchost,svch0st).

     It works by comparing the levenshtein distance between all exe records in the given MFT files against a dictionary of clean windows filenames and output the results based on the distance value specified.

2. Dump out all duplicate executable names that are located in mutiple directories after removing some common false positives.

      Ex: (C:\WlNDOWS\system32\svchost.exe, C:\WlNDOWS\\svchost.exe)

##### Note: MFT CSV files used are generated/parsed by Eric Zimmerman's known tool (MFTECmd) which is located here
https://github.com/EricZimmerman/MFTECmd

___
### Requirements

the script requires pandas & levenshtein(0.11.2) python modules, you can install them using the requirements file

```
 pip3 install -r requirements.txt
```
___
### Usage

```
Usage: MFThunter.py -m [method_number] [options]
 
Options:
        -m [1,2], --method [1,2]   hunt method, specify 1 for Levenshtein distance (measure similarity between two executables)
                                                specify 2 for checking all duplicate executables located in different directories
        -h, --help                 Show this help
        -p, --path                 specify the folder path which contain MFT files in CSV format
        -d, --distance             mandatory for method = 1, specify the Levenshtein distance, a value of 1 is recommended
 
Examples:
  MFThunter.py -m 1 -p /home/MFT/ -d 1
  MFThunter.py -m 2 -p /home/MFT/ 
```
___
### Examples
**Ex1:** hunt method = 1 and distance = 1
```diff
python3 MFThunter.py -m 1 -p /home/MFT/ -d 1
Please wait ... it might take a while, depending on the the Size of your MFT files

       legitimate Files  Suspicious Files
  0    -----------------  ----------------
  1       'convert.exe'    'lconvert.exe'
  2       'cscript.exe'     'Rscript.exe'
  3           'jsc.exe'         'jmc.exe'
  4       'drvinst.exe'    'drv_inst.exe'
  5            'fc.exe'          'lc.exe'
  6        'fsutil.exe'     'dfsutil.exe'
  7        'ksetup.exe'       'setup.exe'
- 8      'explorer.exe'    'expl0rer.exe'
  9        'ksetup.exe'      'RSetup.exe'
  ...
```

**Ex2:** hunt method = 2
```diff
python3 MFThunter.py -m 2 -p /home/MFT/
Please wait ... it might take a while, depending on the the Size of your MFT files

  ('winload.exe', '.\\Windows\\System32\\Boot')
  ('winresume.exe', '.\\Windows\\System32')
  ('winresume.exe', '.\\Windows\\System32\\Boot')
  ('winrs.exe', '.\\Windows\\SysWOW64')
  ('winrs.exe', '.\\Windows\\System32')
  ('winrshost.exe', '.\\Windows\\SysWOW64')
  ('winrshost.exe', '.\\Windows\\System32')
  ('winver.exe', '.\\Windows\\SysWOW64')
  ('winver.exe', '.\\Windows\\System32')
  ('wordpad.exe', '.\\Program Files (x86)\\Windows NT\\Accessories')
  ('wordpad.exe', '.\\Program Files\\Windows NT\\Accessories')
- ('explorer.exe', '.\\Windows')
- ('explorer.exe', '.\\Windows\\System32\\explorer.exe')
  ('explorer.exe', '.\\Windows\\SysWOW64')
  ('wowreg32.exe', '.\\Windows\\SysWOW64')
  ('wowreg32.exe', '.\\Windows\\System32')
  ('write.exe', '.\\Windows')
  ('write.exe', '.\\Windows\\SysWOW64')
  ('write.exe', '.\\Windows\\System32')
  ('wscript.exe', '.\\Windows\\SysWOW64')
  ('wscript.exe', '.\\Windows\\System32')
  ...
```
