# sử dụng Python Alpine
FROM python:3.9-alpine

# đặt thư mục làm việc
WORKDIR /app

# cài đặt các gói hệ thống cần thiết trước để tận dụng caching Docker layer
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev

# sao chép file requirement.txt trước để sử dụng cache của Docker
COPY requirements.txt .

# cài đặt thư viện cần thiết trước (tận dụng caching layer)
RUN pip install --no-cache-dir -r requirements.txt

# sao chép toàn bộ code vào container
COPY . .

# mở cổng 5000
EXPOSE 5000

#chạy ứng dụng
CMD ["python", "app.py"]
