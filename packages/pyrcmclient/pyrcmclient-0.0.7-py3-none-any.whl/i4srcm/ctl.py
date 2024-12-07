import sys,os
import shutil
import time
import re
import io
from io import BytesIO
from datetime import datetime
from typing import NamedTuple
from threading import Thread
from logging import getLogger, Formatter, Handler, StreamHandler, FileHandler, DEBUG, INFO, WARN, ERROR, NOTSET

import pandas as pd
import paramiko
from paramiko import SSHClient, SFTPClient, SSHException, AuthenticationException

sys.path.append(os.getcwd())

logger = getLogger('rcm.ctl')


def sar_to_csv(sar_logpath:str, devmap:dict|None=None):
    #file='result/IP28_RHEL8_RCM1062/interval020/20241028_1002/wfhist/workflow_result_001_perf.log'
    # 空のデータフレームを用意
    mem_df = pd.DataFrame()
    io_df_map:dict[str,pd.DataFrame] = {}
    with open(sar_logpath,'r') as stream:
        while True:
            header_line = stream.readline()
            if not header_line:
                break
            if re.match( r'^[0-9]{2}:[0-9]{2}:[0-9]{2} ', header_line ):
                colums = header_line.split()
                while True:
                    data_line = stream.readline()
                    if data_line and re.match( r'^[0-9]{2}:[0-9]{2}:[0-9]{2} ', data_line ):
                        values = data_line.split()
                        if len(colums)==len(values):
                            t = values[0]
                            if colums[1] == 'DEV':
                                dev = values[1]
                                io_df = io_df_map.get(dev)
                                if io_df is None:
                                    io_df = pd.DataFrame()
                                    io_df_map[dev] = io_df
                                for i in range(2,len(values)):
                                    io_df.loc[t,colums[i]] = values[i]
                            else:
                                for i in range(1,len(values)):
                                    mem_df.loc[t,colums[i]] = values[i]
                    else:
                        break
    base_path = os.path.splitext( sar_logpath )[0]

    mem_df.index.name='Time'
    mem_df.to_csv( f"{base_path}_mem.csv" )
    for dev,df in io_df_map.items():
        df.index.name='Time'
        if devmap and dev in devmap:
            dev = devmap[dev]
        df.to_csv( f"{base_path}_{dev}.csv")

class PerfTracer:

    def __init__(self,addr:str, port:int, username:str, userpass:str|None, logfile):
        self._addr = addr
        self._ssh_port = port
        self._ssh_user:str = username
        self._ssh_pass:str|None = userpass
        self._logfile=logfile
        self._sar_logpath = os.path.splitext(logfile)[0] + "_sar.log"
        self._sshclient:SSHClient|None = None
        self._task:Thread|None = None
        self._devmap = {}

    def _disconnect(self):
        try:
            if self._sshclient:
                self._sshclient.close()
            self._sshclient = None
        except:
            pass

    def _thread(self):
        self._sshclient = SSHClient()
        self._sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._sshclient.connect(hostname=self._addr, port=self._ssh_port, username=self._ssh_user, password=self._ssh_pass)
            command = """awk 'NF==4 && $1 ~/[0-9]+/ {printf "dev%d-%d %s\\n", $1,$2,$4}' /proc/partitions"""
            stdin, stdout, stderr = self._sshclient.exec_command(command)
            try:
                with stdout:
                    for line in iter(stdout.readline, ""):
                        if line.startswith('dev'):
                            values = line.split()
                            self._devmap[values[0]] = values[1]
            finally:
                try:
                    stdin.close()
                except:
                    pass
                try:
                    stderr.close()
                except:
                    pass
            command = f"LANG=C sar -rd 1 2>&1"
            stdin, stdout, stderr = self._sshclient.exec_command(command)
            with stdin:
                with stderr:
                    with stdout:
                        with open(self._sar_logpath,'w') as log_stream:
                            for line in iter(stdout.readline, ""):
                                log_stream.write(line)
        except AuthenticationException as ex:
            print(str(ex))
        finally:
            self._disconnect()
            self._task = None

    def __enter__(self):
        self._task = Thread( target=self._thread, daemon=True )
        self._task.start()

    def __exit__(self,exc_type,exc_value,traceback):
        self._disconnect()
        try:
            if self._task:
                self._task.join()
                self._task = None
        except:
            pass
        try:
            sar_to_csv( self._sar_logpath, self._devmap )
        except:
            pass
        if exc_value:
            return False

