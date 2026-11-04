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

---

## รอบ 5 · 2026-10-31 21:13

- **ทำอะไร:**
  - สร้าง HTML ทีละขั้น `output/CPALL.BK/CPALL.BK_valuation.html` (`valuation/html.py` + `valuation/templates/report.html`) มี 9 ส่วน: football field, วิธีที่เลือกและเหตุผล, WACC, DCF, sensitivity, comps, สมมติฐานทั้งหมดพร้อมที่มา, คำเตือนและข้อจำกัด, แหล่งข้อมูล
  - แก้ปัญหา EV/EBITDA ของ yfinance ที่ค้างจากรอบ 4: คิด EV/EBITDA ของ peer เองจากงบรายปี และเปลี่ยน P/E ให้ใช้ EPS ย้อนหลัง 12 เดือน
  - ทำให้ pipeline ใช้กับ ticker อื่นได้จริง: นับ minority/lease ที่ไม่มีในงบเป็น 0, ดึงข้อมูลใหม่เองเมื่อโครง JSON เปลี่ยน, แจ้งชื่อ input ที่ขาดแทน error
  - อัปเดต `research/CPALL.BK_method_choice.md` และ `output/README.md`
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · browser pane ตรวจ HTML ขนาด desktop และมือถือ · LibreOffice headless ตรวจ Excel
- **Prompt ที่ใช้:**

```text
Start round 5
```

```text
Save round 5
```

- **ผลที่ได้:** HTML ไฟล์เดียวเปิดได้แบบ offline รองรับมือถือ (กว้าง 375px ไม่มี scroll แนวนอน) และ dark mode · Excel ตรงกับ Python ทั้ง 15 ค่า · ผล CPALL (ราคา ฿43.75): DCF ฿28.78–44.13 (ราคาอยู่ในช่วง), P/E ฿46.43–62.80 (ราคาต่ำกว่าช่วง), EV/EBITDA −฿6.44–14.50 (ราคาสูงกว่าช่วง), 52 สัปดาห์ ฿40.50–54.50 · ทดสอบ AAPL รันจบและ Excel ตรงกับ Python ทั้ง 12 ค่า แต่ลบไฟล์ทิ้งเพราะสมมติฐานยังเป็นร่างที่ไม่ได้รีวิว · ยังขาด: ตรวจ dark mode ด้วยตาจริง (pane แสดงไฟล์ local เป็นโหมดสว่างเสมอ จึงตรวจจากสีที่คำนวณได้แทน)
- **ตัดสินใจอะไร และเพราะอะไร:**
  - AI เลิกใช้ `enterpriseToEbitda` ของ Yahoo แล้วคิดเองจากงบรายปี เพราะ Yahoo ใช้ EV ที่รวมหนี้สัญญาเช่าแต่หารด้วย EBITDA ย้อนหลัง 12 เดือนที่ยังหักค่าเช่า (2912.TW: Yahoo 13.65 เท่า คิดเอง 7.37 เท่า) นิยามที่คิดเองให้ CPALL 10.62 เท่า ใกล้กับ 10.67 ที่หน้าเว็บ Yahoo แสดง
  - EV/EBITDA หัก minority ตาม book ขณะที่ DCF หักตามมูลค่าตลาด เพราะ EV ของ peer รวม minority ตาม book ต้องหักกลับด้วยนิยามเดียวกัน
  - ทำ football field เป็นแท่ง HTML/CSS แทนรูป SVG เพราะย่อตามจอมือถือได้โดยตัวหนังสือไม่เล็กลง และไม่ต้องโหลดไลบรารีจากเน็ต
- **ขั้นต่อไป:** เขียน `help.md` 3 ข้อ · ตรวจว่า repo เปิดได้จากหน้าต่าง incognito · ส่งลิงก์ repo

---

## รอบ 6 · 2026-10-31 21:22

- **ทำอะไร:** เขียน `help.md` 3 ข้อจากปัญหาที่ยังไม่มีคำตอบในโปรเจกต์: EV/EBITDA หลัง IFRS 16 ของหุ้นที่หนี้และ minority interest สูง, Rf ของไทยกับ terminal growth, และการเลือก peer ของ CPALL
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5
- **Prompt ที่ใช้:**

```text
Draft help.md
```

```text
Save
```

