# output/

ใส่ผลงานของคุณที่นี่

- ภาพหน้าจอ dashboard หรือผลวิเคราะห์ (`.png`, `.jpg`)
- ลิงก์ผลงานที่เปิดดูได้ (เขียนไว้ในไฟล์นี้)
- ไฟล์ผลลัพธ์เล็ก ๆ ที่สร้างเอง เช่น `dashboard.html`

ห้ามใส่: ไฟล์ข้อมูลดิบที่ซื้อมา (เช่น SETSMART), บทวิเคราะห์โบรกเกอร์, ข้อมูลพอร์ตจริง

## ลิงก์ผลงาน

- [CPALL.BK_valuation.html](CPALL.BK/CPALL.BK_valuation.html): valuation ทีละขั้น พร้อมสมมติฐาน ที่มา และ football field (เปิดในเบราว์เซอร์ได้แบบ offline)
- [CPALL.BK_valuation.xlsx](CPALL.BK/CPALL.BK_valuation.xlsx): Excel ที่ทุกตัวเลขเป็นสูตร แก้สมมติฐานในชีต Inputs แล้วคำนวณใหม่ได้
- [CPALL.BK_results.json](CPALL.BK/CPALL.BK_results.json): ผลคำนวณทั้งหมดในรูป JSON (ใช้สร้าง HTML และตรวจ Excel)

สร้างใหม่ด้วย `.venv/bin/python -m valuation run CPALL.BK` และตรวจ Excel เทียบ Python ด้วย `.venv/bin/python -m valuation verify CPALL.BK`
