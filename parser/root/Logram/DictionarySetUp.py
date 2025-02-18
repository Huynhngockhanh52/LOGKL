"""
This file is modified from:
https://github.com/BlueLionLogram/Logram/tree/master/Evaluation

File này thực hiện xây dựng hai từ điển (bigram và trigram) từ các token được trích xuất từ log file. Ngoài ra, file này trả về hai danh sách chứa các token và message của từng dòng log.
"""

from .Common import regexGenerator
from .Common import tokenSpliter


def dictionaryBuilder(log_format, logFile, rex):
    """
    Xây dựng hai từ điển (bigram và trigram) từ các token được trích xuất từ log file.

    Args:
        - `log_format` (str)): Định dạng của log để tạo regex phù hợp.
        - `logFile` (str)): Đường dẫn đến log file cần phân tích.
        - `rex` (list)): Danh sách các regex bổ sung để xử lý log.

    Returns:
        tuple: 
            - `doubleDictionaryList` (dict)): Từ điển chứa cặp token (bigram) và số lần xuất hiện.
            - `triDictionaryList` (dict)): Từ điển chứa bộ ba token (trigram) và số lần xuất hiện.
            - `allTokenList` (list)): Danh sách chứa danh sách các token của từng dòng log.
            - `allMessageList` (list)): Danh sách chứa phần còn lại của từng dòng log sau khi tách token.
    """
    doubleDictionaryList = {"dictionary^DHT": -1}
    triDictionaryList = {"dictionary^DHT^triple": -1}
    allTokenList = []
    allMessageList = []

    regex = regexGenerator(log_format)

    for line in open(logFile, "r"):
        tokens, message = tokenSpliter(line, regex, rex)
        allMessageList.append(message)
        if tokens == None:
            pass
        else:
            allTokenList.append(tokens)
            
            # Như vậy, trigram không cộng thêm các cuối cùng log hiện tại và đầu tiên của dòng log tiếp theo
            for index in range(len(tokens)):
                if index >= len(tokens) - 2:
                    break
                tripleTmp = (
                    tokens[index] + "^" + tokens[index + 1] + "^" + tokens[index + 2]
                )
                if tripleTmp in triDictionaryList:
                    triDictionaryList[tripleTmp] = triDictionaryList[tripleTmp] + 1
                else:
                    triDictionaryList[tripleTmp] = 1
                    
            # Như vậy, bigram cộng thêm cặp cuối cùng và đầu tiên của dòng log, không như mô tả trong bài báo là cặp cuối cùng của log hiện tại và đầu tiên của dòng log tiếp theo
            for index in range(len(tokens)):
                if index == len(tokens) - 1:
                    doubleTmp = tokens[index] + "^" + tokens[0] # Dòng này
                    if doubleTmp in doubleDictionaryList:
                        doubleDictionaryList[doubleTmp] = (
                            doubleDictionaryList[doubleTmp] + 1
                        )
                    else:
                        doubleDictionaryList[doubleTmp] = 1
                    break
                doubleTmp = tokens[index] + "^" + tokens[index + 1]
                if doubleTmp in doubleDictionaryList:
                    doubleDictionaryList[doubleTmp] = (
                        doubleDictionaryList[doubleTmp] + 1
                    )
                else:
                    doubleDictionaryList[doubleTmp] = 1

    return doubleDictionaryList, triDictionaryList, allTokenList, allMessageList
