#! /bin/sh

## script downloaded from https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python#a-explanation-of-the-circuit

## steps to register for starting up on boot
# sudo cp fancontrol.sh /etc/init.d
# sudo chmod +x /etc/init.d/fancontrol.sh
# sudo update-rc.d fancontrol.sh defaults
# sudo /etc/init.d/fancontrol.sh start


### BEGIN INIT INFO
# Provides:          fancontrol.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

SCRIPT_PATH="/home/pi/workspace/pi-fan/fancontrol.py"

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting fancontrol.py"
    $SCRIPT_PATH &
    ;;
  stop)
    echo "Stopping fancontrol.py"
    pkill -f $SCRIPT_PATH
    ;;
  *)
    echo "Usage: /etc/init.d/fancontrol.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
