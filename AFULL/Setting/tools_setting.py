# ==================== Ghi lại các setting siêu tham số cho từng Tool phân tích log ====================

TOOLS_SETTINGS = {
    # Khai thác mẫu thường xuyên:
    "SLCT": {
        "HDFS": {
            "support": 120,
        },
        "Hadoop": {
            "support": 125,
        },
        "Spark": {
            "support": 30,
        },
        "Zookeeper": {
            "support": 10,
        },
        "BGL": {
            "support": 6,
        },
        "HPC": {
            "support": 7,
        },
        "Thunderbird": {
            "support": 10,
        },
        "Windows": {
            "support": 3,
        },
        "Linux": {
            "support": 100,
        },
        "Android": {
            "support": 1,
        },
        "HealthApp": {
            "support": 100,
        },
        "Apache": {
            "support": 5,
        },
        "Proxifier": {
            "support": 8,
        },
        "OpenSSH": {
            "support": 45,
        },
        "OpenStack": {
            "support": 18,
        },
        "Mac": {
            "support": 3,
        }, 
        "DEFAULT":{
            "support": 5,
        }
    },

    "LFA":{
        "HDFS": {},
        "Hadoop": {},
        "Spark": {},
        "Zookeeper": {},
        "BGL": {},
        "HPC": {},
        "Thunderbird": {},
        "Windows": {},
        "Linux": {},
        "Android": {},
        "HealthApp": {},
        "Apache": {},
        "Proxifier": {},
        "OpenSSH": {},
        "OpenStack": {},
        "Mac": {},
        "DEFAULT":{},
    },
    
    "LogCluster": {
        "HDFS": {
            "rsupport": 10,
        },
        "Hadoop": {
            "rsupport": 10,
        },
        "Spark": {
            "rsupport": 10,
        },
        "Zookeeper": {
            "rsupport": 0.5,
        },
        "BGL": {
            "rsupport": 2,
        },
        "HPC": {
            "rsupport": 0.1,
        },
        "Thunderbird": {
            "rsupport": 2,
        },
        "Windows": {
            "rsupport": 0.2,
        },
        "Linux": {
            "rsupport": 40,
        },
        "Android": {
            "rsupport": 1,
        },
        "HealthApp": {
            "rsupport": 7,
        },
        "Apache": {
            "rsupport": 30,
        },
        "Proxifier": {
            "rsupport": 10,
        },
        "OpenSSH": {
            "rsupport": 0.1,
        },
        "OpenStack": {
            "rsupport": 3,
        },
        "Mac": {
            "rsupport": 0.2,
        },
        "DEFAULT":{
            "rsupport": 0.1,
        },
    },
    
    "Logram":{
        "HDFS": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Hadoop": {
            "doubleThreshold": 9,
            "triThreshold": 10,
        },
        "Spark": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Zookeeper": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "BGL": {
            "doubleThreshold": 92,
            "triThreshold": 4,
        },
        "HPC": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Thunderbird": {
            "doubleThreshold": 35,
            "triThreshold": 32,
        },
        "Windows": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Linux": {
            "doubleThreshold": 120,
            "triThreshold": 100,
        },
        "Android": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "HealthApp": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Apache": {
            "doubleThreshold": 15,
            "triThreshold": 10,
        },
        "Proxifier": {
            "doubleThreshold": 500,
            "triThreshold": 470,
        },
        "OpenSSH": {
            "doubleThreshold": 88,
            "triThreshold": 81,
        },
        "OpenStack": {
            "doubleThreshold": 30,
            "triThreshold": 25,
        },
        "Mac": {
            "doubleThreshold": 2,
            "triThreshold": 2,
        },
        "DEFAULT":{
            "doubleThreshold": 15,
            "triThreshold": 10,
        }
    },
    
    "ULP":{
        "HDFS": {},
        "Hadoop": {},
        "Spark": {},
        "Zookeeper": {},
        "BGL": {},
        "HPC": {},
        "Thunderbird": {},
        "Windows": {},
        "Linux": {},
        "Android": {},
        "HealthApp": {},
        "Apache": {},
        "Proxifier": {},
        "OpenSSH": {},
        "OpenStack": {},
        "Mac": {},
        "DEFAULT":{},
    },
    
    "Drain":{
        "HDFS": {
            "st": 0.5,
            "depth": 4,
        },
        "Hadoop": {
            "st": 0.5,
            "depth": 4,
        },
        "Spark": {
            "st": 0.5,
            "depth": 4,
        },
        "Zookeeper": {
            "st": 0.5,
            "depth": 4,
        },
        "BGL": {
            "st": 0.5,
            "depth": 4,
        },
        "HPC": {
            "st": 0.5,
            "depth": 4,
        },
        "Thunderbird": {
            "st": 0.5,
            "depth": 4,
        },
        "Windows": {
            "st": 0.7,
            "depth": 5,
        },
        "Linux": {
            "st": 0.39,
            "depth": 6,
        },
        "Android": {
            "st": 0.2,
            "depth": 6,
        },
        "HealthApp": {
            "st": 0.2,
            "depth": 4,
        },
        "Apache": {
            "st": 0.5,
            "depth": 4,
        },
        "Proxifier": {
            "st": 0.6,
            "depth": 3,
        },
        "OpenSSH": {
            "st": 0.6,
            "depth": 5,
        },
        "OpenStack": {
            "st": 0.5,
            "depth": 5,
        },
        "Mac": {
            "st": 0.7,
            "depth": 6,
        },
        "DEFAULT":{
            "st": 0.5,
            "depth": 4,
        }
    },
    
    "Brain":{
        "Proxifier": {
            "delimiter": [
                r"\(.*?\)"
            ],
            "theshold": 3,
        },
        "HDFS": {
            "delimiter": [
                ""
            ],
            "theshold": 2,
        },
        "Hadoop": {
            "delimiter": [],
            "theshold": 6,
        },
        "Spark": {
            "delimiter": [],
            "theshold": 4,
        },
        "Zookeeper": {
            "delimiter": [],
            "theshold": 3,
        },
        "BGL": {
            "delimiter": [],
            "theshold": 6,
        },
        "HPC": {
            "delimiter": [],
            "theshold": 5,
        },
        "Thunderbird": {
            "delimiter": [],
            "theshold": 3,
        },
        "Windows": {
            "delimiter": [],
            "theshold": 3,
        },
        "Linux": {
            "delimiter": [
                r""
            ],
            "theshold": 4,
        },
        "Android": {
            "delimiter": [
                r""
            ],
            "theshold": 5,
        },
        "HealthApp": {
            "delimiter": [
                r""
            ],
            "theshold": 4,
        },
        "Apache": {
            "delimiter": [],
            "theshold": 4,
        },
        "OpenSSH": {
            "delimiter": [],
            "theshold": 6,
        },
        "OpenStack": {
            "delimiter": [],
            "theshold": 5,
        },
        "Mac": {
            "delimiter": [],
            "theshold": 5,
        },
        "DEFAULT":{
            "delimiter": [],
            "theshold": 5,
        }
    }, 
}