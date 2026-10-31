# DCF: FCFF vs FCFE, discount rate, และการแปลง enterprise value เป็นมูลค่าต่อหุ้น

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 029aac34-22f4-4229-a8b6-9cc3b8eb831a

## คำถาม

What are the formulas for FCFF (free cash flow to the firm) and FCFE (free cash flow to equity)? When should one use FCFF versus FCFE? Which discount rate goes with each? How do you get from enterprise value to equity value per share (net debt, minority interests, cash, cross holdings, options)?

## คำตอบสรุป

- FCFF = EBIT(1 - tax rate) - (CapEx - Depreciation) - ΔNon-cash working capital เป็นกระแสเงินสดก่อนจ่ายหนี้ ใช้กับทั้งเจ้าหนี้และผู้ถือหุ้น — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Business Analysis and Valuation - docenti.unina.it]
- รูปแบบ stable growth: FCFF = after-tax operating income x (1 - reinvestment rate) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- FCFE (บริษัทที่มีหนี้) = Net Income - (CapEx - Depreciation) - ΔNon-cash WC + (New debt issued - Debt repaid) คือเงินสดส่วนเกินที่จ่ายเป็นเงินปันผลได้ (potential dividend) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ถ้าสมมติ debt ratio (DR) คงที่: FCFE = Net Income - (1-DR)(CapEx - Depreciation) - (1-DR)ΔNon-cash WC; ย้อนหลังใช้ book debt ratio ได้ แต่มองไปข้างหน้าแทนด้วย market debt ratio ได้ — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- อีกทางหนึ่งคือคำนวณ FCFE จาก statement of cash flows: Cash flow from operations + CapEx + cash acquisitions + (Debt repaid - Debt issued) (เครื่องหมาย CapEx ตามงบ) โดย source เตือนว่าไม่ควรเชื่อผลทั้งหมด — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ใช้ FCFF (firm valuation) เมื่อ leverage สูงหรือต่ำเกินไปและคาดว่าจะเปลี่ยน, เมื่อมีข้อมูลหนี้ไม่ครบ (เช่น ไม่มี interest expense), หรือเมื่อสนใจมูลค่ากิจการทั้งก้อน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ใช้ FCFE (equity valuation) เมื่อ leverage คงที่ และกับ financial service firms ทั้งหมด เพราะกำหนด capex/working capital และแยกหนี้ที่เป็น operating ไม่ได้ — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern]
- กฎ rule of thumb: ถ้าเงินปันผลต่ำกว่า 80% ของ FCFE หรือสูงกว่า 110% ในช่วง 5 ปี ให้ใช้ FCFE model แทน DDM — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Discount rate: FCFF ใช้ cost of capital (WACC) = ke x E/(D+E) + kd(1-t) x D/(D+E); FCFE ใช้ cost of equity (CAPM: Rf + beta x risk premium) — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Business Analysis and Valuation - docenti.unina.it]
- Discounting Consistency Principle: ห้ามจับคู่กระแสเงินสดกับ discount rate ผิดประเภท เช่น เอา FCFE ไป discount ด้วย cost of capital จะได้มูลค่าส่วนผู้ถือหุ้นสูงเกินจริง; ตัวอย่างในสไลด์ overstate 540 — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- สกุลเงินของ discount rate ต้องตรงกับสกุลเงินของ cash flow และ nominal/real ต้องตรงกัน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ลำดับ bridge จาก EV ไปมูลค่าต่อหุ้น: Value of operating assets + cash & marketable securities + cross holdings + other non-operating assets = value of firm; ลบ debt = value of equity; ลบ value of equity options = value of common stock; หารด้วย primary shares outstanding = value per share — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Minority interests (บริษัทลูกที่ consolidate): แปลง book value เป็น market value โดยคูณ P/B ของ sector ของบริษัทลูก แล้วหักออก; cross holdings ที่เป็น minority holding แปลง book เป็น market ด้วย P/B ของ sector แล้วบวกเข้า — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Cash: วิธีตรงที่สุดคือแยกเงินสดออกจาก operating cash flow (ไม่รวมดอกเบี้ยรับ) แล้วบวกกลับตอนท้าย — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Employee options/warrants/convertible: หักมูลค่า option ตาม market value หรือ option pricing model ก่อนหารด้วย primary shares (ไม่ใช้ diluted count ซ้ำ) — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences Aswath Damodaran Stern School of Busines - NYU Stern], [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep]
- Restricted stock รวมอยู่ในจำนวนหุ้นที่ออกอยู่แล้ว ไม่ต้องหักแยก — [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Never mix and match cash flows and discount rates." |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "FCFF = Cash flows before debt payments but after reinvestment & taxes." |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "potential dividend" (นิยาม FCFE) |
| Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern | "far easier to value the equity directly in a financial service firm" |
| Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences Aswath Damodaran Stern School of Busines - NYU Stern | "divided by the number of shares outstanding to arrive at value per share" |

## สิ่งที่ไม่พบใน notebook

- ไม่มีการแยกนิยาม "net debt" เป็นสูตรเดี่ยวในคำตอบนี้ source ใช้ลำดับ + cash แล้ว - debt (แต่ในคำตอบเรื่อง beta มีตัวอย่าง net debt = Debt - Cash ใช้กับ D/E ดู log `beta`)
- ไม่มีเกณฑ์ตัวเลขว่า minority interest ควรเป็นกี่ % นอกจากวิธีคูณ P/B ของ sector
- คำตอบนี้ส่วนใหญ่มาจากสไลด์ Damodaran เล่มเดียว (Updated: January 2026); source อื่นเป็นหลักฐานรอง
