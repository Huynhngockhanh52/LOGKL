"""
This file is modified from:
https://github.com/BlueLionLogram/Logram/tree/master/Evaluation

File này chứa các phương thức thực hiện trích xuất thông tin từ dòng log và tách từ dựa trên regex được đưa vào, nếu không sử dụng, mặc định là MyRegex.
"""

import regex as re

# Biểu thức chính quy mặc định, sử dụng để loại bỏ các biến động trong log
MyRegex = [
    r"blk_(|-)[0-9]+",                                          # block id
    r"(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)",                   # IP
    r"(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$",    # Numbers
]

def preprocess(logLine, specialRegex):
    """
    Thay thế các chuỗi khớp với danh sách regex đặc biệt bằng ký tự "<*>" trong dòng log.

    Args:
        - `logLine` (str): Dòng log đầu vào cần xử lý.
        - `specialRegex` (list): Danh sách các biểu thức chính quy cần thay thế.

    Returns:
        str: Dòng log sau khi đã thay thế các mẫu đặc biệt.
    """
    line = logLine
    for regex in specialRegex:
        line = re.sub(regex, "<*>", " " + logLine) # Dấu " " để phân tách với câu phía trước, vì bản chất của Logram là gộp tất cả log thành một chuỗi dài.
    return line 

def tokenSpliter(logLine, regex, specialRegex):
    """
    Trích xuất nội dung message từ dòng log và tách từ dựa trên regex. Phương thức này thực hiện trích xuất log theo từng cột dựa trên các nội dung tiêu đề từng cột được xác định trước.

    Args:
        - `logLine` (str)): Dòng log đầu vào cần xử lý.
        - `regex` (re.Pattern)): Biểu thức chính quy để trích xuất nội dung log.
        - `specialRegex` (list)): Danh sách các biểu thức chính quy đặc biệt để tiền xử lý nội dung.

    Returns:
        tuple: (tokens, message)
            - tokens (list): Danh sách các từ được tách ra từ nội dung log sau khi tiền xử lý.
            - message (str): Nội dung log gốc trích xuất được từ dòng log.
    """
    match = regex.search(logLine.strip())
    # print(match)
    if match == None:
        # tokens = None
        # message = None # Thêm vào nếu không, có thể sẽ bị lỗi
        # pass
        return None, None # Viết mới để tránh lỗi
    else: 
        message = match.group("Content")
        # print(message)
        line = preprocess(message, specialRegex)
        tokens = line.strip().split()
    # print(tokens)
    return tokens, message
    # Ex: message: "Failed login attempt from 192.168.1.1"
    # Ex: tokens: ['Failed', 'login', 'attempt', 'from', '<*>']
    

def regexGenerator(logformat):
    """
    Tạo regex từ mẫu định dạng log để trích xuất thông tin. Phương thức này thực hiện tạo các biểu thức chính quy nhằm trích xuất thông tin từ message log.

    Args:
        - `logformat` (str)): Chuỗi định dạng log chứa các trường (tiêu đề) cần trích xuất.

    Returns:
        tuple: (regex, headers)
            - regex (re.Pattern): Biểu thức chính quy được biên dịch từ mẫu log.
            - headers (list): Danh sách tên các trường trích xuất được từ log.
    """
    headers = []
    splitters = re.split(r"(<[^<>]+>)", logformat)
    regex = ""
    for k in range(len(splitters)):
        if k % 2 == 0:
            splitter = re.sub(" +", "\\\s+", splitters[k])
            regex += splitter
        else:
            header = splitters[k].strip("<").strip(">")
            regex += "(?P<%s>.*?)" % header
            headers.append(header)
    regex = re.compile("^" + regex + "$")
    return regex # ex: ^(?P<Date>.*?)\s+-\s+(?P<Level>.*?)\s+:\s+(?P<Message>.*?)$
