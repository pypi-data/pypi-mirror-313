import sys,os
import time
import uuid
import json
import tempfile
import io
from io import BytesIO
import socket
from urllib.parse import urlparse
from logging import getLogger, Formatter, FileHandler, DEBUG, INFO, WARN, ERROR, NOTSET
from datetime import datetime
from typing import NamedTuple, NewType, Type, Optional
import requests
import http.client

from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment

# sys.path.append(os.getcwd())
import i4srcm.lxmlutil as lx
from i4srcm.selwhere import convert_easypath_to_xml
from i4srcm.workflow_preset import update_preset
from i4srcm.system_config import dict_to_systemConfig, systemConfig_to_dict

logger = getLogger('rcm.client')

UserId = NewType('UserId',int)
UserInfoId = NewType('UserInfoId',str)
ProjectId = NewType('ProjectId',int)
TemplateId = NewType('TemplateId',int)
WorkFlowId = NewType('WorkFlowId',str)
TransactionId = NewType('TransactionId',str)

def get_local_ip( remote_ip:str|None ) ->str|None:
    if remote_ip:
        for port in [80,8080,22]:
            # ダミーのソケットを作成し、通信相手のIPに接続する
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # ソケットを使って相手先に接続し、その際に使用するローカルIPを確認
                s.connect((remote_ip, port))
                # ローカルIPアドレスを取得
                local_addr = s.getsockname()[0]
                return str(local_addr)
            except:
                pass
            finally:
                s.close()
    return None

def b2s(value:bool):
    return 'true' if value else 'false'

def ss(value,default:str='') ->str:
    if isinstance(value,str):
        return value
    return default

def str2int(value) ->int|None:
    try:
        return int(value)
    except:
        pass
    return None

def parse_int(val,default=0) ->int:
    try:
        return int(val)
    except:
        pass
    try:
        return int(default)
    except:
        pass
    return 0

def obj_to_str( obj ) ->str:
    try:
        if isinstance(obj,Elem):
            content_bytes:bytes = etree.tostring( obj, pretty_print=True, xml_declaration=True, encoding='UTF-8')
            content_txt:str = content_bytes.decode().strip()
            return content_txt
        elif isinstance(obj,dict|list):
            return json.dumps(obj,ensure_ascii=False,indent=2).strip()
        elif isinstance(obj,str|float|int):
            return str(obj)
        else:
            return str(obj)
    except:
        pass
    return ''

def astr( value:str|list[str]|None ) ->str:
    if isinstance(value,list):
        return ",".join(value)
    elif value is not None:
        return str(value)
    return ''

def dedent(text:str) ->str:
    lines = text.splitlines()
    # 空でない行の最小インデントを計算する
    min_indent = float('inf')
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:
            indent = len(line) - len(stripped_line)
            min_indent = min(min_indent, indent)

    # インデントを取り除いた新しい行を作成
    if min_indent == float('inf'):
        min_indent = 0

    dedented_lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]
    return '\n'.join(dedented_lines).strip()

class DBContent(NamedTuple):
    tagid:int
    tagname:str
    name:str|None
    latest:bool|None
    delete:bool|None
    childs:list["DBContent"]

    def __str__(self):
        if self.name:
            return f"{self.name}[{self.tagname}@{self.tagid}]"
        else:
            return f"[{self.tagname}@{self.tagid}]"

    def __iter__(self):
        return iter(self.childs)

    @staticmethod
    def lxml_to_tag( e:Elem|None ) ->Optional["DBContent"]:
        if isinstance(e,Elem) and not isinstance(e,Comment) and len(e)>0:
            tagid = parse_int(e.get('tagid'),0)
            tagname = e.tag
            name = lx.xpath_to_str(e, 'name' )
            if not name:
                name = lx.xpath_to_str(e, 'title' )
            latest = lx.xpath_to_bool(e,'latest')
            delete = lx.xpath_to_bool(e,'delete')
            childs = [ ]
            for c in e:
                ct = DBContent.lxml_to_tag(c)
                if ct:
                    childs.append(ct)
            return DBContent(tagid,tagname,name,latest,delete,childs)
        return None

class SizeCounter:
    """HTTPで送信データのサイズを事前にカウントするためのダミークラス"""
    def __init__(self):
        self.size = 0

    def send(self, data):
        self.size += len(data)

    def get_size(self):
        return self.size