- **ผลที่ได้:** `help.md` ครบ 3 ข้อ แต่ละข้อมีสิ่งที่อยากได้ สิ่งที่ลองแล้ว ผลจริงพร้อมตัวเลข และคำถามที่อยากให้ผู้สอนตอบ · ยังขาด: ตรวจว่า repo เปิดได้จากหน้าต่าง incognito และส่งลิงก์ในห้อง
- **ตัดสินใจอะไร และเพราะอะไร:** เลือกเฉพาะปัญหาที่ยังเปิดอยู่ ไม่เอาปัญหาที่แก้แล้ว (เช่น `#NAME?` ใน Excel หรือ beta ของ Yahoo) เพราะ `help.md` มีไว้ให้ผู้สอนเตรียมคำตอบใน Repair Clinic ทั้ง 3 ข้อเป็นเรื่องที่ NotebookLM ไม่มีคำตอบตรง ๆ และเปลี่ยนผล valuation มาก
- **ขั้นต่อไป:** เปลี่ยนสถานะใน `spec.md` และ `README.md` เป็นพร้อมตรวจ · ตรวจ repo จากหน้าต่าง incognito · ส่งลิงก์ผ่าน Google Form ในห้อง

---

## รอบ 7 · 2026-10-31 21:38

- **ทำอะไร:** สร้าง `docs/workflow.md` เป็น sequence diagram แบบ mermaid แสดงภาพรวมของโปรแกรม 6 ช่วง (ค้นวิธีจาก NotebookLM → ดึงข้อมูล → ร่างและรีวิวสมมติฐาน → คำนวณและสร้าง Excel/HTML → ตรวจ Excel เทียบ Python → `/save`) พร้อมตารางไฟล์ของแต่ละขั้นและคำสั่งที่ใช้บ่อย
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · browser pane ตรวจว่า mermaid render ได้
- **Prompt ที่ใช้:**

```text
สร้าง sequence workflow โดยใช้ mermaid เก็บไว้เพื่อทำความเข้าใจภาพรวมของโปรแกรมตอนนี้ให้ดูหน่อย
```

```text
Save
```

- **ผลที่ได้:** แผนภาพ parse และ render ผ่านด้วย mermaid 11.4.1 ใน browser และ GitHub แสดงแผนภาพในไฟล์ .md ให้เอง · มีผู้เล่น 13 ตัว แผนภาพจึงกว้าง บนจอเล็กต้องเลื่อนดูด้านข้าง
- **ตัดสินใจอะไร และเพราะอะไร:** ใช้ sequence diagram ตามที่ผู้เรียนขอ แบ่ง 6 ช่วงด้วยสีให้เห็นลำดับงานชัด และเก็บเป็นไฟล์ .md ใน `docs/` เพราะ GitHub render mermaid ให้โดยไม่ต้องติดตั้งอะไร
- **ขั้นต่อไป:** เปลี่ยนสถานะใน `spec.md` และ `README.md` เป็นพร้อมตรวจ · ตรวจ repo จากหน้าต่าง incognito · ส่งลิงก์ผ่าน Google Form ในห้อง

---

## รอบ 8 · 2026-10-31 21:54

- **ทำอะไร:**
  - ใช้ pipeline เดิมกับหุ้นตัวที่สอง BDMS.BK (บริษัทกรุงเทพดุสิตเวชการ) ได้ `output/BDMS.BK/BDMS.BK_valuation.xlsx`, `.html` และ `_results.json`
  - เพิ่ม `Medical Care Facilities: Hospitals/Healthcare Facilities` ใน `config.yaml` (industry_map) เพื่อให้ดึง unlevered beta ของอุตสาหกรรมโรงพยาบาลจาก Damodaran ได้
  - เขียน `assumptions/BDMS.BK.yaml` (status: reviewed) และ `research/BDMS.BK_method_choice.md` (เลือกวิธี, discount rate, ตารางสมมติฐานที่เปลี่ยนผลมากที่สุด, เลือก peer, อ่าน football field)
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · LibreOffice headless ตรวจ Excel · browser pane ตรวจ HTML
- **Prompt ที่ใช้:**

```text
valuation BDMS
```

```text
ยืนยันตามร่าง
```

```text
Save
```

