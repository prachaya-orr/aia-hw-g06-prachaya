# วิธีสร้าง football field chart

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** e4198d49-beb9-476e-b16d-c75256160461

## คำถาม

How do you build a football field valuation chart? Which methods are included (DCF, trading comps, precedent transactions, 52-week range, analyst price targets)? How do you set the low and high end of each bar? How do you read the current share price against the chart? What are the Excel construction steps (e.g., stacked bar chart with an invisible first series)?

## คำตอบสรุป

notebook ใช้ source เดียวทั้งคำตอบคือ Wall Street Prep

**คืออะไรและใช้ทำอะไร**

- football field คือ floating bar chart ใน Excel ที่วางผลการประเมินมูลค่าหลายวิธีเทียบกัน พบบ่อยใน pitch book ของ investment banking และใน fairness opinion — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- จุดประสงค์คือสรุปภาพรวมของทุกวิธีและเอาวิธีต่าง ๆ มา sanity-check กัน — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- ตัวอย่างความต่างที่ chart ช่วยเห็น: comps อาจสูงในตลาดกระทิง ขณะที่ DCF ให้ค่าต่ำกว่า — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]

**วิธีที่ใส่ใน chart**

- มาตรฐานที่ source ระบุ: DCF, LBO, Comparable Company Analysis, Precedent Transactions, 52-week high/low; ตัวเลือกเสริม: Liquidation, Sum-of-the-Parts — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- Analyst price targets: notebook เขียนไว้ในคำตอบแต่ไม่มี citation และ excerpt ไม่ระบุ จึงถือว่าไม่พบใน source

**กำหนดปลายล่าง/บนของแต่ละแท่ง** (ตามที่ notebook สรุปจาก source เดียวกัน)

- 52-week range: ล่างคือราคาปิดต่ำสุดใน 52 สัปดาห์ บนคือราคาสูงสุด — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- Trading comps และ precedent transactions: ล่าง/บนมาจาก multiple ต่ำ/สูงของ peer (เช่น min/25th percentile ถึง max/75th percentile) — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- DCF: ล่างใช้ scenario ระมัดระวัง (WACC สูง, terminal growth ต่ำ) บนใช้ scenario เชิงบวก — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- (ข้อสังเกต: excerpt ที่ notebook ส่งมาเป็นแค่รายการวิธีและจุดประสงค์ ไม่ได้แสดงรายละเอียดเรื่อง percentile หรือ sensitivity ตรง ๆ จึงมีความเสี่ยงว่ารายละเอียดส่วนนี้ notebook สรุปเกินกว่า excerpt)

**อ่านราคาปัจจุบันเทียบกับ chart**

- วาดเส้นแนวตั้งที่ราคาปัจจุบันตัดผ่านทุกแท่ง; ถ้าราคาอยู่ต่ำกว่าหรือใกล้ปลายล่างของ DCF/comps แปลว่าอาจถูกเกินจริง ถ้าอยู่ใกล้หรือสูงกว่าปลายบนแปลว่าตลาดให้ premium — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]

**ขั้นตอนใน Excel**

- ตารางข้อมูล: วิธี, Low, High, ฐานล่องหน (= Low), ความยาวแท่ง (= High - Low) — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- Insert > Stacked Bar (แนวนอน) แล้วตั้ง series แรก (ฐาน) เป็น No fill / No line ให้เหลือแท่งลอย — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- เพิ่มเส้นราคาปัจจุบันด้วย scatter series หรือเส้นแนวตั้ง และปรับ gap width ประมาณ 50-80% — [Football Field Valuation Chart | Excel Tutorial + Example - Wall Street Prep]
- ตัวเลขในตารางตัวอย่างของ notebook (35, 50, 52 ดอลลาร์ ฯลฯ) เป็นตัวอย่างสมมติ ห้ามนำไปใช้เป็นข้อมูลจริง

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Football Field Valuation Chart \| Excel Tutorial + Example - Wall Street Prep | "floating bar chart in Excel" |
| Football Field Valuation Chart \| Excel Tutorial + Example - Wall Street Prep | "sanity-check various methodologies against one another" |

## สิ่งที่ไม่พบใน notebook

- Analyst price targets ใน football field (คำตอบไม่มี citation)
- notebook มี source เรื่อง football field เพียงชิ้นเดียว จึงไม่มีมุมมองจากแหล่งอื่นเปรียบเทียบ
- ไม่มีข้อมูลว่าควรเลือก percentile เท่าไรเป็นปลายแท่งอย่างเป็นทางการ (รายละเอียด min/25th/75th/max มีความเสี่ยงว่าเกิน excerpt)
