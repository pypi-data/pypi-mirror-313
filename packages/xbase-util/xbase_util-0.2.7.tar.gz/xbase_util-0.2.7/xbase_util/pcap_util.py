import math
import os
import struct
import time
import zlib
from datetime import datetime

from Crypto.Cipher import AES
from zstandard import ZstdDecompressor


def fix_pos(pos, packetPosEncoding):
    if pos is None or len(pos) == 0:
        return
    if packetPosEncoding == "gap0":
        last = 0
        lastgap = 0
        for i, pos_item in enumerate(pos):
            if pos[i] < 0:
                last = 0
            else:
                if pos[i] == 0:
                    pos[i] = last + lastgap
                else:
                    lastgap = pos[i]
                    pos[i] += last
                last = pos[i]


def group_numbers(nums):
    result = []
    for num in nums:
        if num < 0:
            result.append([num])
        elif result:
            result[-1].append(num)
    return result


def decompress_streaming(compressed_data, id, fro):
    try:
        decompressor = ZstdDecompressor()
        with decompressor.stream_reader(compressed_data) as reader:
            decompressed_data = reader.read()
            return decompressed_data
    except Exception as e:
        print(f"解码错误：{e}  {id}")
        return bytearray()


def read_header(param_map, id):
    shortHeader = None
    headBuffer = os.read(param_map['fd'], 64)
    if param_map['encoding'] == 'aes-256-ctr':
        if 'iv' in param_map:
            param_map['iv'][12:16] = struct.pack('>I', 0)
            headBuffer = bytearray(
                AES.new(param_map['encKey'], AES.MODE_CTR, nonce=param_map['iv']).decrypt(bytes(headBuffer)))
        else:
            print("读取头部信息失败，iv向量为空")
    elif param_map['encoding'] == 'xor-2048':
        for i in range(len(headBuffer)):
            headBuffer[i] ^= param_map['encKey'][i % 256]
    if param_map['uncompressedBits']:
        if param_map['compression'] == 'gzip':
            headBuffer = zlib.decompress(bytes(headBuffer), zlib.MAX_WBITS | 16)
        elif param_map['compression'] == 'zstd':
            headBuffer = decompress_streaming(headBuffer, id, "header")
    headBuffer = headBuffer[:24]
    magic = struct.unpack('<I', headBuffer[:4])[0]
    bigEndian = (magic == 0xd4c3b2a1 or magic == 0x4d3cb2a1)
    # nanosecond = (magic == 0xa1b23c4d or magic == 0x4d3cb2a1)
    if not bigEndian and magic not in {0xa1b2c3d4, 0xa1b23c4d, 0xa1b2c3d5}:
        corrupt = True
        # os.close(param_map['fd'])
        raise ValueError("Corrupt PCAP header")
    if magic == 0xa1b2c3d5:
        shortHeader = struct.unpack('<I', headBuffer[8:12])[0]
        headBuffer[0] = 0xd4  # Reset header to normal
    linkType = struct.unpack('>I' if bigEndian else '<I', headBuffer[20:24])[0]
    return headBuffer, shortHeader, bigEndian


def create_decipher(pos, param_map):
    param_map['iv'][12:16] = struct.pack('>I', pos)
    return AES.new(param_map['encKey'], AES.MODE_CTR, nonce=param_map['iv'])


