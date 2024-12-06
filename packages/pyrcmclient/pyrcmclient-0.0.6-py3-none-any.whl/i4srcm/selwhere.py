from lxml import etree
import re

def parse_conditions(condition_str, parent_element):
    """
    ネストされた条件を再帰的に解析し、XMLに変換する。
    """
    condition_pattern = re.compile(r"@?(\w+)\s*(!?=|<|<=|>|>=|lt|le|gt|ge)\s*(?:'(.*?)'|(\d+))")

    # 'or' で条件を分割
    or_parts = re.split(r'\s+or\s+', condition_str, flags=re.IGNORECASE)

    if len(or_parts) > 1:
        # 'or' が存在する場合、'or' 要素を作成
        or_element = etree.Element("or")
        for part in or_parts:
            part = part.strip()
            # 各 'or' 部分を 'and' で分割
            and_conditions = re.split(r'\s+and\s+', part, flags=re.IGNORECASE)
            and_element = etree.Element("and")
            for and_part in and_conditions:
                and_part = and_part.strip()
                if "[" in and_part and "]" in and_part:
                    # ネストされた条件
                    match = re.match(r"(\w+)\[(.*)\]", and_part)
                    if match:
                        tag_name, nested_condition_str = match.groups()
                        nested_element = etree.Element(tag_name)
                        and_element.append(nested_element)
                        parse_conditions(nested_condition_str, nested_element)
                else:
                    # 単純な条件
                    condition_match = condition_pattern.match(and_part)
                    if condition_match:
                        target, operator, value = condition_match.groups()

                        # XMLの条件タグを作成
                        condition_element = etree.Element(target)
                        operand = etree.Element("operand")
                        value_elem = etree.Element("value")

                        # 属性である場合にlayer要素を追加
                        if and_part.startswith('@'):
                            layer = etree.Element("layer")
                            if target == "tagid":
                                layer.text = "tagid"
                            else:
                                layer.text = "attribute"
                            condition_element.append(layer)

                        # 演算子を変換
                        operator_map = {
                            "=": "EQ",
                            "!=": "NE",
                            "<": "LT",
                            "<=": "LTE",
                            ">": "GT",
                            ">=": "GTE",
                            "lt": "LT",
                            "le": "LTE",
                            "gt": "GT",
                            "ge": "GTE"
                        }
                        operand.text = operator_map.get(operator, "EQ")
                        value_elem.text = value

                        # 条件要素に追加
                        condition_element.append(operand)
                        condition_element.append(value_elem)

                        # AND要素に追加
                        and_element.append(condition_element)
            or_element.append(and_element)
        # 親要素に 'or' 要素を追加
        parent_element.append(or_element)
    else:
        # 'or' が存在しない場合、'and' で分割して条件を追加
        and_conditions = re.split(r'\s+and\s+', condition_str, flags=re.IGNORECASE)
        for and_part in and_conditions:
            and_part = and_part.strip()
            if "[" in and_part and "]" in and_part:
                # ネストされた条件
                match = re.match(r"(\w+)\[(.*)\]", and_part)
                if match:
                    tag_name, nested_condition_str = match.groups()
                    nested_element = etree.Element(tag_name)
                    parent_element.append(nested_element)
                    parse_conditions(nested_condition_str, nested_element)
            else:
                # 単純な条件
                condition_match = condition_pattern.match(and_part)
                if condition_match:
                    target, operator, value = condition_match.groups()

                    # XMLの条件タグを作成
                    condition_element = etree.Element(target)
                    operand = etree.Element("operand")
                    value_elem = etree.Element("value")

                    # 属性である場合にlayer要素を追加
                    if and_part.startswith('@'):
                        layer = etree.Element("layer")
                        if target == "tagid":
                            layer.text = "tagid"
                        else:
                            layer.text = "attribute"
                        condition_element.append(layer)

                    # 演算子を変換
                    operator_map = {
                        "=": "EQ",
                        "!=": "NE",
                        "<": "LT",
                        "<=": "LTE",
                        ">": "GT",
                        ">=": "GTE",
                        "lt": "LT",
                        "le": "LTE",
                        "gt": "GT",
                        "ge": "GTE"
                    }
                    operand.text = operator_map.get(operator, "EQ")
                    value_elem.text = value

                    # 条件要素に追加
                    condition_element.append(operand)
                    condition_element.append(value_elem)

                    # 親要素に条件を追加
                    parent_element.append(condition_element)

def convert_easypath_to_xml(easypath, *, upperLevel:int|None=None, lowerLevel:int|None=None):
    # 正規表現パターンを定義
    xpath_pattern = re.compile(r"(\w+)(\[.*?\])?")

    # ターゲットパスを生成
    target_path = []

    # ルート要素を作成
    root_element = etree.Element("instruction", no="")
    instkind = etree.Element("instkind")
    instkind.text = "SEL2"
    instbody = etree.Element("instbody")

    # タグ名と条件を分離して処理
    sel_where = etree.Element("selWhere")
    current_element = None

    for match in xpath_pattern.finditer(easypath):
        tag_name, condition_str = match.groups()
        target_path.append(tag_name)

        # 新しいタグ要素を作成
        new_element = etree.Element(tag_name)
        if current_element is None:
            sel_where.append(new_element)
        else:
            current_element.append(new_element)
        current_element = new_element

        # 条件がある場合に解析
        if condition_str:
            parse_conditions(condition_str.strip('[]'), current_element)

    # ターゲットパスを設定
    target_element = etree.Element("target")
    target_element.text = "/".join(target_path)
    instbody.append(target_element)
    if isinstance(upperLevel,int):
        upper_elem = etree.SubElement(instbody, 'upperLevel' )
        upper_elem.text = str(upperLevel)
    if isinstance(lowerLevel,int):
        lower_elem = etree.SubElement(instbody, 'lowerLevel' )
        lower_elem.text = str(lowerLevel)

    # instbodyにselWhereを追加
    instbody.append(sel_where)

    # ルート要素にinstkindとinstbodyを追加
    root_element.append(instkind)
    root_element.append(instbody)

    return root_element

