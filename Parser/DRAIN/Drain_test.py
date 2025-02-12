# =========================================================================
# Thực hiện viết lại các lớp hàm để chạy tự động Drain, kế thừa từ file Drain.py
# =========================================================================

import regex as re
import os
import pandas as pd
import hashlib

from datetime import datetime
import time
import numpy as np

import Drain

class LogclusterEdit(Drain.Logcluster):
    """
    Class được chỉnh sửa lại, bao gồm một số thông số như sau:
    
    Thuộc tính:
    ----------
        - `logTemplate` : Template đặc trưng đại diện cho nhóm log đó, ["The1", "the2", ...]
        - `logIDL`      : Danh sách các ID message log thuộc nhóm log trên, [1,2,3,4,5, ...] 
        - `idEventHash` : Khởi tạo mã băm ban đầu: 32fsanf32, ...
        - `idEventVN`   : Mã băm theo dạng tự định nghĩa, dựa trên Node root: E1, E2, ...
    """
    def __init__(self, logTemplate="", logIDL=None, num=None):
        self.logTemplate = logTemplate
        if logIDL is None:
            logIDL = []
        self.logIDL = logIDL
        
        if logTemplate != "":
            self.idEventHash = hashlib.md5(" ".join(logTemplate).encode("utf-8")).hexdigest()
            self.idEventHash =  hashlib.md5(self.idEventHash.encode()).hexdigest()[:8]
        else: 
            self.idEventHash = None
        
        if num is None:
            self.idEventVN = "E-1"
        else: 
            self.idEventVN = "E" + str(num)
            
