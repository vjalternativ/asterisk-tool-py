Installation
clone the source or download
    git clone https://github.com/vjalternativ/asterisk-tool-py.git

cd asterisk-tool-py

install the dependency

pip3 install -r requirements.txt


PreReq
copy sip.conf , manager.conf and extensions.conf in load generator asterisk
in asterisk cli  execute reload command

copy simulator.sip.conf and simulator.extensions.conf in simulator asterisk
rename to sip.conf and extensions.conf
reload asterisk

Usage
execute below command to geneator the load
python3 test.py -n 1 -c 1        