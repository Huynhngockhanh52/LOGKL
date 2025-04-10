import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.special import comb
from sklearn.metrics import accuracy_score
import regex as re
import sys


def post_process_tokens(tokens, punc):
    """
    Phương thức xử lý danh sách token để loại bỏ các ký tự không cần thiết, sau đó chuẩn hóa lại các token.
    Cụ thể, phương thức duyệt qua từng token, nếu chứa <*>, thay thế toàn bộ bằng <*>. Sau đó, loại bỏ dấu câu được xác định trong punc trừ một số ký tự đặc biệt ['=', '|', '(', ')']. Cuối cùng, trả về danh sách token đã xử lý.
    Args:
        tokens (list): Danh sách các token đã được tách ra từ chuỗi đầu vào.
        punc (str): Chuỗi chứa các ký tự được sử dụng để loại bỏ.
    
    Returns:
        list: Danh sách các token đã được xử lý và chuẩn hóa.
    """
    excluded_str = ['=', '|', '(', ')']         # Các ký tự đặc biệt không loại bỏ.
    for i in range(len(tokens)):
        if tokens[i].find("<*>") != -1:
            tokens[i] = "<*>"                   # Ex: blk_<*> --> <*>
        else:
            # Loại bỏ các ký tự không cần thiết trong token theo danh sách punc.
            # Default: punc = "!\"#$%&'()+,-/:;=?@.[\]^_`{|}~"
            new_str = ""
            for s in tokens[i]:
                if (s not in punc and s != ' ') or s in excluded_str:
                    new_str += s
            tokens[i] = new_str
    return tokens

def message_split(message):
    """
    Chia một chuỗi đầu vào thành danh sách các token dựa trên khoảng trắng và các dấu câu đặc biệt. 
    Cụ thể, (1) Xác định các ký tự phân tách (dấu câu, khoảng trắng); (2) Sử dụng biểu thức chính quy để tách chuỗi; (3) Loại bỏ các token rỗng hoặc chỉ chứa khoảng trắng; (4)Tiền xử lý token để loại bỏ ký tự không mong muốn; (5) Xử lý trường hợp có nhiều `<*>` liên tiếp.
    Args:
        message (str): Chuỗi đầu vào cần tách.

    Returns:
        list: Danh sách các token sau khi tách.
    
    Example:
        >>> message_split("Hello, world! How are you?")
        ['Hello', ',', 'world', '!', 'How', 'are', 'you', '?']
    """
    punc = "!\"#$%&'()+,-/:;=?@.[\]^_`{|}~"                     # Các ký tự được sử dụng để tách chuỗi.
    splitters = "\s\\" + "\\".join(punc)
    splitter_regex = re.compile("([{}]+)".format(splitters))    # Tạo regex để tách chuỗi, "([{}]+)" sẽ tìm các ký tự trong splitters và giữ chúng lại trong kết quả tách.
    tokens = re.split(splitter_regex, message)                  # Tách chuỗi: "Hello,,, world.. How are you?" --> ["Hello", ",,,", "world", "..", "How", "are", "you", "?"]
    tokens = list(filter(lambda x: x != "", tokens))            # Loại bỏ các token rỗng.
    tokens = post_process_tokens(tokens, punc)                  # Xử lý hậu kỳ
    tokens = [token.strip() for token in tokens if token != "" and token != ' ']        # Loại bỏ các token rỗng và khoảng trắng.
    tokens = [token for idx, token in enumerate(tokens) if not (token == "<*>" and idx > 0 and tokens[idx - 1] == "<*>")] # Loại bỏ các token "<*>" liên tiếp.
    return tokens

