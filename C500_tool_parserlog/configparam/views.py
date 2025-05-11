from django.shortcuts import render, redirect
from django.http import HttpResponse

import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Dataset, LogConfig, RegexPattern, SizeLog
from django.shortcuts import get_object_or_404

# =============== Các phương thức xử lý với dữ liệu cấu hình Log ===============
# Xuất tất cả dữ liệu liên quan đến cấu hình log ra ngoài:
def export_log_config(request):
    data = []
    for dataset in Dataset.objects.all():
        dataset_dict = dataset.to_dict()
        dataset_dict['config'] = [config.to_dict() for config in dataset.config.all()]
        data.append(dataset_dict)
    
    return render(request, 'configs/logs/index.html', {'data': data})



# ------------------------- Phương thức Dataset ---------------------------
# Index Dataset:
def index_dataset(request):
    datasets = Dataset.objects.all()
    dataset_list = [ds.to_index() for ds in datasets]
    return render(request, 'configs/dataset/index.html', {'data': dataset_list})

# Xem chi tiết
def detail_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset_dict = dataset.to_dict()
    dataset_dict['config'] = [config.to_dict() for config in dataset.config.all()]
    return render(request, 'configs/dataset/detail.html', {'dataset': dataset_dict})

# Edit Dataset:
@csrf_exempt
def edit_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    if request.method == 'POST':
        dataset.dataset = request.POST.get('dataset')
        dataset.path = request.POST.get('path')
        dataset.save()
        return redirect('index_dataset')  

    return render(request, 'configs/dataset/edit.html', {'dataset': dataset})

# Thêm mới Dataset
def create_dataset(request):
    if request.method == 'POST':
        dataset = request.POST.get('dataset')
        path = request.POST.get('path')
        obj = Dataset.objects.create(dataset=dataset, path=path)
        return JsonResponse(obj.to_dict())

# Xoá Dataset
def delete_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset.delete()
    return JsonResponse({'status': 'deleted'})

