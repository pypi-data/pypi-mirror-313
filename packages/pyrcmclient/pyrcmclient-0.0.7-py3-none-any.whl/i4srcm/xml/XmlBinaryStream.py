from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment
import struct
from io import IOBase, RawIOBase, BufferedIOBase, BytesIO, BufferedReader, BufferedWriter
from typing import NamedTuple

# 標準拡張子
EXT:str = ".bxml"
# フォーマットバージョン
VER:str = "1.0.0"
# フォーマットヘッダ
HEADER_BYTES:bytes = f"jp.co.i4s.xml.XmlNode/{VER}".encode()
# バッファサイズ
IO_BUFFER_SIZE = 4096
CHAR_BUFFER_SIZE = 100
# ヘッダフラグ
L_8BIT:int = 0 << 6
L_16BIT:int = 1 << 6
L_24BIT:int = 2 << 6
L_32BIT:int = 3 << 6
MASK_LENGTH:int = 3 << 6
F_ATTRIBUTES:int = 2
F_TEXT:int = 1
T_BSTR:int = 0 << 3
T_WSTR:int = 1 << 3
T_COMMENT:int = 2 << 3
T_LEAF:int = 3 << 3
T_NODE:int = 4 << 3
MASK_TYPE:int = 7 << 3

ENC_TABLE:list[str] = [ "UTF-8", "UTF-8","UTF-8","UTF-8","UTF-8","UTF-8","UTF-8","UTF-8","UTF-8","UTF-8",]
ENC_TABLE[0] = "UTF-8"
ENC_TABLE[2] = "ISO2022JP"
ENC_TABLE[3] = "Shift_JIS"
ENC_TABLE[4] = "Windows-31J"
ENC_TABLE[5] = "MS932"
ENC_TABLE[6] = "CP932"

CDATA_ATT=":CDATA:"
KEYWORDS = [
        None, "",
        "tagid", "owner", "auth", "delTime", CDATA_ATT,
        "a,a", "a,g", "a,u", "g,g", "g,u", "u,u"
]
I_NONE:int = KEYWORDS.index(None)
I_BLANK:int = KEYWORDS.index("")

class IllegalStringIndexException(Exception):
    def __init__(self, message:str, length:int, value:int):
        super().__init__(message)
        self.length:int = length
        self.value:int = value

class BinString(NamedTuple):
    valid:bool
    text:str

aEOF:int = -1

