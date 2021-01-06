import socket
import re
import numpy as np

PORT = 5002


def read_register(host, start_digit, digit_num=1, port=PORT, dic=True):
    '''
        最终用了ASCII码的方式
    '''
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect((host, port))
    str1 = "500000FF03FF000018000004010000D*" + '{:0=6d}'.format(start_digit) + "0001"
    msg = np.fromstring(str1, dtype=np.uint8)
    client.send(msg)
    res = client.recv(1024)
    if dic:
        return int(res[22:26], 16)  # 这几位是结果
    else:
        return int(reverse_per_two_char(res[-4 * digit_num:]), 16)


if __name__ == "__main__":
    host = '192.168.1.100'
    start_digit = 400

    # a = is_open(host)
    a = read_register(host, start_digit)  # 读某个寄存器中的内容
    print(a)
