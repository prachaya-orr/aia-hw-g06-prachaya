# Peer selection และการควบคุมความต่างของ growth/risk/ROE

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** f6e35db0-2143-478d-9d07-1e420ec47dbf (คำถามหลัก), f996e517-a818-41f5-bc45-1220418a5bdf (คำถามต่อเรื่อง mean vs median)

## คำถาม

คำถามหลัก: How should one select comparable companies for relative valuation? How do you control for differences in growth, risk and ROE among peers (e.g., regression of multiples on fundamentals, PEG ratio)? Should you use the mean or the median of peer multiples? What are the common mistakes in relative valuation?

คำถามต่อ (1 ข้อ เพราะเรื่อง mean/median บาง): In the sources, what do they say about using the average (mean) versus the median of comparable-company multiples, or about outliers and skewness in peer multiples? Quote only what sources explicitly say about peer multiples.

## คำตอบสรุป

**วิธีเลือก peer**

- เกณฑ์คัด peer: ประเภทธุรกิจ, ขนาด, ตำแหน่งการแข่งขัน, growth/profitability, leverage/risk, บริษัทจดทะเบียน — [Business Analysis and Valuation - docenti.unina.it]
- กรณีศึกษา Luminor คัด peer ด้วยความคล้ายด้านภูมิภาค/กฎระเบียบ, business model และข้อมูลที่หาได้ — [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK: A CASE STUDY OF LUMINOR BANK AS - Digikogu]
- ขั้นตอนทั่วไป: เลือกอุตสาหกรรม แล้วคัดบริษัทที่ต่างมากออก — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]
- บริษัทหลายธุรกิจหา peer เดียวทั้งบริษัทได้ยาก ให้แยกกำไรหรือรายได้ตามส่วนธุรกิจแล้วหา peer ต่อส่วน (sum-of-the-parts) — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]

**ควบคุมความต่างของ growth/risk/ROE**

- ตัวขับที่ต้องควบคุม: growth, risk (cost of equity/beta), payout, ROE — [MDPI bank equity valuation case study (A Case Study of Bank Equity Valuation Methods ... MDPI)]
- ปรับ multiple ด้วย companion variable เช่น PEG ควบคุม growth และ P/BV หารด้วย ROE; ข้อจำกัดคือสมมติว่าความสัมพันธ์เป็นเส้นตรง — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern] (excerpt ที่อ้างไม่มีคำว่า PEG ตรง ๆ)
- regress multiple กับ fundamentals ข้ามกลุ่ม peer: P/E ถดถอยกับ growth, beta, payout; P/BV ถดถอยกับ ROE, beta, growth แล้วแทนค่าของบริษัทเป้าหมายเพื่อได้ predicted multiple เทียบกับค่าจริง — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern], [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ตัวอย่างในหนังสือ Damodaran ch.21: คำนวณ predicted P/E ของ CNO Financial = 6.63 เทียบกับค่าจริง 6.31 สรุปราคายุติธรรม และ Aon predicted 13.44 เทียบกับค่าจริง 21.94 — [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]
- ใช้ justified multiple จากโมเดล Gordon growth/warranted equity เป็น benchmark ได้ — [MDPI bank equity valuation case study]

**Mean vs median**

- notebook ไม่มีกฎชัดเจน source บอกเพียงขั้นตอน "Take average/median/other" — [Business Analysis and Valuation - docenti.unina.it]
- กรณี Luminor ใช้ค่าเฉลี่ย (average) ของ multiple ใน peer group — [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK: A CASE STUDY OF LUMINOR BANK AS - Digikogu]
- คำตอบแรกของ notebook อ้างว่า median ดีกว่าเมื่อข้อมูลเบ้ แต่ citation นั้นเป็นผล Monte Carlo ของมูลค่าธนาคาร ไม่ใช่การกระจายของ peer multiples จึงไม่ถือเป็นหลักฐานของกฎนี้ และ notebook ยอมรับเองในคำถามต่อ

**ข้อผิดพลาดที่พบบ่อย**

- สมมติว่าตลาดถูกโดยเฉลี่ยทั้งกลุ่ม ถ้าทั้ง sector แพงหรือถูก relative valuation ก็พาไปผิดตาม — [Business Analysis and Valuation - docenti.unina.it], [How to: Excess Return Model for Valuing Financial Stocks]
- ใช้ multiple ของ peer ตรง ๆ โดยนัยว่า risk, growth, accounting เหมือนกัน — [Business Analysis and Valuation - docenti.unina.it]
- จับคู่ equity/enterprise ผิด เช่นใช้ EV/EBITDA กับธนาคาร — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]
- ยึดกำไรปีฐานของบริษัท cyclical โดยไม่ normalize: กำไรช่วง peak ทำให้ P/E ต่ำหลอก ช่วง trough ทำให้ใช้ไม่ได้ — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ไม่นับ stock option/restricted stock ทำให้ market cap ต่ำไปและบริษัทดูถูกเกินจริง; การบวกกลับ SBC ก็บิดเบือน — [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences Aswath Damodaran Stern School of Busines - NYU Stern], [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]
- ไม่ปรับรายการพิเศษ, operating lease, R&D ก่อนเทียบ — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Business Analysis and Valuation - docenti.unina.it]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Business Analysis and Valuation - docenti.unina.it | "Take average/median/other." |
| Business Analysis and Valuation - docenti.unina.it | "Assume market correctly sets competitors' stock prices." |
| Business Analysis and Valuation - docenti.unina.it | "they are right, on average, in how they price an industry" |
| Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern | "higher growth firms tend to have higher PE ratios" |

## สิ่งที่ไม่พบใน notebook

- กฎเลือก mean หรือ median สำหรับ peer multiples (notebook ยืนยันว่า source ไม่ได้อธิบาย trade-off ทางสถิติของ peer multiples)
- เกณฑ์เชิงตัวเลขของขนาด peer group หรือจำนวน peer ขั้นต่ำ
- สูตร PEG พร้อม excerpt ยืนยันตรง ๆ
