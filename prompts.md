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

---

## รอบ 2 · 2026-10-31 21:02

- **ทำอะไร:** สร้าง NotebookLM notebook "Valuation Methods" (alias `valuation-methods`) ด้วย `nlm research --mode deep` · สร้าง subagent `.claude/agents/valuation-researcher.md` ที่ถาม notebook ผ่าน `nlm` แล้วบันทึกคำตอบพร้อม citation · ถาม notebook 15 หัวข้อ ได้ log ใน `research/nlm_log/` · รวมเป็น `research/playbook.md` · ทำรอบเสริมแบบ deep แล้วถามซ้ำ 6 หัวข้อ (log `-v2`) และเรื่อง IFRS 16
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 effort high · แยกเป็น session ของตัวเองจาก session หลัก · `nlm` CLI 0.15.8
- **Prompt ที่ใช้:** งานเริ่มจากการ์ดที่ AI เสนอใน session หลัก (brief: สร้าง notebook, ให้ผู้เรียนเลือก source ก่อน import, สร้าง agent, เขียน playbook ที่ทุกข้อมี citation) ผู้เรียนกดเริ่ม แล้วเลือก source ผ่านคำถามของ AI prompt ที่ผู้เรียนพิมพ์เอง:

```text
ไม่ได้ให้ใช้แบบ deep ทุกอัน
```

- **ผลที่ได้:** notebook มี 32 source ที่ผู้เรียนเลือกเอง (NotebookLM เสนอ 83 รายการ เลือก 33 import สำเร็จ 32) · playbook 15 หัวข้อ ทุกข้อระบุชื่อ source และแยกส่วน "ไม่พบใน notebook" ไว้ชัด · รอบ v2 ตรวจเทียบกับข้อความใน source แล้วพบว่ารอบแรกเขียนเกินหลักฐาน 2 เรื่อง (กฎ percentile 25/75 ของ football field และสูตร PEG) จึงย้ายไปไว้ใน "ไม่พบใน notebook" · ยังขาด: Rf/ERP/CRP ของไทย, กฎจับคู่ EV กับ EBITDA หลัง IFRS 16, ข้อมูลเฉพาะของไทย
- **ตัดสินใจอะไร และเพราะอะไร:**
  - เลือก source กลุ่มที่ AI แนะนำ (Damodaran/NYU Stern, งานวิชาการ, แหล่งฝึกอบรมที่รู้ผู้เขียน) และตัดรายงานที่ NotebookLM เขียนเอง, Scribd/SlideShare, YouTube, เว็บแจก ebook เพราะถ้าใส่ไว้ agent จะ cite ข้อความที่ AI สร้างหรือไม่รู้ที่มาแทน source จริง
  - สั่งให้ค้นรอบเสริมใหม่แบบ deep เพราะ brief สั่ง deep แต่ AI ใช้ fast เองในรอบเสริมแรก
  - ให้ agent ตอบเฉพาะจาก notebook และยกข้อความไม่เกิน 15 คำ เพราะ repo เป็น Public และ source ติดลิขสิทธิ์
- **ขั้นต่อไป:** ใช้ playbook เลือกวิธีและตั้งสมมติฐานของ CPALL (รอบ 4)

