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

cleanup the master.csv  on simulator server before intiating the load
cd /dacx/var/ameyo/dacxdata/asterisks/13/var/log/cdr-csv/
> Master.csv

execute below command to geneator the load
python3 test.py -n 1 -c 1 

n = number of channels
c = channels per second (it should not be greater than 50)

when desired load is generated then originate one call from load generator asterisk cli

originate SIP/2323@simulator application playback moh


get the channel from simulator asterisk cli

get the recording from recording path based on the channel
cd /dacx/var/ameyo/dacxdata/asterisks/13/var/spool/monitor
ls -ltrh |grep <channel>

convert alaw to wav
for eg
sox -t al 1691970014-SIP-loadgenerator-00004d30-in.alaw -s -r '8000' output-in.wav

verify the quality in recording


once call is cleanup then get the Master.csv 
import it to sheet, and apply the formula from formula template