def get_remote_abs( remote_path:str,cwd:str) ->str:
    if os.path.isabs(remote_path) or not cwd:
        return remote_path
    return f"{cwd}/{remote_path}"

class CopyTo:

    def __init__(self,local:str|BytesIO, remote:str,*,keep:bool=False):
        if not isinstance(remote,str) or not isinstance(local,str|BytesIO) or not isinstance(keep,bool):
            raise ValueError('invalid data type?')
        self.local:str|BytesIO = local
        self.remote:str = remote
        self.keep:bool = keep

    def get_remote_abs(self,cwd:str) ->str:
        return get_remote_abs(self.remote,cwd)

class CopyFrom:

    def __init__(self,remote:str,local:str|BytesIO,*,keep:bool=False):
        if not isinstance(remote,str) or not isinstance(local,str|BytesIO) or not isinstance(keep,bool):
            raise ValueError('invalid data type?')
        self.local:str|BytesIO = local
        self.remote:str = remote
        self.keep:bool = keep

    def get_remote_abs(self,cwd:str) ->str:
        return get_remote_abs(self.remote,cwd)

class RCMCTL:
    def __init__(self, hostname, user, *, passwd:str|None=None, addr:str='', osid='', rcm='', port=None, logfile:str|None=None):
        self.name:str = hostname
        self.addr:str = addr if addr else hostname
        self.ssh_port:int = port if port and port>0 else 22
        self.ssh_user:str = user
        self.ssh_pass:str|None = passwd
        self.os_id:str = osid
        self.os_name:str = ''
        self.rcm:str = rcm
        self.rcmbuild:str = ''
        self.logger = getLogger('rcm.ctl.trace')
        self.logger.propagate = False
        self.set_logfile(logfile)

    def set_logfile(self,logfile:str|None):
        # Handerをクリアする
        for hdr in [ hdr for hdr in self.logger.handlers]:
            self.logger.removeHandler(hdr)
        if logfile:
            if os.path.isdir(os.path.dirname(logfile)):
                self.logger.setLevel(DEBUG)
                # フォーマットの指定
                file_formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
                file_hdr = FileHandler(logfile)
                file_hdr.setLevel(NOTSET)
                file_hdr.setFormatter(file_formatter)
                self.logger.addHandler(file_hdr)

    def _error(self, msg, *args, **kwargs):
        logger.error(msg,*args,**kwargs)
        self.logger.error(msg,*args,**kwargs)

    def _info(self, msg, *args, **kwargs):
        logger.info(msg,*args,**kwargs)
        self.logger.info(msg,*args,**kwargs)

    def _debug(self, msg, *args, **kwargs):
        logger.debug(msg,*args,**kwargs)
        self.logger.debug(msg,*args,**kwargs)

    def ssh_command( self, sshclient:SSHClient, command:str, logpath:str|BytesIO|None=None ) ->int:
        exit_code = -1
        try:
            # コマンドを実行
            if logpath is None or isinstance(logpath,BytesIO):
                self._info(f"cmd:{command}")
            else:
                self._info(f"cmd:{command} log:{logpath}")
            stdin, stdout, stderr = sshclient.exec_command(command)

            if logpath is not None:
                if isinstance(logpath,BytesIO):
                        for data in iter(lambda: stdout.read(1024), b'' ):
                            logpath.write(data)
                        for data in iter(lambda: stderr.read(1024), b'' ):
                            logpath.write(data)
                else:
                    with open(logpath,'wb') as log_stream:
                        for data in iter(lambda: stdout.read(1024), b'' ):
                            log_stream.write(data)
                        for data in iter(lambda: stderr.read(1024), b'' ):
                            log_stream.write(data)
            else:
                # 実行結果の出力を取得
                output = stdout.read().decode()
                error = stderr.read().decode()
                if output:
                    self.logger.debug("stdout:\n"+output.strip())
                if error:
                    self.logger.debug("stderr:\n"+error.strip())
            exit_code:int = stdout.channel.recv_exit_status()
            if exit_code != 0:
                self._debug(f"exit:{exit_code}")

        finally:
            pass
        return exit_code

    def getinfo(self):
        # rpm -q RCMx 2>/dev/null | grep ^RCM

        # SSHクライアントを作成
        sshclient = SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pretty_name:str = ''
        rcm_ver:str = ''
        try:
            # SSHサーバに接続
            sshclient.connect(hostname=self.addr, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass)
            stdin, stdout, stderr = sshclient.exec_command( "(. /etc/os-release;echo $PRETTY_NAME) 2>/dev/null" )
            pretty_name = stdout.read().decode().strip()
            stdin, stdout, stderr = sshclient.exec_command( "rpm -q RCM 2>/dev/null | grep ^RCM" )
            rcm_ver = stdout.read().decode().strip()
        except AuthenticationException as ex:
            self._error(str(ex))
            return
        finally:
            # SSH接続を閉じる
            sshclient.close()

        self.os_name = pretty_name
        self.os_id = RCMCTL.strip_osname(pretty_name)
        self._info(f"OS:{self.os_id} : \"{self.os_name}\"")
        
        a,b = RCMCTL.strip_rcmver(rcm_ver)
        self.rcm = a
        self.rcmbuild = b
        self._info(f"RCM:{self.rcm} {self.rcmbuild}")

    @staticmethod
    def strip_osname(pretty_name) ->str:
        # PRETTY_NAME="Red Hat Enterprise Linux 9.4 (Plow)"
        # PRETTY_NAME="Red Hat Enterprise Linux 8.10 (Ootpa)"
        # PRETTY_NAME="Rocky Linux 8.10 (Green Obsidian)"
        # PRETTY_NAME="CentOS Linux 7 (Core)"
        # PRETTY_NAME="openSUSE Leap 15.6"
        # PRETTY_NAME="Ubuntu 24.04.1 LTS"
        #  (. /etc/os-release;echo $PRETTY_NAME) 2>/dev/null
        if not pretty_name:
            return ''
        # "(..)"を削除
        os_name = re.sub(r'\s*\(.*?\)', '', pretty_name)
        # Red Hat Enterprise Linux を RHEL に置換
        os_name = os_name.replace('Red Hat Enterprise Linux', 'RHEL')
        # Linux
        os_name = re.sub( 'opensuse leap', 'Leap', os_name, flags=re.IGNORECASE)
        # Linux
        os_name = re.sub( 'linux', '', os_name, flags=re.IGNORECASE)
        # Linux
        os_name = re.sub( 'lts$', '', os_name, flags=re.IGNORECASE)
        # Linux
        os_name = re.sub( r'([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)', r'\1', os_name, flags=re.IGNORECASE)
        os_name = re.sub( r'([0-9]+)\.([0-9]+)\.([0-9]+)', r'\1', os_name, flags=re.IGNORECASE)
        os_name = re.sub( r'([0-9]+)\.([0-9]+)', r'\1', os_name, flags=re.IGNORECASE)
        # 空白なくす
        os_name = os_name.replace(' ','')
        return os_name

    @staticmethod
    def strip_rcmver(rcm_ver) ->tuple[str,str]:
        # 入力のフォーマットにマッチする正規表現パターン
        pattern = r"^RCM-([0-9]+)\.([0-9]+)-([0-9]+).*$"
        # 正規表現を使ってマッチする部分を置換し、最終的な形式に変更
        v = re.sub(pattern, r"RCM\1", rcm_ver)
        d = re.sub(pattern, r"\2-\3", rcm_ver)
        return v,d

    def _sudo(self,name:str,script:str, *,transfer:list|None=None,out:str|BytesIO|None=None) ->bool:
        if not isinstance(transfer,list):
            transfer = []

        remote_dir='/tmp'
        remote_script_path=f'{remote_dir}/{name}.sh'
        init_cmd = f"/bin/rm -f '{remote_script_path}'"
        final_cmd = f"/bin/rm -f '{remote_script_path}'"
        for cp in transfer:
            if isinstance(cp,CopyTo):
                init_cmd += f" '{cp.get_remote_abs(remote_dir)}'"
                if cp.keep == False:
                    final_cmd += f" '{cp.get_remote_abs(remote_dir)}'"
            elif isinstance(cp,CopyFrom):
                if cp.keep == False:
                    final_cmd += f" '{cp.get_remote_abs(remote_dir)}'"


        sudo_passwd=self.ssh_pass
        sudo_script = f"""#!/bin/bash
if [ -n "$SUDO_ASKPASS" ]; then
  echo '{sudo_passwd}'
  exit 0
fi

ScrDir=$(cd $(dirname $0);pwd)
export SUDO_ASKPASS="$ScrDir/$(basename $0)"
function fn_cleanup() {{
  rm -f "$SUDO_ASKPASS"
  {final_cmd}
}}
trap fn_cleanup EXIT

{script}

"""
        file_content=io.BytesIO(sudo_script.encode())
        # SSHクライアントを作成
        sshclient = SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ret:bool = False
        try:
            # SSHサーバに接続
            sshclient.connect( hostname=self.addr, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass )
            # コマンドを実行
            if 0 != self.ssh_command( sshclient, init_cmd ):
                self._error(f'[SUDO] failled to init: {init_cmd}')
                return False
            try:
                with sshclient.open_sftp() as sftp:
                    self._info(f"[SUDO] scp put to {remote_script_path}")
                    sftp.putfo(file_content, remote_script_path)
                    sftp.chmod( remote_script_path, 0o755 )
                    for cp in transfer:
                        if isinstance(cp,CopyTo):
                            if isinstance(cp.local,BytesIO):
                                self._info(f"[SUDO] scp put to {cp.remote}")
                                sftp.putfo(cp.local,cp.get_remote_abs(remote_dir))
                            else:
                                self._info(f"[SUDO] scp put {cp.local} to {cp.remote}")
                                sftp.put(cp.local,cp.get_remote_abs(remote_dir))


                exit_code = self.ssh_command( sshclient, f"cd '{remote_dir}' && {remote_script_path}", logpath=out)
                if 0 == exit_code:
                    ret = True

                if transfer:
                    with sshclient.open_sftp() as sftp:
                        for cp in transfer:
                            if isinstance(cp,CopyFrom):
                                if isinstance(cp.local,BytesIO):
                                    self._info(f"[SUDO] scp get from {cp.remote}")
                                    sftp.getfo( cp.get_remote_abs(remote_dir),cp.local)
                                else:
                                    self._info(f"[SUDO] scp get from {cp.remote} to {cp.local}")
                                    sftp.get( cp.get_remote_abs(remote_dir), cp.local )
            finally:
                try:
                    if 0 != self.ssh_command( sshclient, final_cmd ):
                        self._error(f'[SUDO] failled to cleanup: {final_cmd}')
                        return False
                except SSHException as ex:
                    self._error(f'[SUDO] failled to cleanup: {str(ex)}')
                    ret = False
        except AuthenticationException as ex:
            self._error(str(ex))
            ret = False
        finally:
            # SSH接続を閉じる
            try:
                sshclient.close()
            except:
                pass
        return ret

    def stop_rcm(self) ->bool:

        try:
            script = f"""
sudo -A systemctl stop i4s-rcm
sleep 2
"""
            # コマンドを実行
            if self._sudo('stop_rcm', script):
                return True
        except:
            pass
        return False

    def start_rcm(self) ->bool:

        try:
            script = f"""
sudo -A systemctl restart i4s-rcm
sleep 30
sudo -A systemctl status i4s-rcm
"""
            # コマンドを実行
            if self._sudo('start_rcm', script):
                return True
        except:
            pass
        return False


    def get_loglines(self) ->int|None:

        script = f"""
set -- $(sudo -A wc -l /var/log/rcm/RCM/RCM-Controller.log 2>/dev/null)
echo "${{1:-0}}"
exit 0
"""
        try:
            # コマンドを実行
            out = BytesIO()
            if self._sudo( 'get_log_lines', script, out=out):
                try:
                    return int( out.getvalue().decode().strip() )
                except:
                    pass
        except:
            pass
        return None

    def chk_perflog(self,start_line:int|None=None) ->bool:

        wait_max=120
        if isinstance(start_line,int|float) and start_line>1:
            script = f"""sudo -A tail -n +{start_line} """
        else:
            script = f"""sudo -A cat """
        script = f"""
for(( i=0; i<{wait_max}; i++ )); do
  if {script} /var/log/rcm/RCM/RCM-Controller.log|grep -sq '^ PerfLog .* CPU ' ; then
      exit 0
  fi
  sleep 1
done
exit 56
"""
        if not self._sudo('chk_perflog', script):
            return False
        return True

    def get_perflog(self,logfile:str,start_line:int|None=None) ->bool:

        if logfile is None:
            return False

        logpath = os.path.splitext(logfile)[0] + ".log"
        csvpath = os.path.splitext(logfile)[0] + ".csv"
        if isinstance(start_line,int|float) and start_line>1:
            script = f"""sudo -A tail -n +{start_line} """
        else:
            script = f"""sudo -A cat """
        script = f"""{script} /var/log/rcm/RCM/RCM-Controller.log | grep -A1 '^INFO.*\\.perfLog' | awk -vRS='--\\n' -vFS='[ \\n]+' '{{gsub("[ \\n]+"," ");print}}'"""

        if not self._sudo('get_perflog', script, out=logpath):
            return False

        try:
            chk = {
                0: 'INFO[',
                5: 'PerfLog',
                7: 'CPU',
                13: 'Mem',
                22: 'WFQ',
                26: 'WFW',
                29: 'WFH',
                33: 'WFR',
                37: 'JOB',
                42: 'FILE',
            }
            hdr = [
                'Time','UTC',
                'CPU;All','CPU;User','CPU;Nice','CPU;Sys','CPU;VM',
                'Mem;heapInit', 'Mem;heapUsed', 'Mem;heapCommiteed','Mem;heapMax','Mem;non-heapInit','Mem;non-heapUsed','Mem;non-heap;Committed','Mem;non-heapMax',
                'WFQ;in','WFQ;size','WFQ;out',
                'WFW;wait','WFW;get',
                'WFH;in','WFH;size','WFH;out',
                'WFR;wait','WFR;main','WFR;sub',
                'JOB;run','JOB;core','JOB;pool','JOB;max',
                'FILE;open','FILE;unused','FILE;max',
            ]
            with open(logpath,'r') as rd:
                with open(csvpath,'w') as w:
                    w.write( ','.join(hdr) )
                    w.write('\n')
                    while True:
                        line = rd.readline()
                        if line is None:
                            break
                        values = line.strip().split()
                        if len(values)!=46:
                            break
                        #['INFO[', 'jp.co.i4s.RCM.controller.perfLog', ']', '2024-10-25', '18:45:00,705', 'PerfLog', '1729849500705', 'CPU', '0', '0', '0', '0', '0', 'Mem', '3072', '1729', '3072', '3072', '7', '109', '118', '0', 'WFQ', '0', '0', '0', 'WFW', '0', '0', 'WFH', '8', '0', '8', 'WFR', '0', '0', '0', 'JOB', '0', '10', '10', '10', 'FILE', '1376', '0', '782465']
                        x = True
                        for k,v in chk.items():
                            if values[k] != v:
                                x=False
                        if not x:
                            break
                        datas=[]
                        datas.append( values[4].replace(",",".") )
                        datas.append( values[6] )
                        datas.extend( values[8:13])
                        datas.extend( values[14:22])
                        datas.extend( values[23:26])
                        datas.extend( values[27:29])
                        datas.extend( values[30:33])
                        datas.extend( values[34:37])
                        datas.extend( values[38:42])
                        datas.extend( values[43:47])
                        if len(datas) != len(hdr):
                            break
                        w.write( ','.join(datas) )
                        w.write('\n')
            return True
        except:
            pass
        return False

    def reboot( self) ->bool:

        try:
            script = f"""
sudo -A systemctl stop i4s-rcm
sleep 2
sudo -A shutdown -r now
"""
            self._sudo('reboot',script)
            self._info("wait for reboot")

            # SSHクライアントを作成
            sshclient = SSHClient()
            sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            log_inverfal:float = 60
            next_log:float = time.time()+log_inverfal
            time.sleep(10)

            while True:
                if next_log < time.time():
                    self._info("wait for reboot")
                    next_log = time.time()+log_inverfal
                time.sleep(5)
                try:
                    # SSHサーバに接続
                    sshclient.connect(hostname=self.addr, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass, timeout=1.0)
                    if 97 == self.ssh_command( sshclient, 'exit 97'):
                        self._info("server up!")
                        return True
                except AuthenticationException as ex:
                    self._error(str(ex))
                    return False
                except Exception as ex:
                    self.logger.exception('x')
                    pass
                finally:
                    # SSH接続を閉じる
                    sshclient.close()
        except:
            self.logger.exception('サーバー再起動に失敗した')
        return False

    def cleanup_rcm(self,*, fs:str='', sql:str='', reset_data:bool=False) ->bool:
        local_fstgz_path = fs if fs else 'dmy' # 'FileServer.tgz'
        local_dbsql_path = sql if sql else 'dmy' # 'dumpdb.sql.gz'
        if reset_data:
            if not os.path.exists(local_fstgz_path) or not os.path.exists(local_dbsql_path):
                self._error(f"ERROR: not found {local_fstgz_path} or {local_dbsql_path}")
                return False
        sudo_passwd=self.ssh_pass
        script = f"""#!/bin/bash
if [ -n "$SUDO_ASKPASS" ]; then
  echo '{sudo_passwd}'
  exit 0
fi

ScrDir=$(cd $(dirname $0);pwd)
export SUDO_ASKPASS="$ScrDir/$(basename $0)"
FSTGZ="$ScrDir/{os.path.basename(local_fstgz_path)}"
DBSQL="$ScrDir/{os.path.basename(local_dbsql_path)}"
function fn_cleanup() {{
  rm -f "$SUDO_ASKPASS" "$FSTGZ" "$DBSQL"
}}
trap fn_cleanup EXIT
set -ue

sudo -A systemctl stop i4s-rcm

if [ "{reset_data}" == "True" ]; then
    sudo -A rm -rf /RCM/bkup
    sudo -A /opt/i4s/RCM/bin/init-rcmfs.sh --fs --tgz "$FSTGZ" #>/dev/null
    sudo -A /opt/i4s/RCM/bin/init-rcmdb.sh -y --sql "$DBSQL"
    sudo -A rm -rf /RCM/bkup
else
    sleep 2
fi
sudo -A rm -rf /var/lib/i4s/RCM/P8080/webapps/RCM-Controller/workflow/
sudo -A find /var/log/rcm/ -mindepth 2 -delete
"""
        remote_dir='/tmp'
        remote_script_path=f'{remote_dir}/reset.sh'
        remote_fstgz_path=f"{remote_dir}/{os.path.basename(local_fstgz_path)}"
        remote_dbsql_path=f"{remote_dir}/{os.path.basename(local_dbsql_path)}"
        file_content=io.BytesIO(script.encode())
        # SSHクライアントを作成
        sshclient = SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # SSHサーバに接続
            sshclient.connect( hostname=self.addr, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass )
            # コマンドを実行
            if 0 != self.ssh_command( sshclient, f"rm -f '{remote_script_path}' '{remote_fstgz_path}' '{remote_dbsql_path}'"):
                return False

            try:
                with sshclient.open_sftp() as sftp:
                    self._info(f"scp put to {remote_script_path}")
                    sftp.putfo(file_content, remote_script_path)
                    sftp.chmod( remote_script_path, 0o755 )
                    if reset_data:
                        self._info(f"scp put to {remote_fstgz_path}")
                        sftp.put(local_fstgz_path,remote_fstgz_path)
                        self._info(f"scp put to {remote_dbsql_path}")
                        sftp.put(local_dbsql_path,remote_dbsql_path)

                if 0 != self.ssh_command( sshclient, f"{remote_script_path} 2>&1" ):
                    return False
                return True
            finally:
                self.ssh_command( sshclient, f"rm -f '{remote_script_path}' '{remote_fstgz_path}' '{remote_dbsql_path}'")
        except AuthenticationException as ex:
            self._error(str(ex))
            return False
        finally:
            # SSH接続を閉じる
            sshclient.close()

    def init_rcm(self,*, fs:str='', sql:str='', reset_data:bool=False) ->bool:
        local_fstgz_path = fs if fs else 'dmy' # 'FileServer.tgz'
        local_dbsql_path = sql if sql else 'dmy' # 'dumpdb.sql.gz'
        if reset_data:
            if not os.path.exists(local_fstgz_path) or not os.path.exists(local_dbsql_path):
                self._error(f"ERROR: not found {local_fstgz_path} or {local_dbsql_path}")
                return False
        remote_dir='/tmp'
        remote_fstgz_path=f"{remote_dir}/{os.path.basename(local_fstgz_path)}"
        remote_dbsql_path=f"{remote_dir}/{os.path.basename(local_dbsql_path)}"

        script = f"""set -ue

sudo -A systemctl stop i4s-rcm

if [ "{reset_data}" == "True" ]; then
    FSTGZ="$ScrDir/{os.path.basename(local_fstgz_path)}"
    DBSQL="$ScrDir/{os.path.basename(local_dbsql_path)}"
    sudo -A rm -rf /RCM/bkup
    sudo -A /opt/i4s/RCM/bin/init-rcmfs.sh --fs --tgz "$FSTGZ" #>/dev/null
    sudo -A /opt/i4s/RCM/bin/init-rcmdb.sh -y --sql "$DBSQL"
    sudo -A rm -rf /RCM/bkup
else
    sleep 2
fi
sudo -A rm -rf /var/lib/i4s/RCM/P8080/webapps/RCM-Controller/workflow/
sudo -A rm -rf /var/log/rcm/RCM/* /var/log/rcm/P8080/*
"""
        transfer = [
            CopyTo(local_fstgz_path, remote_fstgz_path),
            CopyTo(local_dbsql_path, remote_dbsql_path),
        ]
        self._sudo('init_rcm', script, transfer=transfer )
        return False

    def get_logs( self, *, local_tgz_path:str ) ->bool:

        remote_dir='/tmp'
        remote_script_path=f'{remote_dir}/getlogs.sh'
        remote_tgz_path = f'{remote_dir}/rcmlogs.tar.gz'
        sudo_passwd=self.ssh_pass
        script = f"""#!/bin/bash
if [ -n "$SUDO_ASKPASS" ]; then
  echo '{sudo_passwd}'
  exit 0
fi

ScrDir=$(cd $(dirname $0);pwd)
export SUDO_ASKPASS="$ScrDir/$(basename $0)"
function fn_cleanup() {{
  rm -rf "$SUDO_ASKPASS" "$WORK_DIR"
}}
trap fn_cleanup EXIT
set -ue
WORK_DIR=$(mktemp -d)
sudo -A rm -f  {remote_tgz_path}
sudo -A cp -pr /var/log/rcm/RCM "$WORK_DIR"
sudo -A cp -pr /var/log/rcm/P8080 "$WORK_DIR"
sudo -A chown -R {self.ssh_user} "$WORK_DIR"
tar -C "$WORK_DIR" -zcvf {remote_tgz_path} .

"""
        file_content=io.BytesIO(script.encode())
        # SSHクライアントを作成
        sshclient = SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # SSHサーバに接続
            sshclient.connect(hostname=self.addr, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass)
            # コマンドを実行
            if 0 != self.ssh_command( sshclient, f"rm -f '{remote_script_path}' '{remote_tgz_path}'"):
                return False

            try:
                with sshclient.open_sftp() as sftp:
                    self._info(f"scp put to {remote_script_path}")
                    sftp.putfo(file_content, remote_script_path)
                    sftp.chmod( remote_script_path, 0o755 )
                    if 0 != self.ssh_command( sshclient, f"{remote_script_path}" ):
                        return False
                    sftp.get( remote_tgz_path, local_tgz_path )
                return True
            finally:
                self.ssh_command( sshclient, f"rm -f '{remote_script_path}' '{remote_tgz_path}'")
        except AuthenticationException as ex:
            self._error(str(ex))
            return False
        finally:
            # SSH接続を閉じる
            sshclient.close()

    def perf_trace(self, logfile) ->PerfTracer:
        sar = PerfTracer(self.addr,self.ssh_port,self.ssh_user, self.ssh_pass, logfile)
        return sar

