#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   analyse_utils.py
# @Time    :   2023/1/17 14:30
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :

# here put the import lib
import struct
from functools import reduce
from Crypto.Util.Padding import unpad
from Crypto.Cipher import DES, AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
import ctypes
import hashlib
import zlib
import gzip
import random
import base64
import binascii


class DataView(object):
    def __init__(self, array, bytes_per_element=1):
        """
        bytes_per_element is the size of each element in bytes.
        By default we are assume the array is one byte per element.
        """
        self.array = array
        self.bytes_per_element = 1

    def __get_binary(self, start_index, byte_count, signed=False):
        integers = [self.array[start_index + x] for x in range(byte_count)]
        bytes = [integer.to_bytes(
            self.bytes_per_element, byteorder='little', signed=signed) for integer in integers]
        return reduce(lambda a, b: a + b, bytes)

    def get_uint_16(self, start_index):
        bytes_to_read = 2
        return int.from_bytes(self.__get_binary(start_index, bytes_to_read), byteorder='little')

    def get_uint_8(self, start_index):
        bytes_to_read = 1
        return int.from_bytes(self.__get_binary(start_index, bytes_to_read), byteorder='little')

    def get_float_32(self, start_index):
        bytes_to_read = 4
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<f', binary)[0]  # <f for little endian


def set_unit_32(num):
    if not isinstance(num, int):
        num = int(num)
        print(num)
    e = [0, 0, 0, 0]
    if num < pow(256, 4) and num // pow(256, 3) > 0:
        e[3] = num // pow(256, 3)
        e[2] = num % pow(256, 3) // pow(256, 2)
        e[1] = (num % pow(256, 3) % pow(256, 2)) // 256
        e[0] = num % pow(256, 3) % pow(256, 2) % 256
    elif num // pow(256, 2) > 0:
        e[2] = num // pow(256, 2)
        e[1] = num % pow(256, 2) // 256
        e[0] = num % pow(256, 2) % 256
    elif num // 256 > 0:
        e[1] = num // 256
        e[0] = num % 256
    else:
        e[0] = num
    return e


def hex_to_bytes(hex_str):
    """

    :param hex_str:
    :return:
    """
    return bytes.fromhex(hex_str)


def bytes_to_hex(byte):
    """

    :param byte:
    :return:
    """
    return byte.hex()


def str_to_hex(string):
    """_summary_

    Args:
        string (_type_): _description_
    """
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')


def hex_to_str(hex_str):
    """_summary_

    Args:
        hex_str (_type_): _description_
    """
    str_bin = binascii.unhexlify(hex_str.encode('utf-8'))
    return str_bin.decode('utf-8')


def array_to_bytes(array):
    """
    [268, 128]
    :param array:
    :return:
    """
    return bytes([x & 0xFF for x in array])


def btoa(string, output_str=True):
    """
    base64 encode
    :param string:
    :param output_str:
    :return:
    """
    if isinstance(string, str):
        string = string.encode('utf-8')
    result = base64.b64encode(string)
    if output_str:
        return result.decode('utf-8')
    return result


def atob(string, output_str=True):
    """
    base64 decode
    :param string:
    :param output_str:
    :return:
    """
    result = base64.b64decode(string)
    if output_str:
        return result.decode('utf-8')
    return result


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shift(n, i):
    """
    js >>>
    :param n:
    :param i:
    :return:
    """
    # 如果js右移为0, 且数字小于0
    if i == 0 and n < 0:
        return n + 2 ** 32
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def char_code_at(string, index):
    """
    string.charCodeAt(index) >>> ord(string[index])
    :param string:
    :param index:
    :return:
    """
    return ord(string[index])