- **ผลที่ได้:** Excel ตรงกับ Python ทั้ง 15 ค่า (ต่างกัน 0.0000%) · ผล BDMS (ราคา ฿19.60, WACC 4.89%): DCF ฿24.02–30.46 (base 26.90) ราคาต่ำกว่าช่วง, P/E ฿16.95–21.99 (base 19.48) ราคาอยู่ในช่วง, EV/EBITDA ฿14.84–18.67 (base 15.81) ราคาสูงกว่าช่วง, 52 สัปดาห์ ฿17.40–22.40 · สรุป: ราคาอยู่ในช่วงมูลค่ายุติธรรม ยังไม่เห็นส่วนลดชัดเจน · ยังขาด: beta ช่วง terminal ที่ playbook §4 บอกให้เข้าใกล้ 1 (โมเดลใช้ WACC เดียวทั้งโมเดล ถ้าใช้ beta ≈ 1 DCF เหลือ ฿16.88–20.18) และ terminal value สูงถึง 85% ของ EV
- **ตัดสินใจอะไร และเพราะอะไร:**
  - AI ตัด DDM เพราะปันผล ÷ FCFE ของ BDMS อยู่นอกช่วง 80–110% เกือบทุกปี (2023: 2.40 เท่า, 2025: 1.33 เท่า) ตาม playbook §1, §5 และตัด P/BV เพราะเหมาะกับธนาคาร และ book มี goodwill ฿17.5 พันล้าน (§9)
  - ผู้เรียนยืนยันข้อเสนอ 4 ข้อของ AI ตามร่าง ("ยืนยันตามร่าง"):
    1. peer เป็นโรงพยาบาลเอกชนไทย 4 ตัว (BH, BCH, CHG, PR9) เพราะสกุลเงิน country risk และมาตรฐานบัญชีเดียวกัน ตัด THG (P/E 55.8 เท่า ผิดปกติ), VIBHA (กำไรพึ่งเงินลงทุน), RJH และ EKH (เล็กกว่า ฿5 พันล้าน) และโรงพยาบาลต่างประเทศ (บทเรียนจาก help.md ข้อ 3)
    2. รายได้โตตาม CAGR 2022–2025 6.65% ทุกปี (ทางเลือกที่ลดลงเส้นตรงหา g ได้ base ฿24.29)
    3. ROC ช่วง terminal = WACC กฎเดียวกับ CPALL ตาม playbook §4 (ใช้ ROC ในอดีต 13.89% ได้ base ฿29.92)
    4. minority interest แปลงเป็นมูลค่าตลาดด้วยมัธยฐาน P/BV ของ peer 2.27 เท่า เพราะ BDMS ไม่มีบริษัทลูกที่จดทะเบียน playbook §2 ให้ใช้ P/B ของ sector
  - AI ทดลองเปลี่ยนสมมติฐานทีละข้อ (material question ข้อ 3) พบว่า beta เปลี่ยนผลมากที่สุด ส่วน terminal growth แทบไม่เปลี่ยนผล เพราะ ROC = WACC ทำให้การโตช่วง terminal ไม่สร้างมูลค่า
- **ขั้นต่อไป:** เพิ่มคำถามเรื่อง beta ช่วง terminal และ WACC ต่ำของหุ้น beta ต่ำใน `help.md` · พิจารณาแยก WACC ช่วง terminal ในโมเดล · เปลี่ยนสถานะใน `spec.md` และ `README.md` เป็นพร้อมตรวจ แล้วส่งลิงก์ repo

---

## รอบ 9 · 2026-10-31 22:50

- **ทำอะไร:**
  - valuation หุ้นตัวที่สาม STPI.BK (STP&I) ได้ `output/STPI.BK/` (Excel, HTML, results.json) · `assumptions/STPI.BK.yaml` (status: reviewed) · `research/STPI.BK_method_choice.md`
  - เพิ่ม input `non_operating_assets` ใน bridge จาก EV เป็น equity ของ DCF (playbook §2) ค่าเริ่มต้น 0 ผล CPALL และ BDMS เท่าเดิม (ตรวจแล้วทุกวิธี) · ให้ P/E ข้ามเองเมื่อ EPS ไม่เป็นบวก · เพิ่ม `Engineering/Construction` ใน industry_map
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · LibreOffice headless · browser pane
- **Prompt ที่ใช้:**

```text
ทำ STPI
```

```text
ยืนยันตามร่าง
```