def calculate_similarity(template1, template2):
    """
    Phương thức đo lường mức độ giống nhau giữa hai chuỗi văn bản (template1 và template2) bằng cách sử dụng Chỉ số Jaccard.
    Chỉ số Jaccard là tỷ lệ giữa số lượng phần tử chung của hai tập hợp và tổng số phần tử của cả hai tập hợp.
    
    Args:
        template1 (str): Chuỗi văn bản đầu tiên.
        template2 (str): Chuỗi văn bản thứ hai. 
        
    Returns:
        float: Chỉ số Jaccard giữa hai chuỗi văn bản.    
    """
    template1 = message_split(template1)
    template2 = message_split(template2)
    intersection = len(set(template1).intersection(set(template2))) # Tính số lượng phần tử chung giữa hai tập hợp.
    union = (len(template1) + len(template2)) - intersection        # Tính tổng số phần tử của cả hai tập hợp.
    return intersection / union

def evaluate_template_level(dataset, df_groundtruth, df_parsedresult, filter_templates=None):
    """
    Phương thức đánh giá chất lượng của một hệ thống trích xuất mẫu sự kiện (EventTemplate) bằng cách so sánh kết quả phân tích (df_parsedresult) với dữ liệu gốc (df_groundtruth).
    
    Args:
        dataset (str): Tên của tập dữ liệu.
        df_groundtruth (pd.DataFrame): DataFrame chứa các mẫu sự kiện gốc.
        df_parsedresult (pd.DataFrame): DataFrame chứa các mẫu sự kiện đã được phân tích.
        filter_templates (list, optional): Danh sách các mẫu sự kiện cần lọc. Mặc định là None.
    
    Returns:
        tuple: (t1, t2, FTA, PTA, RTA), trong đó:
            - t1 (int): Số lượng mẫu được nhận diện.
            - t2 (int): Số lượng mẫu thực tế.
            - FTA (float): F1-score của mẫu trích xuất.
            - PTA (float): Precision (độ chính xác) của mẫu trích xuất.
            - RTA (float): Recall (độ phủ) của mẫu trích xuất.
    """
    correct_parsing_templates = 0
    if filter_templates is not None:
        filter_identify_templates = set()        # Lưu trữ tập hợp các mẫu được lọc (nếu có).
    null_logids = df_groundtruth[~df_groundtruth['EventTemplate'].isnull()].index
    
    # Loại bỏ các dòng có giá trị NaN trong cột EventTemplate của df_groundtruth.
    df_groundtruth = df_groundtruth.loc[null_logids]
    df_parsedresult = df_parsedresult.loc[null_logids]
    
    # Tạo các Series từ cột EventTemplate của df_groundtruth và df_parsedresult, đếm số lần xuất hiện của từng mẫu thực tế.
    series_groundtruth = df_groundtruth['EventTemplate']
    series_parsedlog = df_parsedresult['EventTemplate']
    series_groundtruth_valuecounts = series_groundtruth.value_counts()

    # Gộp dữ liệu từ df_groundtruth và df_parsedresult, nhóm theo parsedlog.
    df_combined = pd.concat([series_groundtruth, series_parsedlog], axis=1, keys=['groundtruth', 'parsedlog'])
    grouped_df = df_combined.groupby('parsedlog')

    for identified_template, group in tqdm(grouped_df):         # tqdm() thực hiện hiển thị tiến trình của vòng lặp.
        corr_oracle_templates = set(list(group['groundtruth']))
        if filter_templates is not None and len(corr_oracle_templates.intersection(set(filter_templates))) > 0:
            filter_identify_templates.add(identified_template)

        if corr_oracle_templates == {identified_template}:
            if (filter_templates is None) or (identified_template in filter_templates):
                correct_parsing_templates += 1

    if filter_templates is not None:
        PTA = correct_parsing_templates / len(filter_identify_templates)
        RTA = correct_parsing_templates / len(filter_templates)
    else:
        PTA = correct_parsing_templates / len(grouped_df)
        RTA = correct_parsing_templates / len(series_groundtruth_valuecounts)
    FTA = 0.0
    if PTA != 0 or RTA != 0:
        FTA = 2 * (PTA * RTA) / (PTA + RTA)
    print('PTA: {:.4f}, RTA: {:.4f} FTA: {:.4f}'.format(PTA, RTA, FTA))
    t1 = len(grouped_df) if filter_templates is None else len(filter_identify_templates)
    t2 = len(series_groundtruth_valuecounts) if filter_templates is None else len(filter_templates)
    print("Identify : {}, Groundtruth : {}".format(t1, t2))
    return t1, t2, FTA, PTA, RTA

