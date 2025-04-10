
# File này chứa các thiết lập mặc định bao gồm các thông tin về định dạng log, regex và đường dẫn đến file log cho các loại log khác nhau trong LogHub.
LOGHUB_SETTINGS = {
    "Proxifier": {
        "log_file": "Logs/Proxifier/Proxifier_2k.log",
        "log_format": "\[<Time>\] <Program> - <Content>",
        "regex": [
            r"<\d+\ssec",
            r"([\w-]+\.)+[\w-]+(:\d+)?",
            r"\d{2}:\d{2}(:\d{2})*",
            r"[KGTM]B",
        ],
        "ground_truth": "Logs/Proxifier/Proxifier_2k.log_structured_corrected.csv",
        "type": "",
    },
    "HDFS": {
        "log_file": "Logs/HDFS/HDFS_2k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [
            r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"
        ],
        "ground_truth": "Logs/HDFS/HDFS_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Hadoop": {
        "log_file": "Logs/Hadoop/Hadoop_2k.log",
        "log_format": "<Date> <Time> <Level> \[<Process>\] <Component>: <Content>",
        "regex": [
            r"(\d+\.){3}\d+"
        ],
        "ground_truth": "Logs/Hadoop/Hadoop_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Spark": {
        "log_file": "Logs/Spark/Spark_2k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [
            r"(\d+\.){3}\d+", 
            r"\b[KGTM]?B\b", 
            r"([\w-]+\.){2,}[\w-]+"
        ],
        "ground_truth": "Logs/Spark/Spark_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Zookeeper": {
        "log_file": "Logs/Zookeeper/Zookeeper_2k.log",
        "log_format": "<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>",
        "regex": [
            r"(/|)(\d+\.){3}\d+(:\d+)?"
        ],
        "ground_truth": "Logs/Zookeeper/Zookeeper_2k.log_structured_corrected.csv",
        "type": "",
    },
    "BGL": {
        "log_file": "Logs/BGL/BGL_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [
            r"core\.\d+"
        ],
        "ground_truth": "Logs/BGL/BGL_2k.log_structured_corrected.csv",
        "type": "",
    },
    "HPC": {
        "log_file": "Logs/HPC/HPC_2k.log",
        "log_format": "<LogId> <Node> <Component> <State> <Time> <Flag> <Content>",
        "regex": [],
        "ground_truth": "Logs/HPC/HPC_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Thunderbird": {
        "log_file": "Logs/Thunderbird/Thunderbird_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>",
        "regex": [
            r"(\d+\.){3}\d+"
        ],
        "ground_truth": "Logs/Thunderbird/Thunderbird_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Windows": {
        "log_file": "Logs/Windows/Windows_2k.log",
        "log_format": "<Date> <Time>, <Level>                  <Component>    <Content>",
        "regex": [
            r"0x.*?\s"
        ],
        "ground_truth": "Logs/Windows/Windows_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Linux": {
        "log_file": "Logs/Linux/Linux_2k.log",
        "log_format": "<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>",
        "regex": [
            r"(\d+\.){3}\d+", 
            r"\d{2}:\d{2}:\d{2}", 
            r"J([a-z]{2})"
        ],
        "ground_truth": "Logs/Linux/Linux_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Android": {
        "log_file": "Logs/Android/Android_2k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "ground_truth": "Logs/Android/Android_2k.log_structured_corrected.csv",
        "type": "",
    },
    "HealthApp": {
        "log_file": "Logs/HealthApp/HealthApp_2k.log",
        "log_format": "<Time>\|<Component>\|<Pid>\|<Content>",
        "regex": [],
        "ground_truth": "Logs/HealthApp/HealthApp_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Apache": {
        "log_file": "Logs/Apache/Apache_2k.log",
        "log_format": "\[<Time>\] \[<Level>\] <Content>",
        "regex": [
            r"(\d+\.){3}\d+"
        ],
        "ground_truth": "Logs/Apache/Apache_2k.log_structured_corrected.csv",
        "type": "",
    },
    "OpenSSH": {
        "log_file": "Logs/OpenSSH/OpenSSH_2k.log",
        "log_format": "<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>",
        "regex": [
            r"(\d+\.){3}\d+", 
            r"([\w-]+\.){2,}[\w-]+"
        ],
        "ground_truth": "Logs/OpenSSH/OpenSSH_2k.log_structured_corrected.csv",
        "type": "",
    },
    "OpenStack": {
        "log_file": "Logs/OpenStack/OpenStack_2k.log",
        "log_format": "<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>",
        "regex": [
            r"((\d+\.){3}\d+,?)+", 
            r"/.+?\s ", 
            r"\d+"
        ],
        "ground_truth": "Logs/OpenStack/OpenStack_2k.log_structured_corrected.csv",
        "type": "",
    },
    "Mac": {
        "log_file": "Logs/Mac/Mac_2k.log",
        "log_format": "<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>",
        "regex": [
            r"([\w-]+\.){2,}[\w-]+"
        ],
        "ground_truth": "Logs/Mac/Mac_2k.log_structured_corrected.csv",
        "type": "",
    },
}