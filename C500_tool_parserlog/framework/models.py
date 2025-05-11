from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
import json
import os

# Create your models here.


# # ======================= Xây dựng Database lưu cấu hình Log =======================
# class Dataset(models.Model):
#     dataset = models.CharField(max_length=100)
#     path = models.CharField(max_length=255)

#     def __str__(self):
#         return self.dataset

#     def to_dict(self):
#         return {
#             "dataset": self.dataset,
#             "path": self.path,
#         }

# class LogConfig(models.Model):
#     dataset = models.ForeignKey(Dataset, related_name='config', on_delete=models.CASCADE)
#     log_name = models.CharField(max_length=100)
#     log_format = models.TextField()

#     def __str__(self):
#         return f"{self.dataset.dataset} - {self.log_name}"

#     def to_dict(self):
#         return {
#             "log_name": self.log_name,
#             "log_format": self.log_format,
#             "regex": [r.regex for r in self.regexpattern_set.all()],
#             "sizelog": [s.to_dict() for s in self.sizelog_set.all()],
#         }

# class RegexPattern(models.Model):
#     regex = models.TextField()
#     log_config = models.ForeignKey(LogConfig, on_delete=models.CASCADE)

#     def to_dict(self):
#         return self.regex

# class SizeLog(models.Model):
#     log_config = models.ForeignKey(LogConfig, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     file_log = models.CharField(max_length=255)
#     ground_truth = models.CharField(max_length=255, blank=True)
#     template = models.CharField(max_length=255, blank=True)

#     def to_dict(self):
#         return {
#             "type": self.type,
#             "file_log": self.file_log,
#             "ground_truth": self.ground_truth,
#             "template": self.template,
#         }

# # ======================== Xây dựng Database lưu cấu hình Parser =======================
# class ParserTool(models.Model):
#     tool_name = models.CharField(max_length=100)
#     heuristic = models.BooleanField(default=False)
#     frequent_pattern = models.BooleanField(default=False)
#     clustering = models.BooleanField(default=False)
#     ml = models.BooleanField(default=False)
#     online = models.BooleanField(default=False)

#     def __str__(self):
#         return self.tool_name

#     def to_dict(self):
#         return {
#             "tool_name": self.tool_name,
#             "heuristics": self.heuristic,
#             "frequent_pattern": self.frequent_pattern,
#             "clustering": self.clustering,
#             "online": self.online,
#             "ml": self.ml,
#             "hyperparameter": [h.to_dict() for h in self.hyperparameter_set.all()],
#             "setting": self._get_setting()
#         }

#     def _get_setting(self):
#         from collections import defaultdict
#         setting_map = defaultdict(list)
#         for s in self.settingparam_set.all():
#             dataset_name = s.log_config.dataset.dataset
#             log_name = s.log_config.log_name
#             setting_map[dataset_name].append({
#                 "log_name": log_name,
#                 s.hyperparameter.name: s.value
#             })
#         return [{"dataset": ds, "config": cfg} for ds, cfg in setting_map.items()]

# class Hyperparameter(models.Model):
#     name = models.CharField(max_length=100)
#     min = models.FloatField()
#     max = models.FloatField()
#     default = models.FloatField()
#     parser_tool = models.ForeignKey(ParserTool, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.parser_tool.tool_name} - {self.name}"

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "min": self.min,
#             "max": self.max,
#             "default": self.default
#         }


# # ==================== Xây dựng Database lưu cấu hình Hyperparameter ====================
# class SettingParam(models.Model):
#     hyperparameter = models.ForeignKey(Hyperparameter, on_delete=models.CASCADE)
#     log_config = models.ForeignKey(LogConfig, on_delete=models.CASCADE)
#     value = models.FloatField()

#     def __str__(self):
#         return f"{self.log_config.log_name} - {self.hyperparameter.name} = {self.value}"

#     def to_dict(self):
#         return {
#             "log_config": self.log_config.id,
#             self.hyperparameter.name: self.value
#         }