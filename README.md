Installation
clone the source or download
    git clone https://github.com/vjalternativ/asterisk-tool-py.git

cd asterisk-tool-py

install the dependency

pip3 install -r requirements.txt


PreReq

copy assets/loadgenerator/sip.conf , assets/loadgenerator/manager.conf and assets/loadgenerator/extensions.conf in load generator asterisk configuration path

for eg for asterisk13 path will be /dacx/var/ameyo/dacxdata/asterisks/13/etc/asterisk/

in asterisk cli  execute reload command

copy assets/simulator/sip.conf and assets/simulator/extensions.conf in simulator asterisk
reload asterisk

change the simulator asterisk ip in loadgenerator asterisk sip.conf 
change the loadgenerator asterisk ip in simulator asterisk sip.conf

Usage
execute below command to geneator the load
python3 test.py -n 1 -c 1 

n = number of channels
c = channels per second (it should not be greater than 50)