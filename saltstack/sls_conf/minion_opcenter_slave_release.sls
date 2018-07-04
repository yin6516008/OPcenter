opcenter_slave_git_latest:
  git.latest:
    - target: /wwwroot/OPcenter-slave
    - name: https://github.com/yin6516008/OPcenter-slave.git
    - order: 1

# 终止进程
opcenter_slave_stop:
  cmd.run:
    - name: kill 9 $[`cat /wwwroot/OPcenter-slave/pidfile.pid`+1]
#    - require:
#      - file: opcenter_slave_release
    - order: 2

# 启动进程
opcenter_slave_start:
  cmd.run:
    - name: (nohup python3 /wwwroot/OPcenter-slave/slave-start.py >/dev/null 2>/wwwroot/OPcenter-slave/error.log &) & echo $! > /wwwroot/OPcenter-slave/pidfile.pid
    - onlyif: test -d /wwwroot/OPcenter-slave
#    - require:
#      - file: opcenter_slave_release
    - order: 3

