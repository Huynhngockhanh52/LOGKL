# Đánh giá thuật toán phân tích Log

## 1. Giới thiệu
Phân tích log đóng vai trò quan trọng trong việc trích xuất thông tin có cấu trúc từ nhật ký hệ thống. Để đo lường hiệu quả của thuật toán phân tích log, chúng ta sử dụng các chỉ số đánh giá: **Precision, Recall, F1-score và Accuracy**. Các thước đo này giúp đánh giá mức độ chính xác của kết quả phân tích so với dữ liệu thực tế.

## 2. Các thành phần của ma trận nhầm lẫn
Trong phân tích log, chúng ta định nghĩa bốn thành phần chính:
- **True Positives (TP):** Các cặp log được nhóm đúng (tức là cùng một sự kiện trong cả dữ liệu thực tế và kết quả phân tích).
- **False Positives (FP):** Các cặp log bị nhóm sai (tức là bị gán chung một sự kiện trong kết quả phân tích nhưng thực tế thuộc các sự kiện khác nhau).
- **False Negatives (FN):** Các cặp log đúng nhưng không được nhóm lại (tức là chúng thuộc cùng một sự kiện trong dữ liệu thực tế nhưng bị phân nhóm sai trong kết quả phân tích).
- **True Negatives (TN):** Các cặp log không cùng sự kiện và được xác định chính xác (ít được sử dụng trong đánh giá phân tích log).

## 3. Các chỉ số đánh giá
Các chỉ số sau được tính dựa trên TP, FP và FN:

### **3.1 Precision (Độ chính xác)**
**Định nghĩa:** Precision đo lường tỷ lệ nhóm sự kiện đúng trên tổng số nhóm sự kiện được phát hiện.

$$
Precision = \frac{TP}{TP + FP}
$$

- Precision cao có nghĩa là số lượng nhóm sai ít.
- Precision thấp có nghĩa là có nhiều log bị nhóm sai.

### **3.2 Recall (Độ bao phủ)**
**Định nghĩa:** Recall đo lường tỷ lệ nhóm sự kiện đúng được phát hiện trên tổng số nhóm sự kiện thực tế.

$$
Recall = \frac{TP}{TP + FN}
$$

- Recall cao có nghĩa là hầu hết các nhóm đúng được nhận diện.
- Recall thấp có nghĩa là nhiều nhóm sự kiện thực tế bị bỏ sót.

### **3.3 F1-score**
**Định nghĩa:** F1-score là trung bình điều hòa giữa Precision và Recall, giúp cân bằng hai chỉ số này.

$$
F1-score = 2 \times \frac{Precision \times Recall}{Precision + Recall}
$$

- F1-score cao cho thấy thuật toán có sự cân bằng tốt giữa Precision và Recall.
- Hữu ích khi cả False Positives và False Negatives đều quan trọng.

### **3.4 Accuracy (Độ chính xác tổng thể)**
**Định nghĩa:** Accuracy đo lường tổng số log được gán nhãn chính xác trên tổng số log.

$$
Accuracy = \frac{Số\ log\ đúng}{Tổng\ số\ log}
$$

- Accuracy phản ánh hiệu suất tổng thể nhưng có thể gây hiểu lầm nếu dữ liệu mất cân đối.

## 4. Ví dụ tính toán
Xét tập dữ liệu log sau:

**Dữ liệu thực tế (Ground Truth - nhóm đúng):**
```
A → {1, 2, 5, 6, 7}
B → {3, 8, 9, 10}
C → {4, 11, 12}
```

**Kết quả phân tích (Parsed Result - nhóm theo thuật toán):**
```
aks → {1, 2, 6, 7, 9}
dfs → {3, 1, 8, 10}
eee → {4, 5, 11, 12}
```

