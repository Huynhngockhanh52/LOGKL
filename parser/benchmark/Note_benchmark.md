# Ghi chú về Đánh giá Mô hình Log Parsing

## 1. Cách Tính accurate_events trong Đánh Giá Log Parsing

### 1.1 Định Nghĩa accurate_events
`accurate_events` là số lượng dòng log được mô hình parsing gán nhãn chính xác, tức là tất cả các log trong một nhóm parsed event phải trùng khớp hoàn toàn với một nhóm ground truth event thì mới được tính là chính xác.

### 1.2 Cách Tính Trong Code
```python
for parsed_eventId in series_parsedlog_valuecounts.index:
    logIds = series_parsedlog[series_parsedlog == parsed_eventId].index
    series_groundtruth_logId_valuecounts = series_groundtruth[logIds].value_counts()
    error_eventIds = (
        parsed_eventId,
        series_groundtruth_logId_valuecounts.index.tolist(),
    )    
    error = True
    if series_groundtruth_logId_valuecounts.size == 1:
        groundtruth_eventId = series_groundtruth_logId_valuecounts.index[0]
        if (
            logIds.size
            == series_groundtruth[series_groundtruth == groundtruth_eventId].size
        ):
            accurate_events += logIds.size
            error = False
```
#### **Phân Tích Đoạn Code**
1. **Lặp qua từng nhóm sự kiện (event) đã được parsing**:
   - Lấy danh sách log ID (`logIds`) thuộc về `parsed_eventId`.
   - Đếm số lần xuất hiện của các `groundtruth_eventId` tương ứng với các `logIds` này.

2. **Xác định xem parsed event có tương ứng với một ground truth event duy nhất hay không**:
   - Nếu nhóm log chỉ liên kết đến một `groundtruth_eventId`, ta tiếp tục kiểm tra.

3. **So sánh số lượng mẫu giữa parsed event và ground truth event**:
   - Nếu **số log ID trong parsed event (`logIds.size`) bằng với số log ID trong ground truth event (`series_groundtruth[series_groundtruth == groundtruth_eventId].size`)**, thì tất cả các log của `parsed_eventId` đã được gán đúng và `accurate_events` sẽ được cộng thêm `logIds.size`.
   - Nếu không trùng khớp hoàn toàn, `accurate_events` không tăng, và lỗi được ghi nhận.

### 1.3 Vấn Đề Khi Xét Tính Chính Xác
Giả sử chúng ta có cấu trúc ground truth như sau:
```
E10: "hello <*> system is err in <*> second"
```
Và hai parsed events:
```
ade: "hello Dell system is err in <*> second"
ffd: "hello Linux system is err in <*> second"
```
Trong đó:
- `E10` có **50 mẫu** trong ground truth.
- `ade` có **30 mẫu**, tất cả đều có chỉ mục tương ứng với `E10`.
- `ffd` có **20 mẫu**, trong đó có một số chỉ mục cũng thuộc `E10`.

Khi kiểm tra điều kiện:
```python
if logIds.size == series_groundtruth[series_groundtruth == groundtruth_eventId].size:
```
Do `logIds.size = 30` (hoặc 20 trong trường hợp `ffd`), nhưng `series_groundtruth[series_groundtruth == groundtruth_eventId].size = 50`, điều kiện này không thỏa mãn, vì vậy `accurate_events` không được cộng thêm.

### 1.4 Tại Sao Kết Quả Không Được Xem Là Chính Xác?
Dù `ade` và `ffd` có mẫu log tương tự `E10`, nhưng chúng vẫn chưa hoàn toàn chính xác do:
1. **Chúng chưa bao quát toàn bộ mẫu gốc của `E10`**:
   - `E10` có 50 mẫu, nhưng `ade` chỉ bao gồm 30 mẫu và `ffd` chỉ bao gồm 20 mẫu. Điều này có nghĩa là mô hình parsing đã chia tách một nhóm duy nhất thành nhiều nhóm nhỏ, làm giảm Recall.
   
2. **Tách nhóm không đúng cách (Over-splitting)**:
   - Mô hình đã không gom tất cả các log của `E10` vào chung một nhóm mà thay vào đó chia thành nhiều nhóm (`ade`, `ffd`).
   - Điều này làm mất đi khả năng nhận diện đầy đủ của một sự kiện thực tế.

3. **Công thức tính accurate_events yêu cầu sự trùng khớp hoàn toàn**:
   - Nếu một `parsed_eventId` chỉ chứa một phần của một `groundtruth_eventId`, thì vẫn bị coi là sai vì chưa đủ chính xác.

## 2. Giải Pháp Cải Tiến
Để cải thiện độ chính xác khi đánh giá log parsing, có thể sử dụng một số phương pháp:

1. **Xây dựng phép đo gần đúng thay vì bắt buộc trùng khớp 100%**:
   - Thay vì yêu cầu `logIds.size` phải bằng với kích thước ground truth, ta có thể cho phép một mức sai lệch nhất định dựa trên tỷ lệ phần trăm tương đồng.

2. **Sử dụng phép đo trung gian như Jaccard Similarity hoặc Fuzzy Matching**:
   - So sánh mức độ trùng khớp giữa parsed event và ground truth event dựa trên nội dung câu log thay vì chỉ so sánh ID.

3. **Xây dựng mô hình học sâu để phân loại log dựa trên nội dung**:
   - Thay vì chỉ dựa vào template matching, có thể áp dụng mô hình NLP để đánh giá mức độ tương đồng giữa các log message.

## 3. Kết Luận
Trong đánh giá log parsing, `accurate_events` yêu cầu sự trùng khớp hoàn toàn giữa nhóm parsed log và ground truth log. Nếu parsed log chỉ bao gồm một phần của một sự kiện thực tế, nó vẫn không được tính là chính xác. Điều này đảm bảo rằng thuật toán parsing không chỉ tìm thấy một phần sự kiện mà phải gom đúng tất cả các log thuộc cùng một sự kiện.

Tuy nhiên, cách tiếp cận này có thể nghiêm ngặt quá mức và bỏ qua các trường hợp gần đúng. Việc cải tiến phép đo bằng các kỹ thuật linh hoạt hơn có thể giúp đánh giá mô hình một cách công bằng và chính xác hơn.