class LogParserEdit(Drain.LogParser):
    """
        Class `LogParserEdit` chỉnh sửa lại các biến sử dụng để có thể đọc, in ra các biến sử dụng và thêm vào các phương thức hỗ trợ đọc biến rootNode

        Các thuộc tính:
        - `rex` (list): Biểu thức chính quy được sử dụng cho quá trình tiền xử lý (step1). Mặc định: []
        - `path` (str): Đường dẫn tệp log đầu vào. Mặc định: ""
        - `depth` (int): Độ sâu của tất cả các Node lá (leaf node). Mặc định: 4 (tính toán: 4 - 2 = 2)
        - `st` (float): Ngưỡng tương đồng (similarity threshold). Mặc định: 0.4
        - `maxChild` (int): Số lượng tối đa node con của một node nội tại. Mặc định: 100
        - `logName` (str): Tên tệp đầu vào chứa các thông báo log thô. Mặc định: ""
        - `savePath` (str): Đường dẫn đầu ra của tệp chứa các log đã được cấu trúc. Mặc định: ""
        - `saveEventPath` (str): Đường dẫn đầu ra của tệp chứa các event đã được cấu trúc.
        - `keep_para` (bool): Yêu cầu có lưu giữ tham số hay không. Mặc định: True
        - `df_log` (pd.DataFrame): DataFrame chứa log đầu vào.
        - `log_format` (str): Định dạng log đầu vào.
        - `rootNode` (Node): Node gốc của cây log.
        - `list_logClust` (list): Danh sách các nhóm log.
    """
    # def __init__(   
    #     self, log_format, 
    #     indir="./", outdir="./result/", eventPath="./event/", finalPath="./final/",
    #     rootNode=None, depth=4, st=0.4, maxChild=100, 
    #     rex=[], keep_para=True,
    # ):
        
    def __init__(
        self, *args,
        rex_unix=None, row_dt=None,
        eventPath="./event/", finalPath="./final/", 
        rootNode=Drain.Node(digitOrtoken=0), list_logClust=[], **kwargs     
    ):
        super().__init__(*args, **kwargs)
        # self.depth = depth - 2 # Tính toán số lượng lớp Node intenal
        self.eventPath = eventPath                      # Thêm
        self.finalPath = finalPath                      # Thêm
        self.rootNode = rootNode                        # Thêm
        self.list_logClust = list_logClust              # Thêm
        
        self.rex_unix = rex_unix                        # Thêm
        self.row_dt = row_dt                            # Thêm
        
    def convert_unixtime(self, rex_date_time, columns_name, row):
        """
        Phương thức trích xuất thời gian theo dạng chuẩn UNIX, truyền vào một biểu thức chính quy, và chuỗi cần chuyển đổi:
        Ví dụ: "%y%m%d %H%M%S", "081109 203615" ==> 1226237775
        """
        try:
            date_time = ""
            columns_names = re.findall(r"<(.*?)>", columns_name)
            for temp in columns_names:
                date_time += row[temp] + " "
            date_time = date_time.strip()
            
            # Xử lý các định dạng khác nhau
            dt = datetime.strptime(date_time, rex_date_time)
            
            # Chuyển sang Unix timestamp
            unixtime = int(time.mktime(dt.timetuple()))
            
            # Trả về các định dạng date và time bổ sung
            format_date = dt.strftime("%d-%m-%Y")
            format_time = dt.strftime("%H:%M:%S")
            
            return unixtime, format_date, format_time
        except Exception as e:
            print(f"Error converting date time: {e}")
            return None, None, None
    
    def parse(self, logName):
        """
        Phương thức thực hiện quá trình phân tích log
        
        Tham số: 
        --------
            - `logName`: Tên file đầu vào thực hiện phân tích
        """
        print("File đầu vào: " + os.path.join(self.path, logName))
        start_time = datetime.now()
        self.logName = logName

        # ----------------Gán lại các đối tượng sử dụng---------------------#
        rootNode = self.rootNode       # Địa chỉ Node gốc
        print("Root Node: ", rootNode.digitOrtoken)
        logCluL = self.list_logClust   # Lưu giữ các đối tượng nhóm log Logcluster2 trước đó.
        # ------------------------- Load dữ liệu ----------------------------#
        # * Trước khi load dữ liệu, cần phải đưa các biến lưu trữ logIDL về dạng empty list:
        for logClust in self.list_logClust:
            logClust.logIDL = [] 
            
        # * Đưa dữ liệu df_log về None:
        self.df_log = None
        
        # * Load dữ liệu từ file log
        self.load_data() 

        #----------------------------Phân tích------------------------------#
        # * Thực hiện phân tích và lấy Template cho từng dòng thông điệp log
        count = 0
        for idx, line in self.df_log.iterrows(): 
            logID = line["LineId"]
            logmessageL = self.preprocess(line["Content"]).strip().split()  
            matchCluster = self.treeSearch(rootNode, logmessageL)           
            if matchCluster is None:
                newCluster = LogclusterEdit(logTemplate=logmessageL, logIDL=[logID], num=int(rootNode.digitOrtoken) + 1)
                rootNode.digitOrtoken += 1

                # - Thêm chúng vào cây phân tích
                logCluL.append(newCluster)
                self.addSeqToPrefixTree(rootNode, newCluster)
                
            else:
                # - Nếu template đã có:
                newTemplate = self.getTemplate(logmessageL, matchCluster.logTemplate)
                matchCluster.logIDL.append(logID)
                # + Nếu có sự thay đổi trong template thành một template mới, cập nhật
                if " ".join(newTemplate) != " ".join(matchCluster.logTemplate):
                    matchCluster.logTemplate = newTemplate
                    
            count += 1
            if count % 100000 == 0 or count == len(self.df_log):
                print("Processed {0:.1f}% of log lines.".format(count * 100.0 / len(self.df_log))) # Chỉ sửa mỗi vị trí này.

        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        if not os.path.exists(self.eventPath):
            os.makedirs(self.eventPath)
        if self.rex_unix is None or self.row_dt is None:
            self.outputResult(self.list_logClust)
        else:
            self.outputResult(self.list_logClust, rex_unix=self.rex_unix, row_dt=self.row_dt)
        print("Phân tích hoàn thành! [Thời gian thực hiện: {!s}]".format(datetime.now() - start_time))
        
    def outputResult(self, logClustL, **kwargs):
        """
        Thực hiện in thông tin kết quả ra ngoài sau khi hoàn thành quá trình phân tích
        
        Tham số:
        --------
            - `logClustL`   : Danh sách các nhóm log đã thu thập được trong quá trình phân tách
        """
        # ----------- Khai báo các biến sử dụng ----------#
        log_templates = [0] * self.df_log.shape[0]
        log_templateids = [0] * self.df_log.shape[0]
        log_templateids_vn = [0] * self.df_log.shape[0]
        list_events = []                            # Mảng list_events lưu giữ các giá trị template

        # --------------Thực hiện phân tích--------------#
        # * Duyệt qua từng đối tượng Logcluster để thêm các giá trị vào từng biến trên
        for logClust in logClustL:
            template_str = " ".join(logClust.logTemplate)
            occurrence = len(logClust.logIDL)
            # template_id = hashlib.md5(template_str.encode("utf-8")).hexdigest()[0:8]
            template_id = logClust.idEventHash
            template_id_vn = logClust.idEventVN
            for logID in logClust.logIDL:
                logID -= 1
                log_templates[logID] = template_str
                log_templateids[logID] = template_id
                log_templateids_vn[logID] = template_id_vn
                
            list_events.append([template_id, template_id_vn, template_str, occurrence]) # Lưu giữ danh sách các Event log và số lần xảy ra
            
        # DataFrame df_event lưu giữ các thông tin của Template
        df_event = pd.DataFrame(
            list_events, columns=["EventId", "EventIdVN", "EventTemplate", "Occurrences"]
        )
        
        # DataFrame df_log lưu giữ các thông tin của từng dòng thông điệp log
        self.df_log["EventId"] = log_templateids
        self.df_log["EventIdVN"] = log_templateids_vn
        self.df_log["EventTemplate"] = log_templates
        
        # Chuyển đổi thời gian theo dạng UnixTime: Tạo thêm cột "UnixTime" trong DataFrame df_log
        if 'rex_unix' in kwargs and 'row_dt' in kwargs:
            self.df_log[["UnixTime", 'Date', 'Time']] = self.df_log.apply(
            lambda row: pd.Series(self.convert_unixtime(kwargs["rex_unix"], kwargs["row_dt"], row)), axis=1
        )
                
        if self.keep_para:
            self.df_log["ParameterList"] = self.df_log.apply(
                self.get_parameter_list, 
                axis=1
            )

        # self.df_log.to_csv(
        #     os.path.join(self.savePath, self.logName.replace('.log', '') + "_structured.csv"),
        #     index=False, sep="~"
        # )
        
        # df_event.to_csv(
        #     os.path.join(self.eventPath, self.logName.replace('.log', '') + "_event.csv"), 
        #     index=False, sep="~"
        # )
        self.df_log.to_csv(
            os.path.join(self.savePath, self.logName.replace('.log', '') + "_structured.csv"),
            index=False, sep="~",
            columns = ['LineId', 'UnixTime', 'Date', 'Time'] + [col for col in self.df_log.columns if col not in ['LineId', 'UnixTime', 'Date', 'Time']]
        )
        
        df_event.to_csv(
            os.path.join(self.eventPath, self.logName.replace('.log', '') + "_event.csv"), index=False, sep="~",
        )