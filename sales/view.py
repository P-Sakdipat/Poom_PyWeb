from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import kagglehub
import os
from functools import lru_cache # 👈 ใช้ Cache เพื่อไม่ให้โหลดข้อมูลใหม่ทุกครั้งที่กราฟรีเฟรช

# 📦 Auto-Connect: โหลดข้อมูลจาก Kaggle
@lru_cache(maxsize=1)
def load_kaggle_data():
    print("กำลังดาวน์โหลด/อัปเดตข้อมูลจาก Kaggle...")
    # *ใส่ชื่อ dataset ของ Kaggle ที่ต้องการตรงนี้* (อันนี้ผมใส่ตัวอย่างไว้ให้)
    path = kagglehub.dataset_download("kyanyoga/sample-sales-data") 
    
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if csv_files:
        # ใช้ pandas อ่านข้อมูล
        return pd.read_csv(os.path.join(path, csv_files[0]), encoding='ISO-8859-1')
    return pd.DataFrame()

def dashboard(request):
    return render(request, 'sales/dashboard.html')

def get_sales_data(request):
    df = load_kaggle_data()
    
    if not df.empty:
        # 🔍 เตรียมข้อมูลสำหรับกราฟ (ตัวอย่าง: จัดกลุ่มยอดขายตามหมวดหมู่สินค้า)
        # ถ้ามี Filter จากผู้ใช้ส่งมา (request.GET) ก็สามารถนำมากรอง df ตรงนี้ได้เลย
        sales_summary = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
        labels = sales_summary['PRODUCTLINE'].tolist()
        data = sales_summary['SALES'].tolist()
        
        # 💰 เตรียมคำนวณ KPIs ส่งไปด้วย
        total_sales = float(df['SALES'].sum())
        total_orders = len(df)
    else:
        labels, data = ["ไม่มีข้อมูล"], [0]
        total_sales, total_orders = 0, 0
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'kpis': {
            'total_sales': f"${total_sales:,.2f}",
            'total_orders': f"{total_orders:,} ออเดอร์"
        }
    })