- **ผลที่ได้:** Excel ตรงกับ Python ทั้ง 15 ค่า · ผล STPI (ราคา ฿5.60, WACC 4.99%): DCF normalize ฿2.24–2.59 (base 2.40), EV/EBITDA normalize ฿0.25–1.29 (base 0.77), P/BV ฿4.64–9.42 (base 5.94), 52 สัปดาห์ ฿3.54–7.10 · สรุป: ราคาแพงเมื่อเทียบกำไรในอดีต แต่ใกล้มูลค่าตาม book · ยังขาด: มูลค่าตลาดของอสังหาฯ เพื่อการลงทุนและเงินลงทุนในบริษัทร่วม/JV, ประวัติงบยาวกว่า 4 ปี, DCF หลาย scenario
- **ตัดสินใจอะไร และเพราะอะไร:**
  - AI จัด STPI เป็นธุรกิจ cyclical (margin −3.2% ถึง 12.5%) จึง normalize ด้วยค่าเฉลี่ย 4 ปีตาม playbook §8 ตัด P/E (EPS TTM ติดลบ) และ DDM (ไม่จ่ายปันผลตั้งแต่ 2020)
  - AI ใช้ Operating Income แทน EBIT ของ Yahoo และบวกสินทรัพย์ที่ไม่ใช่การดำเนินงาน ฿5,170 ล้านตามบัญชี เพราะ EBIT ของ Yahoo รวมส่วนแบ่งกำไรบริษัทร่วม จะนับซ้ำ (playbook §2, §12 ข้อ 5) ถ้าไม่บวก DCF ติดลบ
  - ผลห่างจากราคามาก AI จึงไล่หาสาเหตุก่อนเชื่อผลตามกฎใน PROJECT_MEMORY: สูตรไม่ผิด สาเหตุคือ ROC ในอดีต 1.99% ต่ำกว่า WACC แม้ใช้ margin ปี 2025 DCF ยังได้ ฿4.65
  - ผู้เรียนยืนยันข้อเสนอ 5 ข้อตามร่าง ("ยืนยันตามร่าง"): วิธีที่ใช้, normalize 4 ปี, บวกสินทรัพย์ที่ไม่ใช่การดำเนินงาน, peer 5 ตัว (BJCHI, SRICHA, PSGC, CK, STECON), ใส่ P/BV ใน football field
  - ไม่ commit โฟลเดอร์ `.codex/` ที่โผล่ขึ้นมา เพราะ AI ไม่ได้สร้างและยังไม่รู้เหตุผลจากผู้เรียน (ตรวจแล้วไม่มี key)
- **ขั้นต่อไป:** ถามผู้เรียนเรื่อง `.codex/` · เพิ่มคำถามเรื่อง beta ช่วง terminal และการ normalize ที่ประวัติสั้นใน `help.md` · พิจารณา DCF หลาย scenario

---

## รอบ 10 · 2026-10-31 23:15

- **ทำอะไร:**
  - ร่าง valuation หุ้นตัวที่สี่ CCET.BK ได้ `output/CCET.BK/` (Excel, HTML, results.json), `assumptions/CCET.BK.yaml` และ `research/CCET.BK_method_choice.md` โดยยังคง `status: draft` รอผู้เรียนยืนยันสมมติฐาน
  - เพิ่ม mapping `Computer Hardware: Computers/Peripherals` ใน `config.yaml` หลังตรวจไฟล์ beta ตลาดเกิดใหม่ของ Damodaran โดยตรง
  - ดึง candidate peer 14 ตัวจาก Yahoo แล้วคัดเหลือผู้ผลิตฮาร์ดแวร์/EMS ไต้หวัน 5 ตัว: 2312.TW, 2324.TW, 4938.TW, 3231.TW, 2317.TW
  - ตรวจ P/BV ของ STPI ตามคำถามแทรก พบว่าสูตรถูก แต่ตัวคูณเป้าหมายใช้งบปี 2025 เทียบราคา 2026 ขณะที่ peer ใช้ `priceToBook` ของ Yahoo จึงมี period mismatch; ไม่แก้ไฟล์เพราะผู้เรียนขอให้ตรวจสอบเท่านั้น
- **เครื่องมือ / model:** Codex Desktop · GPT-5 · yfinance 1.7.0 · Damodaran `betaemerg.xls` · LibreOffice headless
- **Prompt ที่ใช้:**

```text
CCET
```

```text
ตรวจสอบ P/BV ของ STPI คำนวณมาจากไหน
```

```text
ทำ CCET ต่อ
```

