# Multiples: P/E, EV/EBITDA, P/BV (นิยาม ตัวขับ ความเหมาะสม consistency rule)

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 378ee342-0f87-478f-9c82-d6730a6efaec

## คำถาม

Define P/E, EV/EBITDA and P/BV (and PEG and EV/Sales if covered): give the formulas. For each multiple, what are its fundamental drivers (growth, payout ratio, ROE, risk)? Which multiple fits which type of business? What is the consistency rule between equity multiples (numerator equity value) and enterprise multiples (numerator enterprise value), including what the denominator must be?

## คำตอบสรุป

**นิยามและสูตร**

- P/E = ราคาต่อหุ้น / EPS (หรือ market cap / net income) — [A Case Study of Bank Equity Valuation Methods ... South African, Nigerian and Kenyan Equity Researchers - MDPI]
- P/E ที่ derive จาก Gordon growth: trailing P/E = (1+g) x payout / (ke - g); forward P/E = payout / (ke - g); เขียนในรูป ROE ได้เป็น (ROE - g) / (ROE x (ke - g)) — [MDPI bank equity valuation case study]
- EV/EBITDA = Enterprise Value / EBITDA โดย EV = market cap + debt - cash — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]
- P/BV = ราคาต่อหุ้น / book value ต่อหุ้น (หรือ market value of equity / book value of equity) — [MDPI bank equity valuation case study]
- Justified P/BV (warranted equity method) = (ROE - g) / (ke - g) — [MDPI bank equity valuation case study]
- EV/Sales = Enterprise Value / ยอดขาย อยู่ในกลุ่ม enterprise multiples ร่วมกับ EV/EBITDA, EV/EBIT — [Business Analysis and Valuation - docenti.unina.it]
- PEG = P/E หารด้วยอัตราเติบโตกำไรที่คาดไว้ — notebook ให้สูตรนี้ แต่ excerpt ที่อ้างไม่มีคำว่า PEG ตรง ๆ จึงมีหลักฐานอ่อน (ดูหัวข้อ "ไม่พบ")

**ตัวขับพื้นฐาน (fundamental drivers)**

- P/E: เพิ่มตามอัตราเติบโตกำไรและ payout ratio และลดลงเมื่อ cost of equity สูงขึ้น — [MDPI bank equity valuation case study]; ROE สูงขึ้นดัน P/E สูงขึ้นตามสูตร derive ข้างต้น — [MDPI bank equity valuation case study]
- EV/EBITDA: ขึ้นกับการเติบโตของ operating income/FCFF (บวก), cost of capital (ลบ), reinvestment และภาษี (ลบ) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- P/BV: ROE เป็นตัวแปรหลัก; growth และ payout เพิ่ม P/BV ส่วน cost of equity สูงขึ้นลด P/BV — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern], [MDPI bank equity valuation case study]
- EV/Sales: ขึ้นกับการเติบโตของรายได้ (บวก) และ WACC (ลบ) — [Aswath Damodaran Updated: January 2026 - NYU Stern] (ส่วน operating margin เป็นตัวแปรหลักของ EV/Sales นั้น notebook เขียนโดยไม่มี citation จึงตัดออก)

**multiple ไหนเหมาะกับธุรกิจแบบไหน**

- P/E: เหมาะกับบริษัทที่มีกำไรเป็นบวก ใช้กับบริษัทขาดทุนไม่ได้เพราะตัวหารติดลบ — [MDPI bank equity valuation case study]
- P/BV: ใช้กับธนาคารและสถาบันการเงิน เพราะ ROE เทียบ ke เป็นตัวขับมูลค่า — [MDPI bank equity valuation case study], [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern]
- EV/EBITDA และ EV/Sales: ใช้กับบริษัท cyclical/commodity ได้ดี เพราะ EBITDA และ revenue ผันผวนน้อยกว่า operating income — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- EV/EBITDA ไม่เหมาะกับสถาบันการเงิน เพราะ value และ operating income ของธนาคารหรือประกันนิยามยาก — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern]

**Consistency rule**

- Equity multiple (ตัวตั้งคือ equity value/ราคาหุ้น) ต้องหารด้วยตัวเลขที่เป็นของผู้ถือหุ้นหลังดอกเบี้ย (levered) เช่น EPS, book value of equity — [Business Analysis and Valuation - docenti.unina.it]
- Enterprise multiple (ตัวตั้งคือ EV) ต้องหารด้วยตัวเลขก่อนดอกเบี้ย (unlevered) เช่น EBITDA, EBIT, Sales — [Business Analysis and Valuation - docenti.unina.it]
- หลักการเดียวกันฝั่ง DCF: ห้ามจับคู่ cash flow กับ discount rate ผิดประเภท (equity cash flow ใช้ ke, firm cash flow ใช้ cost of capital) ผลคือมูลค่าเอนเอียง — [Aswath Damodaran Updated: January 2026 - NYU Stern] (หมายเหตุ: excerpt นี้พูดเรื่อง DCF ไม่ใช่ multiples โดยตรง)

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| MDPI bank equity valuation case study | "cannot, however, be used to value loss-making firms" |
| Business Analysis and Valuation - docenti.unina.it | "Using levered (after interest) cash flows in denominator" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Never mix and match cash flows and discount rates." |

## สิ่งที่ไม่พบใน notebook

- สูตร PEG ที่มี excerpt ยืนยันตรง ๆ (notebook ตอบมาแต่ excerpt ที่อ้างไม่มีคำว่า PEG)
- operating margin เป็นตัวขับ EV/Sales (คำตอบไม่มี citation)
- ไม่มีตัวเลขช่วงที่เหมาะสมของแต่ละ multiple ในคำตอบนี้
