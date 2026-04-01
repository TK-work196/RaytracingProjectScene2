# นี่คือ Scene ที่ 2 สำหรับ Final Project
# การตั้งค่า (Configuration Guide)
ปรับแต่งคุณภาพของภาพผ่านไฟล์ rt_config.py:

## ความละเอียดของภาพ
```python
width = 3840   # ความกว้าง
height = 1440  # ความสูง
```

## คุณภาพของภาพ
```python
samples_per_pixel = 1024  # จำนวนตัวอย่างแสงต่อพิกเซล
max_depth = 3             # จำนวนครั้งที่แสงสะท้อนได้สูงสุด
```

## ติดตั้ง Library ที่จำเป็น:

```bash
pip install taichi numpy Pillow
```

เริ่มการเรนเดอร์:

```Bash
python main.py
```
รูปภาพจะถูกบันทึกในชื่อ football_court_final.png

# จัดทำโดย

นาย ธันยธรณ์ เกศเมตตา 6710404986 <br>
นางสาว จิรัชญา นนทนารักษ์ 6710404901# RaytracingScene1
# RaytracingProjectScene2