- **ผลที่ได้:** ร่าง CCET ที่ราคา ฿7.95 และ WACC 10.91% ให้ DCF ฿0.91–1.13 (base ฿1.02), P/E ฿3.43–3.83 (base ฿3.74), EV/EBITDA ฿3.03–3.28 (base ฿3.05), ช่วง 52 สัปดาห์ ฿4.14–11.20 · Excel ตรงกับ Python ทั้ง 15 ค่า ต่างสูงสุด 0.0000% · ผลยังเป็นร่างและยังไม่ถือว่าผู้เรียนยืนยัน
- **ตัดสินใจอะไร และเพราะอะไร:**
  - เสนอใช้ DCF normalize, P/E, EV/EBITDA และช่วง 52 สัปดาห์; ตัด DDM เพราะ payout ต่อ EPS เปลี่ยน 19%–100% และตัด P/BV เพราะตัวขับหลักคือ ROE ไม่ใช่วิธีหลักของผู้ผลิตฮาร์ดแวร์ตาม playbook §9
  - ไม่ใช้ CAGR รายได้ −6.88% ต่ออีก 5 ปี แต่เสนอ growth 0.80% เท่า terminal g และ operating margin เฉลี่ย 4 ปี 2.2847% เพราะ playbook §8 ให้ normalize ธุรกิจตามรอบ; สมมติฐานนี้ต้องให้ผู้เรียนยืนยัน
  - ใช้ bottom-up beta 1.946 จาก Damodaran เป็น base ตามกฎใน PROJECT_MEMORY และแสดง Yahoo beta 0.657 เป็น sensitivity; DCF ด้วย Yahoo beta ได้ ฿4.38 แต่ยังต่ำกว่าราคา
  - ผลห่างจากราคามากจึงไล่สาเหตุ: ราคาต้องอาศัย operating margin 9.18% ภายใต้ bottom-up beta หรือ 3.72% ภายใต้ Yahoo beta เทียบประวัติสูงสุด 2.66%; P/E และ EV/EBITDA ของ CCET ก็ประมาณสองเท่าของมัธยฐาน peer จึงไม่ใช่ปัญหาสูตร DCF เพียงอย่างเดียว
- **ขั้นต่อไป:** ให้ผู้เรียนยืนยันหรือแก้ข้อเสนอ 5 ข้อใน `research/CCET.BK_method_choice.md` §8 จากนั้นเปลี่ยน `status: reviewed`, รันและ verify ซ้ำ แล้วค่อย `/save`

---

## รอบ 11 · 2026-11-04 09:00

- **ทำอะไร:**
  - เขียน `docs/workflow.md` ใหม่ให้ตรงกับงานหลังทำ CPALL, BDMS, STPI และร่าง CCET มี 2 แผนภาพ: workflow (flowchart จุดตัดสินใจของหุ้น 1 ตัว) และ sequence diagram (ใครส่งอะไรให้ใคร 6 ช่วง) พร้อมตารางหุ้นที่ผ่าน workflow แล้ว
  - เพิ่ม `data/idisc/` ใน `.gitignore`
- **เครื่องมือ / model:** Claude Desktop (แท็บ Code) · Claude Opus 5.5 · browser pane + mermaid 11.4.1 ตรวจการ render
- **Prompt ที่ใช้:**

```text
สร้าง sequence diagram กับ workflow ของ project นี้
```

```text
เพิ่มใน .gitignore
```

```text
Save
```

- **ผลที่ได้:** แผนภาพทั้ง 2 อัน parse และ render ผ่าน · workflow แสดงจุดตัดสินใจ 6 จุด (industry_map, ประเภทธุรกิจตาม playbook §1, เงินลงทุนในบริษัทอื่น, ผลห่างจากราคา, ผู้เรียนยืนยัน, verify ≤ 0.5%) และกฎความสอดคล้องจาก PROJECT_MEMORY · ยังขาด: CCET ยังเป็น draft ในตาราง
- **ตัดสินใจอะไร และเพราะอะไร:**
  - AI แยกเป็น 2 แผนภาพ เพราะ sequence diagram เดิม (รอบ 7) บอกได้แค่ลำดับการส่งข้อมูล แต่ไม่บอกว่าต้องเลือกวิธีหรือแก้สมมติฐานตรงไหน ซึ่งเป็นส่วนที่เปลี่ยนไปมากในรอบ 8–10
  - เปลี่ยนผู้เล่นเป็น "AI (Claude / Codex)" เพราะรอบ 10 ทำด้วย Codex และ repo มี agent ของทั้งสองค่าย
  - ผู้เรียนให้เพิ่ม `data/idisc/` ใน `.gitignore` หลัง AI แจ้งว่ามีไฟล์งบ BGRIM จาก ก.ล.ต. ที่ไม่ได้อยู่ใน ignore ถ้า save จะขึ้น repo Public ด้วย
- **ขั้นต่อไป:** ยืนยันข้อเสนอของ CCET แล้วเปลี่ยนเป็น reviewed · เพิ่มคำถามเรื่อง beta ช่วง terminal และการ normalize ที่ประวัติงบสั้นใน `help.md`
