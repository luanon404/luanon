"""
    Tác giả: GnU
    Ngày tạo: 11/06/2023
    ©2023 LuaNonTeam
"""

import math

from typing import Callable
from dataclasses import dataclass


@dataclass
class DataObject:
    __slots__ = ["val", "position", "index"]
    val: int
    position: int
    index: int


class CfLzString:

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key
        self.table_char = {
            char: index
            for index, char in enumerate(self.secret_key)
        }

    def text_to_base64(self, text: str) -> str:
        result = ""
        if text:
            result = self._compress(text, 6, lambda char: self.secret_key[char])
        return result

    def base64_to_text(self, base64: str) -> str:
        result = ""
        if base64:
            if "%2b" in base64:
                # Cloudflare encode first + to %2b
                base64 = base64.replace("%2b", "+", 1)
            result = self._decompress(base64, 32, lambda index: self.table_char[base64[index]])
        return result

    @staticmethod
    def _compress(text: str, bits_per_char: int, int2char: Callable[[int], str]) -> str:
        context_dictionary = {}
        context_dictionary_to_create = {}
        context_w = ""
        context_enlarge_in = 2
        context_dict_size = 3
        context_num_bits = 2
        context_data = []
        context_data_val = 0
        context_data_position = 0

        for context_c in text:
            if context_c not in context_dictionary:
                context_dictionary[context_c] = context_dict_size
                context_dict_size += 1
                context_dictionary_to_create[context_c] = True
            context_wc = context_w + context_c
            if context_wc in context_dictionary:
                context_w = context_wc
            else:
                if context_w in context_dictionary_to_create:
                    if ord(context_w[0]) < 256:
                        for i in range(context_num_bits):
                            context_data_val = (context_data_val << 1)
                            if context_data_position == bits_per_char - 1:
                                context_data_position = 0
                                context_data.append(int2char(context_data_val))
                                context_data_val = 0
                            else:
                                context_data_position += 1
                        value = ord(context_w[0])
                        for i in range(8):
                            context_data_val = (context_data_val << 1) | (value & 1)
                            if context_data_position == bits_per_char - 1:
                                context_data_position = 0
                                context_data.append(int2char(context_data_val))
                                context_data_val = 0
                            else:
                                context_data_position += 1
                            value = value >> 1
                    else:
                        value = 1
                        for i in range(context_num_bits):
                            context_data_val = (context_data_val << 1) | value
                            if context_data_position == bits_per_char - 1:
                                context_data_position = 0
                                context_data.append(int2char(context_data_val))
                                context_data_val = 0
                            else:
                                context_data_position += 1
                            value = 0
                        value = ord(context_w[0])
                        for i in range(16):
                            context_data_val = (context_data_val << 1) | (value & 1)
                            if context_data_position == bits_per_char - 1:
                                context_data_position = 0
                                context_data.append(int2char(context_data_val))
                                context_data_val = 0
                            else:
                                context_data_position += 1
                            value = value >> 1
                    context_enlarge_in -= 1
                    if context_enlarge_in == 0:
                        context_enlarge_in = math.pow(2, context_num_bits)
                        context_num_bits += 1
                    del context_dictionary_to_create[context_w]
                else:
                    value = context_dictionary[context_w]
                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(int2char(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = value >> 1
                context_enlarge_in -= 1
                if context_enlarge_in == 0:
                    context_enlarge_in = math.pow(2, context_num_bits)
                    context_num_bits += 1
                context_dictionary[context_wc] = context_dict_size
                context_dict_size += 1
                context_w = str(context_c)
        if context_w != "":
            if context_w in context_dictionary_to_create:
                if ord(context_w[0]) < 256:
                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(int2char(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                    value = ord(context_w[0])
                    for i in range(8):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(int2char(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = value >> 1
                else:
                    value = 1
                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | value
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(int2char(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = 0
                    value = ord(context_w[0])
                    for i in range(16):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(int2char(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = value >> 1
                context_enlarge_in -= 1
                if context_enlarge_in == 0:
                    context_enlarge_in = math.pow(2, context_num_bits)
                    context_num_bits += 1
                del context_dictionary_to_create[context_w]
            else:
                value = context_dictionary[context_w]
                for i in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(int2char(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = value >> 1
        context_enlarge_in -= 1
        if context_enlarge_in == 0:
            context_num_bits += 1
        value = 2
        for i in range(context_num_bits):
            context_data_val = (context_data_val << 1) | (value & 1)
            if context_data_position == bits_per_char - 1:
                context_data_position = 0
                context_data.append(int2char(context_data_val))
                context_data_val = 0
            else:
                context_data_position += 1
            value = value >> 1
        while True:
            context_data_val = (context_data_val << 1)
            if context_data_position == bits_per_char - 1:
                context_data.append(int2char(context_data_val))
                break
            else:
                context_data_position += 1
        return "".join(context_data)

    @staticmethod
    def _decompress(base64: str, reset_value: int, int2int: Callable[[int], int]) -> str:
        dictionary = {}
        enlarge_in = 4
        dict_size = 4
        num_bits = 3
        result = []

        data = DataObject(
            val=int2int(0),
            position=reset_value,
            index=1
        )

        for idx in range(3):
            dictionary[idx] = idx

        bits = 0
        max_power = math.pow(2, 2)
        power = 1

        while power != max_power:
            resb = data.val & data.position
            data.position >>= 1
            if data.position == 0:
                data.position = reset_value
                data.val = int2int(data.index)
                data.index += 1

            bits |= power if resb > 0 else 0
            power <<= 1

        match bits:
            case 0:
                bits = 0
                max_power = math.pow(2, 8)
                power = 1
                while power != max_power:
                    resb = data.val & data.position
                    data.position >>= 1
                    if data.position == 0:
                        data.position = reset_value
                        data.val = int2int(data.index)
                        data.index += 1
                    bits |= power if resb > 0 else 0
                    power <<= 1
                char = chr(bits)
            case 1:
                bits = 0
                max_power = math.pow(2, 16)
                power = 1
                while power != max_power:
                    resb = data.val & data.position
                    data.position >>= 1
                    if data.position == 0:
                        data.position = reset_value
                        data.val = int2int(data.index)
                        data.index += 1
                    bits |= power if resb > 0 else 0
                    power <<= 1
                char = chr(bits)
            case 2:
                return ""
            case _:
                char = ""

        dictionary[3] = char
        w = char
        result.append(char)
        counter = 0
        while True:
            counter += 1
            if data.index > len(base64):
                return ""

            bits = 0
            max_power = math.pow(2, num_bits)
            power = 1
            while power != max_power:
                resb = data.val & data.position
                data.position >>= 1
                if data.position == 0:
                    data.position = reset_value
                    data.val = int2int(data.index)
                    data.index += 1
                bits |= power if resb > 0 else 0
                power <<= 1

            char = bits
            if char == 0:
                bits = 0
                max_power = math.pow(2, 8)
                power = 1
                while power != max_power:
                    resb = data.val & data.position
                    data.position >>= 1
                    if data.position == 0:
                        data.position = reset_value
                        data.val = int2int(data.index)
                        data.index += 1
                    bits |= power if resb > 0 else 0
                    power <<= 1

                dictionary[dict_size] = chr(bits)
                dict_size += 1
                char = dict_size - 1
                enlarge_in -= 1
            elif char == 1:
                bits = 0
                max_power = math.pow(2, 16)
                power = 1
                while power != max_power:
                    resb = data.val & data.position
                    data.position >>= 1
                    if data.position == 0:
                        data.position = reset_value
                        data.val = int2int(data.index)
                        data.index += 1
                    bits |= power if resb > 0 else 0
                    power <<= 1
                dictionary[dict_size] = chr(bits)
                dict_size += 1
                char = dict_size - 1
                enlarge_in -= 1
            elif char == 2:
                return "".join(result)

            if enlarge_in == 0:
                enlarge_in = math.pow(2, num_bits)
                num_bits += 1

            if char in dictionary:
                entry = dictionary.get(char)
            else:
                if char == dict_size:
                    entry = w + w[0]
                else:
                    return "".join(result)
            result.append(entry)

            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            enlarge_in -= 1

            w = entry
            if enlarge_in == 0:
                enlarge_in = math.pow(2, num_bits)
                num_bits += 1
