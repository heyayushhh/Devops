#!/bin/sh
# lab3app service control (pidfile-based; containers have no systemd).
# Usage: ctl.sh {start|stop|restart|status}
set -u

APP=/opt/lab3app/bin/app.py
PIDFILE=/var/run/lab3app/app.pid
LOGFILE=/var/log/lab3app/app.log

get_pid() {
    [ -f "$PIDFILE" ] && cat "$PIDFILE" 2>/dev/null
}

start() {
    pid=$(get_pid)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        echo "lab3app already running (pid $pid)"
        return 0
    fi
    : > "$LOGFILE" 2>/dev/null || LOGFILE=/dev/null
    nohup python "$APP" >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "lab3app started (pid $(get_pid))"
}

stop() {
    pid=$(get_pid)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        kill "$pid"
        sleep 1
        kill -0 "$pid" 2>/dev/null && kill -9 "$pid"
        echo "lab3app stopped (pid $pid)"
    else
        echo "lab3app not running"
    fi
    rm -f "$PIDFILE"
}

case "${1:-}" in
    start)   start ;;
    stop)    stop ;;
    restart) stop; start ;;
    status)
        pid=$(get_pid)
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "lab3app running (pid $pid)"
        else
            echo "lab3app not running"
        fi
        ;;
    *) echo "usage: $0 {start|stop|restart|status}"; exit 2 ;;
esac