def sshtest():

    pretty_list = [
        "Red Hat Enterprise Linux 9.4 (Plow)",
        "Red Hat Enterprise Linux 8.10 (Ootpa)",
        "Rocky Linux 8.10 (Green Obsidian)",
        "CentOS Linux 7 (Core)",
        "openSUSE Leap 15.6",
        "Ubuntu 24.04.1 LTS",
    ]
    for p in pretty_list:
        x = RCMCTL.strip_osname(p)
        print(f"{p} => {x}")

    RH8x03 = RCMCTL( 'RHEL8x03', 'maeda', addr='192.168.125.240', passwd='maeda0501')
    RH8x03.getinfo()
    #C7x01.reboot(log_dir='tmp')
    # C7x01.cleanup_rcmcnt(log_dir='tmp')
    sarlogpath='tmp/sarlog.txt'

    nn:int|None = RH8x03.get_loglines()
    print(f"logline:{nn}")

    with RH8x03.perf_trace(sarlogpath):
        time.sleep(10)
    
    rcmlogpath = 'tmp/rcmcnt.log'
    if nn:
        nn = nn -100
    else:
        nn = 1
    RH8x03.get_perflog( rcmlogpath, nn )
    
def transfertest():
    RH8x03 = RCMCTL( 'RHEL8x03', 'maeda', addr='192.168.125.240', passwd='maeda0501')
    script="""
echo "---1"
cat /tmp/data1
echo "---2"
cat /tmp/data2
echo "---3"
echo 'test data 3' >/tmp/data3
echo "---4"
echo 'test data 4' >/tmp/data4
echo "---end"
"""
    out:BytesIO = BytesIO()
    data1:BytesIO = BytesIO('test data 1'.encode())
    data2:BytesIO = BytesIO('test data 2'.encode())
    data3:BytesIO = BytesIO()
    data4:BytesIO = BytesIO()
    transfer = [
        CopyTo( data1, '/tmp/data1', keep=True ),
        CopyTo( data2, '/tmp/data2' ),
        CopyFrom( '/tmp/data3', data3 ),
        CopyFrom( '/tmp/data4', data4, keep=True ),
    ]
    RH8x03._sudo('transfer_test', script, transfer=transfer, out=out )
    print("###output")
    print( out.getvalue().decode() )
    print("###data3")
    print( data3.getvalue().decode() )
    print("###data4")
    print( data4.getvalue().decode() )

def test_systemConfig():
    RH8x03 = RCMCTL( 'RHEL8x03', 'maeda', addr='192.168.125.240', passwd='maeda0501')

    if RH8x03.chk_perflog():
        print("OK")
    else:
        print("NG")

if __name__ == "__main__":
    # sshtest()
    #transfertest()
    test_systemConfig()
