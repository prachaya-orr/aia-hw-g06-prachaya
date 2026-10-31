# Valuation ของธนาคารและธุรกิจการเงิน (ทำไม FCFF/WACC ใช้ไม่ได้ และใช้วิธีไหนแทน)

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 2ba626b0-c583-4619-aef3-033df8b26bd8

## คำถาม

Why does a FCFF/WACC-based DCF not work for banks and financial service firms? Which valuation methods should be used instead (dividend discount model, FCFE with regulatory capital constraints, excess return model, P/BV vs ROE)? Give the excess return model formula. What valuation methods do equity researchers actually use for banks?

## คำตอบสรุป

**ทำไม FCFF/WACC ใช้ไม่ได้**

- หนี้ (รวมเงินฝาก) เป็นวัตถุดิบของธนาคาร ไม่ใช่การเลือกโครงสร้างเงินทุน ธนาคารกู้จากผู้ฝากแล้วปล่อยกู้ต่อเพื่อสร้างส่วนต่างดอกเบี้ย — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Estimating the Value of a Privately Held Bank: Luminor Bank AS]
- ถ้านับเงินฝากเป็นหนี้ อัตราส่วนหนี้จะสูงมากจน WACC ต่ำผิดปกติ (notebook ยกตัวอย่าง 4% หรือต่ำกว่า) และการวัด operating income ก่อนดอกเบี้ยทำไม่ได้ เพราะดอกเบี้ยจ่ายผู้ฝากคือต้นทุนดำเนินงานหลัก — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21)]
- นิยาม capex และ working capital ของธนาคารไม่ชัด เพราะธนาคารลงทุนในคนและแบรนด์ซึ่งบัญชีบันทึกเป็นค่าใช้จ่าย และ working capital คือเกือบทั้งงบดุล จึงคำนวณ FCFF ไม่ได้ — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21)]
- ธนาคารถูกกำกับเรื่องเงินกองทุน การลงทุน และความเร็วในการเติบโต การเปลี่ยนกฎจึงทำให้มูลค่าเปลี่ยนมาก และส่วนของผู้ถือหุ้นเป็นสัดส่วนเล็กของสินทรัพย์ ทำให้มูลค่าไวต่อคุณภาพสินทรัพย์ — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Estimating the Value of a Privately Held Bank: Luminor Bank AS]
- สรุปจาก Damodaran: ธุรกิจการเงินควรใช้ equity valuation model มากกว่า enterprise valuation model และใช้เงินปันผลจริงหรือเงินปันผลที่จ่ายได้ (potential dividends) แทน FCFE — [Valuing Financial Service Firms (Damodaran paper, 2009)]

**วิธีที่ใช้แทน**

- DDM: คิดมูลค่าหุ้นจากเงินปันผลคาดการณ์คิดลดด้วย cost of equity เหมาะกับธนาคารที่จ่ายปันผลสม่ำเสมอ เพราะประมาณกระแสเงินสดของธุรกิจการเงินยาก จึงเชื่อว่าธนาคารจ่ายกระแสเงินสดออกมาเป็นปันผล — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Valuing Financial Service Firms (Damodaran paper, 2009)]
- FCFE แบบมี regulatory capital: นิยาม reinvestment ใหม่เป็นส่วนที่ต้องเพิ่มใน regulatory book equity เพื่อรักษาอัตราส่วนเงินกองทุนเป้าหมาย (เช่น Tier 1) ตามการเติบโตของสินเชื่อ สูตร FCFE = Net Income - reinvestment in regulatory capital — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21)]
- Excess return model (หรือ Residual Income Model, RIM): มูลค่า = book equity ปัจจุบัน + PV ของ excess return สร้างมูลค่าเฉพาะเมื่อ ROE สูงกว่า cost of equity เหมาะกับธนาคารเพราะสินทรัพย์ตีราคาตลาดอยู่แล้ว book value จึงเป็นฐานที่ใช้ได้ — [Estimating the Value of a Privately Held Bank: Luminor Bank AS], [How to: Excess Return Model for Valuing Financial Stocks], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21)]
- P/BV กับ ROE: justified P/BV = (ROE - g) / (k_e - g) ธนาคารที่ ROE สูงกว่าควรได้ P/BV สูงกว่า ใช้ P/BV หรือ P/tNAV แทน EV/EBITDA — [A Case Study of Bank Equity Valuation Methods Employed by South African, Nigerian and Kenyan Equity Researchers - MDPI], [Valuing Financial Service Firms (Damodaran paper, 2009)]

