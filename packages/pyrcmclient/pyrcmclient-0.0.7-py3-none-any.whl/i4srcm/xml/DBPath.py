import sys,os
import math
from typing import Type as XType
from enum import Enum, auto
from functools import lru_cache

from lxml import etree
from lxml.etree import _Element as Elem

import i4srcm.lxmlutil as lx


INTEGER_MAX_VALUE = 2**31 - 1

# 定数定義
PARSE_LOCATION = 0
PARSE_PREDICATES_TOP = 1
PARSE_PREDICATES_NEST = 2
PARSE_FUNCTION_PARAMETER = 3

MSG00000 = "()が正しく閉じていません"
MSG00010 = "評価式の構文エラーです"
MSG00020 = "ロケーションパスを複数記述する場合は'|'を使って下さい。"
MSG00030 = "ロケーションパスが不正です"
MSG00100 = "階層飛ばし//は使えません"
MSG00200 = "ノードテスト%sは使えません"

MSG00310 = "述語の前にはノードテストが必要です"
MSG00320 = "述語が正しく閉じていません"
MSG00330 = "述部以外で演算子が使われています"
MSG00340 = "述部以外で文字列が使われています"
MSG00350 = "述部以外で式が使われています"

MSG00400 = "関数%s()は使えません"
MSG00410 = "関数%sの引数の数が不正です"
MSG00420 = "関数%sの引数%sを論理値に評価できません"
MSG00430 = "関数%sの引数%sを数値に評価できません"
MSG00440 = "関数%sの引数%sを文字列に評価できません"
MSG00450 = "関数%sの引数区切り(カンマ)が不正です"

MSG00510 = "演算子%sのオペランド%sが定数として評価できません"
MSG00520 = "演算子のオペランドの型が不正です"

ERR00020 = "%sの否定形は存在しません"
ERR00030 = "%sのオペランドを交換できません"
ERR02010 = "targetパスを特定できません"
ERR80010 = "%sの述部は未実装です"
ERR99999 = "DBPathを処理できませんでした"

CONST_TRUE = "true"
F_TRUE = CONST_TRUE + "()"
CONST_FALSE = "false"
F_FALSE = CONST_FALSE + "()"

TAGNAME_DBPATH = "DBPath"
TAGNAME_DBREQUEST = "DBRequest"
TAGNAME_TRANSACTION = "transaction"
TAGNAME_INSTRUCTION = "instruction"
ATTNAME_NO = "no"
TAGNAME_INSTKIND = "instkind"
INSTKIND_SEL2 = "SEL2"
INSTKIND_SUBGROUP_LIST = "SUBGROUP_LIST"
TAGNAME_INSTBODY = "instbody"
TAGNAME_TARGET = "target"
TAGNAME_LOWERLEVEL = "lowerLevel"
DEFAULT_LOWERLEVEL:int = 1
TAGNAME_UPPERLEVEL = "upperLevel"
DEFAULT_UPPERLEVEL:int = 0
TAGNAME_APPEND = "append"
TAGNAME_DROP = "drop"
TAGNAME_LAYER = "layer"
LAYER_TAGID = "tagid"
LAYER_OWNER = "owner"
LAYER_READ_AUTH = "readAuth"
LAYER_WRITE_AUTH = "writeAuth"
LAYER_ATT = "attribute"
LAYER_VALUE = "value"
TAGNAME_OPERAND = "operand"
DBOP_WITHOUT = "WITHOUT"
DBOP_EQ = "EQ"
X_EQ = "="
DBOP_NE = "NOT"
DBOP_NE2 = "NE"
X_NE = "!="
DBOP_GT = "GT"
X_GT = ">"
DBOP_GTE = "GTE"
X_GE = ">="
DBOP_LT = "LT"
X_LT = "<"
DBOP_LTE = "LTE"
X_LE = "<="
DBOP_STARTS_WITH = "STARTS-WITH"
DBOP_ENDS_WITH = "ENDS-WITH"
DBOP_BLANK = "BLANK"
DBOP_NOT_BLANK = "NOT_BLANK"
DBOP_LIKE = "LIKE"
DBOP_NOT_LIKE = "NOT_LIKE"
DBOP_ILIKE = "ILIKE"
DBOP_NOT_ILIKE = "NOT_ILIKE"
TAGNAME_VALUE = "value"
DBOP_IN = "IN"

SUBGROUP_LIST = "SUBGROUP_LIST"

UNIQ_TAGNAME_NOT = "___not_function___"

# --------------------------------------------------------
# デバッグテスト用
# --------------------------------------------------------
dbg = None  # デバッグ用の出力先 (例えば sys.stdout に設定可能)

def dbg_println(aObj: object) -> None:
    if dbg is not None:
        print(str(aObj), file=dbg)

def dbg_print(aObj: object) -> None:
    if dbg is not None:
        print(str(aObj), file=dbg, end="")

trace = None  # トレース用の出力先 (例えば sys.stdout に設定可能)

def trace_println(aObj: object) -> None:
    if trace is not None:
        print(str(aObj), file=trace)

#
# DBPath専用例外
#
class DBPathException(Exception):
    """
    DBPath専用例外
    """
    def __init__(self, message=None):
        """
        コンストラクタ
        :param message: 例外メッセージ
        """
        super().__init__(message)
def _parse_int( value, default:int) ->int:
    try:
        return int(value)
    except:
        pass
    return default

def convert_dbrequest( aDBRequest:Elem|None ):
    if not isinstance(aDBRequest,Elem):
        return
    for zIdx in range( len(aDBRequest)-1,-1,-1):
        zDBPathNode = aDBRequest[zIdx]
        if TAGNAME_DBPATH != zDBPathNode.tag:
            continue
        zDBPath:str|None = zDBPathNode.text
        if zDBPath is None or len(zDBPath.strip())==0:
            zDBPath = zDBPathNode.attrib.get(TAGNAME_DBPATH)
        if zDBPath is None or len(zDBPath.strip())==0:
            continue
        zUpperLevel:int = _parse_int( zDBPathNode.attrib.get(TAGNAME_UPPERLEVEL), DEFAULT_UPPERLEVEL )
        zLowerLevel:int = _parse_int( zDBPathNode.attrib.get(TAGNAME_LOWERLEVEL), DEFAULT_LOWERLEVEL )
        zAppend:str|None = zDBPathNode.attrib.get(TAGNAME_APPEND)
        zDrop:str|None = zDBPathNode.attrib.get(TAGNAME_DROP)
        zReq:Elem = make_dbrequest( zDBPath, zUpperLevel, zLowerLevel, None, zAppend, zDrop )
        zInstList:list[Elem]|None = zReq.findall(TAGNAME_INSTRUCTION) if zReq is not None else None
        if zInstList is None or len(zInstList)==0:
            continue
        aDBRequest.remove(zDBPathNode)
        aDBRequest.insert( zIdx, etree.Comment(zDBPath) )
        for offset,zInst in enumerate(zInstList):
            zInst.attrib[ATTNAME_NO] = ""
            aDBRequest.insert( zIdx+1+offset, zInst)

def make_dbrequest( db_path:str|None, upper_level:int|None=None, lower_level:int|None=None, transaction_id:str|None=None, append:str|None=None, drop:str|None=None ) ->Elem:
    db_path = db_path.strip() if db_path else None
    upper_level = int(upper_level) if isinstance(upper_level,int|float) else DEFAULT_UPPERLEVEL
    lower_level = int(lower_level) if isinstance(lower_level,int|float) else DEFAULT_LOWERLEVEL

    if is_tag_id_list(db_path):
        # tagidリストの場合
        db_request = etree.Element(TAGNAME_DBREQUEST)
        inst_node = etree.SubElement( db_request, TAGNAME_INSTRUCTION, attrib={ATTNAME_NO:""})
        lx.set_text(inst_node, TAGNAME_INSTBODY, INSTKIND_SEL2)
        inst_body_node = etree.SubElement( inst_node, TAGNAME_INSTBODY )
        sel_where_node = etree.SubElement( inst_body_node, "tagidList" )
        lx.set_text(sel_where_node, "tagid", is_tag_id_list(db_path))
    elif db_path:
        # 条件検索の場合
        db_request = make_dbrequest_dbpath(db_path)

    # upperLevel, lowerLevel 設定
    sep = "|"
    for inst_node in db_request:
        if inst_node.tag == TAGNAME_INSTRUCTION:
            for inst_body_node in inst_node:
                if inst_body_node.tag == TAGNAME_INSTBODY:
                    target = inst_body_node.find(TAGNAME_TARGET)
                    for n in [TAGNAME_TARGET, TAGNAME_UPPERLEVEL, TAGNAME_LOWERLEVEL, TAGNAME_APPEND, TAGNAME_DROP]:
                        lx.remove_all_nodes(inst_body_node, n)
                    pos = 0
                    if target is not None:
                        lx.insert_node(inst_body_node, target, pos)
                        pos += 1
                    if upper_level != 0:
                        upper_node = etree.Element(TAGNAME_UPPERLEVEL)
                        upper_node.text = str(upper_level)
                        lx.insert_node(inst_body_node, upper_node, pos)
                        pos += 1
                    if lower_level >= 0:
                        lower_node = etree.Element(TAGNAME_LOWERLEVEL)
                        lower_node.text = str(lower_level)
                        lx.insert_node(inst_body_node, lower_node, pos)
                        pos += 1
                    for name in split(append, sep):
                        append_node = etree.Element(TAGNAME_APPEND)
                        append_node.text = name
                        lx.insert_node(inst_body_node, append_node, pos)
                        pos += 1
                    for name in split(drop, sep):
                        drop_node = etree.Element(TAGNAME_DROP)
                        drop_node.text = name
                        lx.insert_node(inst_body_node, drop_node, pos)
                        pos += 1

    # transactionID
    if transaction_id:
        transaction_node = db_request.find(TAGNAME_TRANSACTION)
        if transaction_node is None:
            transaction_node = etree.Element(TAGNAME_TRANSACTION)
            transaction_node.text = str(transaction_id)
            lx.insert_node(db_request, transaction_node, 0)
        else:
            transaction_node.text = transaction_id

    return db_request

def split(string:str|None, sep:str|None) -> list[str]:
    if string and sep:
        parts = [part.strip() for part in string.split(sep) if part.strip()]
        return list(dict.fromkeys(parts))  # Remove duplicates while preserving order
    return []

def is_tag_id_list(tag_id_list:str|None) -> str|None:
    if tag_id_list:
        for char in tag_id_list:
            if not (char.isdigit() or char in " ,|"):
                return None
        numbers = sorted(set(int(x) for x in tag_id_list.replace(",", " ").replace("|", " ").split() if x.isdigit()))
        return ",".join(map(str, numbers))
    return None

def make_dbrequest_dbpath( aDBPath:str ) -> Elem:
    # デコードする
    zResult:Node = parse( aDBPath )
    # 変換する

    zDBRequest:Elem = etree.Element( TAGNAME_DBREQUEST )
    zInstNo:int = 1
    zChild:Node|None = zResult.get_first_child()
    while zChild is not None:
        # target
        zTargetPath:str|None = zChild.get_target_path()
        # instruction
        zInstruction:Elem = etree.SubElement( zDBRequest, TAGNAME_INSTRUCTION, attrib={ATTNAME_NO:str(zInstNo)} )
        zInstNo += 1
        lx.set_text( zInstruction, TAGNAME_INSTKIND, INSTKIND_SEL2 )
        zInstBody:Elem = etree.SubElement( zInstruction, TAGNAME_INSTBODY )
        if zChild.get_first_child() is None and zChild.get_predicate() is None and SUBGROUP_LIST == zChild.get_text():
            lx.set_text( zInstruction, TAGNAME_INSTKIND, INSTKIND_SUBGROUP_LIST )
            zTagIDListNode:Elem = etree.SubElement(zInstBody, "tagidList" )
            zTagDIs:Elem = etree.SubElement(zTagIDListNode, "tagid" )
        elif zChild.get_type().is_const():
            zTagIDListNode:Elem = etree.SubElement(zInstBody,"tagidList" )
            zValue:float = zChild.get_number_value()
            lx.set_text(zTagIDListNode, "tagid", number_to_string( zValue ) )
        else:
            lx.set_text(zInstBody, TAGNAME_TARGET, zTargetPath )
            zSelWhere:Elem = etree.SubElement( zInstBody, "selWhere" )
            # selWehere
            make_sel_where( 0, zSelWhere, zChild )
            dbg_print( "makeSelWhere:" + lx.to_str(zSelWhere,xml_declaration=False) )
            if convert_sel_where( zSelWhere ):
                dbg_print( "convertSelWhere:" + lx.to_str(zSelWhere,xml_declaration=False) )
            while optimize_sel_where( zSelWhere ):
                dbg_print( "optimizeSelWhere:" + lx.to_str(zSelWhere,xml_declaration=False) )
            while convert_or_to_in( zSelWhere ):
                dbg_print( "convertOr2In:" + lx.to_str(zSelWhere,xml_declaration=False) )

        zChild = zChild.get_next_sibling()

    return zDBRequest

