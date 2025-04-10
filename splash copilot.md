# 📘 GitHub Copilot Chat Cheat Sheet (Tiếng Việt)

Sử dụng bảng này để tham khảo nhanh các lệnh thường dùng trong **GitHub Copilot Chat**. Bao gồm các lệnh slash, biến chat và chuyên gia hỗ trợ.

---

## 💬 Slash Commands (Lệnh dấu gạch chéo `/`)

| Lệnh               | Mô tả                                                                 |
|--------------------|----------------------------------------------------------------------|
| `/clear`           | Xoá cuộc trò chuyện hiện tại hoặc bắt đầu trò chuyện mới             |
| `/new`             | Bắt đầu cuộc trò chuyện mới hoặc tạo dự án mới (tùy môi trường)      |
| `/rename`          | Đổi tên cuộc trò chuyện                                               |
| `/delete`          | Xoá cuộc trò chuyện                                                   |
| `/explain`         | Giải thích đoạn mã đang mở trong trình soạn thảo                     |
| `/fix`             | Đề xuất sửa lỗi cho đoạn mã đã chọn                                   |
| `/fixTestFailure`  | Sửa lỗi cho bài test bị thất bại                                      |
| `/tests`           | Tạo unit test cho đoạn mã được chọn                                   |
| `/optimize`        | Phân tích và tối ưu hiệu năng đoạn mã                                 |
| `/simplify`        | Đơn giản hóa đoạn mã hiện tại                                         |
| `/doc`             | Tạo ghi chú tài liệu cho đoạn mã hoặc biểu tượng                      |
| `/help`            | Hiển thị hướng dẫn cơ bản về cách dùng Copilot Chat                   |

---

## #️⃣ Biến Chat (Chat Variables)

Dùng để thêm ngữ cảnh từ mã nguồn vào yêu cầu. Gõ `#` rồi chọn biến phù hợp.

| Biến          | Mô tả                                                        |
|---------------|--------------------------------------------------------------|
| `#block`      | Toàn bộ khối mã hiện tại                                     |
| `#class`      | Lớp hiện tại                                                 |
| `#comment`    | Ghi chú hiện tại                                             |
| `#file`       | Toàn bộ nội dung của file hiện tại                           |
| `#function`   | Hàm hoặc phương thức hiện tại                                |
| `#line`       | Dòng mã hiện tại                                             |
| `#path`       | Đường dẫn của file                                           |
| `#project`    | Bối cảnh toàn bộ dự án                                       |
| `#selection`  | Đoạn văn bản đang được chọn                                  |
| `#sym`        | Biểu tượng hiện tại (tên hàm, lớp, biến...)                 |

---

## 👤 Chat Participants (Chuyên gia hỗ trợ - dùng `@`)

Sử dụng `@` để gọi chuyên gia Copilot có chuyên môn theo từng lĩnh vực cụ thể.

| Tên chuyên gia | Mô tả                                                                                   |
|----------------|------------------------------------------------------------------------------------------|
| `@github`      | Hỗ trợ các kỹ năng liên quan đến GitHub                                                 |
| `@azure`       | Hỗ trợ triển khai, sử dụng và quản lý dịch vụ Azure                                     |
| `@terminal`    | Hỗ trợ lệnh và nội dung trong terminal (VS Code)                                        |
| `@vscode`      | Hiểu các tính năng, phím tắt và lệnh trong VS Code                                      |
| `@workspace`   | Nắm được cấu trúc toàn dự án để tư vấn về thiết kế và tổ chức mã                        |
| `@project`     | (trong JetBrains) Tương tự `@workspace`, nắm ngữ cảnh toàn bộ dự án                    |

---

## 🔍 Ví dụ sử dụng

```text
/fix #selection


link: https://github.com/github/docs/blob/main/content/copilot/using-github-copilot/copilot-chat/github-copilot-chat-cheat-sheet.md?utm_source=chatgpt.com 