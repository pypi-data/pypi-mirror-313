from logging import getLogger
import re
import json
from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment

logger = getLogger('rcm.client')

def from_str( data:str ) -> Elem|None:
    try:
        if data is not None and data.startswith('<?xml'):
            data = re.sub( r"^<\?xml.*\?>[\s\n]*", "", data )
        root:Elem = etree.fromstring(data)
        return root
    except Exception as e:
        logger.exception('can not parse')
    return None

def _enc_tagname(name:str|None, ns:dict) ->str|None:
    if name is not None and name.startswith('{') and '}' in name:
        sp,nm = name[1:].split('}')
        for k,v in ns.items():
            if v==sp:
               return f"{k}:{nm}"
    return name

def _enc_att_value(value):
    # 属性値のエンコード（例: 特殊文字をエスケープ）
    return value.replace('"', '&quot;')

def _enc_text(value):
    # テキストのエンコード（例: 特殊文字をエスケープ）
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _elem_to_str( elem:Elem, indent:str='', ns:dict={} ):
    if isinstance(elem,Comment):
        yield f"<!--{_enc_text(elem.text)}-->"
    else:
        tagname = _enc_tagname(str(elem.tag),elem.nsmap)
        yield f"<{tagname}"
        for k,v in elem.nsmap.items():
            if k not in ns:
                yield f" xmlns:{k}=\"{v}\""
        for k,v in elem.attrib.items():
            yield f" {_enc_tagname(k,elem.nsmap)}=\"{_enc_att_value(v)}\""
        nchilds:int = len(elem)
        if nchilds==0:
            if elem.text is None or elem.text=='':
                yield f"/>"
            else:
                yield f">{_enc_text(elem.text)}</{tagname}>"
        else:
            next_indent = indent + "  "
            yield f">\n{next_indent}"
            for idx,child in enumerate(elem):
                yield from _elem_to_str( child, f"{indent}  ", elem.nsmap)
                if idx<nchilds-1:
                    yield f"\n{next_indent}"
                else:
                    yield f"\n{indent}"
            yield f"</{tagname}>"

def _root_to_str( elem:Elem ):
    yield "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    yield from _elem_to_str(elem)

def xml_lint( value:str|None, *, xml_declaration:bool=True ) ->str|None:
    if isinstance(value,str):
        elem = from_str(value)
        if isinstance(elem,Elem):
            if xml_declaration:
                return ''.join( _root_to_str(elem) )
            else:
                return ''.join( _elem_to_str(elem) )
    return value

def to_str( obj, *, xml_declaration:bool=True, pretty_print:bool=True ) ->str:
    try:
        if isinstance(obj,Elem):
            if pretty_print:
                if xml_declaration:
                    return ''.join( _root_to_str(obj) )
                else:
                    return ''.join( _elem_to_str(obj) )
            else:
                content_bytes:bytes = etree.tostring( obj, pretty_print=True, xml_declaration=xml_declaration, encoding='UTF-8')
                content_txt:str = content_bytes.decode().strip()
                if xml_declaration:
                    lines = content_txt.splitlines()
                    if len(lines)>0 and lines[0].startswith('<?xml'):
                        lines[0] = lines[0].replace("'",'"')
                        content_txt = '\n'.join(lines)
                return content_txt
        elif isinstance(obj,dict|list):
            return json.dumps(obj,ensure_ascii=False,indent=2).strip()
        elif isinstance(obj,str|float|int):
            return str(obj)
        elif isinstance(obj,bool):
            return 'true' if obj else 'false'
        else:
            return str(obj)
    except:
        pass
    return ''

def _reindent( elem:Elem, indent:str ):
    n:int = len(elem)
    if n>0:
        next_indent = f"{indent}  "
        elem.text = f"\n{next_indent}"
        for i,child  in enumerate(elem):
            _reindent(child,next_indent)
            child.tail = f"\n{next_indent}"
        elem[-1].tail = f"\n{indent}"
        
def reindent( elem:Elem|None ):
    if isinstance(elem,Elem):
        _reindent(elem,'')

def reindents( text:str ) ->str|None:
    elem:Elem|None = from_str(text)
    if elem is not None:
        reindent(elem)
        return to_str(elem)
    return None

def from_file( xml_file:str ) -> Elem|None:
    try:
        parser = etree.XMLParser() 
        tree = etree.parse(xml_file,parser)
        root:Elem = tree.getroot()
        return root
    except Exception as e:
        logger.exception('can not parse')
    return None

def to_file( elem:Elem, filepath:str ):
    with open(filepath,'wb') as stream:
        stream.write( etree.tostring( elem, xml_declaration=True, pretty_print=True, encoding='UTF-8' ))