def make_sel_where( aDepth:int, aParent:Elem, aNode:"Node|None" ):
    while aNode is not None:
        zText = aNode.get_text()
        zType = aNode.get_type()
        if zText == "/":
            zXML:Elem = aParent
            make_sel_where(aDepth + 1, zXML, aNode.get_predicate())
            make_sel_where(aDepth + 1, zXML, aNode.get_first_child())
        elif is_and_or(zType) or zType == Type.NOT:
            if zType == Type.NOT:
                zText = zType.get_tag_name()
            else:
                zText = zType.get_key()
            zXML:Elem = etree.SubElement(aParent, zText)
            make_sel_where(aDepth + 1, zXML, aNode.get_predicate())
            make_sel_where(aDepth + 1, zXML, aNode.get_first_child())
        elif can_db_operand(zType):
            zParent:Node|None = aNode.get_parent()
            zLayer = get_layer(zParent.get_text()) if zParent is not None else None
            if zLayer is not None:
                lx.set_text(aParent, TAGNAME_LAYER, zLayer)
            zOp = convert_operator(zType, zText)
            try:
                zChild:Node|None = aNode.get_first_child()
                zVal = zChild.get_string_value() if zChild is not None else None
                if zOp == DBOP_EQ and (zVal is None or len(zVal) == 0):
                    zOp = DBOP_BLANK
                if zOp == DBOP_NE and (zVal is None or len(zVal) == 0):
                    zOp = DBOP_NOT_BLANK

                lx.set_text(aParent, TAGNAME_OPERAND, zOp)
                lx.set_text(aParent, TAGNAME_VALUE, zVal)
            except ParameterException as ex:
                print(f"Error: {ex}")
        else:
            #TODO zTextが"."の時は、述部の上のノードのタイプからタグ名とLayerを決定する必要があるが未実装
            zXML:Elem = etree.SubElement(aParent, tagname(zText))
            zLayer = get_layer(zText)
            if zLayer is not None:
                lx.set_text(zXML, TAGNAME_LAYER, zLayer)
                lx.set_text(zXML, TAGNAME_OPERAND, DBOP_EQ)
                lx.set_text(zXML, TAGNAME_VALUE, "")
            if zLayer is not None and aNode.get_predicate() is not None:
                raise DBPathException(f"{ERR80010 % f'{zText}({zLayer})'}")
                #TODO zTextが"."の時は、述部の上のノードのタイプからタグ名とLayerを決定する必要があるが未実装
            make_sel_where(aDepth + 1, zXML, aNode.get_predicate())
            make_sel_where(aDepth + 1, zXML, aNode.get_first_child())

        if aDepth == 0:
            break
        aNode = aNode.get_next_sibling()

def can_db_operand(aType: "Type|None") -> bool:
    return aType is not None and aType.get_result_type() == Type.Bool and not is_and_or(aType) and not is_not(aType)

def get_layer(aValue: str|None) -> str | None:
    if aValue is not None:
        if aValue == "@tagid":
            return LAYER_TAGID
        elif aValue == "@owner":
            return LAYER_OWNER
        elif aValue == "@readAuth":
            return LAYER_READ_AUTH
        elif aValue == "@writeAuth":
            return LAYER_WRITE_AUTH
        elif aValue.startswith("@"):
            return LAYER_ATT
        elif aValue == ".":
            return LAYER_VALUE
    return None

def convert_sel_where(aNode: Elem) -> bool:
    """
    XMLノードに対して選択条件の変換を行う。

    :param aNode: 処理対象のXMLノード
    :return: 変換が行われた場合はTrue
    """
    if aNode is None:
        return False

    zResult = False

    #--------------------------
    # _not_の変換処理
    #--------------------------
    if aNode.tag == Type.NOT.get_tag_name():
        zResult = True
        zChildLength = len(aNode)

        if zChildLength == 1:
            zChild = aNode[0]
            if invert_with_logic_node(zChild):
                aNode.tag = Type.AND.get_tag_name()
            elif invert_logic_node(zChild):
                aNode.tag = Type.OR.get_tag_name()
                lx.append_node(aNode, make_with_logic(str(zChild.tag), lx.get_text( zChild, TAGNAME_LAYER), False))
            else:
                zLogicName = zChild.tag
                zLogicLength = len(zChild)
                is_and_or = zLogicName in [Type.AND.get_tag_name(), Type.OR.get_tag_name()]

                if zLogicLength > 1 and is_and_or:
                    zLogicList = list(zChild)
                    zChild.clear()
                    if zLogicName == Type.AND.get_tag_name():
                        aNode.tag = Type.OR.get_tag_name()
                    elif zLogicName == Type.OR.get_tag_name():
                        aNode.tag = Type.AND.get_tag_name()

                    zChild.tag = Type.NOT.get_tag_name()
                    lx.append_node(zChild, zLogicList[0])
                    for i in range(1, zLogicLength):
                        zNotNode = etree.Element(Type.NOT.get_tag_name())
                        lx.append_node(zNotNode, zLogicList[i])
                        lx.append_node(aNode, zNotNode)

                elif zLogicLength == 1 and zLogicName == Type.NOT.get_tag_name():
                    aNode.tag = Type.AND.get_tag_name()
                    zChild.tag = Type.AND.get_tag_name()

                elif zLogicLength == 1 and not is_and_or:
                    zLowerTag = zChild[0]
                    zChild.clear()
                    zNotTag = etree.Element(Type.NOT.get_tag_name())
                    lx.append_node(zNotTag, zLowerTag)
                    lx.append_node(zChild, zNotTag)
                    aNode.tag = Type.OR.get_tag_name()
                    lx.append_node(aNode, make_with_logic(str(zChild.tag), zChild.get(TAGNAME_LAYER), False))

        elif zChildLength == 2:
            # 2つの子ノードを持つ場合の処理（未実装箇所）
            pass

    #-------------------------------
    # 下位ノードを処理
    #-------------------------------
    for zChild in list(aNode):
        if convert_sel_where(zChild):
            zResult = True

    return zResult

def optimize_sel_where(aNode: Elem) -> bool:
    """
    XMLノードに対して条件の最適化を行う。

    :param aNode: 処理対象のXMLノード
    :return: 最適化が行われた場合はTrue
    """
    if aNode is None:
        return False

    zResult = False

    #-------------------------------
    # 下位ノードを処理
    #-------------------------------
    for zChild in list(aNode):
        if optimize_sel_where(zChild):
            zResult = True

    zType = is_and_or_node(aNode)
    zLogic = Type.AND if zType == Type.Path else zType

    #--------------------------------------
    # andの下のandを結合する, orの下のorを結合する
    #--------------------------------------
    for zChild in list(aNode):
        if is_and_or_node(zChild) == zLogic:
            zResult = True
            zBase = zChild
            for ccc in list(zChild):
                lx.insert_node(aNode, ccc, zBase)
                zBase = ccc
            aNode.remove(zChild)

    zChildLength = len(aNode)

    #--------------------------------------
    # 重複する条件を削除する
    #--------------------------------------
    if zChildLength > 1:
        zMap: dict[str, Elem] = {}
        for zChild in list(aNode):
            if is_and_or_node(zChild) == Type.Path:
                zTagName = str(zChild.tag)
                zBefore = zMap.get(zTagName)
                if zBefore is None:
                    zMap[zTagName] = zChild
                else:
                    if zType == Type.OR:
                        # OR条件の場合は、条件なしタグがあったら他を削除する
                        if len(zBefore) == 0:
                            aNode.remove(zChild)
                            zResult = True
                        elif len(zChild) == 0:
                            zMap[zTagName] = zChild
                            aNode.remove(zBefore)
                            zResult = True
                    else:
                        # AND条件の場合は、条件付きタグが在ったら条件なしタグを削除する
                        if len(zChild) == 0:
                            aNode.remove(zChild)
                            zResult = True
                        elif len(zBefore) == 0:
                            zMap[zTagName] = zChild
                            aNode.remove(zBefore)
                            zResult = True

    #--------------------------------------
    # 条件が一個だけのAnd/Orを削除する
    #--------------------------------------
    for zChild in list(aNode):
        if is_and_or_node(zChild) != Type.Path:
            if len(zChild) == 1:
                zResult = True
                lx.insert_node(aNode, zChild[0], zChild)
                aNode.remove(zChild)

    return zResult

def convert_or_to_in(aNode: Elem) -> bool:
    """
    XMLノードに対して条件の最適化を行い、OR条件をIN条件に変換します。

    :param aNode: 処理対象のXMLノード
    :return: 変換が行われた場合はTrue
    """
    zType = is_and_or_node(aNode)
    zResult = False

    for zChild in list(aNode):
        if convert_or_to_in(zChild):
            zResult = True

        # 条件が一個だけのvalueを削除する
        if len(zChild) == 1:
            zLogicNode = zChild[0]
            if lx.get_text(zLogicNode, TAGNAME_LAYER) == LAYER_VALUE and zLogicNode.find(TAGNAME_OPERAND) is not None:
                zResult = True
                lx.remove_all_nodes(zLogicNode, TAGNAME_LAYER)
                zPos = zLogicNode
                for zCondition in list(zLogicNode):
                    lx.insert_node(zChild, zCondition, zPos)
                    zPos = zCondition
                zChild.remove(zLogicNode)

    if is_and_or_node(aNode) == Type.OR and len(aNode) > 1:
        # 条件タグ名毎に分類する
        zMap: dict[str, list[Elem]] = {}
        for zChild in list(aNode):
            # EQとINを結合する
            zOperator = lx.get_text(zChild, TAGNAME_OPERAND)
            if zOperator not in {DBOP_EQ, DBOP_IN}:
                continue

            # layerがvalue,tagid,attributeの時だけ結合する
            zLayer = lx.get_text(zChild, TAGNAME_LAYER)
            if zLayer and zLayer not in {LAYER_VALUE, LAYER_TAGID, LAYER_ATT}:
                continue

            # layerがtagidの場合はvalueがブランクか数字じゃないとだめ
            if zLayer == LAYER_TAGID:
                zValue = lx.get_text(zChild, TAGNAME_VALUE)
                if zValue and not is_number(zValue):
                    continue

            zKey = str(zChild.tag)
            zMap.setdefault(zKey, []).append(zChild)

        for zKey, zList in zMap.items():
            if len(zList) < 2:
                continue

            # 空タグ条件があるか確認する
            zIsEmpty = any(not lx.get_text(zChild, TAGNAME_VALUE) for zChild in zList)
            if zIsEmpty:
                continue

            while len(zList) > 1:
                zFirstNode = None
                zLayer = None
                zINValue = []
                zCount = 0
                for zChild in zList[:]:
                    if zFirstNode is None or zLayer == lx.get_text(zChild, TAGNAME_LAYER):
                        zList.remove(zChild)
                        if zFirstNode is None:
                            zFirstNode = zChild
                            zLayer = lx.get_text(zFirstNode, TAGNAME_LAYER)
                        else:
                            aNode.remove(zChild)
                            zResult = True
                        zValue = lx.get_text(zChild, TAGNAME_VALUE) or ""
                        if lx.get_text(zChild, TAGNAME_OPERAND) == DBOP_EQ:
                            zValue = zValue.replace("\\", "\\\\").replace(",", "\\,")
                        zINValue.append(zValue)
                        zCount += 1

                if zFirstNode is not None and zCount > 0:
                    operand = DBOP_EQ if zLayer == LAYER_TAGID else DBOP_IN
                    lx.set_text(zFirstNode, TAGNAME_OPERAND, operand)
                    lx.set_text(zFirstNode, TAGNAME_VALUE, ",".join(zINValue))
                    zResult = True

        # 条件が一個だけのOrを削除する
        if len(aNode) == 1:
            zChild = aNode[0]
            aNode.tag = zChild.tag
            zPos = zChild
            for zCondition in list(zChild):
                lx.insert_node(aNode, zCondition, zPos)
                zPos = zCondition
            aNode.remove(zChild)

    return zResult

