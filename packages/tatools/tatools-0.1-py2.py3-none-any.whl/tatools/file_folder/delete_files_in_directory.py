import os


def delete_files_in_directory(directory, extension=".npy"):
    if not os.path.exists(directory):
        print(f"Đường dẫn không tồn tại: {directory}")
        return

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extension):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Đã xóa: {file_path}")
                except Exception as e:
                    print(f"Lỗi khi xóa {file_path}: {e}")


def iconsole_delete_files():
    import argparse

    parser = argparse.ArgumentParser( description="Xóa tất cả các file có đuôi chỉ định trong thư mục và các thư mục con." )
    parser.add_argument( "--directory", type=str, help="Đường dẫn đến thư mục cần xóa các file" )
    parser.add_argument( "--ext", type=str, help="Phần mở rộng của file cần xóa (ví dụ: .npy)" )

    args = parser.parse_args()

    print("Thực hiện xóa các file với tham số:")
    print("Thư mục:", args.directory)
    print("Phần mở rộng:", args.ext)

    delete_files_in_directory(args.directory, args.ext)

# # Cách dùng: python your_script.py directory .npy