class RCMCNT_api:
    def __init__(self, url, *, tmpdir:str|None=None, logfile:str|None=None):
        self._api_tmp:str|None = tmpdir
        self._url = f"{url}/RCM-Controller"
        self._client_ip:str = ''
        self._connect_timeout:float = 10
        self._read_timeout:float = 30
        self._error_retry:int = 3
        self.logger = getLogger('rcm.client.api')
        self.logger.propagate = False
        if logfile:
            if os.path.isdir(os.path.dirname(logfile)):
                self.logger.setLevel(DEBUG)
                # フォーマットの指定
                file_formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
                file_hdr = FileHandler(logfile)
                file_hdr.setLevel(NOTSET)
                file_hdr.setFormatter(file_formatter)
                self.logger.addHandler(file_hdr)

    def _exception(self, msg, *args, exc_info=True, **kwargs):
        logger.exception(msg, *args, exc_info=exc_info, **kwargs)
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def _error(self, msg, *args, **kwargs):
        logger.error(msg,*args,**kwargs)
        self.logger.error(msg,*args,**kwargs)

    def _info(self, msg, *args, **kwargs):
        logger.info(msg,*args,**kwargs)
        self.logger.info(msg,*args,**kwargs)

    def _debug(self, msg, *args, **kwargs):
        logger.debug(msg,*args,**kwargs)
        self.logger.debug(msg,*args,**kwargs)

    def gettmpdir(self):
        tmpdir = self._api_tmp
        if tmpdir is not None:
            try:
                os.makedirs(tmpdir,exist_ok=True)
            except:
                tmpdir=None
        if tmpdir is None or not os.path.isdir(tmpdir):
            tmpdir = os.path.join(tempfile.gettempdir(),'rcmclient')
            os.makedirs(tmpdir,exist_ok=True)
        return tmpdir

    def mktmpfile(self,fileid:str):
        tmpdir = self.gettmpdir()
        for i in range(9999999):
            p = os.path.join( tmpdir, f"{i:04d}_{fileid}")
            if not os.path.exists(p):
                return p
        raise ValueError(f'can not create temp file {fileid}')

    def _get_local_ip(self) ->str|None:
        if self._client_ip == '':
            self._client_ip = 'false'
            url = urlparse(self._url)
            addr = get_local_ip( url.hostname )
            if addr:
                self._client_ip = addr
        return self._client_ip if self._client_ip!='false' else None

    def api_rest(self, request:Elem|str, *, read_timeout:float|None=None, logging_request=True, logging_response=True, debug=False) ->Elem|None:
        response_xml:Elem|None = None
        read_time_out = float(read_timeout) if isinstance(read_timeout,int|float) and read_timeout>0 else float(self._read_timeout)
        to = (float(self._connect_timeout),read_time_out)
        try:
            request_xml:Elem|None = lx.from_str(request) if not isinstance(request,Elem) else request
            if not isinstance(request_xml,Elem):
                self._error( 'request is None')
                return None
            api_name = lx.xpath_to_str( request_xml, "name(/*[1])")
            if not api_name:
                self._error(f"(RCMapi) can't get apiname in request")
                return None
            url:str = f"{self._url}/action/request.html/{api_name}"
            client_ip = self._get_local_ip()
            if client_ip:
                lx.set_text( request_xml, 'clientIP', client_ip )
            if logging_request:
                self.logger.info( obj_to_str(request_xml) )
            else:
                self.logger.info( f"{request_xml.tag}" )
            request_bytes:bytes = etree.tostring(request_xml,pretty_print=True, xml_declaration=True, encoding='UTF-8')
            headers = {"Content-Type": "application/xml"}
            if debug:
                headers['x-rcm-debug'] = 'ignoreLogDB;ignoreFS'
            for ntry in range(self._error_retry+1):
                try:
                    with requests.post(url, timeout=to, headers=headers, data=request_bytes) as response:
                        if response.status_code == 200:
                            try:
                                response_xml = etree.fromstring(response.content)
                                if logging_response:
                                    self.logger.info( obj_to_str( response_xml ))
                                else:
                                    stat = lx.xpath_to_str(response_xml, 'result')
                                    self.logger.info(f"{response_xml.tag} result:{stat}")
                            except:
                                self._exception(f"request error {api_name} {response.status_code} parse error")
                            break
                        else:
                            self._error(f"request error {api_name} {response.status_code}")
                            self.logger.error(f"request error {api_name} {response.status_code}")
                            if ntry==self._error_retry:
                                break
                except requests.exceptions.ConnectTimeout as ex:
                    self._error( f"{ex}" )
                time.sleep(3)
        except requests.exceptions.ReadTimeout as ex:
            self._error( f"{ex}" )
        except Exception as ex:
            self._exception("error in api")
        return response_xml

    def api_rest_s(self, request:Elem|str, out, *, read_timeout:float|None=None, logging_request=True, logging_response=True, debug=False) ->Elem|None:
        response_xml:Elem|None = None
        read_time_out = float(read_timeout) if isinstance(read_timeout,int|float) and read_timeout>0 else float(self._read_timeout)
        to = (float(self._connect_timeout),read_time_out)
        try:
            request_xml:Elem|None = lx.from_str(request) if not isinstance(request,Elem) else request
            if not isinstance(request_xml,Elem):
                self._error( 'request is None')
                return None
            api_name = lx.xpath_to_str( request_xml, "name(/*[1])")
            if not api_name:
                self._error(f"(RCMapi) can't get apiname in request")
                return None
            url:str = f"{self._url}/action/request.html/{api_name}"
            client_ip = self._get_local_ip()
            if client_ip:
                lx.set_text( request_xml, 'clientIP', client_ip )
            if logging_request:
                self.logger.info( obj_to_str(request_xml) )
            else:
                self.logger.info( f"{request_xml.tag}" )
            request_bytes:bytes = etree.tostring(request_xml,pretty_print=True, xml_declaration=True, encoding='UTF-8')
            headers = {"Content-Type": "application/xml"}
            if debug:
                headers['x-rcm-debug'] = 'ignoreLogDB;ignoreFS'
            for ntry in range(self._error_retry+1):
                try:
                    with requests.post(url, timeout=to, headers=headers, data=request_bytes) as response:
                        if response.status_code == 200:
                            #response.
                            try:
                                response_xml = etree.fromstring(response.content)
                                if logging_response:
                                    self.logger.info( obj_to_str( response_xml ))
                                else:
                                    stat = lx.xpath_to_str(response_xml, 'result')
                                    self.logger.info(f"{response_xml.tag} result:{stat}")
                            except:
                                self._exception(f"request error {api_name} {response.status_code} parse error")
                            break
                        else:
                            self._error(f"request error {api_name} {response.status_code}")
                            self.logger.error(f"request error {api_name} {response.status_code}")
                            if ntry==self._error_retry:
                                break
                except requests.exceptions.ConnectTimeout as ex:
                    self._error( f"{ex}" )
                time.sleep(3)
        except requests.exceptions.ReadTimeout as ex:
            self._error( f"{ex}" )
        except Exception as ex:
            self._exception("error in api")
        return response_xml

    # リクエストボディの作成を共通化した関数
    @staticmethod
    def _build_multipart_body(form_data, boundary, conn):
        boundary_str = f'--{boundary}\r\n'

        # form_dataからデータを構築
        for key, value in form_data.items():
            if isinstance(value, tuple):
                if value[0] == 'file':
                    file_path = value[1]
                    if not os.path.isfile(file_path):
                        raise ValueError(f"Invalid file path: {file_path}")
                    file_name = os.path.basename(file_path)
                else:
                    value_bytes = str(value[1]).encode('utf-8')
                    file_name = 'dummy'
                # ファイルフィールドのヘッダーを追加
                conn.send(boundary_str.encode('utf-8'))
                conn.send(f'Content-Disposition: form-data; name="{key}"; filename="{file_name}"\r\n'.encode('utf-8'))
                conn.send(b'Content-Type: application/octet-stream\r\n\r\n')

                if value[0] == 'file':
                    # ファイルを読み込んで追加
                    with open(file_path, 'rb') as f:
                        while True:
                            chunk = f.read(81920)  # 8KBずつ読み込む
                            if not chunk:
                                break
                            conn.send(chunk)
                else:
                    conn.send( value_bytes )
                conn.send(b'\r\n')

            else:
                # 通常のフィールドの処理
                conn.send(boundary_str.encode('utf-8'))
                conn.send(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8'))
                conn.send(f'{str(value)}\r\n'.encode('utf-8'))

        # 最終バウンダリを追加
        conn.send(f'--{boundary}--\r\n'.encode('utf-8'))

    def api_post_to_xml(self, api_name:str, form_data:dict, *, read_timeout:float|None=None, retry_wait=5) ->Elem|None:

        self.logger.info( f"{api_name} {obj_to_str(form_data)}")
        read_time_out = float(read_timeout) if isinstance(read_timeout,int|float) and read_timeout>0 else float(self._read_timeout)

        parsed_url = urlparse(f"{self._url}/action/request.html/{api_name}")
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")
        host = parsed_url.netloc
        endpoint = parsed_url.path or "/"

        # バウンダリの生成
        boundary = str(uuid.uuid4())

        # サイズカウンタを使ってリクエストボディのサイズを計算
        size_counter = SizeCounter()
        RCMCNT_api._build_multipart_body(form_data, boundary, size_counter)
        content_length = size_counter.get_size()

        # ヘッダーの設定
        headers = {
            "Content-Type": f"multipart/form-data; boundary=\"{boundary}\"; charset=\"UTF-8\"",
            "Content-Length": str(content_length),
        }
        # リトライ処理のためのループ
        try:
            for attempt in range(self._error_retry+1):
                if attempt>0:
                    time.sleep(retry_wait)
                try:
                    # 接続
                    conn = http.client.HTTPConnection(host, timeout=self._connect_timeout)
                    conn.putrequest("POST", endpoint)
                    # ヘッダ送信
                    for header, value in headers.items():
                        conn.putheader(header, value)
                    conn.endheaders()
                except (http.client.HTTPException, TimeoutError, OSError) as e:
                    self._error(f"Attempt {attempt + 1} failed: {e}")
                    continue
                try:
                    # ボディをストリーム形式で送信
                    RCMCNT_api._build_multipart_body(form_data, boundary, conn )
                    # レスポンスを取得（read_timeoutを指定）
                    conn.sock.settimeout(read_time_out)  # read_timeoutの設定
                    response = conn.getresponse()
                    if response.status == 200:
                        try:
                            response_xml = etree.fromstring(response.read())
                            self.logger.info( obj_to_str(response_xml) )
                            return response_xml
                        except:
                            self._exception(f"request error {api_name} {response.status} parse error")
                        break
                    else:
                        self._error(f"request error {api_name} {response.status}")
                        if response.status != 500:
                            break
                finally:
                    try:
                        conn.close()
                    except:
                        pass
        except Exception as ex:
            self._exception("error in api")

    def api_isAlive(self):
        try:
            req = f"""<isAlive></isAlive>"""
            res = self.api_rest(req)
            result:str|None = lx.xpath_to_str(res,"/isAlive_res/result")
            if result=="OK":
                return True
        finally:
            pass
        return False

    def api_get_user_info_id(self,user_name:str,passwd:str) ->tuple[UserInfoId,UserId]|tuple[None,None]:

        request_xml = etree.Element("getUserInfo")
        lx.set_text(request_xml, "username", user_name )
        lx.set_text(request_xml, "password", passwd )
        lx.set_text(request_xml, "clearText", "true" )
        res:Elem|None = self.api_rest(request_xml)
        user_info_id = lx.xpath_to_str(res,"/getUserInfo_res/userInfoID")
        if not user_info_id:
            self._error("(AUTO_userInfoID) /getUserInfo_res/userInfoID not found")
            return None,None
        user_id = lx.xpath_to_int( res, "/getUserInfo_res/userid" )
        if not user_id:
            self._error("(AUTO_userInfoID) /getUserInfo_res/userid not found")
            return None,None
        return UserInfoId(user_info_id), UserId(user_id)

    def api_remove_user_info_id(self, user_info_id:UserInfoId) ->bool:
        if user_info_id:
            request_xml = etree.Element("removeUserInfo")
            lx.set_text(request_xml,'userInfoID',user_info_id)
            res:Elem|None = self.api_rest(request_xml)
            if res is not None:
                result_status = lx.xpath_to_str(res,"/*/result")
                if result_status=='OK':
                    return True
        return False

    def api_get_controller_info(self, user_info_id:UserInfoId)->tuple[str,str]|tuple[None,None]:
        try:
            request_xml = etree.Element("getControllerInfo" )
            lx.set_text(request_xml,'userInfoID',user_info_id)
            res:Elem|None = self.api_rest(request_xml)
            version:str|None = lx.xpath_to_str(res,"/rcmServer/version")
            buildTime:str|None = lx.xpath_to_str( res, "/rcmServer/buildTime")
            if isinstance(version,str) and isinstance(buildTime,str) and version.strip()!='' and buildTime.strip()!='':
                return version,buildTime
        except:
            pass
        return None,None


    def api_systemConfig(self, user_info_id:UserInfoId, config:dict[str,object]|None = None ) ->dict[str,object]|None:
        try:
            request:Elem = etree.Element('systemConfig')
            dict_to_systemConfig(config,request)
            lx.set_text(request,'userInfoID',user_info_id)
            res:Elem|None = self.api_rest(request)
            if res is not None:
                result_status = lx.xpath_to_str(res,"/*/result")
                if result_status=='OK':
                    # print( etree.tostring(res,pretty_print=True, xml_declaration=True, encoding='UTF-8').decode() )
                    res_dict = systemConfig_to_dict(res)
                    # print( json.dumps(res_dict,ensure_ascii=False,indent=2) )
                    return res_dict
        except:
            pass
        return None

    def api_submit_workflow(self, user_info_id:UserInfoId, project_id:int, template_id:int, wf_xml, *, name:str|None=None, params:dict|None=None, attache_file:bool=False) ->str|None:

        RCMAPI_submitRequestID = f"test{os.getpid()}"
        if os.path.exists(wf_xml):
            if os.path.getsize(wf_xml) == 0:
                self._error("(api_submit_workflow) Workflow XML file is missing or empty")
                return None

        # XML文字列を解析してElementツリーに変換
        parser = etree.XMLParser() 
        # with open(wf_xml, 'r') as stream:
        #     wf_content = stream.read()
        # wf_root = etree.fromstring(wf_content,parser)
        wf_root:ETree = etree.parse(wf_xml,parser)
        wf_body:Elem = wf_root.xpath('//WorkFlow')
        wf_body:Elem = wf_body[0]
        update_preset(wf_body,params=params)
        if name:
            name_elem:Elem = etree.SubElement(wf_body,"name")
            name_elem.text = name
        #
        request_elem:Elem = etree.Element('submitWorkFlow')
        lx.set_text( request_elem, 'userInfoID', user_info_id )
        lx.set_text( request_elem, 'templateID', template_id )
        lx.set_text( request_elem, 'projectID', project_id )
        lx.set_text( request_elem, 'projectIDOrg', project_id )
        lx.set_text( request_elem, 'submitRequestID', RCMAPI_submitRequestID )
        request_elem.append( wf_body )

        response_elem = self.api_rest( request_elem, logging_request=False )
        stat = lx.xpath_to_str(response_elem, 'result')
        wfid = lx.xpath_to_str(response_elem,'workFlowID') if stat=='OK' else None
        return wfid if isinstance(wfid,str) and len(wfid)>0 else None

        # # 更新されたXMLを文字列として返す
        # wf_content:str = etree.tostring(wf_body, xml_declaration=False, encoding='UTF-8', pretty_print=True).decode()

        # attache_flg = 'true' if attache_file else 'false'
        # content = f"""
        # <?xml version="1.0" encoding="UTF-8"?>
        # <submitWorkFlow>
        #  <clientIP>{self._client_ip}</clientIP>
        # <userInfoID>{user_info_id}</userInfoID>
        # <templateID>{template_id}</templateID>
        # <projectID>{project_id}</projectID>
        # <projectIDOrg>{project_id}</projectIDOrg>
        # <submitRequestID>{RCMAPI_submitRequestID}</submitRequestID>
        # <attacheFile>{attache_flg}</attacheFile>
        # {wf_content}
        # </submitWorkFlow>
        # """
        # make_xml(input_file, content)
        # self.rcm_api(input_file, output_file)
        # result = get_xpath("/*/result", output_file)
        # RCMAPI_workFlowID = get_xpath("/submitWorkFlow_res/workFlowID", output_file)
        # # print(f"submitWorkFlow result: {result}")
        # # print(f"workFlowID: {RCMAPI_workFlowID}")
        # return RCMAPI_workFlowID

    def api_execute_workflow(self):
        pass

    def api_execute_template(self, user_info_id:UserInfoId, project_id:ProjectId, template_id:TemplateId, *, transaction_id:TransactionId|None=None, params:dict|None=None, defines:dict|None=None, attache_file:bool=False) ->WorkFlowId|None:
        api_name:str = 'executeTemplate'
        RCMAPI_submitRequestID = f"test{os.getpid()}"

        api_parameters:list[str] = []

        api_parameters.append(f'<{api_name}>')
        api_parameters.append(f'<userInfoID>{user_info_id}</userInfoID>')

        if transaction_id:
            api_parameters.append(f'<transaction>{transaction_id}</transaction>')
        api_parameters.append(f'<wait>false</wait>')
        api_parameters.append(f'<templateID>{template_id}</templateID>')
        api_parameters.append(f'<projectID>{project_id}</projectID>')
        api_parameters.append(f'<projectIDOrg>{project_id}</projectIDOrg>')
        api_parameters.append(f'<submitRequestID>{RCMAPI_submitRequestID}</submitRequestID>')
        if isinstance(attache_file,bool) and attache_file:
            api_parameters.append(f'<attacheFile>true</attacheFile>')
        if isinstance(params,dict):
            for k,v in params.items():
                api_parameters.append(f'<parameter name="{k}">{v}</parameter>')
        if isinstance(defines,dict):
            for k,v in defines.items():
                api_parameters.append(f'<define name="{k}">{v}</define>')

        api_parameters.append(f'</{api_name}>')

        request = '\n'.join(api_parameters)
        res = self.api_rest(request)
        result = lx.xpath_to_str(res,"/*/result")
        RCMAPI_workFlowID = lx.xpath_to_str(res,"/*[1]/workFlowID")
        if RCMAPI_workFlowID:
            return WorkFlowId(RCMAPI_workFlowID)
        return None

    def api_set_workflow_label(self, user_info_id:UserInfoId, workflow_id:WorkFlowId, label_name, file_path) ->bool:
        
        file_name = os.path.basename(file_path)
        form_data = {
            'userInfoID': user_info_id,
            'workFlowID': workflow_id,
            f'{label_name}_NAME': ('text',file_name),
            f'{label_name}': ('file',file_path),
        }
        res:Elem|None = self.api_post_to_xml("setWorkFlowLabel", form_data )
        if 'OK' != lx.xpath_to_str(res,'result'):
            return False
        return True

    def api_start_workflow(self, user_info_id:UserInfoId, workflow_id:WorkFlowId) ->bool:
        request:Elem = etree.Element('startWorkFlow')
        lx.set_text(request,'workFlowID',workflow_id)
        lx.set_text(request,'userInfoID',user_info_id)
        res:Elem|None = self.api_rest(request)
        result = lx.xpath_to_str(res,"/startWorkFlow_res/result")
        if result!='OK':
            return False
        return True
        # print(f"startWorkFlow result: {result}")

    def api_getWorkFlow(self, user_info_id:UserInfoId, workflow_id:WorkFlowId, *, wait:int|None=None,statistics:bool=False ) ->Elem|None:

        request:Elem = etree.Element('getWorkFlow')
        lx.set_text(request,'workFlowID',workflow_id)
        lx.set_text(request,'userInfoID',user_info_id)
        if statistics:
            lx.set_text(request,'statistics','true')
        readtimeout=None
        if isinstance(wait,int) and wait>0:
            readtimeout = wait + 5
            lx.set_text(request,'wait',str(wait))
        res = self.api_rest( request, read_timeout=readtimeout, logging_response=False)
        if res is not None and res.tag=='Error':
            # RCM1062-2401ではCNTのバグ(ConcurrentModificationException)で以下が返ってくる場合がある
            #<Error>
            #  <result>NG</result>
            #  <reason/>
            #</Error>
            res = self.api_rest( request, read_timeout=readtimeout)
        return res

class RCMCNT_Client(RCMCNT_api):
    def __init__(self, url, *, username:str,passwd:str,logfile:str|None=None,tmpdir:str='tmp'):
        super().__init__(url,logfile=logfile,tmpdir=tmpdir)
        self._user_name=username
        self._user_passwd=passwd
        self._user_info_id:UserInfoId=UserInfoId('')
        self._user_id:UserId = UserId(0)
        self._project_id:ProjectId = ProjectId(0)
        self._version:str = ''
        self._buildTime:str = ''

    def login(self) ->bool:
        user_info_id, user_id = self.api_get_user_info_id( self._user_name, self._user_passwd )
        if user_info_id and user_id:
            self._user_info_id = user_info_id
            self._user_id = user_id
            a,b = self.api_get_controller_info(user_info_id)
            self._version = a if a else ''
            self._buildTime = b if b else ''
            return True
        else:
            return False

    def logout(self, *, user_info_id:str|None=None) ->bool:
        uid:UserInfoId = user_info_id if user_info_id else self._user_info_id
        return self.api_remove_user_info_id( uid )

    def api(self, request:Elem|str, *, user_info_id:str|None=None, debug=False) ->tuple[bool,Elem|None]:
        try:
            request_xml:Elem|None = lx.from_str(request) if not isinstance(request,Elem) else request
            if not isinstance(request_xml,Elem):
                self._error( 'request is None')
                return False,None
            if user_info_id:
                lx.set_text(request_xml,'userInfoID',user_info_id)
            elif self._user_info_id:
                lx.set_text(request_xml,'userInfoID',self._user_info_id)
            resp = self.api_rest(request_xml, debug=debug)
            result = lx.xpath_to_str(resp,"/DBResponse/result")
            if result=='OK':
                return True, resp
            else:
                return False, resp
        except:
            return False,None

    def systemConfig(self,config:dict|None=None ):
        return self.api_systemConfig( self._user_info_id, config )

    def get_loglevel(self) ->str:
        config = self.systemConfig()
        log4j = config.get('log4j',{}) if isinstance(config,dict) else {}
        lv = ''
        if isinstance(log4j,dict):
            lv = log4j.get('jp.co.i4s','')
        return lv

    def set_loglevel(self,lv:str) ->bool:
        if not lv in [ 'DEBUG', 'INFO', 'ERROR' ]:
            return False
        xconfig = { 'log4j': { 'jp.co.i4s': lv } }
        config = self.systemConfig(xconfig)
        log4j = config.get('log4j',{}) if isinstance(config,dict) else {}
        xlv = ''
        if isinstance(log4j,dict):
            xlv = log4j.get('jp.co.i4s','')
        return xlv==lv

    def get_licenseInfo(self) ->str:
        config = self.systemConfig()
        licenseInfo = config.get('licenseInfo',{}) if isinstance(config,dict) else {}
        text = ''
        if isinstance(licenseInfo,dict):
            text = licenseInfo.get('info','').strip()
        return text

    def DBRequest(self, request:Elem|str, *, transaction_id:TransactionId|None=None, user_info_id:str|None=None, debug=False) ->tuple[bool,Elem|None]:
        try:
            request_xml:Elem|None = lx.from_str(request) if not isinstance(request,Elem) else request
            if not isinstance(request_xml,Elem):
                self._error( 'request is None')
                return False,None
            if transaction_id:
                lx.set_text(request_xml,'transaction',transaction_id)
            stat,resp = self.api(request_xml, user_info_id=user_info_id, debug=debug)
            if stat:
                result = lx.xpath_to_str(resp,"/DBResponse/instresult")
                if result=='OK':
                    return True, resp
            return False, resp
        except:
            return False, None

    def SEL2(self, ezpath, *, upperLevel:int|None=None, lowerLevel:int|None=None,transaction_id:TransactionId|None=None, user_info_id:str|None=None)->tuple[bool,Elem|None]:
        
        inst:Elem = convert_easypath_to_xml(ezpath, upperLevel=upperLevel, lowerLevel=lowerLevel)
        
        request:Elem = etree.Element('DBRequest')
        inst.set('no','')
        request.append(inst)
        return self.DBRequest( request, transaction_id=transaction_id, user_info_id=user_info_id)

    def DBPath(self, dbpath:str, *, upperLevel:int|None=None, lowerLevel:int|None=None, append:str|None=None, drop:str|None=None, transaction_id:TransactionId|None=None, user_info_id:str|None=None, debug=False) ->tuple[bool,Elem|None]:
        try:
            request_xml = etree.Element("DBRequest")
            if transaction_id:
                lx.set_text(request_xml,'transaction',transaction_id)
            dbpath_node = lx.set_text(request_xml,"DBPath",dbpath)
            if upperLevel:
                dbpath_node.set("upperLevel", str(upperLevel) )
            if lowerLevel:
                dbpath_node.set("lowerLevel", str(lowerLevel) )
            if append:
                dbpath_node.set("append", astr(append) )
            if drop:
                dbpath_node.set("drop", astr(drop) )
            stat,resp = self.api(request_xml, user_info_id=user_info_id, debug=debug)
            if stat:
                result = lx.xpath_to_str(resp,"/DBResponse/instresult")
                if result=='OK':
                    return True, resp
            return False, resp
        except:
            return False, None

    def get_project_list(self, *,user_info_id:str|None=None)->list[str]:
        request = dedent(f"""
        <DBRequest>
        <instruction no="">
            <instkind>SEL2</instkind>
            <instbody>
            <target>/project/name</target>
            <lowerLevel>0</lowerLevel>
            <selWhere>
                <project>
                <name></name>
                </project>
            </selWhere>
            </instbody>
        </instruction>
        </DBRequest>
        """)
        result:list[str] = []
        stat,res = self.DBRequest(request,user_info_id=user_info_id)
        if stat:
            resset:list|None = lx.xpath_to_obj(res,"/DBResponse/instruction/resultSet/name")
            if resset:
                for res in resset:
                    if isinstance(res,Elem) and res.tag=='name' and res.text is not None:
                        result.append( res.text )
        return result

    def set_project(self, project_name:str, *, root_passwd:str|None = None) ->ProjectId|None:
        pid:ProjectId|None = self.get_project_id(project_name, user_info_id=self._user_info_id )
        if pid is None:
            if root_passwd:
                root_uid,x = self.api_get_user_info_id( 'root', root_passwd )
                if root_uid is not None:
                    pid = self.create_project( project_name, user_info_id=root_uid )
        if pid:
            self._project_id = pid
            return pid
        else:
            return None

    def get_project_id(self, name:str,*,user_info_id:str|None=None)->ProjectId|None:
        request = dedent(f"""
        <DBRequest>
        <instruction no="">
            <instkind>SEL2</instkind>
            <instbody>
            <target>/project</target>
            <lowerLevel>1</lowerLevel>
            <selWhere>
                <project>
                <name>
                    <operand>EQ</operand>
                    <value>{name}</value>
                </name>
                </project>
            </selWhere>
            </instbody>
        </instruction>
        </DBRequest>
        """)
        stat,res = self.DBRequest(request,user_info_id=user_info_id)
        if stat:
            project_id = lx.xpath_to_int(res,"/DBResponse/instruction/resultSet/project/@tagid")
            try:
                if isinstance(project_id,int):
                    return ProjectId(project_id)
            except:
                pass
        return None

    def create_project(self,name,*,user_info_id:UserInfoId|None=None) ->ProjectId|None:
        project_id = self.get_project_id( name, user_info_id=user_info_id)
        if project_id:
            return project_id
        
        # プロジェクトが存在しない場合、新規作成
        request = dedent(f"""
        <DBRequest>
        <instruction no="">
            <instkind>INS</instkind>
            <instbody>
            <project auth="gg">
                <name auth="gu">{name}</name>
                <startDate auth="gu"/>
                <endDate auth="gu"/>
                <page auth="gu">/action/workflow/top.html</page>
                <comment auth="gu">comment</comment>
                <otherProject auth="gu">false</otherProject>
                <nodeReadAuth auth="gu">g</nodeReadAuth>
                <nodeWriteAuth auth="gu">g</nodeWriteAuth>
                <leafReadAuth auth="gu">g</leafReadAuth>
                <leafWriteAuth auth="gu">u</leafWriteAuth>
                <activeProject auth="gu">true</activeProject>
                <member auth="gu">
                <userid auth="gu">3</userid>
                {f'<userid auth="gu">{self._user_id}</userid>' if self._user_id else ''}
                </member>
            </project>
            </instbody>
        </instruction>
        </DBRequest>
        """)
        stat,res = self.api(request,user_info_id=user_info_id)
        if stat:
            project_id = lx.xpath_to_int(res,"/DBResponse/instruction/tagid")
            try:
                if isinstance(project_id,int):
                    return ProjectId(project_id)
            except:
                pass
        self._error("(AUTO_projectID) DBRequest result is NG")
        return None

    def get_children(self, tagid:int, *, appends:list[str]|None=['name','title'], user_info_id:str|None=None)->list[DBContent]:
        request:Elem = etree.Element('DBRequest')
        inst_elem:Elem = etree.SubElement(request,'instruction', attrib={'no':''})
        lx.set_text( inst_elem, 'instkind', 'GET_CHILDREN')
        body_elem:Elem = etree.SubElement(inst_elem, 'instbody')
        lx.set_text( body_elem, 'tagid', str(tagid) )
        if isinstance(appends,list):
            for name in appends:
                lx.set_text( body_elem, 'append', name )
        result:list[DBContent] = []
        stat,res = self.DBRequest(request,user_info_id=user_info_id)
        if stat:
            parent_list:list|None = lx.xpath_to_obj(res,"/DBResponse/instruction/resultSet/*")
            if parent_list:
                for parent in parent_list:
                    tag = DBContent.lxml_to_tag(parent)
                    if tag:
                        result.append(tag)
        return result

    def get_template_id(self, name:str, *, project_id:ProjectId|None=None ) ->TemplateId|None:
        project_id = project_id if project_id is not None else self._project_id
        if project_id is None:
            return None
        # テンプレートの検索
        request = dedent(f"""
        <DBRequest>
        <instruction no="">
            <instkind>SEL2</instkind>
            <instbody>
            <target>/project/template</target>
            <lowerLevel>1</lowerLevel>
            <selWhere>
                <project>
                <tagid>
                    <layer>tagid</layer>
                    <operand>EQ</operand>
                    <value>{project_id}</value>
                </tagid>
                <template>
                    <name>
                    <operand>EQ</operand>
                    <value>{name}</value>
                    </name>
                </template>
                </project>
            </selWhere>
            </instbody>
        </instruction>
        </DBRequest>
        """)
        stat,res = self.DBRequest(request)
        if stat:
            template_id = lx.xpath_to_int(res,"/DBResponse/instruction/resultSet/template/@tagid")
            try:
                if isinstance(template_id,int):
                    return TemplateId(template_id)
            except:
                pass
            self._info(f"(get_template_id) not found {name}")
        else:
            self._error("(get_template_id) DBRequest result is NG")
        return None

    def update_template(self, name:str, wfxml, *, project_id:ProjectId|None=None, transaction_id:TransactionId|None=None ) ->TemplateId|None:
        project_id = project_id if project_id is not None else self._project_id
        if project_id is None:
            return None        
        template_id = self.get_template_id(name,project_id=project_id)
        if isinstance(template_id,int) and template_id>0:
            # テンプレートの検索
            request1 = lx.from_str( dedent(f"""
            <DBRequest>
            <instruction no="">
                <instkind>SEL2</instkind>
                <instbody>
                <target>/project/template/body</target>
                <lowerLevel>0</lowerLevel>
                <selWhere>
                              <project>
                    <template>
                    <tagid>
                        <layer>tagid</layer>
                        <operand>EQ</operand>
                        <value>{template_id}</value>
                    </tagid>
                    <body/>
                    </template>
                    </project>
                </selWhere>
                </instbody>
            </instruction>
            </DBRequest>
            """) )
            if request1 is None:
                raise Exception("")
            stat,res = self.DBRequest(request1,transaction_id=transaction_id)
            if not stat:
                self._error("(update_template) DBRequest result is NG")
                return None
            body_id = lx.xpath_to_int(res,"/DBResponse/instruction/resultSet/body/@tagid")
            if not isinstance(body_id,int):
                self._error("(update_template) failled to get body tag")
                return None
            # テンプレートの更新
            request2:Elem|None = lx.from_str(dedent(f"""
            <DBRequest>
            <instruction no="">
                <instkind>DEL</instkind>
                <instbody>
                <tagid>{body_id}</tagid>
                </instbody>
            </instruction>
            <instruction no="">
                <instkind>ADD</instkind>
                <instbody>
                <targetTagid>{template_id}</targetTagid>
                    <body auth="gu"/>
                </instbody>
            </instruction>
            </DBRequest>
            """))
            if request2 is None:
                raise Exception("xxx")
            body:Elem|None = lx.xpath_to_elem( request2, '/DBRequest/instruction/instbody/body' )
            if body is None:
                raise Exception("xxx")
            for e in wfxml.iter():
                if not isinstance(e,etree._Comment):
                    e.set('auth','aa')
            body.append( wfxml )
            stat,res = self.DBRequest(request2,transaction_id=transaction_id)
            if stat:
                body_id = lx.xpath_to_int(res,"/DBResponse/instruction[2]/tagid")
                if isinstance(body_id,int):
                    self._info(f"(update_template) updated {template_id} {name}")
                    return template_id
                self._error(f"(update_template) failled to update {name}")
            else:
                self._error("(update_template) DBRequest result is NG")
            return None
        else:
            # テンプレートが存在しない場合、新規作成
            request:Elem|None = lx.from_str( dedent(f"""
            <DBRequest>
            <instruction no="">
                <instkind>ADD</instkind>
                <instbody>
                <targetTagid>{project_id}</targetTagid>
                <template auth="gu">
                    <name auth="gu">{name}</name>
                    <date auth="gu">2010-12-22</date>
                    <hidden auth="gu">false</hidden>
                    <editable auth="gu">false</editable>
                    <comment auth="gu">general template</comment>
                    <VRule auth="gu"/>
                    <body auth="gu"/>
                </template>
                </instbody>
            </instruction>
            </DBRequest>
            """) )
            if request is None:
                raise Exception("xxx")
            body:Elem|None = lx.xpath_to_elem( request, '/DBRequest/instruction/instbody/template/body' )
            if body is None:
                raise Exception("xxx")
            for e in wfxml.iter():
                if not isinstance(e,etree._Comment):
                    e.set('auth','aa')
            body.append( wfxml )

            stat, res = self.DBRequest(request,transaction_id=transaction_id)
            if stat:
                template_id = lx.xpath_to_int(res,"/DBResponse/instruction/tagid")
                try:
                    if isinstance(template_id,int):
                        self._info(f"(update_template) created {template_id} {name}")
                        return TemplateId(template_id)
                except:
                    pass
                self._error(f"(update_template) failled to create {name}")
            else:
                self._error("(update_template) DBRequest result is NG")
            return None

    def execute_template(self, template_id:TemplateId, *, transaction_id:TransactionId|None=None, params:dict|None=None, defines:dict|None=None, attache_file:bool=False) ->WorkFlowId|None:
        return self.api_execute_template(self._user_info_id, self._project_id, template_id, transaction_id=transaction_id, params=params, defines=defines, attache_file=attache_file)

    def set_workflow_label(self,workflow_id:WorkFlowId, label_name, file_path) ->bool:
        return self.api_set_workflow_label( self._user_info_id, workflow_id, label_name, file_path)

    def start_workflow(self,workflow_id:WorkFlowId) ->bool:
        return self.api_start_workflow( self._user_info_id, workflow_id)

    def get_workflow(self,workflow_id:WorkFlowId, *, wait:int|None=None, statistics:bool=False ) ->Elem|None:
        return self.api_getWorkFlow( self._user_info_id, workflow_id, wait=wait, statistics=statistics )