def is_and_or_node(aNode: Elem) -> "Type":
    """
    ノードがAND/ORかどうかを判定する。

    :param aNode: 判定対象のXMLノード
    :return: ノードのタイプ (Type.Path, Type.AND, Type.OR)
    """
    if aNode is not None:
        if len(aNode) == 0:
            return Type.Path
        zOp = aNode.find(TAGNAME_OPERAND)
        if zOp is not None:
            return Type.Path
        zTagName = aNode.tag
        if zTagName == Type.AND.get_tag_name():
            return Type.AND
        if zTagName == Type.OR.get_tag_name():
            return Type.OR
    return Type.Path

def make_with_logic(a_tag_name: str, a_layer: str | None, ex: bool) -> Elem:
    """
    ロジック付きのXMLノードを作成する。

    :param a_tag_name: ノードのタグ名
    :param a_layer: レイヤー名
    :param ex: 条件付きかどうかのフラグ
    :return: 作成されたXMLノード
    """
    z_result = etree.Element(a_tag_name)
    if a_layer is not None and len(a_layer) > 0:
        lx.set_text(z_result, TAGNAME_LAYER, a_layer)
    
    if not ex or (a_layer is not None and len(a_layer) > 0):
        lx.set_text(z_result, TAGNAME_OPERAND, DBOP_EQ if ex else DBOP_WITHOUT)
        lx.set_text(z_result, TAGNAME_VALUE, "")
    
    return z_result

def invert_with_logic_node(a_node: Elem) -> bool:
    """
    ロジックノードを反転する。

    :param a_node: 対象のXMLノード
    :return: 反転処理が行われた場合はTrue、それ以外はFalse
    """
    if a_node is not None:
        z_operator = lx.get_text(a_node, TAGNAME_OPERAND)
        if z_operator in {DBOP_BLANK, DBOP_NOT_BLANK}:
            return False
        if z_operator == DBOP_WITHOUT:
            # タグ無し条件の場合は反転可能
            z_layer = lx.get_text(a_node, TAGNAME_LAYER)
            if not z_layer:
                lx.remove_all_nodes(a_node)
            else:
                lx.set_text(a_node, TAGNAME_OPERAND, DBOP_EQ)
                lx.set_text(a_node, TAGNAME_VALUE, "")
            return True

        z_value = lx.get_text(a_node, TAGNAME_VALUE)
        if len(a_node) == 0 or (z_operator and len(z_operator) > 0) and (not z_value or len(z_value) == 0):
            # 子タグがない、もしくはvalueが空でoperandが存在する場合
            lx.set_text(a_node, TAGNAME_OPERAND, DBOP_WITHOUT)
            lx.set_text(a_node, TAGNAME_VALUE, "")
            return True
    return False

def invert_logic_node(a_node: Elem) -> bool:
    """
    ロジックノードの演算子を反転する。

    :param a_node: 対象のXMLノード
    :return: 反転処理が行われた場合はTrue、それ以外はFalse
    :raises: ValueError (DBPathExceptionに相当)
    """
    if a_node is not None:
        z_op = a_node.find(TAGNAME_OPERAND)
        z_val = a_node.find(TAGNAME_VALUE)
        if z_op is not None and z_val is not None:
            operator = lx.get_text(z_op)
            if operator in {DBOP_EQ, X_EQ}:
                z_op.text = DBOP_NE
                return True
            elif operator in {DBOP_NE, DBOP_NE2, X_NE}:
                z_op.text = DBOP_EQ
                return True
            elif operator in {DBOP_LT, X_LT}:
                z_op.text = DBOP_GTE
                return True
            elif operator in {DBOP_LTE, X_LE}:
                z_op.text = DBOP_GT
                return True
            elif operator in {DBOP_GT, X_GT}:
                z_op.text = DBOP_LTE
                return True
            elif operator in {DBOP_GTE, X_GE}:
                z_op.text = DBOP_LT
                return True
            elif operator == DBOP_LIKE:
                z_op.text = DBOP_NOT_LIKE
                return True
            elif operator == DBOP_NOT_LIKE:
                z_op.text = DBOP_LIKE
                return True
            elif operator == DBOP_ILIKE:
                z_op.text = DBOP_NOT_ILIKE
                return True
            elif operator == DBOP_NOT_ILIKE:
                z_op.text = DBOP_ILIKE
                return True
            elif operator == DBOP_BLANK:
                z_op.text = DBOP_NOT_BLANK
                return True
            elif operator == DBOP_NOT_BLANK:
                z_op.text = DBOP_BLANK
                return True
            elif operator in {DBOP_STARTS_WITH, DBOP_ENDS_WITH}:
                raise DBPathException(f"{ERR00020 % (lx.get_text(z_op))}")
    return False

def tagname(aValue: str|None ) -> str:
    """
    タグ名を判定する。

    :param a_value: 判定対象の文字列
    :return: タグ名
    """
    if aValue is not None:
        if aValue == "/":
            return "_ROOT_"
        if aValue == ".":
            return "value"
        if aValue == f"@{LAYER_READ_AUTH}" or aValue == f"@{LAYER_WRITE_AUTH}":
            return "auth"
        if aValue.startswith("@"):
            return aValue[1:]
        if len(aValue) > 2 and aValue.endswith("()"):
            return f"_{aValue.replace('()', '')}_"
        return aValue
    else:
        return ""

def is_valid_name1(cc: str) -> bool:
    """
    文字が有効な名前の最初の条件を満たしているかを判定。

    :param cc: 判定対象の文字
    :return: 有効であれば True
    """
    if cc in ('@', '_', ':'):
        return True
    if 'a' <= cc <= 'z' or 'A' <= cc <= 'Z':
        return True
    if ord(cc) > 128:  # Unicodeコードポイントが128を超える文字
        return True
    return False


def is_valid_name2(cc: str) -> bool:
    """
    文字が有効な名前の条件を満たしているかを判定。

    :param cc: 判定対象の文字
    :return: 有効であれば True
    """
    if is_valid_name1(cc):
        return True
    if cc in ('-', '.'):
        return True
    return False


def is_valid_path(cc: str) -> bool:
    """
    パスの有効性を判定する（現状は常に True を返す）。

    :param cc: 判定対象の文字
    :return: 有効であれば True
    """
    return True  # 条件が未実装なため、常にTrueを返す

def convert_operator(a_type: "Type|None", a_operator: str|None) -> str:
    if a_type is None or a_operator is None:
        raise ValueError("Both a_type and a_operator must be non-null.")
    
    match a_type:
        case Type.EQ:
            return DBOP_EQ
        case Type.NE:
            return DBOP_NE
        case Type.LT:
            return DBOP_LT
        case Type.LTE:
            return DBOP_LTE
        case Type.GTE:
            return DBOP_GTE
        case Type.GT:
            return DBOP_GT
        case Type.CONTAINS | Type.LIKE:
            return DBOP_LIKE
        case Type.ILIKE:
            return DBOP_ILIKE
        case Type.NOT_LIKE:
            return DBOP_NOT_LIKE
        case Type.NOT_ILIKE:
            return DBOP_NOT_ILIKE
        case Type.STARTS_WITH:
            return DBOP_STARTS_WITH
        case Type.ENDS_WITH:
            return DBOP_ENDS_WITH
        case _:
            return a_operator  # デフォルト値

def get_type(aType: "Type", zValue: str|None) -> "Type":
    if aType is not None and aType != Type.Unknown:
        return aType
    return Type.by_value(zValue)

def is_operand_node(aNode: "Node|None") -> bool:
    if aNode is not None:
        if is_path(aNode.get_type()):
            zChild = aNode.get_first_child()
            while zChild is not None:
                if is_operator0(zChild.get_type()):
                    return True
                zChild = zChild.get_next_sibling()
    return False

def is_operator0(aType: "Type") -> bool:
    return aType is not None and (aType.is_operator() or aType.is_function())

def parse(aDBPath: str) -> "Node":
    """
    デコードする (テスト用)

    :param aDBPath: デコード対象のDBPath文字列
    :return: デコードされたNode
    :raises DBPathException: エラーが発生した場合
    """
    return parse_dbpath( Reader(aDBPath) )

def parse_dbpath(aReader:"Reader") -> "Node":
    """
    デコードする

    :param aReader: 読み込み用Readerオブジェクト
    :return: デコードされたNode
    :raises DBPathException: エラーが発生した場合
    """
    zLocationPath = Node("::")
    zLocationPath.set_string_builder([])  # StringBuilderの代わりにPythonリストを使用

    parse_dbpath_childs(PARSE_LOCATION, aReader, zLocationPath)
    dbg_println(dump("parse", zLocationPath))

    zCheck = 5
    zChild = zLocationPath.get_first_child()

    if relocate_operator(zChild, zCheck):
        dbg_println(dump("relocateOperator", zLocationPath))

    m = split_auth_with_node(zLocationPath)
    if m:
        dbg_println(dump("splitAuth", zLocationPath))

    m = optimize_logic(zLocationPath)
    if m:
        dbg_println(dump("optimizeLogic", zLocationPath))

    m = cleanup_logic(zLocationPath)
    if m:
        dbg_println(dump("cleanupLogic", zLocationPath))

    zChild = zLocationPath.get_first_child()
    while zChild is not None:
        zTargetPath = zChild.get_target_path()
        dbg_println(f"target: {zTargetPath}")
        zChild = zChild.get_next_sibling()

    return zLocationPath

def relocate_operator(zThis: "Node|None", aCheck: int) -> bool:
    if zThis is None:
        return False

    if zThis.check == aCheck:
        return False

    zThis.check = aCheck
    zResult = False

    # 再帰的に子ノード、述語、次兄弟を処理
    if relocate_operator(zThis.get_first_child(), aCheck):
        zResult = True
    if relocate_operator(zThis.get_predicate(), aCheck):
        zResult = True
    if relocate_operator(zThis.get_next_sibling(), aCheck):
        zResult = True

    # 演算子の再配置
    if is_relocate(zThis.get_type()) and zThis.get_child_length() == 2:
        zPathNode = zThis.get_first_child()
        zValue = zPathNode.get_next_sibling() if zPathNode is not None else None

        if zPathNode is not None and zValue is not None:
            zResult = True

            # パスノードと値を判定
            if not is_path(zPathNode.get_type()):
                zPathNode, zValue = zValue, zPathNode
                zThis.invert_operator()

            if not is_path(zPathNode.get_type()) or not zValue.get_type().is_const():
                raise DBPathException(
                    f"{MSG00520} {zPathNode.get_text()} {zThis.get_text()} {zValue.get_text()}"
                )

            # 値ノードを切り離し
            zValue.unlink()

            # パスの一番下を取得
            zBottom = zPathNode.get_bottom_child()
            if zBottom is None:
                raise ValueError("can not get bottom child")
            # 新しいノードを作成して演算子をコピー
            zOp = Node()
            zOp.set_value(zThis)
            zBottom.append_last_child(zOp)

            # zThisを削除して繰り上げ
            zThis.join_first_child()

            # 演算子ノードの下に値を移動
            zOp.append_last_child(zValue)

    return zResult

def is_relocate(aType: "Type") -> bool:
    return (
        aType is not None and 
        (aType.is_operator() or aType.is_function()) and 
        not is_and_or(aType)
    )

def split_auth_with_node(aNode: "Node|None") -> bool:
    zResult = False

    if aNode is None:
        return False

    # 再帰的に述語、子ノード、次兄弟を処理
    if split_auth_with_node(aNode.get_predicate()):
        zResult = True
    if split_auth_with_node(aNode.get_first_child()):
        zResult = True
    if split_auth_with_node(aNode.get_next_sibling()):
        zResult = True

    # 現在のノードが "@auth" かつ子ノードが1つの場合
    if aNode.get_text() == "@auth" and aNode.get_child_length() == 1:
        zOp = aNode.get_first_child()
        if zOp is not None and zOp.get_child_length() == 1:
            zType = zOp.get_type()
            if zType in {Type.EQ, Type.NE}:
                zResult = True
                zChild:Node|None = zOp.get_first_child()
                if zChild is None:
                    raise ValueError("can not get first child")
                zAuthStr = zChild.get_text()
                zAuth = split_auth_with_str(zAuthStr)  # splitAuth(String) に対応

                if zAuth is not None:
                    aNode.remove_all_children()
                    aNode.set_value(Type.AND if zType == Type.EQ else Type.OR)
                    aNode.append_last_child().set_value("@" + LAYER_READ_AUTH) \
                        .append_last_child().set_value(zType) \
                        .append_last_child().set_value(zAuth[0])
                    aNode.append_last_child().set_value("@" + LAYER_WRITE_AUTH) \
                        .append_last_child().set_value(zType) \
                        .append_last_child().set_value(zAuth[1])
                else:
                    aNode.remove_all_children()
                    aNode.set_value(Type.FALSE if zType == Type.EQ else Type.TRUE)

    return zResult

