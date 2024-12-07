import os

class LocalStorageFlask:
    def __init__(self, app=None):
        """
        Khởi tạo thư viện và kết nối với Flask nếu ứng dụng Flask được truyền.
        """
        self.commands = []  # Danh sách lệnh JS sẽ được thêm vào localStorage
        self.output_path = None  # Đường dẫn file JS
        if app is not None:
            self.init_app(app)
        print("The variables you set in localstorage.getItem can be used in javascript to display local storage in html or...")

    def init_app(self, app):
        """
        Kết nối với ứng dụng Flask.
        """
        self.app = app
        # Đường dẫn để lưu file JS
        self.output_path = os.path.join(app.static_folder, "js", "localstorage_script.js")
        # Tạo context processor để tự động chèn script
        app.after_request(self.after_request)

    def after_request(self, response):
        """
        Tự động chèn mã JS vào phản hồi trả về.
        """
        if self.commands:
            self.generate_js_file()
            # Chèn script vào phản hồi (tự động thêm vào HTML)
            response.data = response.data.decode('utf-8').replace(
                "</body>",
                f'<script src="/static/js/localstorage_script.js"></script></body> <!-- The variables you set in localstorage.getItem can be used in javascript to display local storage in html or... -->'
            ).encode('utf-8')
        return response

    def setItem(self, key, value):
        """
        Thêm mục vào localStorage.
        """
        self.commands.append(f'localStorage.setItem("{key}", "{value}");')

    def getItem(self, key, var_name):
        """
        Lấy mục từ localStorage và gán giá trị vào biến JavaScript.
        """
        if not var_name:
            raise ValueError("var_name is required for getItem.")
        self.commands.append(f'var {var_name} = localStorage.getItem("{key}");')

    def removeItem(self, key):
        """
        Xóa mục khỏi localStorage.
        """
        self.commands.append(f'localStorage.removeItem("{key}");')

    def clear(self):
        """
        Xóa toàn bộ localStorage.
        """
        self.commands.append("localStorage.clear();")

    def generate_js_file(self):
        """
        Ghi mã JavaScript từ lệnh đã thu thập vào file JS.
        """
        if not self.output_path:
            raise RuntimeError("LocalStorageFlask is not initialized with Flask.")

        js_code = "\n".join(self.commands)
        self.commands.clear()  # Xóa lệnh sau khi ghi file

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(f"if (typeof(Storage) !== 'undefined') {{\n{js_code}\n}} else {{\nconsole.error('localStorage is not supported.');\n}}")