def get_nonce(num, string_table='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    nonce 返回随机字符串
    :param num:
    :param string_table:
    :return:
    """
    return ''.join(random.sample(string_table, num))


def get_md5(obj, output_hex=True):
    """
    获取 md5 的值
    :param obj:
    :param output_hex:
    :return:
    """
    if isinstance(obj, str):
        obj = obj.encode()
    m = hashlib.new('md5')
    m.update(obj)
    if output_hex:
        return m.digest().hex().lower()
    return m.digest()


def get_sha1(obj, output_hex=True):
    """
    获取 sha1 的值
    :param obj:
    :param output_hex:
    :return:
    """
    if isinstance(obj, str):
        obj = obj.encode()
    m = hashlib.new('sha1')
    m.update(obj)
    if output_hex:
        return m.digest().hex().lower()
    return m.digest()


def gzip_compress(obj, output_base64=True):
    """
    bytes ==> string
    :param obj:
    :param output_base64: 是否要转成base64 变成字符串形式输出
    :return:
    """
    if isinstance(obj, str):
        obj = obj.encode()
    result = gzip.compress(obj)
    if output_base64:
        return btoa(result)
    return result


def gzip_decompress(obj: bytes, output_str=True):
    """
    bytes ==> string
    :param obj:
    :param output_str:
    :return:
    """

    result = gzip.decompress(obj)
    if output_str:
        return result.decode()
    return result


def rsa_encrypt(public_key, data, output_base64=True):
    """
    rsa 加密
    :param public_key:
    :param data:
    :param output_base64:
    :return:
    """
    if isinstance(data, str):
        data = bytes(data, encoding="utf8")
    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsakey)
    result = cipher.encrypt(data)
    if output_base64:
        return btoa(result)
    return result


def rsa_decrypt(private_key, data, output_str=True, max_length=128):
    """
    rsa 加密
    :param private_key:
    :param data:
    :param output_str:
    :param max_length: 分组长度
    :return:
    """
    data = atob(data, output_str=False)
    rsakey = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(rsakey)
    clip_num = data.__len__() // max_length + 1
    result = b""
    for n in range(clip_num):
        if len(data[n * max_length:(n + 1) * max_length]):
            tmp = cipher.decrypt(
                data[n * max_length:(n + 1) * max_length], b"xyz")
            result += tmp
    if output_str:
        return result.decode('utf-8', 'ignore')
    return result


class CipherUtil(object):

    def __init__(self, key, mode, iv, padding, block_size, encrypt_func='DES'):
        self.block_size = block_size
        self.key = key.encode('utf-8') if isinstance(key,
                                                     str) else key  # 初始化密钥
        if encrypt_func == 'DES':
            if mode == 'ecb':
                self.mode = DES.MODE_ECB
                self.cipher = DES.new(self.key, mode=self.mode)
            else:
                self.mode = DES.MODE_CBC
                self.iv = iv.encode('utf-8') if isinstance(iv, str) else iv
                self.cipher = DES.new(self.key, mode=self.mode, iv=self.iv)
        else:
            if mode == 'ecb':
                self.mode = AES.MODE_ECB
                self.cipher = AES.new(self.key, mode=self.mode)
            else:
                self.mode = AES.MODE_CBC
                self.iv = iv.encode('utf-8') if isinstance(iv, str) else iv
                self.cipher = AES.new(self.key, mode=self.mode, iv=self.iv)
        self.padding = padding

    def no_padding(self, text):
        """

        :param text:
        :return:
        """
        count = len(text)
        add = self.block_size - (count % self.block_size)
        entext = text + b'\0' * add
        return entext

    def PKCS7Padding(self, text):
        """

        :param text:
        :return:
        """
        pl = self.block_size - (len(text) % self.block_size)
        return text + bytearray([pl for i in range(pl)])

    @staticmethod
    def PKCS5Padding(text):
        """

        :param text:
        :return:
        """
        pl = 8 - (len(text) % 8)
        return text + bytearray([pl for i in range(pl)])

    def _padding(self, text):
        """
        根据padding 模式进行加密
        :param text:
        :return:
        """
        if self.padding in ('no', 'zero'):
            return self.no_padding(text)
        if self.padding == 'pkcs7':
            return self.PKCS7Padding(text)
        if self.padding == 'pkcs5':
            return self.PKCS5Padding(text)

    def _unpad(self, text):
        """
        去除多余补的数据
        :param text:
        :return:
        """
        if self.padding in ('NoPadding', 'Zero padding'):
            pad = '\0' if isinstance(text, str) else b'\0'
            return text.strip(pad)
        return unpad(text, self.block_size, style='pkcs7')

    @staticmethod
    def add_to_16(text):
        pad = '\0' if isinstance(text, str) else b'\0'
        while len(text) % AES.block_size != 0:
            text += pad
        return text

    def encrypt(self, text, output_base64=True):
        """

        :param text:
        :param output_base64:
        :return:
        """
        if isinstance(text, str):
            text = text.encode("utf8")
        text_pad = self._padding(text)
        res = self.cipher.encrypt(text_pad)
        if output_base64:
            return btoa(res)
        return res

    def decrypt(self, text):
        """

        :param text:
        :return:
        """
        if isinstance(text, str):
            text = text.encode("utf-8")
        result = self.cipher.decrypt(text)
        return self._unpad(result)


class DESUtil(CipherUtil):

    def __init__(self, key, mode='ecb', iv=None, padding='no'):
        super(DESUtil, self).__init__(key, mode, iv,
                                      padding, DES.block_size, encrypt_func='DES')


class AESUtil(CipherUtil):

    def __init__(self, key, mode='ecb', iv=None, padding='no', key_length=16):
        if padding == 'pkcs5':
            padding = 'pkcs7'
        _key_length = len(key)
        if _key_length < 16:
            key = self.add_to_16(key)
        if key_length not in (16, 24, 32):
            raise Exception('Incorrect AES key length')
        key = key[:key_length]
        super(AESUtil, self).__init__(key, mode, iv,
                                      padding, AES.block_size, encrypt_func='AES')


def crc32_checksum(data):
    crc = zlib.crc32(data.encode())
    if crc < 0:
        return unsigned_right_shift(crc, 0)
    return crc