def split_auth_with_str(aString: str|None) -> list[str] | None:
    if aString is None:
        return None

    zAuth = aString.strip()
    zLen = len(zAuth)
    if zLen < 2:
        return None

    zReadAuth = None
    zWriteAuth = None

    if zLen == 2:
        # gg とか gu 型
        zReadAuth = zAuth[0]
        zWriteAuth = zAuth[1]
    else:
        # g,g とか g,1234 型
        idx = zAuth.find(',')
        if idx < 1 or (zLen - 1) <= idx:
            return None
        zReadAuth = zAuth[:idx]
        zWriteAuth = zAuth[idx + 1:]

    if zReadAuth is None or (zReadAuth not in {"a", "u", "g"} and not is_number(zReadAuth)):
        return None
    if zWriteAuth is None or (zWriteAuth not in {"a", "u", "g"} and not is_number(zWriteAuth)):
        return None

    return [zReadAuth, zWriteAuth]

def optimize_logic(aNode: "Node|None") -> bool:
    if aNode is None:
        return False

    zResult = False
    zType = aNode.get_type()

    # AND/ORの結合処理
    if aNode.get_predicate() is None and is_and_or(zType):
        zPathNode = aNode.get_first_child()
        zPathX = None

        while zPathNode is not None:
            if is_path(zPathNode.get_type()) and not is_operand_node(zPathNode):
                zTagName = zPathNode.get_text()
                zNextPath = zPathNode.get_next_sibling()

                while zNextPath is not None:
                    zContext = zNextPath
                    zNextPath = zNextPath.get_next_sibling()

                    if (is_path(zContext.get_type()) and 
                        zTagName == zContext.get_text() and 
                        not is_operand_node(zContext)):
                        zResult = True
                        if zPathX is None:
                            zPathX = Node()
                            zPathX.set_value(aNode)
                            zPathX.append_last_child(zPathNode.get_first_child())
                            zPathNode.append_last_child(zPathX)

                        zContext.unlink()
                        zPathX.append_last_child(zContext.get_first_child())
            zPathNode = zPathNode.get_next_sibling()

    # 再帰的に子ノード、次兄弟、述語を最適化
    if optimize_logic(aNode.get_predicate()):
        zResult = True
    if optimize_logic(aNode.get_next_sibling()):
        zResult = True
    if optimize_logic(aNode.get_first_child()):
        zResult = True

    return zResult

def cleanup_logic(aNode: "Node|None") -> bool:
    if aNode is None:
        return False

    zResult = False

    # 再帰的に子ノード、次兄弟、述語を整理
    if cleanup_logic(aNode.get_predicate()):
        zResult = True
    if cleanup_logic(aNode.get_next_sibling()):
        zResult = True
    if cleanup_logic(aNode.get_first_child()):
        zResult = True

    zType = aNode.get_type()
    if is_logic(zType):
        zFirstChild = aNode.get_first_child()
        if zFirstChild is None:
            aNode.clear()
            zResult = True
        elif zFirstChild.get_next_sibling() is None:
            aNode.join_first_child()
            zResult = True

    return zResult

def is_logic(aType: "Type") -> bool:
    return is_and_or(aType) or aType == Type.EXP

def parse_dbpath_childs(aMode: int, aReader, aParent: "Node") -> None:
    while parse_dbpath2(aMode, aReader, aParent):
        pass
    if aParent.get_type() == Type.EXP and aParent.get_child_length() == 1:
        aParent.join_first_child()

def parse_dbpath2(aMode: int, aReader:"Reader", aParent: "Node") -> bool:
    zHasNext = False
    zEXP = Node(":parse:")
    zEXP.set_value(Type.EXP)
    aParent.append_last_child(zEXP)
    zNode:Node|None = None
    # 先頭の空白読み飛ばし
    aReader.seek_space()
    cc = ''
    while True:
        cc:str|None = aReader.poll()
        zPos = aReader.get_pos()
        zEXP.set_pos(zPos)
        zPrevChar = cc

        if cc is None:
            zHasNext = False
            break
        elif cc == '|':
            if aMode != PARSE_LOCATION:
                raise DBPathException(xMsg(aReader.get_pos(), MSG00030))
            zHasNext = True
            break
        elif cc == ']':
            if aMode != PARSE_PREDICATES_TOP:
                raise DBPathException(xMsg(aReader.get_pos(), MSG00320))
            zHasNext = False
            break
        elif cc == ')':
            if aMode not in (PARSE_FUNCTION_PARAMETER, PARSE_PREDICATES_NEST):
                raise DBPathException(xMsg(aReader.get_pos(), MSG00000))
            zHasNext = False
            break
        elif cc == ',':
            if aMode != PARSE_FUNCTION_PARAMETER:
                raise DBPathException(xMsg(aReader.get_pos(), MSG00450, zEXP.get_text()))
            zHasNext = True
            break
        elif cc == ' ':
            zNode = None
            aReader.seek_space()
        elif cc in ('!', '<', '>', '='):
            if aMode not in (PARSE_PREDICATES_TOP, PARSE_PREDICATES_NEST, PARSE_FUNCTION_PARAMETER):
                raise DBPathException(xMsg(aReader.get_pos(), MSG00330))
            zNode = zEXP.append_last_child()
            zNode.append_text(cc).set_pos(zPos)
            if cc != '=' and aReader.peek() == '=':
                aReader.poll()
                zNode.append_text('=').set_pos(zPos + 1)
            zNode = None
            aReader.seek_space()
        elif cc == "'":
            if aMode not in (PARSE_PREDICATES_TOP, PARSE_PREDICATES_NEST, PARSE_FUNCTION_PARAMETER):
                raise DBPathException(xMsg(aReader.get_pos(), MSG00340))
            if zNode is None:
                zNode = zEXP.append_last_child()
            zNode.set_pos(zPos)
            while (xc := aReader.poll())is not None and xc != "'":
                zNode.append_text(xc)
            zNode.set_pos(aReader.get_pos())
            zNode.set_string_type()
            zNode = None
        elif cc == '[':
            if zNode is None:
                raise DBPathException(xMsg(aReader.get_pos(), MSG00310))
            zPredicate = zNode.add_predicate()
            zPredicate.set_value(Type.EXP).set_pos(zPos)
            parse_dbpath_childs(PARSE_PREDICATES_TOP, aReader, zPredicate)
            if zPredicate.get_type().is_const():
                if zPredicate.get_boolean_value():
                    zPredicate.unlink()
                else:
                    zPredicate.set_value(False)
        elif cc == '(' and zNode is None:
            zNode = zEXP.append_last_child()
            zNode.set_value(Type.EXP).set_pos(zPos)
            parse_dbpath_childs(PARSE_PREDICATES_NEST, aReader, zNode)
            zNode = None
        elif cc == '(' and zNode is not None:
            zFunctionName = zNode.get_text()
            zType = Type.by_function_name(zFunctionName)
            if zType is not None:
                zNode.set_value(zType).set_pos(aReader.get_pos())
                parse_dbpath_childs(PARSE_FUNCTION_PARAMETER, aReader, zNode)
                zNode = None
            else:
                raise DBPathException(xMsg(aReader.get_pos(), MSG00400, zFunctionName))
        elif is_operator(cc, zNode, zEXP.get_last_child(), zPrevChar, aReader.peek()):
            if aMode not in (PARSE_PREDICATES_TOP, PARSE_PREDICATES_NEST, PARSE_FUNCTION_PARAMETER):
                raise DBPathException(xMsg(aReader.get_pos(), MSG00330))
            zNode = zEXP.append_last_child()
            zOp = Type.by_operator_name(cc)
            if zOp is not None:
                zNode.set_value(zOp).set_pos(zPos)
            else:
                raise DBPathException(f"{cc}が演算子に変換できません")
            aReader.seek_space()
            zNode = None
        elif cc == '/':
            if zNode is None:
                zNode = zEXP.append_last_child()
                zNode.append_text('/').set_pos(zPos)
            if zNode.is_empty():
                raise DBPathException(xMsg(aReader.get_pos(), MSG00100))
            if is_number(zNode.get_text()):
                raise DBPathException(xMsg(aReader.get_pos(), MSG00030))
            if is_number_char(aReader.peek()):
                raise DBPathException(xMsg(aReader.get_pos() + 1, MSG00030))
            zNode = zNode.append_last_child()
        elif cc == '*':
            raise DBPathException(xMsg(aReader.get_pos(), MSG00200, "*"))
        else:
            if zNode is None:
                zNode = zEXP.append_last_child()
            zNode.append_text(cc).set_pos(zPos)
        if aMode == PARSE_LOCATION and zEXP.get_child_length() > 1:
            raise DBPathException(xMsg(aReader.get_pos(), MSG00020))
        if trace is not None:
            trace_println("--------------------------------------")
            zModeStr = {
                PARSE_LOCATION: " Location",
                PARSE_PREDICATES_TOP: " Predicate",
                PARSE_PREDICATES_NEST: " Predicate...",
                PARSE_FUNCTION_PARAMETER: " Function"
            }.get(aMode, f" Mode:{aMode}")
            trace_println(f"=== char:{cc}{zModeStr}")
            trace_println(dump("trace", zEXP))
            print("",end="")

    aParent.set_string_builderX()
    evaluate_expression(zEXP)

    zChildLength = zEXP.get_child_length()
    if zChildLength > 1 or (aParent.get_type() == Type.EXP and zChildLength == 0):
        zChild = zEXP.get_first_child()
        while zChild is not None:
            aParent.set_pos(zChild.get_end_pos())
            zChild = zChild.get_next_sibling()
        raise DBPathException(xMsg(aParent, MSG00010))

    zResult = zEXP.mFirstChild
    if zResult is not None:
        if check_predicate(zResult):
            zResult.remove_all_children()
            zResult.set_value(Type.EMPTY_NODE_SET)
            trace_println(dump("trace", zEXP))
        zEXP.join_first_child()
        return zHasNext
    else:
        zEXP.unlink()
        return False

def check_predicate(aNode: "Node") -> bool:
    if aNode is not None:
        zPre = aNode.get_predicate()
        if zPre is not None and zPre.get_type().is_const():
            try:
                if not zPre.get_boolean_value():
                    return True
            except ParameterException:
                pass

        zChild = aNode.get_first_child()
        while zChild is not None:
            if check_predicate(zChild):
                return True
            zChild = zChild.get_next_sibling()
        
        return False
    return False

def is_operator(aOp: str, aPrevNode: "Node|None", aLastChild: "Node|None", aPrevChar: str|None, aNextChar: str|None) -> bool:
    if aOp == '+':
        if (aLastChild is None or aLastChild.get_type().is_operator()) and aNextChar is not None and ( aNextChar=='.' or '0'<=aNextChar<='9'):
            return False
        else:
            return True
    elif aOp == '-':
        if aLastChild is not None:
            zText = aLastChild.get_text()
            if is_number(zText):
                return True
            if aNextChar is not None and aNextChar<'0' and '9'<aNextChar:
                return True
            if zText is not None:
                zType = get_type(aLastChild.get_type(), zText)
                if zType.is_const():
                    return True
                elif aPrevChar == ' ' and is_value(zType):
                    return True
                elif zText.endswith("()"):
                    return True
        return False
    elif aOp == '*':
        if aPrevNode is not None:
            zText = aPrevNode.get_text()
            if is_number(zText):
                return True
            if zText == "@":
                return False
            zType = get_type(aPrevNode.get_type(), zText)
            if zType == Type.Num:
                return True
            if zType.is_operator():
                return False
            if zText is not None and zText.endswith("()"):
                return True
            return False
        return True
    return False

def is_value( aType:"Type" ) ->bool:
    return aType.is_const() or aType == Type.Path

