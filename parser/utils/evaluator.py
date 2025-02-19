# =========================================================================
# Copyright (C) 2016-2023 LOGPAI (https://github.com/logpai).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

import pandas as pd
from scipy.special import comb


def evaluate(groundtruth, parsedresult):
    """
    Đánh giá độ chính xác Accuracy và F1-score của thuật toán phân tích log bằng cách so sánh dữ liệu ground truth với kết quả đã phân tích.

    Args:
        groundtruth (str): Đường dẫn tới file ground truth (dữ liệu đúng).
        parsedresult (str): Đường dẫn tới file kết quả đã phân tích.

    Returns:
        tuple: (f_measure, accuracy)
            - f_measure (float): Chỉ số F1-score (đánh giá độ chính xác tổng hợp).
            - accuracy (float): Độ chính xác của việc gán nhãn log.
    """
    df_groundtruth = pd.read_csv(groundtruth)       # File chính xác
    df_parsedlog = pd.read_csv(parsedresult)        # File kết quả phân tích
    
    # Remove invalid groundtruth event Ids
    non_empty_log_ids = df_groundtruth[~df_groundtruth["EventId"].isnull()].index # Lấy index của các dòng không rỗng EventId
    df_groundtruth = df_groundtruth.loc[non_empty_log_ids]  # Lấy các dòng log không rỗng tương ứng trong file chính xác
    df_parsedlog = df_parsedlog.loc[non_empty_log_ids]      # Tương tự
    
    (precision, recall, f_measure, accuracy) = get_accuracy(
        df_groundtruth["EventId"], df_parsedlog["EventId"]
    )
    print(
        "Precision: {:.4f}, Recall: {:.4f}, F1_measure: {:.4f}, Parsing_Accuracy: {:.4f}".format(
            precision, recall, f_measure, accuracy
        )
    )
    return f_measure, accuracy


def get_accuracy(series_groundtruth: pd.Series, series_parsedlog:pd.Series, debug=False) -> tuple:
    """
    Tính toán các chỉ số đánh giá của thuật toán phân tích log.
    `Chú ý`: Giá trị tính toán được xác định là số cặp có trong nhóm log được phân cụm (vì EventID có thể khác nhau giữa file truth và file parse, do đó, cần tính một chỉ số khác).
    Chỉ số được sử dụng không phải tính độ chính xác theo mẫu mà sẽ tính theo số cặp trong nhóm đó.

    Giả sử với n mẫu trong nhóm A, đoán đúng k mẫu, sai (n-k) mẫu.Như vậy, số cặp đoán đúng là:
    TP = C(k, 2) + C(n-k, 2)
    Số cặp đoán sai: k(n-k)
    Số cặp chính xác: C(n, 2)
    Như vậy: TP + Số cặp sai = Số cặp chính xác
        
    Args:
        series_groundtruth (pd.Series): Chuỗi `EventId` của dữ liệu ground truth.
        series_parsedlog (pd.Series): Chuỗi `EventId` của kết quả phân tích.
        debug (bool, optional): In thông tin debug khi có lỗi. Mặc định là False.

    Returns:
        tuple: (precision, recall, f_measure, accuracy)
            - precision (float): Độ chính xác (Precision).
            - recall (float): Độ bao phủ (Recall).
            - f_measure (float): Chỉ số F1-score.
            - accuracy (float): Độ chính xác của việc gán nhãn log.
    """
    
    # Tính toán số lượng các cặp log đúng trong dữ liệu ground truth và dữ liệu kết quả phân tích
    series_groundtruth_valuecounts = series_groundtruth.value_counts()
    real_pairs = 0
    for count in series_groundtruth_valuecounts:
        if count > 1:
            real_pairs += comb(count, 2)

    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    parsed_pairs = 0
    for count in series_parsedlog_valuecounts:
        if count > 1:
            parsed_pairs += comb(count, 2)

    # Xác định có bao nhiêu cặp chính xác và bao nhiêu dòng log chính xác
    accurate_pairs = 0
    accurate_events = 0  # determine how many lines are correctly parsed
    for parsed_eventId in series_parsedlog_valuecounts.index:
        logIds = series_parsedlog[series_parsedlog == parsed_eventId].index
        series_groundtruth_logId_valuecounts = series_groundtruth[logIds].value_counts()
        error_eventIds = (
            parsed_eventId,
            series_groundtruth_logId_valuecounts.index.tolist(),
        )       # Định danh phần tử EventID tương ứng với các eventId nào trong dữ liệu thực
        error = True
        
        # Nếu kích thước của mảng ánh xạ tương ứng bằng 1
        if series_groundtruth_logId_valuecounts.size == 1:
            groundtruth_eventId = series_groundtruth_logId_valuecounts.index[0]
            # Kiểm tra số lượng log thuộc eventIds trong dữ liệu ground truth và dữ liệu phân tích có bằng nhau không, nếu không bằng nhau thì đó là eventId sai, vì nó đã được tính toán trước đó
            if (
                logIds.size
                == series_groundtruth[series_groundtruth == groundtruth_eventId].size
            ):
                accurate_events += logIds.size
                error = False
            
        if error and debug:
            print(
                "(parsed_eventId, groundtruth_eventId) =",
                error_eventIds,
                "failed",
                logIds.size,
                "messages",
            )
        # Sau đó tính toán TP:
        for count in series_groundtruth_logId_valuecounts:
            if count > 1:
                accurate_pairs += comb(count, 2)

    precision = float(accurate_pairs) / parsed_pairs
    recall = float(accurate_pairs) / real_pairs
    f_measure = 2 * precision * recall / (precision + recall)
    accuracy = float(accurate_events) / series_groundtruth.size
    return precision, recall, f_measure, accuracy
