# gpu_protector

Cron
* * * * * cd ~/gpu_protector/;/usr/bin/timeout 25 python gpu_protector.py 72
* * * * * sleep 30;cd ~/gpu_protector/;/usr/bin/timeout 25 python gpu_protector.py 72