def evaluate_expression(aParentNode: "Node") ->bool:
    zResult = False
    # 関数を評価する zPri==0
    # 乗算と除算を先頭から処理する : zPri==2
    # 加算と減算を先頭から処理する : zPri==3
    # 比較演算子を先頭から処理する: zPri==4,5
    for zPri in range(9):
        zUpdate = False
        zNode = aParentNode.get_first_child()
        while zNode is not None:
            if Type.AND.get_pri() == zPri:
                if (zNode.get_type() == Type.Path and 
                    Type.AND.get_tag_name() == zNode.get_text()):
                    if (zNode.get_first_child() is None and 
                        zNode.get_prev_sibling() is not None and 
                        zNode.get_next_sibling() is not None):
                        zNode.set_value(Type.AND)
                        zUpdate = True
            
            if Type.OR.get_pri() == zPri:
                if (zNode.get_type() == Type.Path and 
                    Type.OR.get_tag_name() == zNode.get_text()):
                    if (zNode.get_first_child() is None and 
                        zNode.get_prev_sibling() is not None and 
                        zNode.get_next_sibling() is not None):
                        zNode.set_value(Type.OR)
                        zUpdate = True
            
            if zNode.get_type() is not None and zPri == zNode.get_type().get_pri():
                if zNode.get_type().is_function() or zNode.get_type().is_nodeset():
                    if evaluate(zNode.get_type(), zNode):
                        zUpdate = True
                
                if (zNode.get_type().is_operator() and 
                    zNode.get_prev_sibling() is not None and 
                    zNode.get_next_sibling() is not None):
                    if evaluate(zNode.get_type(), zNode):
                        zUpdate = True
            
            zNode = zNode.get_next_sibling()
        
        if zUpdate:
            zResult = True
            if trace is not None:
                trace_println(dump(f"evaluateExpression Pri:{zPri}", aParentNode))
    
    return zResult

def evaluate(zType: "Type", aNode: "Node") -> bool:
    zUpdate = False

    if zType.is_function():
        try:
            result_type = zType.get_result_type()
            if result_type == Type.Str:
                zString = zType.evaluate_string(aNode)
                aNode.set_value(zString)
            elif result_type == Type.Num:
                zNumber = zType.evaluate_number(aNode)
                aNode.set_value(zNumber)
            elif result_type == Type.Bool:
                zBool = zType.evaluate_boolean(aNode)
                aNode.set_value(zBool)
            else:
                raise DBPathException(f"{zType.get_id()} は未実装です")
            zUpdate = True
            aNode.remove_all_children()
        except ParameterException as ex:
            zNode = ex.getNode()
            if ex.getType() == Type.ERR1:
                raise DBPathException(xMsg(zNode, MSG00410, zNode.get_text()))
            elif zNode.get_type().is_const() or not zType.can_transpose():
                if ex.getType() == Type.Bool:
                    raise DBPathException(xMsg(zNode, MSG00420, aNode.get_text(), zNode.get_text()))
                elif ex.getType() == Type.Num:
                    raise DBPathException(xMsg(zNode, MSG00430, aNode.get_text(), zNode.get_text()))
                elif ex.getType() == Type.Str:
                    raise DBPathException(xMsg(zNode, MSG00440, aNode.get_text(), zNode.get_text()))
                else:
                    raise ex
            else:
                if zType.transpose(aNode):
                    zUpdate = True

    elif zType.is_nodeset():
        zType.evaluate_nodeset(aNode)

    elif zType.is_operator():
        zV1Node = aNode.get_prev_sibling()
        zV2Node = aNode.get_next_sibling()
        if zV1Node is None or zV2Node is None:
            raise DBPathException("オペランドがnull?")
        zV1Type = zV1Node.get_type()
        zV2Type = zV2Node.get_type()
        if zV1Type is None or zV2Type is None:
            raise DBPathException("オペランドの型が未確定？")
        if zV1Type.is_const() and zV2Type.is_const():
            zV1Node.unlink()
            zV2Node.unlink()
            zUpdate = True
            # オペランドが両方定数
            if zType.get_result_type() == Type.Num:
                d1 = zV1Node.get_number_value()
                d2 = zV2Node.get_number_value()
                zResult = zType.evaluate_number_with_values(d1, d2)
                aNode.set_value(zResult)
            elif zType.get_result_type() == Type.Bool:
                zBool = False
                if zType.is_str_operand() and (zV1Type == Type.Str or zV2Type == Type.Str):
                    zS1 = zV1Node.get_string_value()
                    zS2 = zV2Node.get_string_value()
                    zBool = zType.evaluate_boolean_with_strings(zS1, zS2)
                elif zType.is_num_operand() and (zV1Type == Type.Num or zV2Type == Type.Num) or not zType.is_bool_operand():
                    d1 = zV1Node.get_number_value()
                    d2 = zV2Node.get_number_value()
                    zBool = zType.evaluate_boolean_with_values(d1, d2)
                elif zType.is_bool_operand():
                    b1 = zV1Node.get_boolean_value()
                    b2 = zV2Node.get_boolean_value()
                    zBool = zType.evaluate_boolean_with_booleans(b1, b2)
                else:
                    raise DBPathException(f"{zType.get_id()} は未実装です")
                aNode.set_value(zBool)
            else:
                raise DBPathException(f"{zType.get_id()} は未実装です")
        elif zType.can_transpose():
            if zType.transpose(aNode):
                zUpdate = True
        else:
            if not zV1Type.is_const():
                raise DBPathException(xMsg(zV1Node, MSG00510, aNode.get_text(), zV1Node.get_text()))
            else:
                raise DBPathException(xMsg(zV1Node, MSG00510, aNode.get_text(), zV2Node.get_text()))
    elif zType.can_transpose():
        if zType.transpose(aNode):
            zUpdate = True

    return zUpdate

def number_to_string( zValue:float ) ->str:
    if math.isnan(zValue):
        return "NaN"
    zResult:str = f"{zValue}"
    if zResult.endswith(".0"):
        return zResult[:len(zResult)-2]
    else:
        return zResult

