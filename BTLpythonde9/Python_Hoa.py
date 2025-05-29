import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình Quản Lý Thư Mục")

        # Frame chính
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Nút chọn thư mục
        self.select_button = tk.Button(self.main_frame, text="Chọn Thư Mục", command=self.select_folder)
        self.select_button.pack(pady=5)

        # Treeview hiển thị danh sách file
        self.tree = ttk.Treeview(self.main_frame, columns=("Tên File", "Loại"), show="headings")
        self.tree.heading("Tên File", text="Tên File")
        self.tree.heading("Loại", text="Loại File")
        self.tree.column("Tên File", width=300)
        self.tree.column("Loại", width=100)
        self.tree.pack(fill="both", expand=True, pady=5)

        # Nút mở file
        self.open_button = tk.Button(self.main_frame, text="Mở File", command=self.open_file)
        self.open_button.pack(pady=5)

        # Gắn sự kiện double-click để mở file
        self.tree.bind("<Double-1>", self.open_file)

        # Biến lưu đường dẫn thư mục
        self.current_folder = ""

    def select_folder(self):
        # Mở dialog chọn thư mục
        folder = filedialog.askdirectory(title="Chọn Thư Mục")
        if folder:
            self.current_folder = folder
            self.show_files()

    def show_files(self):
        # Xóa nội dung Treeview hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Kiểm tra thư mục hợp lệ
        if not os.path.isdir(self.current_folder):
            messagebox.showerror("Lỗi", "Thư mục không hợp lệ hoặc không tồn tại.")
            return

        try:
            # Lọc các file với phần mở rộng .txt, .py, .jpg
            valid_extensions = (".txt", ".py", ".jpg")
            for file_name in os.listdir(self.current_folder):
                if file_name.lower().endswith(valid_extensions):
                    file_path = os.path.join(self.current_folder, file_name)
                    if os.path.isfile(file_path):
                        # Xác định loại file
                        ext = os.path.splitext(file_name)[1].lower()
                        file_type = {
                            ".txt": "Text",
                            ".py": "Python",
                            ".jpg": "Image"
                        }.get(ext, "Unknown")
                        # Thêm vào Treeview
                        self.tree.insert("", "end", values=(file_name, file_type))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể liệt kê file: {e}")

    def open_file(self, event=None):
        # Lấy item được chọn trong Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một file để mở.")
            return

        # Lấy tên file từ Treeview
        file_name = self.tree.item(selected_item)["values"][0]
        file_path = os.path.join(self.current_folder, file_name)

        try:
            # Mở file bằng chương trình mặc định
            os.startfile(file_path)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file: {file_name}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManager(root)
    root.geometry("450x400")  # Kích thước cửa sổ
    root.mainloop()