def xpath_to_obj( elem:Elem|None, xpath:str|None):
    try:
        if elem is None or xpath is None:
            return None
        result = elem.xpath(xpath)
        if isinstance(result, list):
            return result
        return [result]
    except Exception as e:
        logger.error(f"(getXPATH) XPATH={xpath} {e}")
        return None

def xpath_to_elem( elem:Elem|None, xpath:str|None) ->Elem|None:
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is not None and len(obj)>0:
        val = obj[0]
        if isinstance(val,Elem):
            return val
    return None

def xpath_to_str( elem:Elem|None, xpath:str|None, *, default:str|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        return val.text
    elif isinstance(val,etree._ElementUnicodeResult) or isinstance(val,int) or isinstance(val,float):
        return str(val)
    elif isinstance(val,bool):
        return 'true' if val else 'false'
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def xpath_to_bool( elem:Elem|None, xpath:str|None, *, default:bool|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    text = ''
    if isinstance(val,Elem):
        text = val.text
    elif isinstance(val,bool):
        return val
    else:
        text = str(val)
    if text == 'true':
        return True
    if text == 'false':
        return False
    return default

def xpath_to_int( elem:Elem|None, xpath:str|None, *, default:int|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        if val.text:
            try:
                return int(float(val.text))
            except:
                pass
        return default
    elif isinstance(val,etree._ElementUnicodeResult) or isinstance(val,str):
        try:
            return int(float(val))
        except:
            pass
        return default
    elif isinstance(val,int) or isinstance(val,float):
        return int(val)
    elif isinstance(val,bool):
        return 1 if val else 0
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def xpath_to_float( elem:Elem, xpath:str, *, default:float|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        if val.text:
            try:
                return float(val.text)
            except:
                pass
        return default
    elif isinstance(val,int) or isinstance(val,float):
        return float(val)
    elif isinstance(val,bool):
        return 1.0 if val else 0.0
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def create_element( tagname:str ) ->Elem:
    return etree.Element(tagname)

def get_text(e:Elem, tagname:str|None=None) ->str:
    if tagname is None:
        if isinstance(e,Elem):
            return e.text if e.text is not None else ""
        return str(e)
    else:
        child:Elem|None = e.find(tagname)
        if child is not None and child.text is not None:
            return child.text
        return ""

def add_node( parent:Elem, name:str, value:str|None=None )->Elem:
    e:Elem = etree.SubElement( parent, name )
    if value is not None:
        e.text = value
    return e

def append_node( parent:Elem, child:Elem ):
    """
    親ノードに子ノードを追加する。子ノードが既に他の親を持っている場合は解除してから追加する。

    :param parent: 追加先の親ノード
    :param child: 追加する子ノード
    """
    if parent is None or child is None:
        return
    # 子ノードが既に親を持っている場合は、その親から削除
    child_parent = child.getparent()
    if child_parent is not None:
        child_parent.remove(child)
    
    # 子ノードを親ノードに追加
    parent.append(child)

def insert_node(parent: Elem, child: Elem, reference: Elem|int):
    """
    指定した子ノードの直後に新しい子ノードを挿入する。

    :param parent: 親ノード
    :param new_child: 挿入する新しい子ノード
    :param reference_child: 挿入位置の基準となる子ノード
    """
    # 親ノードのすべての子ノードを取得
    children = list(parent)

    # 挿入位置を見つける
    if isinstance(reference,int):
        pos = reference
    elif isinstance(reference,Elem):
        try:
            pos = children.index(reference)
            pos += 1
        except ValueError:
            raise ValueError("reference_child is not a child of the parent")
    else:
        raise ValueError("reference_child is not a child of the parent")

    # 挿入前に新しい子ノードを既存の親から切り離す
    child_parent = child.getparent()
    if child_parent is not None:
        child_parent.remove(child)

    # 挿入位置の次に新しい子ノードを挿入
    parent.insert(pos, child)

def set_text( parent:Elem, name:str, value:str|int|float|None )->Elem:
    """
    子要素のテキスト値を設定します。要素が存在しない場合は新しく作成します。

    Parameters
    ----------
    parent : Elem
        親XML要素。
    name : str
        子要素の名前。
    value : str or int or float
        子要素に設定する値。

    Returns
    -------
    Elem
        更新されたテキスト値を持つ子要素。
    """
    elem:Elem|None = parent.find(name)
    if elem is None:
        elem = etree.SubElement( parent, name )
    if value is not None:
        elem.text = str(value)
    else:
        elem.text = None
    return elem

def remove_all_nodes(parent: Elem, tagname:str|None=None):
    """
    指定された親ノードからすべての子ノードを削除
    """
    if parent is not None:
        remove_list = parent.findall( tagname ) if tagname else list(parent)  # 削除中に反復問題を回避
        for child in remove_list: 
            parent.remove(child)  # 親ノードから削除