class Node:
    def __init__(self, text=None):
        self.mParent:Node|None = None
        self.mPrev:Node|None = None
        self.mNext:Node|None = None
        self.mFirstChild:Node|None = None
        self.mPredicate:Node|None = None
        self.mText:str|None = text
        self.mType:"Type|None" = None
        self.mSB:list[str]|None = None
        self.check:int = 0
        self.mStartPos:int = -1
        self.mEndPos:int = -1

    def get_start_pos(self) ->int:
        return self.mStartPos

    def get_end_pos(self) ->int:
        return self.mEndPos

    def set_pos(self, pos:int) ->"Node":
        if self.mStartPos < 0 or self.mStartPos > pos:
            self.mStartPos = pos
        if self.mEndPos < 0 or self.mEndPos < pos:
            self.mEndPos = pos
        return self

    def get_type(self) ->"Type":
        return self.mType if self.mType else Type.Unknown

    def set_string_type(self):
        if self.get_text() is None:
            self.mText = ""
        self.mType = Type.Str

    def is_empty(self) ->bool:
        return (self.mText is None or len(self.mText) == 0) and (self.mSB is None or len(self.mSB) == 0)

    def get_text(self) ->str|None:
        if self.mText is None:
            if self.mSB:
                return ''.join([str(s) for s in self.mSB])
            return None
        else:
            if self.mSB:
                return self.mText + (''.join([str(s) for s in self.mSB]))
            else:
                return self.mText

    def get_boolean_value(self) ->bool:
        zText = self.get_text()
        if self.mType:
            if self.mType == Type.Str:
                return zText is not None and len(zText) > 0
            elif self.mType == Type.Num:
                try:
                    return zText is not None and float(zText) != 0
                except ValueError:
                    return False
            elif self.mType == Type.Bool:
                return zText == F_TRUE
            elif self.mType == Type.EMPTY_NODE_SET:
                return False
        raise ParameterException(self, Type.Bool)

    def get_number_value(self) ->float:
        zText = self.get_text()
        if self.mType:
            if self.mType in {Type.Str, Type.Num}:
                try:
                    return float(zText) # type: ignore
                except ValueError:
                    return float("nan")
            elif self.mType == Type.Bool:
                return 1.0 if zText == F_TRUE else 0.0
            elif self.mType == Type.EMPTY_NODE_SET:
                return 0.0
        raise ParameterException(self, Type.Num)

    def get_string_value(self) ->str:
        zText = self.get_text()
        if self.mType:
            if self.mType == Type.Str and zText is not None:
                return zText
            elif self.mType == Type.Num and zText is not None:
                return zText
            elif self.mType == Type.Bool:
                return CONST_TRUE if zText == F_TRUE else CONST_FALSE
            elif self.mType in {Type.EMPTY_NODE_SET, Type.Unknown}:
                return ""
        raise ParameterException(self, Type.Str)

    def invert_operator(self) ->bool:
        if self.mType:
            if self.mType == Type.LT:
                self.set_value(Type.GTE)
                return True
            elif self.mType == Type.LTE:
                self.set_value(Type.GT)
                return True
            elif self.mType == Type.GT:
                self.set_value(Type.LTE)
                return True
            elif self.mType == Type.GTE:
                self.set_value(Type.LT)
                return True
        return False

    def __set_value00(self, text, node_type) ->"Node":
        if text is None or node_type is None:
            raise ValueError("text and node_type cannot be None")
        
        if node_type.is_const():  # Type クラスに is_const メソッドが必要
            self.remove_predicate()
            # self.remove_all_children()  # コメントアウトと同じ状態に

        if self.mSB is not None:  # StringBuilder の処理
            self.mSB.clear()  # 長さをゼロにリセット
            if self.mParent is not None:
                self.mParent.mSB = self.mSB
                self.mSB = None
        
        self.mText = text
        self.mType = node_type
        return self

    def set_value(self, value:"Node|Type|bool|float|str") ->"Node":
        if isinstance(value, Node):  # Node 型の場合
            return self.__set_value00(value.get_text(), value.mType)
        elif isinstance(value, Type):  # Type 型の場合
            return self.__set_value00(value.get_id(), value)
        elif isinstance(value, bool):  # boolean 型の場合
            return self.__set_value00(F_TRUE if value else F_FALSE, Type.Bool)
        elif isinstance(value, (int, float)):  # 数値の場合
            return self.__set_value00(number_to_string(value), Type.Num)
        elif isinstance(value, str):  # 文字列の場合
            return self.__set_value00(value, Type.Str)
        else:
            raise ValueError(f"Unsupported type for set_value: {type(value)}")

    def append_text(self, value:str) ->"Node":
        if self.mType is not None:
            raise Exception("タイプが確定した後でappendしようとした")
        
        # mSB が None の場合、StringBuilder を取得
        if self.mSB is None:
            self.mSB = self.get_string_builder()
        
        # mSB がまだ None の場合、新しい StringBuilder を作成
        if self.mSB is None:
            self.mSB = []

        # mText を mSB に追加し、mText をクリア
        if self.mText is not None:
            self.mSB.append(self.mText)
            self.mText = None

        # value を mSB に追加
        if isinstance(value, str) and len(value) == 1:
            self.mSB.append(value)
        else:
            raise ValueError("append_text には単一の文字または整数を渡してください")
        
        return self

    def get_target_path(self) ->str|None:
        if self.mFirstChild is not None:
            # 子ノードが複数ある場合、例外をスロー
            if self.mFirstChild.get_next_sibling() is not None or self.mFirstChild.get_prev_sibling() is not None:
                raise DBPathException(ERR02010)

            # 子ノードのパスを取得
            x = self.mFirstChild.get_target_path()
            if not x:
                raise DBPathException(ERR02010)

            # 自分のテキストを取得
            v = self.get_text()
            if v == "/":
                return f"/{x}"
            else:
                return f"{v}/{x}"

        # 子ノードがない場合、自分のテキストを返す
        return self.get_text()

    def add_predicate(self) ->"Node":
        z_result = Node()
        z_result.mParent = self
        self.mPredicate = z_result
        z_result.set_string_builder(self.get_string_builder())
        return z_result

    def __unlinka(self):
        if self.mParent is not None:
            if self.mParent.mFirstChild == self:
                self.mParent.mFirstChild = self.mNext
            if self.mParent.mPredicate == self:
                self.mParent.mPredicate = self.mNext
            self.mParent = None

        if self.mPrev is not None:
            if self.mPrev.mNext == self:
                self.mPrev.mNext = self.mNext
            self.mPrev = None

    def unlink(self):
        z_prev = self.mPrev
        self.__unlinka()
        if self.mNext is not None:
            if self.mNext.mPrev == self:
                self.mNext.mPrev = z_prev
            self.mNext = None

    def clear(self):
        self.unlink()

        # 子ノードを処理
        z_child = self.mFirstChild
        while z_child is not None:
            if z_child.mParent == self:
                z_child.mParent = None
            z_child = z_child.get_next_sibling()
        self.mFirstChild = None

        # 述語ノードを処理
        if self.mPredicate is not None:
            if self.mPredicate.mParent == self:
                self.mPredicate.mParent = None
            self.mPredicate = None

        # その他のフィールドをリセット
        self.mStartPos = -1
        self.mEndPos = -1
        self.mText = None
        self.mType = None

        # StringBuilder（Pythonではstr）をクリア
        z_sb = self.mSB
        if z_sb is not None:
            self.mSB = None

        return z_sb

    def join_first_child(self) ->bool:
        if self.mPredicate is None:
            z_child = self.get_first_child()
            if z_child is not None and z_child.mPrev is None and z_child.mNext is None:
                z_child.unlink()
                self.set_pos(z_child.mStartPos)
                self.set_pos(z_child.mEndPos)

                # StringBuilderの処理
                z_sb = z_child.remove_string_builder()
                if z_sb is not None and self.mSB is None:
                    self.mSB = z_sb

                # 値と述語をセット
                self.set_value(z_child)
                self.mPredicate = z_child.mPredicate
                if self.mPredicate is not None:
                    self.mPredicate.mParent = self

                # 子ノードの再配置
                z_lowers = z_child.mFirstChild
                if z_lowers is not None:
                    z_last_child = self.get_last_child()
                    if z_last_child is None:
                        self.mFirstChild = z_lowers
                    else:
                        z_lowers.mPrev = z_last_child
                        z_last_child.mNext = z_lowers

                    while z_lowers is not None:
                        z_lowers.mParent = self
                        z_lowers = z_lowers.mNext

                return True

        return False

    def remove_string_builder(self) ->list[str]|None:
        z_result = self.mSB
        zText = self.get_text()
        
        if self.mSB is not None:
            self.mText = zText
            self.mSB.clear()  # StringBuilderのクリアに対応
            self.mSB = None
        
        if self.mType is None:
            self.mType = Type.by_value(zText)
        
        return z_result

    def get_string_builder_L(self) ->list[str]|None:
        z_result = None

        # 自分の子孫にStringBuilderがあれば取ってくる
        z_child = self.get_first_child()
        if z_child is not None:
            z_sb = z_child.get_string_builder_L()
            if z_sb is not None:
                z_result = z_sb

        # 自分のStringBuilderを取ってくる
        z_sb = self.remove_string_builder()
        if z_sb is not None:
            z_result = z_sb

        # 自分の下の兄弟からStringBuilderを取ってくる
        z_sibling = self.get_next_sibling()
        if z_sibling is not None:
            z_sb = z_sibling.get_string_builder_L()
            if z_sb is not None:
                z_result = z_sb

        return z_result

    def get_string_builder_0(self) ->list[str]|None:
        zRoot:Node = self

        # ルートノードに移動
        while zRoot.get_parent() is not None:
            zRoot = zRoot.get_parent() # type: ignore

        # ルートノードから先頭ノードに移動
        while zRoot.get_prev_sibling() is not None:
            zRoot = zRoot.get_prev_sibling() # type: ignore

        # 最終的にStringBuilderLを取得
        return zRoot.get_string_builder_L()

    def get_string_builder(self) ->list[str]|None:
        if self.mSB is None:
            if self.mPrev is not None:
                return self.mPrev.get_string_builder()
            elif self.mParent is not None:
                return self.mParent.get_string_builder()
            return None
        else:
            return self.remove_string_builder()

    def set_string_builderX(self):
        z_sb = self.get_string_builder_L()
        if z_sb is not None:
            z_sb.clear()
            if self.mSB is None:
                self.mSB = z_sb

    def set_string_builder(self, aSB:list[str]|None):
        if aSB is not None:
            aSB.clear()
            if self.mText is not None:
                aSB.append(self.mText)
                self.mText = None
        self.mSB = aSB

    def append_next_sibling(self, aSibling:"Node"):
        z_next = self.mNext
        aSibling.__unlinka()
        z_last = aSibling
        z_node = aSibling
        while z_node is not None:
            z_node.mParent = self.mParent
            z_last = z_node
            z_node = z_node.mNext
        self.mNext = aSibling
        aSibling.mPrev = self
        z_last.mNext = z_next
        if z_next is not None:
            z_next.mPrev = z_last

    def append_last_sibling(self, aSibling:"Node"):
        z_prev = self
        while z_prev.mNext is not None:
            z_prev = z_prev.mNext
        aSibling.__unlinka()
        z_prev.mNext = aSibling
        aSibling.mParent = z_prev.mParent
        aSibling.mPrev = z_prev

    def add_last_sibling(self):
        z_result = Node()
        self.append_last_sibling(z_result)
        z_result.set_string_builder(self.get_string_builder())
        return z_result

    def append_last_child(self, child:"Node|None"=None) ->"Node":
        if child is not None:
            if child == self:
                raise ValueError("appendLastChild(this) is not allowed")
            
            if self.mFirstChild is None:
                child.__unlinka()
                self.mFirstChild = child
                child.mParent = self
            else:
                self.mFirstChild.append_last_sibling(child)
            return child
        else:
            new_child = Node()
            self.append_last_child(new_child)
            new_child.set_string_builder(self.get_string_builder())
            return new_child

    def get_parent(self):
        return self.mParent

    def get_first_sibling(self):
        z_result = self
        while z_result.mPrev is not None:
            z_result = z_result.mPrev
        return z_result

    def get_prev_sibling(self):
        return self.mPrev

    def get_next_sibling(self):
        return self.mNext

    def get_last_sibling(self):
        z_result = self
        while z_result.mNext is not None:
            z_result = z_result.mNext
        return z_result

    def get_child_length(self):
        z_count = 0
        z_child = self.mFirstChild
        while z_child is not None:
            z_count += 1
            z_child = z_child.mNext
        return z_count

    def get_first_child(self):
        return self.mFirstChild

    def get_last_child(self):
        z_result = self.mFirstChild
        if z_result is not None:
            while z_result.mNext is not None:
                z_result = z_result.mNext
        return z_result

    def get_bottom_child(self) ->"Node|None":
        if self.get_type() != Type.Path:
            return None
        if self.mFirstChild is None:
            return self
        z_child = self.mFirstChild
        while True:
            if z_child.get_type() == Type.Path and z_child.mFirstChild is not None:
                z_child = z_child.mFirstChild
            elif z_child.mNext is not None:
                z_child = z_child.mNext
            else:
                break
        return z_child

    def get_predicate(self):
        return self.mPredicate

    def is_predicate(self):
        z_node = self
        while z_node is not None and z_node.mParent is not None:
            if z_node.mParent.mPredicate == z_node:
                return True
            z_node = z_node.mParent
        return False   

    def remove_predicate(self):
        if self.mPredicate is not None:
            self.mPredicate.unlink()

    def remove_all_children(self):
        z_child = self.get_first_child()
        while z_child is not None:
            z_child.unlink()
            z_child = self.get_first_child()

    def dump(self, aSB: list[str|None], indent: str):
        aSB.append(indent)
        self.to_string(aSB)
        if self.mPredicate is not None:
            aSB.append('\n')
            self.mPredicate.dump(aSB, indent + "  []")
        if self.mFirstChild is not None:
            aSB.append('\n')
            self.mFirstChild.dump(aSB, indent + "  ")
        if self.mNext is not None:
            aSB.append('\n')
            self.mNext.dump(aSB, indent)

    def to_string(self, aSB: list[str|None]) -> list:
        if self.mType is not None:
            if self.mType == Type.Str:
                aSB.append("'")
                aSB.append(self.get_text())
                aSB.append("'")
            elif self.mType == Type.Path:
                aSB.append("[Path]")
                aSB.append(self.get_text())
            elif self.mType in (Type.Bool, Type.Num):
                aSB.append(self.get_text())
            elif self.mType == Type.EMPTY_NODE_SET:
                aSB.append("[Path]{}")
            elif self.mType == Type.Unknown:
                aSB.append("[")
                aSB.append(self.mType.get_id())
                aSB.append("]")
                aSB.append(self.get_text())
            elif self.mType == Type.EXP:
                aSB.append(self.mType.get_id())
            else:
                if self.mType.is_operator() or self.mType.is_function():
                    aSB.append(self.mType.get_id())
                elif self.mType.is_nodeset():
                    aSB.append("[Path]")
                    aSB.append(self.mType.get_id())
                else:
                    aSB.append("[")
                    aSB.append(self.mType.get_id())
                    aSB.append("]")
        else:
            aSB.append("[NULL]")
            aSB.append(self.get_text())

        if self.mSB is not None:
            aSB.append("<*>")
        if self.mPrev is not None and (self.mPrev.mNext != self or self.mPrev == self):
            aSB.append("{bad prev}")
        if self.mNext is not None and (self.mNext.mPrev != self or self.mNext == self):
            aSB.append("{bad next}")
        
        return aSB
    
    def __str__(self):
        sb:list[str|None] = []
        self.to_string(sb)
        return "".join([str(s) for s in sb])

def dump( aTitle:str, aNode:Node ) ->str:
    zSB = []
    zSB.append('[Node:')
    zSB.append( aTitle )
    zSB.append( ']' )
    aNode.dump( zSB, "    " )
    return ''.join([str(s) for s in zSB])

