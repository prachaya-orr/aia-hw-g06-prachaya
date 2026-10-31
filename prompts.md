# บันทึกขั้นตอน (process log)

> เพิ่ม 1 entry ทุกครั้งก่อน commit ต่อท้ายไฟล์ ห้ามลบของเก่า
> ผู้สอนอ่านไฟล์นี้เพื่อดูวิธีคิดของคุณ ไม่ใช่แค่ผลงานสุดท้าย
> ถ้าใช้ AI ช่วยทำงาน AI จะเขียน entry ให้ตาม AGENTS.md ถ้า commit เอง ให้เขียนเองตามแบบด้านล่าง

---

## รอบ 1 · 2026-10-31 20:13

- **ทำอะไร:** เชื่อมโฟลเดอร์กับ GitHub แล้วเปลี่ยนชื่อ repo เป็น `aia-hw-g06-prachaya` ตามรูปแบบ `aia-hw-เลขกลุ่ม-ชื่อเล่น` · วางแผนโปรเจกต์ใน Plan mode · ร่าง `spec.md` ครบ 5 หัวข้อ และกรอกตารางหัว `README.md`
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · Plan mode
- **Prompt ที่ใช้:**

```text
เปลี่ยนชื่อ อยู่กลุ่ม 6
```

```text
ทำโปรเจค เกี่ยวกับ Valuation / Deep Research ต่อหุ้น เริ่มต้น idea ฉันอยาก deep research valuation method โดยการใช้ notebooklm และอยากมี agent ใน project นี้ไปถามวิธี valuation ใน nlm เพื่อหา method valuation ที่ถูกต้อง โดย source fact พวกค่า ต่างๆ ให้เอามาจา yhfinance ก่อน  และ output เป็น excel format และ output html ที่แสดงวิธีการ valuation step by step พร้อม สมมติฐาน และอยากได้ แบบ football field valuation
```

- **ผลที่ได้:** ได้แผน 5 รอบ (spec → NotebookLM + agent → ดึงข้อมูล → คำนวณ + Excel → HTML + football field) และ `spec.md` ฉบับร่างที่ยืนยันแล้ว ยังไม่มีโค้ดหรือผลงานใน `output/`
- **ตัดสินใจอะไร และเพราะอะไร:** (เลือกจากตัวเลือกที่ AI เสนอพร้อมเหตุผล)
  - ทำเป็น pipeline ที่ใส่ ticker อะไรก็ได้ แทนการทำหุ้นตัวเดียว เพราะอยากใช้ซ้ำกับหุ้นตัวอื่น โดยทดสอบกับ CPALL.BK
  - สร้าง NotebookLM notebook ใหม่ "Valuation Methods" ด้วย deep research และคัด source เองก่อน import เพราะยังไม่มี notebook ที่รวมวิธี valuation โดยเฉพาะ
  - Rf ใช้ ThaiBMA 10 ปี (หุ้นไทย) หรือ `^TNX` (หุ้นสหรัฐ) และ ERP/CRP ใช้ Damodaran เพราะ Yahoo Finance ไม่มีค่าเหล่านี้ และทั้งสองแหล่งให้ URL กับวันที่อ้างอิงได้
  - agent เป็น Claude subagent ที่เรียก `nlm` CLI เพราะแยก context ได้ บันทึกคำถาม-คำตอบพร้อม citation ลงไฟล์ และ AI ค่ายอื่นอ่านขั้นตอนได้
  - ไม่ใส่ analyst target price จาก Yahoo ใน football field เพราะ README ห้ามใช้บทวิเคราะห์โบรกเกอร์
- **ขั้นต่อไป:** รอบ 2 สร้าง notebook + researcher agent + `research/playbook.md` · รอบ 3 โค้ดดึงข้อมูล (สองรอบนี้ทำคู่ขนานคนละ session)
