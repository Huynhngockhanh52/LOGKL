"""
This file is modified from:
https://github.com/BlueLionLogram/Logram/tree/master/Evaluation
"""

import hashlib
import regex as re
import pandas as pd
import os
from .Common import regexGenerator


def tripleMatch(tokens, triDictionaryList, triThreshold):
    """
    Kiểm tra xem các bộ ba từ liên tiếp có xuất hiện đủ số lần trong từ điển hay không.

    Args:
        -  `tokens` (list)): Danh sách các từ (tokens) được trích xuất từ log.
        - `triDictionaryList` (dict)): Từ điển chứa các bộ ba từ phổ biến cùng số lần xuất hiện.
        - `triThreshold` (int)): Ngưỡng số lần xuất hiện tối thiểu để bộ ba được coi là hợp lệ.

    Returns:
        list: Danh sách các chỉ mục của những cụm không vượt qua ngưỡng giới hạn cho phép.
    """
    indexList = {}

    for index in range(len(tokens)):
        if index >= len(tokens) - 2:
            break
        tripleTmp = tokens[index] + "^" + tokens[index + 1] + "^" + tokens[index + 2]
        if (
            tripleTmp in triDictionaryList
            and triDictionaryList[tripleTmp] >= triThreshold
        ):
            pass    # Vượt qua ngưỡng --> Không cần xử lý --> Không chứa giá trị biến
        else:
            indexList[index] = 1
            indexList[index + 1] = 1
            indexList[index + 2] = 1
    return list(indexList.keys()) # [0,2,6,8,9, ...]


def doubleMatch(tokens, indexList, doubleDictionaryList, doubleThreshold, length):
    """
    Kiểm tra xem các cặp từ có phổ biến trong từ điển hay không dựa trên ngưỡng số lần xuất hiện và cụm log trong trigram không vượt qua ngưỡng giới hạn cho phép.

    Args:
        - `tokens` (list)): Danh sách từ (tokens) được trích xuất từ log.
        - `indexList` (list)): Danh sách chỉ mục của những từ không khớp với bộ ba phổ biến.
        - `doubleDictionaryList` (dict)): Từ điển chứa các cặp từ phổ biến cùng số lần xuất hiện.
        - `doubleThreshold` (int)): Ngưỡng số lần xuất hiện tối thiểu để cặp từ được coi là hợp lệ.
        - `length` (int)): Độ dài của danh sách token.

    Returns:
        list: Danh sách chỉ mục của những từ không khớp với các cặp phổ biến.
    """
    dynamicIndex = []
    for i in range(len(indexList)):
        index = indexList[i]
        if index == 0:
            doubleTmp = tokens[index] + "^" + tokens[index + 1]
            if (
                doubleTmp in doubleDictionaryList
                and doubleDictionaryList[doubleTmp] > doubleThreshold
            ):
                pass
            else:
                dynamicIndex.append(index)
        elif index == length - 1:
            doubleTmp1 = tokens[index - 1] + "^" + tokens[index]
            doubleTmp2 = tokens[index] + "^" + tokens[0]
            if (
                doubleTmp1 in doubleDictionaryList
                and doubleDictionaryList[doubleTmp1] >= doubleThreshold
            ) or (
                doubleTmp2 in doubleDictionaryList
                and doubleDictionaryList[doubleTmp2] >= doubleThreshold
            ):
                pass
            else:
                dynamicIndex.append(index)
        else:
            doubleTmp1 = tokens[index] + "^" + tokens[index + 1]
            doubleTmp2 = tokens[index - 1] + "^" + tokens[index]
            if (
                doubleTmp1 in doubleDictionaryList
                and doubleDictionaryList[doubleTmp1] >= doubleThreshold
            ) or (
                doubleTmp2 in doubleDictionaryList
                and doubleDictionaryList[doubleTmp2] >= doubleThreshold
            ):
                pass
            else:
                dynamicIndex.append(index) 
    return dynamicIndex # Trả về danh sách các chỉ mục được xem là giá trị của biến (token động): [2, 5, ...]


def tokenMatch(
    allTokensList,
    doubleDictionaryList, triDictionaryList,
    doubleThreshold, triThreshold,
    outdir, log_file_basename,
    allMessageList,
):
    """
    Xử lý danh sách token từ log, tạo template, và lưu kết quả vào file CSV.

    Args:
        - `allTokensList` (list)): Danh sách danh sách token từ log.
        - `doubleDictionaryList` (dict)): Từ điển chứa các cặp từ phổ biến.
        - `triDictionaryList` (dict)): Từ điển chứa các bộ ba từ phổ biến.
        - `doubleThreshold` (int)): Ngưỡng số lần xuất hiện tối thiểu cho cặp từ.
        - `triThreshold` (int)): Ngưỡng số lần xuất hiện tối thiểu cho bộ ba từ.
        - `outdir` (str)): Thư mục đầu ra để lưu file kết quả.
        - `log_file_basename` (str)): Tên file cơ sở của log.
        - `allMessageList` (list)): Danh sách nội dung log gốc.

    Returns:
        None: Kết quả được ghi vào file CSV.
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    template_file = os.path.join(outdir, log_file_basename + "_templates.csv")
    structured_log_file = os.path.join(outdir, log_file_basename + "_structured.csv")

    structured_log_lines = []
    template_lines = []
    assert len(allTokensList) == len(allMessageList)
    for tokens in allTokensList:
        index = allTokensList.index(tokens)
        indexList = tripleMatch(tokens, triDictionaryList, triThreshold)
        dynamicIndex = doubleMatch(
            tokens, indexList, doubleDictionaryList, doubleThreshold, len(tokens)
        )

        logEvent = ""
        for i in range(len(tokens)):
            if i in dynamicIndex:
                tokens[i] = "<*>"
            logEvent = logEvent + tokens[i] + " "

        logEvent = re.sub(",", "", logEvent).strip() # Để viết vào file csv một cách thuận tiện, tránh việc tạo cột mới
        template_id = hashlib.md5(logEvent.encode("utf-8")).hexdigest()[0:8]

        if not (template_id, logEvent) in template_lines:
            template_lines.append((template_id, logEvent))

        structured_log_lines.append(
            (index + 1, allMessageList[index], template_id, logEvent)
        )

    template_df = pd.DataFrame(template_lines, columns=["EventId", "EventTemplate"])
    template_df.to_csv(template_file, index=False)
    structured_log_df = pd.DataFrame(
        structured_log_lines, columns=["LineId", "Content", "EventId", "EventTemplate"]
    )
    structured_log_df.to_csv(structured_log_file, index=False)
