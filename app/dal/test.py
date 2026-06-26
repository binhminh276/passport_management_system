# Chạy 1 lần trong Python để tạo hash đúng
import bcrypt
print(bcrypt.hashpw("123".encode(), bcrypt.gensalt()).decode())