# バイナリデータ用InputStream
class XmlBinaryInputStream:
    EOF:int = aEOF
    def __init__(self, input_stream:RawIOBase|BufferedIOBase, header_bytes:bytes=HEADER_BYTES):
        self.EOF = aEOF
        self._in = input_stream
        self._buffer:bytearray = bytearray(IO_BUFFER_SIZE)
        self._buffer_len:int = 0
        self._buffer_pos:int = 0
        self._value_list:list[BinString] = [BinString(True, kw) for kw in KEYWORDS]
        self._char_buff:list = [''] * CHAR_BUFFER_SIZE

        b:bytearray = bytearray(256)
        while self._buffer_len < len(header_bytes):
            n = self._in.readinto(b)
            if n < 0:
                break
            self._buffer[self._buffer_len:self._buffer_len+n] = b
            self._buffer_len += n

        if self._buffer_len < len(header_bytes) or self._buffer[:len(header_bytes)] != header_bytes:
            raise Exception("invalid header")

        self._buffer_pos = len(header_bytes)

    def read(self):
        if self._buffer_pos == self._buffer_len:
            self._buffer_len = 0
            i=0
            while self._buffer_len == 0 and i<3:
                self._buffer_len = self._in.readinto(self._buffer)
                i+=1
            self._buffer_pos = 0

        if self._buffer_len < 0:
            return XmlBinaryInputStream.EOF

        b = self._buffer[self._buffer_pos]
        self._buffer_pos += 1
        return b

    def read8bit(self) ->int:
        return int(self.read())

    def read16bit(self) ->int:
        b2 = self.read()
        b1 = self.read()
        if b2 < 0 or b1 < 0:
            return XmlBinaryInputStream.EOF
        return int((b2 << 8) | b1)

    def read24bit(self) ->int:
        b3 = self.read()
        b2 = self.read()
        b1 = self.read()
        if b3 < 0 or b2 < 0 or b1 < 0:
            return XmlBinaryInputStream.EOF
        return int((b3 << 16) | (b2 << 8) | b1)

    def read32bit(self):
        b4 = self.read()
        b3 = self.read()
        b2 = self.read()
        b1 = self.read()
        if b4 < 0 or b3 < 0 or b2 < 0 or b1 < 0:
            return XmlBinaryInputStream.EOF
        unsigned_value = int( (b4 << 24) | (b3 << 16) | (b2 << 8) | b1 )
        # 符号付き整数に変換
        if unsigned_value >= 0x80000000:
            signed_value = unsigned_value - 0x100000000  # 負の値に調整
        else:
            signed_value = unsigned_value

        return signed_value

    def read16bit_with_header(self, header):
        if header & MASK_LENGTH == L_8BIT:
            return self.read8bit()
        else:
            return self.read16bit()

    def read32bit_with_header(self, header):
        if header & MASK_LENGTH == L_8BIT:
            return self.read8bit()
        elif header & MASK_LENGTH == L_16BIT:
            return self.read16bit()
        elif header & MASK_LENGTH == L_24BIT:
            return self.read24bit()
        else:
            return self.read32bit()

    def read_string(self, flag):
        z_len = self.read32bit_with_header(flag)
        if z_len < 0:
            return False

        if z_len > len(self._char_buff):
            self._char_buff = [''] * z_len

        for i in range(z_len):
            self._char_buff[i] = chr(self.read16bit())

        z_text = ''.join(self._char_buff[:z_len])
        T = not (z_len > 0 and '0' <= self._char_buff[0] <= '9')
        self._value_list.append(BinString(T, z_text))
        return True

    def get_string(self):
        idx:int = self.read32bit()
        if idx < 0:
            num:int = ~idx
            p:int = len(self._char_buff)
            while True:
                p -= 1
                self._char_buff[p] = chr(ord('0') + num % 10)
                num //= 10
                if num<=0:
                    break
            text:str = ''.join( self._char_buff[p:])
            return BinString(False, text )
        elif idx < len(self._value_list):
            return self._value_list[idx]
        raise IllegalStringIndexException("end of file in getString {} {}".format(idx, len(self._value_list)), L_32BIT, idx)

    def close(self):
        self._in.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

default_ns = {"xsl": "http://www.w3.org/1999/XSL/Transform"}
# `fromBinary`メソッドをPythonに移植
def _from_binary(inp:XmlBinaryInputStream,name_space:dict) ->Elem:
    header:int = inp.read8bit()
    typ:int = header & MASK_TYPE

    # 文字列情報を読み込み
    while header != inp.EOF and (typ == T_BSTR or typ == T_WSTR):
        inp.read_string(header)
        header = inp.read8bit()
        typ = header & MASK_TYPE

    if header == inp.EOF:
        raise IOError(f"EOF")

    # タグ名と属性処理
    tag_name:str|None = None
    att_dict:dict|None = None
    local_ns:dict = name_space
    child_ns:bool = False
    if typ == T_NODE or typ == T_LEAF:
        x = inp.get_string()
        if not x.valid:
            raise IOError(f"invalid tagname {x.text}")

        tag_name = x.text

        # 属性がある場合の処理
        if (header & F_ATTRIBUTES) != 0:
            att_dict = {}
            att_size = inp.read16bit_with_header(header)
            for _ in range(att_size):
                att_name:BinString = inp.get_string()
                att_value:BinString = inp.get_string()
                if att_name.text.startswith("xmlns:"):
                    if not child_ns:
                        child_ns = True
                        local_ns = local_ns.copy()
                    local_ns[att_name.text.replace("xmlns:","")] = att_value.text
                else:
                    att_dict[att_name.text] = att_value.text
        p = tag_name.find(':')
        if p>0:
            ns_name = tag_name[:p]
            url = local_ns.get(ns_name)
            if url is None:
                url = default_ns.get(ns_name,"")
                name_space[ns_name] = url
                local_ns[ns_name] = url
            tag_name = f"{{{url}}}{tag_name[p+1:]}"
    else:
        tag_name = None

    # テキスト処理
    text_value:str|None = None
    if (header & F_TEXT) != 0:
        try:
            text_value = inp.get_string().text
        except IllegalStringIndexException as ex:
            if header == 17 and ex.length == L_32BIT and ex.value != 0 and (ex.value & 0xffffff) == 0:
                # 過去バージョンで書き出しにバグがあったので読み込み時に修正
                att_size = (ex.value >> 24)
                inp.read8bit()  # 属性名のidxをスキップ
                inp.read32bit()  # 属性テキストのidxをスキップ
                for _ in range(1, att_size):
                    inp.read32bit()  # 属性名のidxをスキップ
                    inp.read32bit()  # 属性テキストのidxをスキップ
                text_value = inp.get_string().text
            else:
                raise ex

    # XmlNodeインスタンスを生成
    if tag_name:
        node_elem = etree.Element( tag_name, attrib=att_dict, nsmap=name_space )
        if text_value:
            node_elem.text = text_value
    else:
        node_elem = etree.Comment( text_value )

    # 子ノードの数
    num_childs:int = 0
    if typ == T_NODE:
        num_childs = inp.read32bit_with_header(header)
        if num_childs < 0:
            raise IOError("end of file in number of children")

    # ノードのオブジェクトを構築
    if typ == T_NODE:
        for i in range(num_childs):
            child_elem:Elem|None = _from_binary(inp,local_ns)
            if child_elem is None:
                raise IOError("end of file in read children")
            elif isinstance(node_elem,Elem):
                node_elem.append(child_elem) # type: ignore
        z_trailer = inp.read8bit()
        if z_trailer != header:
            raise IOError("read error in trailer")

    return node_elem