### **Bước 1: Tính số cặp**
Một nhóm có `n` log sẽ có $ \frac{n(n-1)}{2} $ cặp log:
- **Cặp log thực tế:**
  - A: $ \frac{5(5-1)}{2} = 10 $
  - B: $ \frac{4(4-1)}{2} = 6 $
  - C: $ \frac{3(3-1)}{2} = 3 $
  - **Tổng số cặp đúng:** **10 + 6 + 3 = 19**

- **Cặp log theo thuật toán:**
  - aks: $ \frac{5(5-1)}{2} = 10 $
  - dfs: $ \frac{4(4-1)}{2} = 6 $
  - eee: $ \frac{4(4-1)}{2} = 6 $
  - **Tổng số cặp theo thuật toán:** **10 + 6 + 6 = 22**

- **Số cặp đúng (TP) = 15**
- **Số cặp sai (FP) = 22 - 15 = 7**
- **Số cặp bị bỏ sót (FN) = 19 - 15 = 4**

### **Bước 2: Tính các chỉ số đánh giá**
- **Precision:**
  $$
  Precision = \frac{15}{15 + 7} = \frac{15}{22} = 0.68
  $$

- **Recall:**
  $$
  Recall = \frac{15}{15 + 4} = \frac{15}{19} = 0.79
  $$

- **F1-score:**
  $$
  F1-score = 2 \times \frac{0.68 \times 0.79}{0.68 + 0.79} = 0.73
  $$

- **Accuracy (dựa trên số dòng đúng, giả sử có tổng cộng 12 log):**
  $$
  Accuracy = \frac{Số\ log\ đúng}{Tổng\ số\ log} = \frac{9}{12} = 0.75
  $$

## 5. Kết luận
Mỗi chỉ số đánh giá cung cấp một góc nhìn khác nhau:
- **Precision:** Quan trọng khi việc nhóm sai các log không liên quan là vấn đề nghiêm trọng.
- **Recall:** Quan trọng khi việc bỏ sót nhóm log đúng có thể gây ảnh hưởng lớn.
- **F1-score:** Cung cấp sự cân bằng giữa Precision và Recall.
- **Accuracy:** Đơn giản nhưng có thể gây hiểu lầm nếu dữ liệu không đồng đều.

Việc hiểu rõ các chỉ số này giúp tối ưu hóa thuật toán phân tích log, cân bằng giữa Precision và Recall để đạt hiệu suất tốt nhất.

## 5. Tại Sao Sử Dụng Cặp Log Thay Vì Từng Dòng Log?
Phân tích log dựa trên **cặp log** thay vì từng dòng riêng lẻ vì:
1. **Mục tiêu chính là nhóm log:** Việc nhóm đúng các log vào sự kiện quan trọng hơn việc chỉ nhận diện từng dòng.
2. **Độ chính xác theo từng cặp:** Nếu hai log nên cùng nhóm nhưng bị tách ra hoặc bị nhóm sai, điều này ảnh hưởng đến đánh giá.
3. **Đánh giá đáng tin cậy hơn:** Đếm từng dòng log có thể gây hiểu lầm vì thuật toán có thể đúng ở mức dòng nhưng sai ở mức nhóm.

## 6. Tại Sao Precision Chia Cho Số Cặp Phân Tích, Còn Recall Chia Cho Số Cặp Thực Tế?
- **Precision = TP / (TP + FP)**
  - Mẫu số là **số cặp phân tích** vì Precision đo lường độ chính xác của các nhóm được phát hiện.
  - Nếu log bị gộp sai quá nhiều, FP tăng lên, làm giảm Precision.
  - Việc tính toán FP, ta phải sử dụng parse

- **Recall = TP / (TP + FN)**
  - Mẫu số là **số cặp thực tế** vì Recall đo lường mức độ nhận diện đúng các nhóm log thực tế.
  - Nếu log bị tách sai, FN tăng lên, làm giảm Recall.
  - Việc tính toán FN ta phải sử dụng real

Precision giúp kiểm soát việc nhóm sai, Recall giúp đảm bảo không bỏ sót nhóm log đúng. F1-score giúp cân bằng cả hai yếu tố để có đánh giá tổng thể chính xác.

