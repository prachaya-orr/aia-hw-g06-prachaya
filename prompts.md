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

---

## รอบ 3 · 2026-10-31 21:02

- **ทำอะไร:** เขียน package `valuation/` ส่วนดึงข้อมูล: `python -m valuation fetch <TICKER> [--peers ...]` ดึงราคา, งบรายปี, ปันผลจาก Yahoo Finance (yfinance) · Rf จาก ThaiBMA 10 ปี (ticker `.BK`) หรือ `^TNX` · ERP/CRP จากตาราง Damodaran · ค่าคงที่ทั้งหมดอยู่ใน `config.yaml` · ทุกค่าเก็บเป็น `{value, source, url, fetched_at, asof}` ถ้าหาไม่ได้เป็น null พร้อมเหตุผล
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 effort high · แยกเป็น session ของตัวเอง · Python 3.12 ใน `.venv` (สร้างด้วย `uv`)
- **Prompt ที่ใช้:** ไม่มี prompt ที่ผู้เรียนพิมพ์ในรอบนี้ งานเริ่มจากการ์ดที่ AI เสนอใน session หลักและผู้เรียนกดเริ่ม (brief: ดึงข้อมูลจาก yfinance/ThaiBMA/Damodaran ตามแหล่งที่เลือกในรอบ 1 ทุกค่าต้องมีที่มา ห้ามเดา)
- **ผลที่ได้:** ดึง CPALL.BK และ AAPL ได้ครบ ไม่มีค่าไหนขาดที่มา · ราคา, จำนวนหุ้น และ FCF ปี 2025 ของ CPALL ตรงกับหน้า Yahoo Finance · เอารูปแบบโค้ดมาจาก `data/fetch.py` ของ workspace คอร์ส · ปัญหาข้อมูลที่เจอบันทึกใน `PROJECT_MEMORY.md`
- **ตัดสินใจอะไร และเพราะอะไร:**
  - ไม่ commit `data/raw/` เพราะดึงใหม่ได้ทุกเมื่อ และเป็นไฟล์ดิบขนาดใหญ่
  - ใช้ Python 3.12 แทน 3.15 ของเครื่อง เพราะ yfinance/pandas อาจยังไม่รองรับเวอร์ชันใหม่
  - ใช้แหล่ง Rf และ ERP ตามที่ผู้เรียนเลือกในรอบ 1
- **หมายเหตุ:** `fetch.py`, `config.yaml` และ `__main__.py` ใน commit นี้มีส่วนที่รอบ 4 เพิ่มแล้วด้วย (beta อุตสาหกรรม, synthetic rating, minority proxy, คำสั่ง draft/run/verify) เพราะแก้ไฟล์เดียวกันก่อนได้ commit
- **ขั้นต่อไป:** เขียนส่วนคำนวณและ Excel (รอบ 4)

---

## รอบ 4 · 2026-10-31 21:02

- **ทำอะไร:**
  - เขียน `valuation/assumptions.py` (ร่างสมมติฐานจากข้อมูลจริง ทุกค่ามีที่มา), `methods.py` (DCF FCFF, DDM, comps P/E · EV/EBITDA · P/BV, ช่วง 52 สัปดาห์), `excel.py` (Excel 9 ชีต สูตรจริงทั้งหมด), `pipeline.py` และ `verify.py` (ให้ LibreOffice คำนวณ Excel ใหม่แล้วเทียบกับ Python)
  - เพิ่มการดึง unlevered beta รายอุตสาหกรรม และตาราง synthetic rating จาก Damodaran และ P/BV ของบริษัทลูกที่จดทะเบียน (CPAXT.BK)
  - ปรับโมเดลตาม playbook: Rf หัก country default spread, Kd = Rf + default spread, terminal reinvestment = g ÷ ROC, minority interest ตามมูลค่าตลาด, คำเตือนเมื่อสมมติฐานขัดกับ playbook
  - เขียน `research/CPALL.BK_method_choice.md` และ `assumptions/CPALL.BK.yaml` (status: reviewed)
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · LibreOffice headless สำหรับตรวจ Excel
- **Prompt ที่ใช้:**

```text
Apply all
```

```text
Save first
```

- **ผลที่ได้:** `output/CPALL.BK/CPALL.BK_valuation.xlsx` และ `CPALL.BK_results.json` · Excel ตรงกับ Python ทั้ง 15 ค่า (ต่างกัน 0.0000%) · ผล CPALL (ราคา ฿43.75, WACC 6.49%): DCF ฿28.78–44.13 (base 35.85), P/E ฿42.83–57.94 (base 52.67), EV/EBITDA ฿18.86–61.04 (base 36.00), 52 สัปดาห์ ฿40.50–54.50 · ยังขาด: HTML ทีละขั้น และ football field ใน HTML (รอบ 5) · terminal value เป็น 77% ของ EV และ peer มีแค่ 3 ตัว
- **ตัดสินใจอะไร และเพราะอะไร:**
  - AI เปลี่ยนจาก beta ของ Yahoo (0.44) เป็น bottom-up beta (unlevered beta อุตสาหกรรม Retail Grocery ตลาดเกิดใหม่ 0.856 relever ได้ 1.63) เพราะ beta 0.44 ทำให้ WACC 3.8% และ DCF ได้ ฿293 ต่อหุ้น ซึ่งผิดชัดเจน และ playbook §3 บอกว่า regression beta มี standard error สูง
  - ผู้เรียนยืนยันข้อเสนอ 4 ข้อ:
    1. peer เป็นร้านสะดวกซื้อ 3 ตัว (2912.TW, 3382.T, AMRT.JK) เพราะตรงเกณฑ์ peer ใน playbook §9 มากกว่า BJC.BK (หลายธุรกิจ) และ CRC.BK (ห้างสรรพสินค้า)
    2. capex = D&A (4.05% ของรายได้) เพราะ capex เฉลี่ยในอดีต 3.07% ต่ำกว่า D&A ทำให้ reinvestment ติดลบทั้งที่รายได้โต (playbook §12 ข้อ 4) สาเหตุคือค่าเสื่อมของสัญญาเช่าตาม TFRS 16
    3. ROC ช่วง terminal = WACC เพราะ playbook §4 บอกให้ excess return เข้าหา 0
    4. terminal growth 0.80% = Rf เพราะ playbook §4 บอกว่า g ไม่ควรเกิน Rf
  - ตัด DDM ออกจาก football field ของ CPALL เพราะปันผลเทียบ FCFE ผันผวนมากช่วงลดหนี้ (playbook §1, §5) และตัด P/BV เพราะเหมาะกับธนาคาร (§9)
- **ขั้นต่อไป:** รอบ 5 สร้าง HTML อธิบาย valuation ทีละขั้นพร้อมสมมติฐานและ football field · ตรวจปัญหา EV/EBITDA ของ yfinance ไม่ตรงกับหน้าเว็บ