def from_binary( aIn ) ->Elem:
    with XmlBinaryInputStream( aIn, HEADER_BYTES ) as zIn:
        # read encoding
        zEncode:int = zIn.read8bit()
        # read node
        zNode:Elem = _from_binary( zIn, {} )
        # set encode
        # if 0 <= zEncode and zEncode < ENC_TABLE.length:
        #     zNode.setEncoding( ENC_TABLE[zEncode] )
        return zNode

class XmlBinaryOutputStream:
    def __init__(self, out:RawIOBase|BufferedIOBase):
        self._out = out
        self._dictionary: dict[str,int] = {}

        self._out.write(HEADER_BYTES)
        for i, keyword in enumerate(KEYWORDS):
            if keyword is not None:
                self._dictionary[keyword] = i

    def flush(self):
        self._out.flush()

    def close(self):
        self.flush()
        self._out.close()

    def write8bit(self, aValue: int):
        if aValue < 0:
            raise IOError("Invalid value")
        self._out.write(struct.pack('B', aValue))  # 'B' for unsigned 8-bit

    def _write16bit(self, aValue: int):
        if aValue < 0:
            raise IOError("Invalid value")
        self._out.write(struct.pack('>H', aValue))  # '>H' for big-endian 16-bit

    def writeChar(self, aValue: int):
        if aValue < 0:
            raise IOError("Invalid value")
        self._out.write(struct.pack('>H', aValue))  # UTF-16用の2バイト

    def write24bit(self, aValue: int):
        if aValue < 0 or aValue >= (1 << 24):  # 24ビットの範囲外チェック
            raise IOError("Invalid value for 24-bit integer")
        # 3バイトに分解して書き込み
        self._out.write(bytes([(aValue >> 16) & 0xFF, (aValue >> 8) & 0xFF, aValue & 0xFF]))

    def _write32bit(self, aValue: int):
        if aValue < 0:
            # 2の補数形式で符号なし整数に変換（32ビット）
            aValue = (1 << 32) + aValue
        # structで32ビット符号なし整数として書き込み
        self._out.write(struct.pack('>I', aValue))  # '>I' for big-endian 32-bit unsigned int

    @staticmethod
    def setLength( aHeader: int, aLength: int) -> int:
        if aLength < 256:
            return aHeader | L_8BIT
        elif aLength < 65536:
            return aHeader | L_16BIT
        elif aLength < 16777216:
            return aHeader | L_24BIT
        else:
            return aHeader | L_32BIT

    def write16bit(self, aValue: int, aHeader: int|None=None):
        if aHeader is None or (aHeader & MASK_LENGTH) != L_8BIT:
            self._write16bit(aValue)
        else:
            self.write8bit(aValue)

    def write32bit(self, aValue: int, aHeader: int|None=None):
        typ:int = (aHeader & MASK_LENGTH) if aHeader is not None else -1
        if typ == L_8BIT:
            self.write8bit(aValue)
        elif typ == L_16BIT:
            self._write16bit(aValue)
        elif typ == L_24BIT:
            self.write24bit(aValue)
        else:
            self._write32bit(aValue)

    def writeString(self, aValue: str|None) -> int:
        for i,v in enumerate(KEYWORDS):
            if v==aValue:
                return i
        if aValue is None:
            return 0

        zLen = len(aValue)
        if zLen == 0:
            return I_BLANK

        zFirstChar = aValue[0]
        if zFirstChar == '0' and zLen == 1:
            return ~0
        elif '1' <= zFirstChar <= '9':
            num = ord(zFirstChar) - ord('0')
            for char in aValue[1:]:
                if '0' <= char <= '9':
                    num = num * 10 + (ord(char) - ord('0'))
                else:
                    num = -1
                    break
            if 0 <= num < (1 << 31) - 1:
                return ~num

        zIndex = len(self._dictionary) + 1
        if aValue in self._dictionary:
            return self._dictionary[aValue]
        self._dictionary[aValue] = zIndex

        zStringHeader = XmlBinaryOutputStream.setLength(T_WSTR, zLen)
        self.write8bit(zStringHeader)
        self.write32bit(zLen, zStringHeader)
        for char in aValue:
            self.writeChar(ord(char))
        
        return zIndex

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
def _to_binary( node:Elem, bout:XmlBinaryOutputStream, namespace:dict ):
    # タグ名
    if isinstance(node.tag,str):
        if not node.tag.startswith('{'):
            tag_name_id:int = bout.writeString( node.tag )
        else:
            e = node.tag.find('}')
            if e<0:
                raise IOError(f'invalid tagname {node.tag}')
            ns = node.tag[1:e]
            for k,v in node.nsmap.items():
                if ns==v:
                    ns = k
            tag_name_str = f"{ns}:{node.tag[e+1:]}"
            tag_name_id:int = bout.writeString( tag_name_str )
    else:
        tag_name_id:int = I_NONE
    tag_name_bool:bool = tag_name_id != I_NONE and tag_name_id != I_BLANK
    # 属性
    attrib_list:list[int] = []
    if tag_name_bool:
        if node.nsmap != namespace:
            for k,v in node.nsmap.items():
                ns = namespace.get(k)
                if v!=ns:
                    attrib_list.append( bout.writeString( f"xmlns:{k}" ) )
                    attrib_list.append( bout.writeString( v ) )
        for zAttName,zAttValue in node.attrib.items():
            attrib_list.append( bout.writeString( zAttName ) )
            attrib_list.append( bout.writeString( zAttValue ) )
    num_atts:int = len(attrib_list)//2
    # 子ノードの数
    num_childs:int = len(node)
    # テキスト
    if node.text is not None and num_childs>0 and node.text.strip()=='':
        text_id = I_NONE
    else:
        text_id:int = bout.writeString( node.text )
    text_bool:bool = text_id!=I_NONE and text_id!=I_BLANK
    # ノードヘッダ
    node_header:int = 0
    if tag_name_bool:
        if num_childs > 0:
            node_header = T_NODE
        else:
            node_header = T_LEAF
        if num_atts > 0:
            node_header = node_header | F_ATTRIBUTES
    else:
        node_header = T_COMMENT
    if text_bool:
        node_header = node_header | F_TEXT
    max_sz:int = num_atts if num_atts>num_childs else num_childs
    if not isinstance(max_sz,int):
        raise IOError('x')
    node_header = XmlBinaryOutputStream.setLength( node_header, max_sz )

    # ノードヘッダ出力
    bout.write8bit( node_header )
    # タグ名出力
    if tag_name_bool:
        bout.write32bit( tag_name_id )
    # 属性出力
    if num_atts > 0:
        bout.write16bit( num_atts, node_header )
        for aa in attrib_list:
            bout.write32bit( aa )
    # テキスト出力
    if text_bool:
        bout.write32bit( text_id )
    # 子ノード出力
    if num_childs > 0:
        bout.write32bit( num_childs, node_header )
        for child_node in node:
            _to_binary( child_node, bout, node.nsmap )
        bout.write8bit( node_header )

def to_binary( aNode:Elem, out:RawIOBase|BufferedIOBase ):
    with XmlBinaryOutputStream( out ) as bout:
        # write encode
        enc_code:int = 0 # UTF-8
        bout.write8bit( enc_code )
        # write node
        _to_binary( aNode, bout, {} )