def correct_lstm(groundtruth, parsedresult):
    """
    Phương thức này kiểm tra xem hai chuỗi groundtruth (chuẩn) và parsedresult (kết quả đã phân tích) có giống nhau hay không, nhưng có một điều kiện đặc biệt: Nếu một token trong groundtruth chứa "<*>", thì toàn bộ token đó sẽ được thay thế bằng "<*>", sau đó mới so sánh hai danh sách token.
    
    Args:
        groundtruth (str): Chuỗi đầu vào gốc.
        parsedresult (str): Chuỗi đầu vào đã được phân tích.    
    
    Returns:
        bool: True nếu hai chuỗi giống nhau sau khi xử lý, False nếu không.
    """
    tokens1 = groundtruth.split(' ')
    tokens2 = parsedresult.split(' ')
    tokens1 = ["<*>" if "<*>" in token else token for token in tokens1]
    return tokens1 == tokens2

def calculate_parsing_accuracy(groundtruth_df, parsedresult_df, filter_templates=None):
    """
    Phương thức tính độ chính xác của quá trình phân tích cú pháp (Parsing Accuracy - PA) dựa trên số lượng thông điệp được phân tích đúng so với tổng số thông điệp.
    
    Args:
        groundtruth_df (pd.DataFrame): DataFrame chứa các mẫu sự kiện gốc.
        parsedresult_df (pd.DataFrame): DataFrame chứa các mẫu sự kiện đã được phân tích.
        filter_templates (list, optional): Danh sách các mẫu sự kiện cần lọc. Mặc định là None.
        
    Returns:
        float: Độ chính xác của quá trình phân tích cú pháp (PA).
    """
    if filter_templates is not None:
        groundtruth_df = groundtruth_df[groundtruth_df['EventTemplate'].isin(filter_templates)]
        parsedresult_df = parsedresult_df.loc[groundtruth_df.index]
    correctly_parsed_messages = parsedresult_df[['EventTemplate']].eq(groundtruth_df[['EventTemplate']]).values.sum()
    total_messages = len(parsedresult_df[['Content']])
    PA = float(correctly_parsed_messages) / total_messages
    print('Parsing_Accuracy (PA): {:.4f}'.format(PA))
    return PA

def calculate_parsing_accuracy_lstm(groundtruth_df, parsedresult_df, filter_templates=None):
    """
    Phương thức `calculate_parsing_accuracy_lstm` được sử dụng để tính độ chính xác của việc phân tích cú pháp (Parsing Accuracy - PA) giữa dữ liệu thực tế (groundtruth_df) và dữ liệu kết quả được phân tích (parsedresult_df). Phương thức này đặc biệt sử dụng trong bối cảnh mô hình LSTM để phân tích mẫu sự kiện (Event Templates).
    
    Args:
        groundtruth_df (pd.DataFrame): DataFrame chứa các mẫu sự kiện gốc.
        parsedresult_df (pd.DataFrame): DataFrame chứa các mẫu sự kiện đã được phân tích.
        filter_templates (list, optional): Danh sách các mẫu sự kiện cần lọc. Mặc định là None.
        
    Returns:
        float: Độ chính xác của quá trình phân tích cú pháp (PA).
    """
    # parsedresult_df = pd.read_csv(parsedresult)
    # groundtruth_df = pd.read_csv(groundtruth)
    if filter_templates is not None:
        groundtruth_df = groundtruth_df[groundtruth_df['EventTemplate'].isin(filter_templates)]
        parsedresult_df = parsedresult_df.loc[groundtruth_df.index]
    # correctly_parsed_messages = parsedresult_df[['EventTemplate']].eq(groundtruth_df[['EventTemplate']]).values.sum()
    groundtruth_templates = list(groundtruth_df['EventTemplate'])
    parsedresult_templates = list(parsedresult_df['EventTemplate'])
    correctly_parsed_messages = 0
    for i in range(len(groundtruth_templates)):
        if correct_lstm(groundtruth_templates[i], parsedresult_templates[i]):
            correctly_parsed_messages += 1

    PA = float(correctly_parsed_messages) / len(groundtruth_templates)

    # similarities = []
    # for index in range(len(groundtruth_df)):
    #     similarities.append(calculate_similarity(groundtruth_df['EventTemplate'][index], parsedresult_df['EventTemplate'][index]))
    # SA = sum(similarities) / len(similarities)
    # print('Parsing_Accuracy (PA): {:.4f}, Similarity_Accuracy (SA): {:.4f}'.format(PA, SA))
    print('Parsing_Accuracy (PA): {:.4f}'.format(PA))
    return PA