**สูตร Excess return model (ตามที่ notebook ให้)**

- แบบ perpetuity: Value of equity = Equity_0 + [(ROE - k_e) / (k_e - g)] x Equity_0 (หรือต่อหุ้น P_0 = BVPS_0 + [(ROE - k_e) / (k_e - g)] x BVPS_0) — [A Case Study of Bank Equity Valuation Methods ... - MDPI], [Estimating the Value of a Privately Held Bank: Luminor Bank AS]
- แบบหลายช่วงเวลา: Value of equity = Equity_0 + ผลรวมของ PV[(ROE_t - k_e) x Equity_(t-1)] + PV ของ terminal value โดย excess return ปีที่ t = Net Income_t - k_e x Equity_(t-1) — [A Case Study of Bank Equity Valuation Methods ... - MDPI], [How to: Excess Return Model for Valuing Financial Stocks], [Valuing Financial Service Firms (Damodaran paper, 2009)]
- terminal value ของ excess return = (ROE_terminal - k_e) x Equity_n / (k_e - g) — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Estimating the Value of a Privately Held Bank: Luminor Bank AS]

**นักวิเคราะห์ที่ทำ equity research ใช้วิธีไหนจริง (ผลสำรวจแอฟริกาใต้ ไนจีเรีย เคนยา)**

- Warranted Equity Method (WEM) ใช้กันแพร่หลายที่สุด: ประมาณการ 3 ปี คำนวณ P/BV หรือ P/tNAV ที่เหมาะสมจาก ROE หรือ ROTE ที่ยั่งยืน คูณกับ book value ปีสุดท้าย แล้วคิดลดพร้อมปันผลระหว่างทาง — [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- RIM / Excess return model ใช้บ่อย (เช่น Standard Bank Group) โดยรวม tangible NAV กับ residual income — [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- Sum-of-the-parts สำหรับกลุ่มธนาคารที่มีบริษัทลูกนอกธนาคาร (ประกัน บริหารสินทรัพย์) — [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- Market multiples (P/E, P/BV, P/tBV) ใช้โดยนักวิเคราะห์เกิน 90% เพื่อเทียบ target price กับกลุ่มเปรียบเทียบ — [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- บางทีมถ่วงน้ำหนักหลายโมเดล เช่น RIM 35%, multiples 50%, DDM 15% — [A Case Study of Bank Equity Valuation Methods ... - MDPI]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern | "best valued using equity valuation models, rather than enterprise valuation models" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "we trust financial service firms to pay out their cash flows as dividends" |
| How to: Excess Return Model for Valuing Financial Stocks | "the excess return model, is probably the best of both worlds" |
| Estimating the Value of a Privately Held Bank: Luminor Bank AS - Digikogu | "RIM, also known as Excess Return Model, is a well-suited model" |
| Estimating the Value of a Privately Held Bank: Luminor Bank AS - Digikogu | "banks are heavily regulated by the government and restricted in the area of investments" |
| A Case Study of Bank Equity Valuation Methods ... - MDPI | "banks exhibit distinctive features in their capital structures" |

## สิ่งที่ไม่พบใน notebook

- ตัวเลขสัดส่วน 90% และน้ำหนัก 35/50/15 มาจากผลสำรวจนักวิเคราะห์ในแอฟริกา (แอฟริกาใต้ ไนจีเรีย เคนยา) เท่านั้น ไม่ใช่ตลาดไทยหรือตลาดโลก
- ข้อความ cited_text ที่ตรวจเองยืนยันได้เฉพาะบางประโยค (ดูตารางหลักฐาน) ส่วนที่เหลือเป็นการสรุปของ notebook ที่อ้าง source ตามหมายเลข citation
- notebook ไม่ได้ให้ค่า ROE, k_e, g ของธนาคารจริงใดๆ (ต้องหาจากแหล่ง Trust sources ใน spec.md แยกต่างหาก)
