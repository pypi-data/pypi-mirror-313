
from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment

def ss(value,default:str='') ->str:
    if isinstance(value,str):
        return value
    return default

def systemConfig_to_dict( el:Elem|None) ->dict[str,object]|None:
    """systemConfigレスポンスをdictに変換する"""
    if not isinstance(el,Elem):
        return None
    result = {}
    for child in el:
        if len(child)>0:
            result[child.tag] = systemConfig_to_dict(child)
        elif child.tag=='license' and child.get('option'):
            opt = result.get(child.tag)
            if not isinstance(opt,dict):
                opt = {}
                result[child.tag] = opt
            opt[child.get('option')] = child.text
        elif child.tag=='log4j' and child.get('level') and child.get('name'):
            opt = result.get(child.tag)
            if not isinstance(opt,dict):
                opt = {}
                result[child.tag] = opt
            opt[child.get('name')] = child.get('level')
        else:
            result[child.tag] = ss(child.text)
    return result

_SYSCONFIG_REQ_IGNORE=['result','userid','userInfoID','Statistics','userInfoList','daily','CoreJob','PoolJob','LargestJob','LogDBQueueSize']

def dict_to_systemConfig( config:dict[str,object]|None, el:Elem ):
    """dictからsystemConfigリクエストに変換する"""
    return _dict_to_systemConfig(config,el)

def _dict_to_systemConfig( config:dict[str,object]|None, el:Elem, *, depth:int=0 ):
    """dictからsystemConfigリクエストに変換する"""
    if not isinstance(config,dict) or len(config)==0:
        return
    for k,v in config.items():
        if depth==0 and ( k.endswith('Info') or k.startswith('running') or k in _SYSCONFIG_REQ_IGNORE ):
            continue

        if depth==0 and k=='log4j':
            if isinstance(v,dict):
                for cls,lv in v.items():
                    child = etree.SubElement(el,k, attrib={'name':cls,'level':lv})
        else:
            child = etree.SubElement(el,k)
            if isinstance(v,dict):
                _dict_to_systemConfig( v, child, depth=depth+1 )
            elif isinstance(v,bool):
                child.text = 'true' if v else 'false'
            else:
                child.text = str(v)
