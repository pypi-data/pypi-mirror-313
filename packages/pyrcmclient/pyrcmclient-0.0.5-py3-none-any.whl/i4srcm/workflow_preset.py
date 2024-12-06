
from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment

def update_preset( wfnode:Elem, *, params:dict|None=None):
    # preset属性をキーにして辞書を作成
    key_values:dict[str,str] = {}
    preset_nodes:dict[str,list[Elem]] = {}
    for elem in wfnode.xpath("//*[@preset]"):
        key = elem.get("preset")
        if key not in preset_nodes:
            preset_nodes[key] = [elem]
        else:
            preset_nodes[key].append(elem)
        if key not in key_values and elem.text not in (None, ''):
            key_values[key] = elem.text

  # define属性をキーにして辞書を作成
    define_nodes:dict[str,list[Elem]] = {}
    for elem in wfnode.xpath("//*[@define]"):
        define = elem.get("define")
        if define not in define_nodes:
            define_nodes[define] = [elem]
        else:
            define_nodes[define].append(elem)

    if isinstance(params,dict):
        for key,value in params.items():
            key_values[key] = value

    # 辞書を使用して同じpreset属性を持つすべてのタグのテキストを更新
    for key,value in key_values.items():
        if key in preset_nodes:
            for elem in preset_nodes[key]:
                elem.text = value
        if key in define_nodes:
            for elem in define_nodes[key]:
                elem.text = value

def str_update_preset(xml_string, *, params:dict|None=None):
    # XML文字列を解析してElementツリーに変換
    parser = etree.XMLParser() 
    root = etree.fromstring(xml_string,parser)
    lx_update_preset(root,params=params)
    # 更新されたXMLを文字列として返す
    return etree.tostring(root, pretty_print=True).decode()