def read_packet_internal(pos_arg, hp_len_arg, param_map, id):
    pos = pos_arg
    hp_len = hp_len_arg
    if hp_len == -1:
        if param_map['compression'] == "zstd":
            hp_len = param_map['uncompressedBitsSize']
        else:
            hp_len = 2048
    inside_offset = 0
    if param_map['uncompressedBits']:
        inside_offset = pos & param_map['uncompressedBitsSize'] - 1
        pos = math.floor(pos / param_map['uncompressedBitsSize'])
    pos_offset = 0
    if param_map['encoding'] == 'aes-256-ctr':
        pos_offset = pos % 16
        pos = pos - pos_offset
    elif param_map['encoding'] == 'xor-2048':
        pos_offset = pos % 256
        pos = pos - pos_offset

    hp_len = 256 * math.ceil((hp_len + inside_offset + pos_offset) / 256)
    buffer = bytearray(hp_len)
    os.lseek(param_map['fd'], pos, os.SEEK_SET)
    read_buffer = os.read(param_map['fd'], len(buffer))
    if len(read_buffer) - pos_offset < 16:
        return None
    if param_map['encoding'] == 'aes-256-ctr':
        decipher = create_decipher(pos // 16, param_map)
        read_buffer = bytearray(decipher.decrypt(read_buffer))[pos_offset:]
    elif param_map['encoding'] == 'xor-2048':
        read_buffer = bytearray(b ^ param_map['encKey'][i % 256] for i, b in enumerate(read_buffer))[pos_offset:]
    if param_map['uncompressedBits']:
        try:
            if param_map['compression'] == 'gzip':
                read_buffer = zlib.decompress(read_buffer, zlib.MAX_WBITS | 16)
            elif param_map['compression'] == 'zstd':
                read_buffer = decompress_streaming(read_buffer, id, "packet")
        except Exception as e:
            print(f"PCAP uncompress issue:  {pos} {len(buffer)} {read_buffer} {e}")
            return None
    if inside_offset:
        read_buffer = read_buffer[inside_offset:]
    header_len = 16 if param_map['shortHeader'] is None else 6
    if len(read_buffer) < header_len:
        if hp_len_arg == -1 and param_map['compression'] == 'zstd':
            return read_packet_internal(pos_arg, param_map['uncompressedBitsSize'] * 2, param_map, id)
        print(f"Not enough data {len(read_buffer)} for header {header_len}")
        return None
    packet_len = struct.unpack('>I' if param_map['bigEndian'] else '<I', read_buffer[8:12])[
        0] if param_map['shortHeader'] is None else \
        struct.unpack('>H' if param_map['bigEndian'] else '<H', read_buffer[:2])[0]
    if packet_len < 0 or packet_len > 0xffff:
        return None
    if header_len + packet_len <= len(read_buffer):
        if param_map['shortHeader'] is not None:
            t = struct.unpack('<I', read_buffer[2:6])[0]
            sec = (t >> 20) + param_map['shortHeader']
            usec = t & 0xfffff
            new_buffer = bytearray(16 + packet_len)
            struct.pack_into('<I', new_buffer, 0, sec)
            struct.pack_into('<I', new_buffer, 4, usec)
            struct.pack_into('<I', new_buffer, 8, packet_len)
            struct.pack_into('<I', new_buffer, 12, packet_len)
            new_buffer[16:] = read_buffer[6:packet_len + 6]
            return new_buffer
        return read_buffer[:header_len + packet_len]

    if hp_len_arg != -1:
        return None

    return read_packet_internal(pos_arg, 16 + packet_len, param_map, id)


def read_packet(pos, param_map, id):
    if 'fd' not in param_map or not param_map['fd']:
        time.sleep(0.01)
        return read_packet(pos, param_map['fd'], id)
    return read_packet_internal(pos, -1, param_map, id)


def get_file_and_read_pos(id, file, pos_list):
    filename = file['name']
    if not os.path.isfile(filename):
        print(f"文件不存在:{filename}")
        return None
    encoding = file.get('encoding', 'normal')
    encKey = None
    iv = None
    compression = None
    if 'dek' in file:
        dek = bytes.fromhex(file['dek'])
        encKey = AES.new(file['kek'].encode(), AES.MODE_CBC).decrypt(dek)

    if 'uncompressedBits' in file:
        uncompressedBits = file['uncompressedBits']
        uncompressedBitsSize = 2 ** uncompressedBits
        compression = 'gzip'
    else:
        uncompressedBits = None
        uncompressedBitsSize = 0
    if 'compression' in file:
        compression = file['compression']

    if 'iv' in file:
        iv_ = bytes.fromhex(file['iv'])
        iv = bytearray(16)
        iv[:len(iv_)] = iv_
    fd = os.open(filename, os.O_RDONLY)
    param_map = {
        "fd": fd,
        "encoding": encoding,
        "iv": iv,
        "encKey": encKey,
        "uncompressedBits": uncompressedBits,
        "compression": compression,
        "uncompressedBitsSize": uncompressedBitsSize
    }
    res = bytearray()
    headBuffer, shortHeader, bigEndian = read_header(param_map, id)
    res.extend(headBuffer)
    param_map['shortHeader'] = shortHeader
    param_map['bigEndian'] = bigEndian
    # _________________________________
    byte_array = bytearray(0xfffe)
    next_packet = 0
    b_offset = 0
    packets = {}
    i = 0
    for pos in pos_list:
        packet_bytes = read_packet(pos, param_map, id)
        if not packet_bytes:
            continue
        packets[i] = packet_bytes
        while next_packet in packets:
            buffer = packets[next_packet]
            del packets[next_packet]
            next_packet = next_packet + 1
            if b_offset + len(buffer) > len(byte_array):
                res.extend(byte_array[:b_offset])
                b_offset = 0
                byte_array = bytearray(0xfffe)
            byte_array[b_offset:b_offset + len(buffer)] = buffer
            b_offset += len(buffer)
        i = i + 1
    os.close(fd)
    res.extend(byte_array[:b_offset])
    return res


def process_session_id_disk_simple(id, node, packet_pos, esdb, pcap_path_prefix):
    packetPos = packet_pos
    file = esdb.get_file_by_file_id(node=node, num=abs(packetPos[0]),
                                    prefix=None if pcap_path_prefix == "origin" else pcap_path_prefix)
    if file is None:
        return None
    fix_pos(packetPos, file['packetPosEncoding'])
    pos_list = group_numbers(packetPos)[0]
    pos_list.pop(0)
    return get_file_and_read_pos(id, file, pos_list)