def evaluate(groundtruth, parsedresult):
    df_groundtruth = pd.read_csv(groundtruth)
    df_parsedlog = pd.read_csv(parsedresult)
    
    # Remove invalid groundtruth event Ids
    non_empty_log_ids = df_groundtruth[~df_groundtruth["EventTemplate"].isnull()].index
    df_groundtruth = df_groundtruth.loc[non_empty_log_ids]
    df_parsedlog = df_parsedlog.loc[non_empty_log_ids]

    GA, FGA = get_accuracy(df_groundtruth["EventTemplate"], df_parsedlog["EventTemplate"])

    accuracy_exact_string_matching = accuracy_score(
        np.array(df_groundtruth.EventTemplate.values, dtype='str'),
        np.array(df_parsedlog.EventTemplate.values, dtype='str')
    )
    # PA = calculate_parsing_accuracy_lstm(df_groundtruth, df_parsedlog)


    _, _, FTA, PTA, RTA = evaluate_template_level(None, df_groundtruth, df_parsedlog)

    print(
        "Grouping_Accuracy (GA): {:.4f},  FGA: {:.4f}, FTA: {:.4f}, PTA: {:.4f}, RTA: {:.4f}".format(
            GA, FGA, FTA, PTA, RTA
        )
    )
    return GA, FGA, FTA, PTA, RTA

def get_accuracy(series_groundtruth, series_parsedlog, filter_templates=None):
    series_groundtruth_valuecounts = series_groundtruth.value_counts()
    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    df_combined = pd.concat([series_groundtruth, series_parsedlog], axis=1, keys=['groundtruth', 'parsedlog'])
    grouped_df = df_combined.groupby('groundtruth')
    accurate_events = 0 # determine how many lines are correctly parsed
    accurate_templates = 0
    if filter_templates is not None:
        filter_identify_templates = set()
    for ground_truthId, group in tqdm(grouped_df):
        series_parsedlog_logId_valuecounts = group['parsedlog'].value_counts()
        if filter_templates is not None and ground_truthId in filter_templates:
            for parsed_eventId in series_parsedlog_logId_valuecounts.index:
                filter_identify_templates.add(parsed_eventId)
        if series_parsedlog_logId_valuecounts.size == 1:
            parsed_eventId = series_parsedlog_logId_valuecounts.index[0]
            if len(group) == series_parsedlog[series_parsedlog == parsed_eventId].size:
                if (filter_templates is None) or (ground_truthId in filter_templates):
                    accurate_events += len(group)
                    accurate_templates += 1
    if filter_templates is not None:
        GA = float(accurate_events) / len(series_groundtruth[series_groundtruth.isin(filter_templates)])
        PGA = float(accurate_templates) / len(filter_identify_templates)
        RGA = float(accurate_templates) / len(filter_templates)
    else:
        GA = float(accurate_events) / len(series_groundtruth)
        PGA = float(accurate_templates) / len(series_parsedlog_valuecounts)
        RGA = float(accurate_templates) / len(series_groundtruth_valuecounts)
    FGA = 0.0
    if PGA != 0 or RGA != 0:
        FGA = 2 * (PGA * RGA) / (PGA + RGA)
    return GA, FGA