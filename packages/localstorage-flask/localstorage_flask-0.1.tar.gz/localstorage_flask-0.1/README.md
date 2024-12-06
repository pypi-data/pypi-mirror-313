LocalStorageFlask
LocalStorageFlask là một thư viện dành cho Flask giúp bạn dễ dàng thao tác với localStorage trong trình duyệt người dùng từ phía server. Thư viện này hỗ trợ các lệnh để lưu trữ, truy xuất và xóa dữ liệu trong localStorage.

Cài đặt
Để cài đặt LocalStorageFlask, bạn có thể cài đặt thư viện từ PyPI bằng lệnh sau:
```bash
pip install localstorage-flask
```
Cách sử dụng
Mã Python (Flask)
Đầu tiên, bạn cần khởi tạo một ứng dụng Flask và sử dụng thư viện LocalStorageFlask.
```python
from flask import Flask, render_template
from localstorage_flask import LocalStorageFlask

app = Flask(__name__)

# Khởi tạo thư viện LocalStorageFlask
localstorage = LocalStorageFlask(app)

@app.route("/")
def index():
    # Lưu thông tin vào localStorage
    localstorage.setItem("username", "currentUser")
    localstorage.setItem("theme", "dark")

    # Lấy dữ liệu từ localStorage
    username = localstorage.getItem("username", "username")
    theme = localstorage.getItem("theme", "theme")

    # Trả về trang HTML với mã JavaScript cần thiết
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```
Mã HTML Template
Trong mã HTML này, bạn có thể tương tác với localStorage và hiển thị dữ liệu từ localStorage sau khi lấy từ Flask.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LocalStorage Example</title>
</head>
<body>
    <h1>Welcome to LocalStorageFlask</h1>
    <p>Open the browser's console to see localStorage operations in action.</p>

    <h2>LocalStorage Data:</h2>
    <p id="username">Username: </p>
    <p id="theme">Theme: </p>

    <button id="fetchDataBtn">Fetch LocalStorage Data</button>

    <script>
        document.getElementById("fetchDataBtn").addEventListener("click", function() {
            // Hiển thị giá trị từ localStorage vào các phần tử trên HTML
            document.getElementById("username").innerText = "Username: " + username;
            document.getElementById("theme").innerText = "Theme: " + theme;
        });
    </script>
</body>
</html>
```
Các lệnh để tương tác với localStorage
Dưới đây là các lệnh mà bạn có thể sử dụng để tương tác với localStorage thông qua thư viện LocalStorageFlask.

1. Lưu trữ dữ liệu vào localStorage
Sử dụng lệnh sau để lưu trữ dữ liệu vào localStorage:
```python
localstorage.setItem("key", "value")
```
key: Tên của mục bạn muốn lưu.
value: Giá trị bạn muốn lưu trữ.
3. Lấy dữ liệu từ localStorage
Để lấy dữ liệu từ localStorage, sử dụng lệnh sau:
```python
localstorage.getItem("key", "variable_name")
```
key: Tên của mục mà bạn muốn lấy dữ liệu.
variable_name: Tên biến JavaScript sẽ chứa giá trị của mục đã lấy.
3. Xóa mục khỏi localStorage
Để xóa một mục khỏi localStorage, sử dụng lệnh sau:
```python
localstorage.removeItem("key")
```
key: Tên của mục bạn muốn xóa.
4. Xóa toàn bộ dữ liệu trong localStorage
Sử dụng lệnh sau để xóa toàn bộ dữ liệu trong localStorage:
```python
localstorage.clear()
```
Kết luận
LocalStorageFlask giúp bạn dễ dàng thao tác với localStorage trong các ứng dụng Flask. Các lệnh trên cho phép bạn lưu trữ, lấy và xóa dữ liệu từ localStorage mà không cần phải phụ thuộc vào cơ sở dữ liệu.