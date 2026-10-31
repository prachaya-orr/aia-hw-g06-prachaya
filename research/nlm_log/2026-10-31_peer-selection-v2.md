# Peer selection v2: เกณฑ์ จำนวน peer, mean/median/harmonic, ความแม่นยำ, ข้อผิดพลาด

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`) หลังเพิ่ม source ใหม่ 5 ชิ้น
- **conversation_id:** ddc343ff-293d-4268-a9a8-71f9d2c7310d
- **หมายเหตุ:** เติมจาก `2026-10-31_peer-selection.md` ที่ log เดิมระบุว่า "ไม่พบ" กฎ mean/median และจำนวน peer ตอนนี้พบบางส่วนแล้ว

## คำถาม

How should one choose comparable companies (criteria, how many peers)? Mean vs median vs harmonic mean of peer multiples: what do the sources say? How to adjust for differences in growth and risk? What evidence do the sources give on the accuracy of multiples-based valuation (which multiples are most accurate, valuation errors)? What are the common mistakes in peer group selection and comparable valuation?

## คำตอบสรุป

**เกณฑ์เลือก peer (ใหม่)**

- ในทางทฤษฎี peer เทียบกันได้เมื่อ value driver คือ profitability, risk, growth ใกล้กัน แต่ยังไม่มีฉันทามติว่าทำให้เกิดจริงอย่างไร มีวิธีเลือก 3 กลุ่ม: อิงอุตสาหกรรม, อิง fundamentals, และวิธีใหม่ ๆ — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- แนวปฏิบัติที่พบมากคือเลือก peer จากการอยู่อุตสาหกรรมเดียวกันอย่างเดียว — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- ยิ่งเพิ่มเกณฑ์ fundamentals หลายตัว จำนวนบริษัทที่เข้าเกณฑ์ทุกข้อยิ่งลดลงเร็ว (อ้าง Alford 1992) — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- GICS อธิบายความแปรผันของ multiple และ growth ที่คาดได้ดีกว่า SIC และ NAICS (Bhojraj, Lee & Ng 2003 ตามที่ source สรุป) — [Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review]
- SIC/GICS กว้างเกินไป ทำให้บริษัทในกลุ่มไม่คล้ายกันพอ — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ข้อผิดพลาดของการประเมินลดลงเมื่อนิยามอุตสาหกรรมแคบลงเหลือ SIC 2-3 หลัก (Alford) และ comps ควรเลือกตามอุตสาหกรรม ขนาด leverage และ earnings growth — [Examining IPO Valuation Methods - NYU Stern]
- เกณฑ์ที่ source ตำราให้: listed companies, ขนาด, อุตสาหกรรม, ตำแหน่งการแข่งขัน, growth/profitability, leverage/risk — [Business Analysis and Valuation - docenti.unina.it]
- วิธีทางเลือกที่ถูกกล่าวถึง: SARD (รวมผลต่างอันดับของตัวแทน profitability/growth/risk ได้ไม่จำกัดและไม่ขึ้นกับรหัสอุตสาหกรรม ผลแม่นกว่าการใช้ industry classification), K-medians clustering ของ financial ratios, co-search บน EDGAR, ความคล้ายของคำอธิบายธุรกิจ, GBDT/machine learning — [(Out)smart the Peer Group in Market Comparison - ResearchGate]; "Warranted Multiple" ของ Bhojraj & Lee 2002 ให้ peer ที่ดีกว่าวิธีอื่น (ตามที่ source สรุป) — [Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review]
- ผล ML ของ Geertsema & Lu: ทำนาย multiple ได้แม่นกว่าโมเดลดั้งเดิม และแสดง multiple ที่ทำนายเป็นค่าเฉลี่ยถ่วงน้ำหนักของ multiple ของ peer ได้ โดย weight คือระดับความ comparable — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- ข้อควรระวังของ peer ที่เลือกเองตาม fundamentals: เสี่ยง bias ในการเลือก (De Franco et al. 2015 ตามที่ source อ้าง) — [(Out)smart the Peer Group in Market Comparison - ResearchGate]

**จำนวน peer**

- ไม่มีกฎตัวเลข ที่พบเป็นตัวอย่างการปฏิบัติ: CFI แนะนำหา 5-10 บริษัทแล้วตัดตัวที่ต่างมากออก — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]; กรณี Luminor ใช้ 11 ธนาคาร (เกณฑ์ภูมิภาค/กฎระเบียบ, business model, ข้อมูลที่หาได้) — [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK: A CASE STUDY OF LUMINOR BANK AS - Digikogu]; กรณี Lockheed Martin ใช้ 6 บริษัทเทียบ (Boeing ถูกตัดออกบางตัวคูณ) — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]

**Mean vs median vs harmonic mean (ตอบสิ่งที่ log เดิมไม่พบ)**

- นักปฏิบัติมักเลือก median เพราะอธิบายง่ายและทนต่อ outlier ส่วนงานวิชาการบางชิ้นเสนอ harmonic mean (Baker & Ruback 1999, Liu et al. 2002) — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- ผลทดสอบเชิงประจักษ์ที่ระดับ GICS Industry: median ให้ค่า error แบบ median ต่ำสุด (MdAPE, MdPE) harmonic mean ให้ error แบบ mean ต่ำสุด (MAPE, MPE) และ arithmetic mean ให้ R² และ correlation สูงสุด ข้อสรุปของผู้เขียนคือไม่มีวิธีที่ดีที่สุดเสมอ (ตัวอย่าง EV/EBITDA: MdAPE median 25%, mean 27%, harmonic 25%) — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- กฎปฏิบัติจากกรณีศึกษา (อ้าง Fazzini 2018): ถ้าช่วงค่าของ peer ไม่กว้างมาก ใช้ mean หรือ median ได้ ถ้ากว้างให้ใช้ median — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ตัวอย่างการกรอง outlier ก่อนหาค่าเฉลี่ย: ตัดค่า P/E, P/B, EV/EBITDA ของ Boeing ที่ติดลบหรือผิดปกติ (P/E -46.04, P/B -5.94, EV/EBITDA 61.19) แล้วจึงใช้ average ของที่เหลือ — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ตำรายังเขียนเพียงขั้นตอน "average/median/other" เหมือน log เดิม — [Business Analysis and Valuation - docenti.unina.it]

**ปรับความต่างของ growth/risk**

- สมการถดถอยตัวอย่างของ Damodaran: PE = 12.41 + 109.95 x growth - 6.60 x beta (R² 59%) และ PE = 12.311 - 1.953 x beta + 9.70 x payout (R² 37.6%, ตัด growth ออกเพราะไม่มีนัยสำคัญ) ค่าสัมประสิทธิ์เป็นของชุดข้อมูลในหนังสือ ห้ามนำไปใช้กับหุ้นอื่น — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]
- เทียบ risk ด้วย unlever beta ของ peer แล้ว relever ตามโครงสร้างทุนของเป้าหมาย (pure play) — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Pure Play Method - What Is It, Process Steps, Formula, Examples - WallStreetMojo]
- ถ้า leverage ของ peer ต่างกันมาก ใช้ EV multiples แทน price multiples — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- CFI ยอมรับว่า EV/EBITDA ปรับตามความต่างของ growth ยาก และอธิบาย premium/discount ได้ยาก — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]

**หลักฐานความแม่นยำของ multiples (ใหม่)**

- ใน sample บริษัทจดทะเบียนขนาดใหญ่ (ข้อมูลจาก Thomson Reuters; excerpt ที่ได้ไม่ระบุตลาด) benchmark แบบ mean GICS industry มี MdAPE: EV/EBITDA 25%, EV/EBIT 26%, P/E 25%, EV/Sales 47% และ R² ต่ำ (8%-23%) ส่วนโมเดล GBDT ลด MdAPE เหลือ 6%-8% และ R² 67%-80% EV/Sales คลาดเคลื่อนสูงสุดและไม่เหมาะทุกอุตสาหกรรมหรือทุกช่วงชีวิตบริษัท — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- งาน IPO (4 บริษัท เล็กเกินสรุปทั่วไป): P/E และ EV/LTM Revenue ทำนายราคา 1 เดือนหลังจดทะเบียนได้แม่นสุด ขณะที่ EV/EBITDA และ EV/EBIT ให้ราคาที่ห่างจากความเป็นจริงมากในตัวอย่าง Volcom (ราคาที่คำนวณ 85.05 และ 106.04 เทียบ P/E 25.88) — [Examining IPO Valuation Methods - NYU Stern]
- ตัวอย่าง Lockheed Martin แสดงความกระจายของผลจากคนละ multiple: ราคาที่ implied ต่างกันมาก (P/E 882.86, P/B 92.54, P/S 494.40, EV/EBITDA 647.32 เทียบราคาตลาด 465.31) ผู้เขียนสรุปว่า relative valuation ให้ผลปนกัน — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ธนาคาร: P/BV, P/tBV, P/tNAV บอกผลงานระยะยาวได้ดีกว่า P/E (Forte et al. 2020 ตามที่ source อ้าง) — [MDPI bank equity valuation case study]
- relative valuation อาจไม่จับลักษณะเฉพาะของบริษัทและได้รับอิทธิพลจากตลาดที่ไม่มีประสิทธิภาพ — [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK: A CASE STUDY OF LUMINOR BANK AS - Digikogu]

**ข้อผิดพลาดที่พบบ่อย (ใหม่หรือเสริม log เดิม)**

- พึ่งรหัสอุตสาหกรรมกว้าง ๆ อย่างเดียว ทำให้ peer ไม่คล้ายกัน — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu], [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- เลือก peer เองแบบมี bias — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- ไม่กรอง outlier ที่ติดลบ/ผิดปกติก่อนหาค่าเฉลี่ย — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ผูกฐานกำไรของบริษัท cyclical กับปี peak/trough (base year fixation) และ "false stability" คือขยับไปใช้ EBITDA/revenue โดยไม่คุมความผันผวนต่างกันของแต่ละบริษัท รวมทั้งนับ growth ซ้ำเมื่อ normalize กำไรแล้วยังใช้ growth สูงจากนักวิเคราะห์ — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- จับคู่ cash flow กับ discount rate ผิดประเภท (บริบท DCF) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- จัดการ stock option/SBC ผิด: ควรนับ option ที่ค้างอยู่เข้า market cap (option-corrected P/E) และไม่ควรบวกกลับ SBC เข้ากำไร — [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences Aswath Damodaran Stern School of Busines - NYU Stern], [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| (Out)smart the Peer Group in Market Comparison - ResearchGate | "There is no single optimal method" |
| (Out)smart the Peer Group in Market Comparison - ResearchGate | "the median is preferred by practitioners thanks to its robustness to outliers" |
| VALUATION OF LOCKHEED MARTIN ... - Digikogu | "In the case of a larger range of values, the median would be preferred" |
| Examining IPO Valuation Methods - NYU Stern | "valuation errors decline when the industry definition ... is narrowed" |
| VALUATION OF LOCKHEED MARTIN ... - Digikogu | "these classification codes tend to be too broad" |
| EV/EBITDA - Definition, Formula, Uses & Pros and Cons - CFI | "Find 5-10 companies that you believe are similar enough" |

## สิ่งที่ไม่พบใน notebook

- กฎจำนวน peer ขั้นต่ำหรือเหมาะสม: มีแต่ตัวอย่าง (5-11) ไม่ใช่กฎ
- เกณฑ์ตัวเลขสำหรับตัด outlier หรือ trim (source มีเพียงหัวข้อรูปทดสอบ trimming 1%-20% โดยไม่มี excerpt ผลสรุป)
- วิธี median/mean/harmonic ที่ดีที่สุดสำหรับ multiples เดี่ยว ๆ: source สรุปเองว่าไม่มีวิธีที่ดีที่สุด และผลทดสอบเป็นของ benchmark แบบ industry-mean ใน ResearchGate ไม่ใช่ peer group 5-10 ตัวที่เลือกเอง
- PEG (ดู log multiples-pe-ev-pbv-v2)
- ตัวเลขความแม่นยำของ multiples ในตลาดหุ้นไทย/ตลาดเกิดใหม่ ไม่มีใน source
- ตัวเลข MdAPE ข้างต้นเป็นผลของ sample ในงานวิจัยนั้น (excerpt ไม่ระบุตลาดชัดเจน) ไม่ควรนำไปอ้างเป็นช่วงความคลาดเคลื่อนของหุ้นไทยหรือหุ้นอื่น