class Type(Enum):
    ERR1 = 1
    ERR2 = 2
    Unknown = 3
    Bool = 4
    Num = 5
    Str = 6
    Path = 7
    EMPTY_NODE_SET = 8
    TEXT = 9
    COMMENT = 10
    PROCESSING_INSTRUCTION = 11
    NODE = 12
    EXP =( 113, "()" )
    OR = ( 114, "or", 7 )
    AND = ( 115,"and", 6 )
    EQ = ( 116, "=", 5 )
    NE = ( 117, "!=", 5 )
    LT = ( 118, "<", 4 )
    LTE = ( 119, "<=", 4 ) 
    GT = ( 120, ">", 4 ) 
    GTE = ( 121, ">=", 4 )
    ADD = ( 122, "+", 3 )
    SUB = ( 123, "-", 3 )
    MUL = ( 124, "*", 2 )
    DIV = ( 125, "div", 2 )
    IDIV = ( 126, "idiv", 2 )
    MOD = ( 127, "mod", 2 )
    NUMBER = 228
    BOOLEAN = 229
    TRUE = 230
    FALSE = 231
    NOT = 232
    STRING = 233
    CEILING = 234
    FLOOR = 235
    ROUND = 236
    MIN = 237
    MAX = 238
    SUM = 239
    STRING_LENGTH = 440
    CONCAT = 441
    NORMALIZE_SPACE = 442
    SUBSTRING = 443
    SUBSTRING_BEFORE = 444
    SUBSTRING_AFTER = 445
    TRANSLATE = 446
    STARTS_WITH = 447
    ENDS_WITH = 448
    CONTAINS = 449
    LIKE = 450
    ILIKE = 451
    NOT_LIKE = 452
    NOT_ILIKE = 453

    def __init__(self, value, aID:str|None=None, aPri:int|None=None ):
        if isinstance(aID,str):
            if isinstance(aPri,int):
                # 演算子のコンストラクタ
                if aPri <= 0:
                    raise Exception("演算子の優先度は１以上でないといけない")
                self.mKey:str = aID
                self.mID:str = f"({aID})"
                self.mPri:int = aPri
            else:
                # EXPのコンストラクタ
                self.mKey:str = aID
                self.mID:str = aID
                self.mPri:int = -1
        else:
            # 関数のコンストラクタ
            self.mKey:str = self.name.lower().replace('_','-')
            self.mID:str = f"{self.mKey}()"
            self.mPri:int = 0
        self.mResultType:Type|None = None
        self.mIsNodeset:bool = False
        self.mIsOprator:bool = False
        self.mIsFunction:bool = False
        self.mBoolOperand:bool = False
        self.mNumOperand:bool = False
        self.mStrOperand:bool = False
        self.mTranspose:bool = False

    def get_key(self) -> str:
        return self.mKey

    def get_id(self) -> str:
        return self.mID

    def get_tag_name(self) -> str:
        if self==Type.NOT:
            return UNIQ_TAGNAME_NOT # self.mID
        return self.mKey

    def get_pri(self) -> int:
        return self.mPri

    def evaluate_string(self, aNode: "Node") -> str:
        if self == Type.STRING:
            zParam:list[str] = get_string_param( aNode, 0, 1, 1, 1)
            return zParam[0]
        elif self == Type.CONCAT:
            zParam:list[str] = get_string_param( aNode, 0, 1, INTEGER_MAX_VALUE, INTEGER_MAX_VALUE)
            return ''.join(zParam)
        elif self == Type.NORMALIZE_SPACE:
            zParam:list[str] = get_string_param( aNode, 0, 1, 1, 1)
            return zParam[0].strip()
        elif self == Type.SUBSTRING:
            zParam:list[str] = get_string_param( aNode, 0, 1, 1, 3 )
            zNumber:list[float] = get_number_param( aNode, 1, 2, 3, 3)
            s:int = int(zNumber[0])
            zValue:str = zParam[0]
            l:int = len(zValue)
            if s >= 1:
                if s<=l:
                    zValue = zValue[s-1:]
                    l = len(zValue)
                else:
                    return ""
            if len(zNumber)>=1:
                e:int = int(zNumber[1])
                e = s + e - 1
                if e<l:
                    zValue = zValue[0:e]
            return zValue
        elif self == Type.SUBSTRING_BEFORE:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            zPos: int = zParam[0].find(zParam[1])
            if zPos >= 0:
                return zParam[0][:zPos]
            else:
                return zParam[0]
        elif self == Type.SUBSTRING_AFTER:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            zPos: int = zParam[0].find(zParam[1])
            if zPos >= 0:
                return zParam[0][zPos + len(zParam[1]):]
            else:
                return zParam[0]
        elif self == Type.TRANSLATE:
            zParam: list[str] = get_string_param(aNode, 0, 3, 3, 3)
            zValue: str = zParam[0]
            zFrom: str = zParam[1]
            zTo: str = zParam[2]
            zSB: list[str] = []
            for cc in zValue:
                i = zFrom.find(cc)  # indexOf -> find
                if i >= 0:
                    if i < len(zTo):
                        cc = zTo[i]
                    else:
                        continue
                zSB.append(cc)
            return ''.join([str(s) for s in zSB])
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_number(self, aNode: "Node") -> float:
        if self == Type.NUMBER:
            zParam:list[float] = get_number_param( aNode, 0, 1, 1, 1)
            return zParam[0]
        elif self == Type.CEILING:
            zParam:list[float] = get_number_param( aNode, 0, 1, 1, 1)
            return math.ceil(zParam[0])
        elif self == Type.FLOOR:
            zParam:list[float] = get_number_param( aNode, 0, 1, 1, 1)
            return math.floor(zParam[0])
        elif self == Type.ROUND:
            zParam:list[float] = get_number_param( aNode, 0, 1, 1, 1)
            return math.floor( zParam[0] + 0.5 )
        elif self == Type.MIN:
            zParam:list[float] = get_number_param( aNode, 0, 1, INTEGER_MAX_VALUE, INTEGER_MAX_VALUE)
            return min(zParam)
        elif self == Type.MAX:
            zParam:list[float] = get_number_param( aNode, 0, 1, INTEGER_MAX_VALUE, INTEGER_MAX_VALUE)
            return max(zParam)
        elif self == Type.SUM:
            zParam:list[float] = get_number_param( aNode, 0, 1, INTEGER_MAX_VALUE, INTEGER_MAX_VALUE)
            return sum(zParam)
        elif self == Type.STRING_LENGTH:
            zsParam:list[str] = get_string_param( aNode, 0, 1, 1, 1 )
            return len(zsParam[0]) if zsParam[0] is not None else 0
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_boolean(self, aNode: "Node") -> bool:
        if self == Type.BOOLEAN:
            zbParam:list[bool] = get_boolean_param( aNode, 0, 1, 1, 1)
            return zbParam[0]
        elif self == Type.TRUE:
            return True
        elif self == Type.FALSE:
            return False
        elif self == Type.NOT:
            return not Type.BOOLEAN.evaluate_boolean(aNode)
        elif self == Type.STARTS_WITH:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[0].startswith(zParam[1])
        elif self == Type.ENDS_WITH:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[0].endswith(zParam[1])
        elif self == Type.CONTAINS or self == Type.LIKE:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[1] in zParam[0]
        elif self == Type.ILIKE:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[1].lower() in zParam[0].lower()
        elif self == Type.NOT_LIKE:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[1] not in zParam[0]
        elif self == Type.NOT_ILIKE:
            zParam: list[str] = get_string_param(aNode, 0, 2, 2, 2)
            return zParam[1].lower() not in zParam[0].lower()
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_number_with_values(self, aValue1: float, aValue2: float) -> float:
        if self == Type.ADD:
            return aValue1 + aValue2
        elif self == Type.SUB:
            return aValue1 - aValue2
        elif self == Type.MUL:
            return aValue1 * aValue2
        elif self == Type.DIV:
            return aValue1 / aValue2
        elif self == Type.IDIV:
            return float(aValue1//aValue2)
        elif self == Type.MOD:
            return aValue1 % aValue2
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_boolean_with_values(self, aValue1: float, aValue2: float) -> bool:
        if self == Type.EQ:
            return aValue1 == aValue2
        elif self == Type.NE:
            return aValue1 != aValue2
        elif self == Type.LT:
            return aValue1 < aValue2
        elif self == Type.LTE:
            return aValue1 <= aValue2
        elif self == Type.GT:
            return aValue1 > aValue2
        elif self == Type.GTE:
            return aValue1 >= aValue2
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_boolean_with_booleans(self, aValue1: bool, aValue2: bool) -> bool:
        if self == Type.OR:
            return aValue1 or aValue2
        elif self == Type.AND:
            return aValue1 and aValue2
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_boolean_with_strings(self, aValue1: str|None, aValue2: str|None) -> bool:
        if self == Type.EQ:
            return aValue1 is not None and aValue1==aValue2 or aValue2 is None
        elif self == Type.NE:
            return aValue1 is not None and aValue1!=aValue2 or aValue2 is not None
        raise NotImplementedError(f"{self.mID} は未実装です")

    def transpose(self, aNode: "Node|None") -> bool:
        if self == Type.EXP:
            pass
        #     if aNode is not None and aNode.get_child_length()==1 and is_constant( aNode.get_first_child().get_type()):
        #         aNode.set_value( aNode.get_first_child )
        #         aNode.get_first_child().unlink()
        #         return True
        #     return False
        elif self == Type.OR:
            if aNode is None:
                raise DBPathException()
            
            zType:Type = aNode.get_type()
            zV1Node:Node|None = aNode.get_prev_sibling()
            zV2Node:Node|None = aNode.get_next_sibling()
            
            if zV1Node is None or zV2Node is None:
                raise DBPathException("オペランドがnull?")
            
            zV1Type:Type = zV1Node.get_type()
            zV2Type:Type = zV2Node.get_type()
            
            if zV1Type is None or zV2Type is None:
                raise DBPathException("オペランドの型が未確定？")
            
            zV1Node.unlink()
            zV2Node.unlink()
            
            if zType == Type.AND and zV1Type.is_const() and not zV1Node.get_boolean_value():
                aNode.set_value(False)
            elif zType == Type.AND and zV2Type.is_const() and not zV2Node.get_boolean_value():
                aNode.set_value(False)
            elif zType == Type.OR and zV1Type.is_const() and zV1Node.get_boolean_value():
                aNode.set_value(True)
            elif zType == Type.OR and zV2Type.is_const() and zV2Node.get_boolean_value():
                aNode.set_value(True)
            elif not zV1Type.is_const() and not zV2Type.is_const():
                if zType == zV1Type:
                    z_child:Node|None = zV1Node.get_first_child()
                    while z_child is not None:
                        z_child.unlink()
                        aNode.append_last_child(z_child)
                        z_child = zV1Node.get_first_child()
                else:
                    aNode.append_last_child(zV1Node)
                aNode.append_last_child(zV2Node)
            else:
                if zV1Type.is_const():
                    zV1Node = zV2Node
                aNode.set_value(zV1Node)
                z_child = zV1Node.get_first_child()
                while z_child is not None:
                    z_child.unlink()
                    aNode.append_last_child(z_child)
                    z_child = zV1Node.get_first_child()
            
            return True         
        elif self == Type.AND:
            return Type.OR.transpose( aNode )
        elif self == Type.EQ:
            if aNode is None:
                raise DBPathException()
            
            zType:Type = aNode.get_type()
            zV1Node:Node|None = aNode.get_prev_sibling()
            zV2Node:Node|None = aNode.get_next_sibling()
            
            if zV1Node is None or zV2Node is None:
                raise DBPathException("オペランドがnull?")
            
            zV1Type:Type = zV1Node.get_type()
            zV2Type:Type = zV2Node.get_type()
            
            if zV1Node is None or zV2Node is None:
                raise DBPathException("オペランドの型が未確定？")
            
            zV1Node.unlink()
            zV2Node.unlink()

            if zV1Type.is_const() and not zV2Type.is_const():
                aNode.invert_operator()
                a:Node = zV2Node
                zV2Node = zV1Node
                zV1Node = a
                zV1Type = zV1Node.get_type()
                zV2Type = zV2Node.get_type()
            
            if is_path(zV1Type) and zType.get_result_type() == Type.Bool:
                if zV2Type.is_const():
                    aNode.append_last_child(zV1Node)
                    aNode.append_last_child(zV2Node)
                else:
                    raise DBPathException(xMsg(zV1Node, MSG00510, aNode.get_text(), zV2Node.get_text()))
            else:
                raise DBPathException(xMsg(zV1Node, MSG00510, aNode.get_text(), zV1Node.get_text()))
            
            return True
        elif self == Type.NE or self == Type.LT or self == Type.LTE or self == Type.GT or self == Type.GTE:
            return Type.EQ.transpose( aNode )
        elif self == Type.NOT:
            if aNode is not None and aNode.get_child_length() == 1:
                zChild:Node|None = aNode.get_first_child()
                if zChild is not None and zChild.get_type() == Type.NOT and zChild.get_child_length()==1:
                    aNode.join_first_child()
                    aNode.join_first_child()
            return False
        elif self == Type.STARTS_WITH or self == Type.ENDS_WITH or self == Type.CONTAINS or self == Type.LIKE or self == Type.ILIKE or self == Type.NOT_LIKE or self == Type.NOT_ILIKE:
            return False
        raise NotImplementedError(f"{self.mID} は未実装です")

    def evaluate_nodeset(self, aNode: "Node|None") -> bool:
        if aNode is None:
            raise ValueError("can not evaluate aNode is None")
        if self == Type.Path:
            zResult:bool = False
            if aNode is not None:
                zTagName = aNode.get_text()
                if is_number( zTagName ):
                    print(f"xxx")
                zChild:Node|None = aNode.get_first_child()
                while zChild is not None:
                    zType:Type = zChild.get_type()
                    if zType.is_nodeset():
                        if zType.evaluate_nodeset( zChild ):
                            zResult = True
                    zChild = zChild.get_next_sibling()
            return zResult
        elif self == Type.EMPTY_NODE_SET:
            return False
        elif self == Type.TEXT or self == Type.COMMENT or self == Type.PROCESSING_INSTRUCTION or self == Type.NODE:
            raise DBPathException( xMsg( aNode, MSG00200, aNode.get_text() ))
        raise NotImplementedError(f"{self.mID} は未実装です")

    def is_function(self) -> bool:
        return self.mIsFunction

    def is_operator(self) -> bool:
        return self.mIsOprator

    def is_nodeset(self) -> bool:
        return self.mIsNodeset

    def get_result_type(self) -> "Type|None":
        return self.mResultType

    def is_bool_operand(self) -> bool:
        return self.mBoolOperand

    def is_num_operand(self) -> bool:
        return self.mNumOperand

    def is_str_operand(self) -> bool:
        return self.mStrOperand

    def can_transpose(self) -> bool:
        return self.mTranspose

    def is_const(self) ->bool:
        return self == Type.Bool or self == Type.Num or self == Type.Str or self == Type.EMPTY_NODE_SET
    
    @staticmethod
    @lru_cache(maxsize=1)
    def init():
        zDmy:Node = Node()
        zDmy.set_value( 0.0 )
        zKEY2FUNCTION:dict[str,Type] = {} # MAP_KEY2FUNCTION;
        zKEY2OPERATOR:dict[str,Type] = {} # MAP_KEY2FUNCTION;
        zID2TYPE:dict[str,Type] = {} # MAP_ID2TYPE;
        zNode:Node = Node()
        for zType in Type:
            #--------------------------------
            # 関数判定
            #--------------------------------
            try:
                try:
                    zType.evaluate_string( zNode )
                except DBPathException:
                    pass
                zType.mIsFunction = True
                zType.mResultType = Type.Str
            except NotImplementedError:
                pass
            if zType.mResultType is None:
                try:
                    try:
                        zType.evaluate_number( zNode )
                    except DBPathException:
                        pass
                    zType.mIsFunction = True
                    zType.mResultType = Type.Num
                except NotImplementedError:
                    pass

            if zType.mResultType is None:
                try:
                    try:
                        zType.evaluate_boolean( zNode )
                    except DBPathException:
                        pass
                    zType.mIsFunction = True
                    zType.mResultType = Type.Bool
                except NotImplementedError:
                    pass
            #--------------------------------
            # 演算子判定
            #--------------------------------
            if zType.mResultType is None:
                try:
                    try:
                        zType.evaluate_number_with_values( 3, 4 )
                    except DBPathException:
                        pass
                    zType.mIsOprator = True
                    zType.mResultType = Type.Num
                    zType.mNumOperand = True
                except NotImplementedError:
                    pass
            if zType.mResultType is None:
                try:
                    try:
                        zType.evaluate_boolean_with_values( 3, 4 )
                    except DBPathException:
                        pass
                    zType.mIsOprator = True
                    zType.mResultType = Type.Bool
                    zType.mNumOperand = True
                except NotImplementedError:
                    pass
                try:
                    try:
                        zType.evaluate_boolean_with_booleans( True, False )
                    except DBPathException:
                        pass
                    zType.mIsOprator = True
                    zType.mResultType = Type.Bool
                    zType.mBoolOperand = True
                except NotImplementedError:
                    pass
                try:
                    try:
                        zType.evaluate_boolean_with_strings( "a", "b" )
                    except DBPathException:
                        pass
                    zType.mIsOprator = True
                    zType.mResultType = Type.Bool
                    zType.mStrOperand = True
                except NotImplementedError:
                    pass
            
            #--------------------------------
            # 演算子判定
            #--------------------------------
            try:
                try:
                    zType.transpose( None )
                except DBPathException:
                    pass
                zType.mTranspose = True
            except NotImplementedError:
                pass
            #--------------------------------
            # Nodeset判定
            #--------------------------------
            try:
                try:
                    zType.evaluate_nodeset( zNode )
                except DBPathException:
                    pass
                zType.mIsNodeset = True
            except NotImplementedError:
                pass
            if zType.mResultType is not None or zType.mTranspose or zType.mIsNodeset:
                if not ( zType == Type.Path or zType == zType.EMPTY_NODE_SET ):
                    if zType.mIsFunction or zType.mIsNodeset:
                        zKEY2FUNCTION[zType.mKey] = zType
                    if zType.mIsOprator:
                        zKEY2OPERATOR[zType.mKey] = zType
                    zID2TYPE[zType.mID] = zType

        return zKEY2FUNCTION,zKEY2OPERATOR,zID2TYPE        

    @staticmethod
    def _get_key_to_operator() ->dict[str,"Type"]:
        return { t.name: t for t in Type}

    @staticmethod
    def by_function_name( zKey:str|None ) ->"Type|None":
        KEY2FUNCTION,KEY2OPERATOR,ID2TYPE = Type.init()
        return KEY2FUNCTION.get( zKey ) if zKey else None

    @staticmethod
    def by_operator_name( zKey:str ) ->"Type|None":
        KEY2FUNCTION,KEY2OPERATOR,ID2TYPE = Type.init()
        return KEY2OPERATOR.get( zKey )

    @staticmethod
    def by_operator_nameC( zKey ) ->"Type|None":
        KEY2FUNCTION,KEY2OPERATOR,ID2TYPE = Type.init()
        a = "" + zKey
        return KEY2OPERATOR.get( a )

    @staticmethod
    def by_id( aID:str ) ->"Type|None":
        KEY2FUNCTION,KEY2OPERATOR,ID2TYPE = Type.init()
        return ID2TYPE.get( aID )

    @staticmethod
    def by_value( zValue:str|None ) ->"Type":
            if zValue is None or len(zValue)==0:
                return Type.Unknown
            if zValue == F_TRUE or zValue==F_FALSE:
                return Type.Bool
            zType:Type|None = Type.by_operator_name( zValue )
            if zType is not None:
                if zType == Type.AND or zType == Type.OR:
                    return Type.Path
                return zType
            if is_number( zValue ):
                return Type.Num
            return Type.Path

def check_parameter_number(zNode:"Node", aStartPos:int, aEndPos1:int, aEndPos2:int, aEndPos3:int) ->int:
    if zNode is None or aStartPos < 0 or aStartPos > aEndPos1 or aEndPos1 > aEndPos2:
        raise ValueError("Invalid arguments")

    zParamNum:int = zNode.get_child_length()
    if zParamNum < aEndPos1 or aEndPos3 < zParamNum:
        raise ParameterException(zNode, Type.ERR1 )

    zNum:int = zParamNum - aStartPos
    zPos:int = 0
    zIdx:int = 0

    zParamNode:Node|None = zNode.get_first_child()
    while zParamNode is not None:
        if aStartPos <= zPos and zIdx < zNum:
            if zParamNode.get_first_child() is not None:
                raise ParameterException(zNode, Type.ERR2 )
            zIdx += 1
        zParamNode = zParamNode.get_next_sibling()
        zPos += 1

    return zNum

def get_number_param(zNode:"Node", aStartPos:int, aEndPos1:int, aEndPos2:int, aEndPos3:int) ->list[float]:
    zNum = check_parameter_number(zNode, aStartPos, aEndPos1, aEndPos2, aEndPos3)
    zResult = [0.0] * zNum  # Javaのdouble[]をPythonのリストに置き換え
    zPos = 0
    zIdx = 0
    zParamNode = zNode.get_first_child()
    while zParamNode is not None:
        if aStartPos <= zPos and zIdx < zNum:
            zResult[zIdx] = zParamNode.get_number_value()
            zIdx += 1
        zParamNode = zParamNode.get_next_sibling()
        zPos += 1
    return zResult

def get_boolean_param(zNode:"Node", aStartPos:int, aEndPos1:int, aEndPos2:int, aEndPos3:int):
    zNum = check_parameter_number(zNode, aStartPos, aEndPos1, aEndPos2, aEndPos3)
    zResult = [False] * zNum  # Javaのboolean[]をPythonのリストに置き換え
    zPos = 0
    zIdx = 0
    zParamNode = zNode.get_first_child()
    while zParamNode is not None:
        if aStartPos <= zPos and zIdx < zNum:
            zResult[zIdx] = zParamNode.get_boolean_value()
            zIdx += 1
        zParamNode = zParamNode.get_next_sibling()
        zPos += 1
    return zResult

def get_string_param(zNode:"Node", aStartPos:int, aEndPos1:int, aEndPos2:int, aEndPos3:int) ->list[str]:
    zNum = check_parameter_number(zNode, aStartPos, aEndPos1, aEndPos2, aEndPos3)
    zResult:list[str] = [''] * zNum  # JavaのString[]をPythonのリストに置き換え
    zPos = 0
    zIdx = 0
    zParamNode = zNode.get_first_child()
    while zParamNode is not None:
        if aStartPos <= zPos and zIdx < zNum:
            zResult[zIdx] = zParamNode.get_string_value()
            zIdx += 1
        zParamNode = zParamNode.get_next_sibling()
        zPos += 1
    return zResult

def is_number_char(a_char: str|None) -> bool:
    return a_char is not None and '0' <= a_char <= '9'

def is_number(a_value: str|None) -> bool:
    if a_value is None:
        return False
    
    z_comma = 0
    z_num = 0
    
    for i, cc in enumerate(a_value):
        if cc in '+-':
            if i != 0:
                return False
        elif cc == '.':
            if z_comma > 0:
                return False
            z_comma += 1
        elif cc in '0123456789':
            z_num += 1
        else:
            return False
    
    return z_num > 0

def is_and_or( aType:Type ) -> bool:
    return aType == Type.OR or aType == Type.AND # or aType == Type.PREDICATE or aType == Type.EXP

def is_not( aType: Type ) -> bool:
    return aType == Type.NOT

def is_path( aType:"Type" ) ->bool:
        return aType == Type.Path

class ParameterException(DBPathException):
    def __init__(self, node, type):
        super().__init__(f"Parameter error in node: {node}, expected type: {type}")
        self._node = node
        self._type = type
    def getType(self):
            return self._type
    def getNode(self):
        return self._node

class Reader:
    def __init__(self, aString: str):
        """
        初期化

        :param aString: 読み込む文字列
        """
        self.mString = aString
        self.mLength = len(aString) if aString is not None else 0
        self.mPos = 0

    def get_pos(self) -> int:
        """
        現在の位置を取得

        :return: 現在の文字位置
        """
        return self.mPos

    def poll(self) -> str|None:
        """
        現在の文字を取得して、次の位置に進む

        :return: 現在の文字コード (int)、文字列の終わりの場合は -1
        """
        if self.mPos < self.mLength:
            char = self.mString[self.mPos]
            self.mPos += 1
            return char
        return None

    def peek(self) -> str|None:
        """
        現在の位置の文字を取得 (進めない)

        :return: 現在の文字コード (int)、文字列の終わりの場合は -1
        """
        if self.mPos < self.mLength:
            return self.mString[self.mPos]
        return None

    def peek_token(self) -> str:
        """
        トークンを先読み

        :return: 空白以外のトークン
        """
        zStart = self.mPos
        while zStart < self.mLength and self.mString[zStart] == ' ':
            zStart += 1
        zEnd = zStart
        while zEnd < self.mLength and self._seek(self.mString[zEnd]):
            zEnd += 1
        if zStart < zEnd:
            return self.mString[zStart:zEnd]
        else:
            return ""

    def _seek(self, cc: str) -> bool:
        """
        空白以外の文字かを判定

        :param cc: 判定する文字
        :return: 空白以外なら True
        """
        return cc != ' '

    def seek_space(self) -> None:
        """
        空白をスキップ
        """
        while self.peek() == ' ':
            self.poll()

def xMsg(*args):
    if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], str):
        # xMsg(int aPos, String aMesg)
        aPos, aMesg = args
        return f"{aPos}文字目:{aMesg}"
    
    elif len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], str):
        # xMsg(int aStartPos, int aEndPos, String aMesg)
        aStartPos, aEndPos, aMesg = args
        return f"{aStartPos}-{aEndPos}文字目:{aMesg}"
    
    elif len(args) == 2 and hasattr(args[0], "get_start_pos") and isinstance(args[1], str):
        # xMsg(Node aNode, String aMesg)
        aNode, aMesg = args
        return xMsg(aNode.get_start_pos(), aNode.get_end_pos(), aMesg)
    
    elif len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], str) and isinstance(args[2], str):
        # xMsg(int aPos, String aMesg, String arg)
        aPos, aMesg, arg = args
        return xMsg(aPos, aMesg) % (arg)
    
    elif len(args) == 4 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], str) and isinstance(args[3], str):
        # xMsg(int aStartPos, int aEndPos, String aMesg, String arg)
        aStartPos, aEndPos, aMesg, arg = args
        return xMsg(aStartPos, aEndPos, aMesg) % (arg)
    
    elif len(args) == 3 and hasattr(args[0], "get_start_pos") and isinstance(args[1], str) and isinstance(args[2], str|None):
        # xMsg(Node aNode, String aMesg, String arg)
        aNode, aMesg, arg = args
        if arg:
            return xMsg(aNode.get_start_pos(), aNode.get_end_pos(), aMesg) % (arg)
        else:
            return xMsg(aNode.get_start_pos(), aNode.get_end_pos(), aMesg)
    
    elif len(args) == 3 and hasattr(args[0], "get_start_pos") and isinstance(args[1], str) and isinstance(args[2], (list, tuple)):
        # xMsg(Node aNode, String aMesg, String... arg)
        aNode, aMesg, arg = args
        return xMsg(aNode.get_start_pos(), aNode.get_end_pos(), aMesg) % arg

    elif len(args) == 4 and hasattr(args[0], "get_start_pos") and isinstance(args[1], str) and isinstance(args[2], str) and isinstance(args[3], str):
        aNode, aMesg, arg1, arg2 = args
        return xMsg(aNode.get_start_pos(), aNode.get_end_pos(), aMesg) % (arg1,arg2)
    
    elif len(args) == 4 and hasattr(args[0], "get_start_pos") and hasattr(args[1], "get_end_pos") and isinstance(args[2], str) and isinstance(args[3], str):
        # xMsg(Node aStart, Node aEnd, String aMesg, String arg)
        aStart, aEnd, aMesg, arg = args
        return xMsg(aStart.get_start_pos(), aEnd.get_end_pos(), aMesg) % (arg)
    
    else:
        raise TypeError("Invalid arguments for xMsg")

