# ใช้ Python เวอร์ชัน 3.10 แบบเบาๆ (slim)
FROM python:3.10-slim

# ไม่ให้ Python เขียนไฟล์ .pyc และให้แสดง log ทันที
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# กำหนดโฟลเดอร์ทำงานใน Docker
WORKDIR /app

# ก๊อปปี้ requirements.txt ไปก่อนแล้วติดตั้ง
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ก๊อปปี้ไฟล์โปรเจกต์ทั้งหมดของเราเข้าไปใน Docker
COPY . /app/

# เปิดพอร์ต 8000 ให้คนภายนอกเข้ามาได้
EXPOSE 8000

# คำสั่งสำหรับรันเซิร์ฟเวอร์ Django (สำคัญ: ต้องใช้ 0.0.0.0 เพื่อให้ Docker ส่งต่อพอร์ตได้)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]