# Multiples v2: P/E, EV/EBITDA, P/BV, EV/Sales, PEG (trailing vs forward, ความเหมาะสม, consistency)

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`) หลังเพิ่ม source ใหม่ 5 ชิ้น
- **conversation_id:** e7db482c-086e-425d-926c-3e03851a2830 (คำถามหลัก), 42065706-cd77-4591-a26a-e3e35e4df19e (คำถามต่อเรื่อง PEG)
- **หมายเหตุ:** log นี้เติมจาก `2026-10-31_multiples-pe-ev-pbv.md` ที่ถามไปแล้ว เนื้อหาส่วนที่ซ้ำกับ log เดิม (สูตร Gordon growth, justified P/BV, consistency rule จาก docenti) ไม่เขียนซ้ำ เน้นสิ่งที่ใหม่

## คำถาม

คำถามหลัก: Define P/E, EV/EBITDA, P/BV, EV/Sales and PEG: give the formulas. For each, what are the fundamental drivers (growth, payout, ROE, risk, margins)? Which business types does each multiple fit best? What do the sources say about trailing versus forward multiples? What is the consistency rule between equity multiples and enterprise multiples, including the required denominator? Include evidence from the thematic multiples paper, the IPO valuation paper, and the Valuation Methods CFI page.

คำถามต่อ: Do any sources define the PEG ratio (P/E divided by expected earnings growth) or explain how to use it to compare companies with different growth rates? Quote or paraphrase only text that explicitly mentions PEG or P/E-to-growth.

## คำตอบสรุป

**Trailing vs forward (ใหม่ ครั้งก่อนไม่ได้ครอบคลุม)**

- Forward (leading) P/E ใช้กำไรที่คาดการณ์ โดยนักวิเคราะห์ส่วนใหญ่ใช้ forecast 1-3 ปี สูตร forward P/E = payout / (ke - g) — [MDPI bank equity valuation case study]
- ตัวอย่างว่า trailing P/E เพี้ยนได้: ราคา 14.80 EPS 12 เดือนย้อนหลัง 0.05 ได้ trailing P/E = 296 เทียบ P/E อุตสาหกรรม 28 แต่ถ้าใช้กำไรที่คาด 0.27 forward P/E = 55 วิธีแก้ที่ slide เสนอคือใช้ forward P/E หรือใช้กำไร pro forma ที่ตัดรายการไม่เกิดซ้ำ — [Business Analysis and Valuation - docenti.unina.it]
- ในวงการ M&A มีการพึ่ง trailing multiple มากกว่า forward ส่วนนักวิเคราะห์หุ้นเลือก P/E เป็นโมเดลโปรดใน 20 จาก 25 กลุ่มอุตสาหกรรม GICS (ตารางสรุป literature review ที่ source นี้รวบรวม ไม่ใช่ผลวิจัยของ source เอง) — [Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review]
- ผลทดสอบ IPO: P/E ปีก่อนหน้า (ตามรายงานนักวิเคราะห์) ทำนายราคาหลังจดทะเบียน 1 เดือนได้แม่นกว่า P/E ปีถัดไปที่คาด แต่งานของ Deloof และคณะ (Ghent) ที่ source อ้างถึงพบตรงข้ามคือใช้กำไรปีหลัง IPO ที่คาดแม่นกว่ากำไรปี IPO ผู้เขียนเตือนว่ากลุ่มตัวอย่าง 4 บริษัทเล็กเกินจะสรุปทั่วไป — [Examining IPO Valuation Methods - NYU Stern]
- งานทดสอบ machine learning เลือกใช้ข้อมูลบัญชีย้อนหลังแทน forecast เพื่อไม่ให้ตัวอย่างลดลงจากการที่ไม่มี forecast — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- วิธีทำ trailing 12 เดือนจากงบ: ใช้ 10-K ฉบับล่าสุดลบไตรมาสแรก ๆ ของปีก่อนแล้วบวกไตรมาสของปีนี้ การ update มีผลมากกับบริษัทเล็ก ผันผวน หรือเพิ่ง restructure — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- บริษัท cyclical: multiple ของกำไรต่ำสุดที่จุด peak และสูงสุดที่จุด trough ตัวอย่าง P/E 6 ถือว่า fair ที่ peak แต่ P/E 15 fair ที่ trough — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**นิยามที่ได้เพิ่ม**

- EV = market cap + debt - cash (debt หัก cash คือ net debt) EV/EBITDA คือ EV หาร EBITDA ใช้ 5 อย่าง: ดู multiple ปัจจุบัน, เทียบหลายบริษัท, คำนวณ terminal value ใน DCF, เจรจาซื้อธุรกิจ, ตั้งราคาเป้าหมายในรายงาน equity research — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]
- ข้อดีข้อเสียของ EV/EBITDA ตาม CFI: คำนวณง่าย ใช้กันกว้าง เหมาะกับธุรกิจนิ่งที่ capex ต่ำ แต่ไม่ใช่ตัวแทน cash flow ที่ดี ไม่นับ capex ปรับตามความต่างของ growth ยาก และอธิบาย premium/discount ได้ยาก — [EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute]
- การแบ่งกลุ่ม: equity multiples = P/E, P/B, P/S (ราคาหุ้นเทียบตัวเลขทางบัญชี) ส่วน enterprise value multiples คิดมูลค่าเงินทุนทั้งหมดเทียบมาตรวัดของทั้งธุรกิจ เช่น EV/EBITDA — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu] (สังเกต: P/S ใน source นี้เป็น equity multiple ส่วน EV/Sales เป็น enterprise multiple)
- กลุ่ม enterprise ที่ตัวหารเป็น unlevered: EV/NOPAT, EV/EBIT, EV/EBITDA, EV/Sales ส่วนกลุ่ม levered: P/E, P/CF — [Business Analysis and Valuation - docenti.unina.it]

**ตัวขับ (drivers) ที่ใหม่**

- EV/Sales: ในโมเดล machine learning ปัจจัยสำคัญสุด 3 อันดับคือ asset turnover, ค่าเฉลี่ย multiple ของ GICS Industry และ EBIT margin ส่วน P/E มี ROE เป็นปัจจัยเด่นเพิ่ม (นี่คือหลักฐานเชิงประจักษ์ ไม่ใช่สูตรทฤษฎี) — [(Out)smart the Peer Group in Market Comparison - ResearchGate]
- หลักทั่วไป: multiple ผูกกับ growth, risk, profitability ตามกรอบ DCF — [Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review]; firm ที่มี growth สูงกว่าได้ multiple ของกำไรที่ normalize สูงกว่า ส่วนบริษัทกำไรผันผวนได้ต่ำกว่า — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**ความเหมาะสมกับธุรกิจ (ที่ใหม่)**

- ธนาคาร/ประกัน: value และ operating income ประมาณยาก จึงใช้ equity multiples (P/E, P/BV, P/S) — [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern]; งานที่ review ใน source ธีมเมติกระบุว่า book value อธิบายมูลค่าได้ดีกว่ากำไรเมื่อบริษัทเข้าใกล้ภาวะล้มละลาย — [Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review]
- บริษัทที่ขาดทุน: EV/LTM Revenue ใช้ได้เมื่อบริษัทหรือคู่เทียบมีกำไรติดลบ — [Examining IPO Valuation Methods - NYU Stern]
- ถ้า leverage ของ peer ต่างกันมาก ควรใช้ EV multiples แทน price multiples (Trugman อ้างโดย source) — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ผลสำรวจการจัดอันดับโมเดลของนักวิเคราะห์ใน source: multiples มีบทบาทมากกว่า DCF ในแทบทุกภาคส่วน ยกเว้น Utilities — [Examining IPO Valuation Methods - NYU Stern]

**ความแม่นยำ (สรุปสั้น ละเอียดอยู่ใน log peer-selection-v2)**

- ในงาน IPO P/E และ EV/LTM Revenue แม่นที่สุด — [Examining IPO Valuation Methods - NYU Stern]; ในงาน ML EV/Sales คลาดเคลื่อนสูงสุดและไม่เหมาะทุกอุตสาหกรรม/ทุกช่วงชีวิตบริษัท — [(Out)smart the Peer Group in Market Comparison - ResearchGate]

**Consistency rule**

- ยืนยันซ้ำจาก log เดิม (levered denominator สำหรับ equity multiple, unlevered สำหรับ enterprise multiple) ด้วย [Business Analysis and Valuation - docenti.unina.it] และเพิ่มหลักฐานฝั่ง DCF ว่าการจับคู่ cash flow กับ discount rate ผิดประเภททำให้มูลค่าบิดเบือน (ตัวอย่างตัวเลข equity เกิน/ขาด) — [Aswath Damodaran Updated: January 2026 - NYU Stern] (excerpt พูดเรื่อง DCF ไม่ใช่ multiples)

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Business Analysis and Valuation - docenti.unina.it | "Use the forward P/E ratio" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "will bottom out at the peak of the cycle" |
| (Out)smart the Peer Group in Market Comparison - ResearchGate | "EV/Sales multiple consistently shows higher prediction errors across all metrics" |
| Examining IPO Valuation Methods - NYU Stern | "proved to be the most accurate forecasters" |
| VALUATION OF LOCKHEED MARTIN ... - Digikogu | "using enterprise value multiples rather than price multiples could be wiser" |
| EV/EBITDA - Definition, Formula, Uses & Pros and Cons - Corporate Finance Institute | "Hard to adjust for different growth rates" |

## สิ่งที่ไม่พบใน notebook

- **PEG ratio:** คำถามต่อยืนยันว่าไม่มี source ใดนิยามหรือกล่าวถึง PEG ตรง ๆ notebook ตอบเองว่า "None of the provided sources explicitly define or mention the PEG ratio" สูตร PEG ในคำตอบแรกจึงมาจากความรู้ของโมเดลไม่ใช่ source ห้ามนำไปอ้าง สิ่งที่ source มีใกล้เคียงที่สุดคือ P/E เพิ่มตาม growth (P/E = 1/(r-g)) และสมการถดถอย P/E กับ growth และ beta — [Business Analysis and Valuation - docenti.unina.it], [Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern]
- สูตร EV/Sales และ drivers เชิงทฤษฎี (นอกจากผล feature importance ของ ML) ไม่มี excerpt สูตรตรง ๆ
- ตัวเลขช่วง multiple ที่เหมาะสมของแต่ละกลุ่มธุรกิจ
- ข้อสรุปว่า trailing หรือ forward ดีกว่าอย่างสม่ำเสมอ: source ขัดกันเอง (ดูผล IPO) และกลุ่มตัวอย่างเล็ก
- ข้อดีข้อเสียของ trailing/forward ตามที่ notebook สรุป (เช่น forward ขึ้นกับความแม่นของนักวิเคราะห์) ไม่มี citation ที่พูดตรง ๆ จึงตัดออก
