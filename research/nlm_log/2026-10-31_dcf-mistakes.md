# ข้อผิดพลาดที่พบบ่อยใน DCF

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 5c974322-40bd-40a1-a03a-02fddacc5fff (คำถามหลัก), cf3b2496-34e1-4fda-add8-66e58d80a0f5 (follow-up เรื่อง lease)

## คำถาม

1. "What are common mistakes in DCF valuation? Consider: mismatch between discount rate and cash flows (equity vs firm, nominal vs real, currency), growth rate above the economy, inconsistent reinvestment with growth, double counting, ignoring stock-based compensation, lease treatment, and inconsistency between terminal value assumptions and the rest of the model."
2. Follow-up: "How should operating leases be treated in DCF valuation and cost of capital (lease as debt, adjusting operating income and invested capital)? What do the sources say about the risk of treating leases inconsistently?"

## คำตอบสรุป

- Discounting consistency: cash flow หลังจ่ายหนี้ (FCFE) ต้องคิดลดด้วย cost of equity, cash flow ก่อนหนี้ (FCFF) ต้องคิดลดด้วย cost of capital การจับคู่ผิดเรียกว่า mismatch effect — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ผลของ mismatch ตามตัวอย่างใน source: คิดลด FCFE ด้วย cost of capital ทำให้ equity value สูงเกิน, คิดลด FCFF ด้วย cost of equity ทำให้ firm value ต่ำเกิน, และถ้าคิดลด FCFF ด้วย cost of equity แล้วลืมหักหนี้ equity value จะสูงเกินมาก — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Nominal vs real และสกุลเงิน: cash flow แบบ nominal ใช้ discount rate แบบ nominal, แบบ real ใช้ real และสกุลเงินของ cash flow กับ discount rate (risk-free) ต้องตรงกัน ถ้าแปลงสกุลต้องใช้ exchange rate ที่สะท้อน purchasing power parity — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Growth เกินเศรษฐกิจ: stable growth ต้องไม่เกินอัตราเติบโตของเศรษฐกิจ และ risk-free rate ที่ใช้เท่ากับสมมติฐานเรื่อง nominal growth โดยปริยาย ถ้าสมมติ nominal growth สูงแต่ risk-free ต่ำ จะ overvalue และกลับกันจะ undervalue — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Reinvestment ไม่สอดคล้องกับ growth: growth = reinvestment rate x ROC (หรือ retention x ROE) ใน stable growth reinvestment rate = g / ROC — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]
- ข้อผิดพลาด "capex เท่ากับ depreciation และไม่มี working capital" ใน terminal year แต่ยังให้โตตลอดไป: บริษัทที่ไม่ลงทุนใหม่ก็โตไม่ได้ ทำให้ประเมินมูลค่าสูงเกิน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Terminal value ไม่สอดคล้องกับส่วนอื่น: ใน stable growth excess return ควรเข้าใกล้ศูนย์, beta เข้าใกล้ 1, debt ratio เข้าใกล้ค่าเฉลี่ยอุตสาหกรรม (แต่ Damodaran ยอมรับว่า excess return บางกรณีอยู่ได้นานมาก) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Reinvestment rate ปีท้ายของช่วงโตเร็วควรลดลงล่วงหน้าหนึ่งปีเพื่อให้ตรงกับ growth ปีแรกของ stable period (Damodaran ยอมรับว่าไม่ได้ทำสม่ำเสมอเพราะผลต่อมูลค่าน้อย) — [Equity Risk Premiums: Globalization and Country risk - Musings on Markets]
- SBC: การ add back SBC ว่าเป็น non-cash เป็นข้อผิดพลาด เพราะเป็นการจ่ายเป็นหุ้น (in-kind) ที่ทำให้ผู้ถือหุ้นเดิมเจือจาง การ add back ทำให้ overvalue ควรถือ SBC เป็นค่าใช้จ่ายเสมือนเงินสด — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep], [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]
- การหักหนี้ตามมูลค่า: ตัวอย่างบริษัทที่หนี้ซื้อขายที่ 50% ของ face value เป็นคำถามว่าควรหักมูลค่าตลาดหรือ face value (source ตั้งเป็นโจทย์ ไม่ได้สรุปในข้อความที่ได้) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Double counting: ถ้าสินทรัพย์ใดสร้าง cash flow อยู่แล้ว ห้ามเอามูลค่าตลาดของสินทรัพย์นั้นไปบวกซ้ำ และถ้ารวมดอกเบี้ยรับจากเงินสดไว้ใน cash flow แล้ว ต้องปรับ discount rate ให้สะท้อนเงินสดนั้น — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Lease: เนื่องจากเป็นภาระผูกพันตามสัญญา ให้ถือเป็นหนี้ คิดมูลค่าหนี้เท่ากับ PV ของ lease commitment ที่ pre-tax cost of debt สร้างสินทรัพย์เท่ากัน และปรับ operating earnings เท่ากับ stated operating earnings + lease expense − depreciation ของสินทรัพย์เช่า (ประมาณได้ด้วย pre-tax cost of debt x PV ของ lease) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ผลกระทบของ lease ในตัวอย่าง The Gap: debt เพิ่ม ทำให้ cost of capital ลดลงและ return on capital ลดลง ถ้าไม่ปรับอย่างสม่ำเสมอ (เช่น ปรับหนี้แต่ไม่ปรับ operating income) จะได้ margin ต่ำเกิน ROC สูงเกิน และ debt ratio ต่ำเกิน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- หลังปี 2019 IFRS และ GAAP กำหนดให้แสดง lease เป็นหนี้และสินทรัพย์ในงบดุลแล้ว — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ค่าใช้จ่ายที่เป็น capital expense (เช่น R&D) ที่บัญชีบันทึกเป็น operating expense ทำให้ earnings และ invested capital ผิด — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- เตือนให้ระวังการนับทุกอย่างเป็นหนี้ เพราะจะดัน debt ratio ให้สูงและทำให้ cost of capital ต่ำเกินจริง — [Aswath Damodaran Updated: January 2026 - NYU Stern]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Never mix and match cash flows and discount rates." |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Mismatching cash flows to discount rates is deadly." |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "options are not non-cash expenses, but in-kind expenses" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "operating lease expenses should be treated as financing expenses" |
| Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets | "closer in spirit to an in-kind compensation than a non-cash compensation" |

## สิ่งที่ไม่พบใน notebook

- คำตอบแรกของ notebook เรื่อง lease อ้าง citation ที่ไม่ตรงประเด็น จึงทำ follow-up และใช้เฉพาะผลของ follow-up
- ไม่พบรายการ "ข้อผิดพลาด DCF" ที่รวบรวมไว้เป็นหมวดเดียวใน source ใด ๆ ข้อสรุปข้างต้นเป็นการรวบรวมจากหลายส่วนของ source (ส่วนใหญ่จาก Damodaran)
- ไม่พบเรื่อง double counting ที่เกี่ยวกับ SBC หรือ lease โดยตรง (มีเฉพาะเรื่องสินทรัพย์ที่สร้าง cash flow อยู่แล้ว และ Damodaran ชี้ว่าการหัก SBC ใน cash flow แล้วหักมูลค่า options เดิมอีกครั้ง ไม่ใช่ double counting ดูไฟล์ sbc-dilution)
