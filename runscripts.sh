#!/bin/sh

# find attack vectors
cd utils
python3 linkScrap.py listOfApps

# try to generate exploit scripts
cd ..
python3 utils/tryExploit.py

# set executable for all shell
for i in 'exploits/*.sh'; do
  chmod +x  $i
done


