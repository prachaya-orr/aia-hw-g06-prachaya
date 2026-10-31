# Football field v2: วิธีที่ใส่ กำหนดช่วงแท่ง ตีความราคาปัจจุบัน และการรวม DCF/comps/precedents

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`) หลังเพิ่ม source ใหม่ 5 ชิ้น (โดยเฉพาะ CFI Valuation Methods)
- **conversation_id:** 10c6d8bb-508f-47b4-9a4b-45a5310a6567 (คำถามหลัก), dd0d5a56-9b41-4f39-b75e-39ebd29498c9 (คำถามต่อ ตรวจว่า WSP/CFI พูดอะไรตรง ๆ)
- **หมายเหตุ:** เติมจาก `2026-10-31_football-field.md` ที่ใช้ Wall Street Prep เป็น source เดียว

## คำถาม

คำถามหลัก: How is a football field valuation chart constructed? Which methods are included (DCF, trading comps, precedent transactions, 52-week range, analyst price targets)? How are the low and high ends of each bar set (percentiles, sensitivity analysis)? How is the current share price interpreted against the chart? How are the three main approaches (DCF, comparable companies, precedent transactions) combined or weighted to reach a conclusion on value?

คำถามต่อ: In the Wall Street Prep football field page and the CFI Valuation Methods page, what exactly do they say about (a) how bar ranges are set (percentiles, min/max, sensitivity), (b) analyst price targets as a bar, (c) the average or midpoint line, and (d) any weighting of DCF, comps and precedents? Report only what is explicitly stated.

## คำตอบสรุป

**วิธีที่ใส่ในแท่ง (ใหม่: analyst targets และเส้นเฉลี่ยมี source แล้ว)**

- CFI ระบุว่านักวิเคราะห์ทำ football field เพื่อสรุปช่วงมูลค่าจากหลายวิธี ตัวอย่างกราฟมีแท่ง: 52-week trading range, ช่วงราคาเป้าหมายของนักวิเคราะห์ (analyst price targets), ช่วงจาก comps, ช่วงจาก precedent transactions และ DCF และมีเส้นประสีส้มกลางกราฟแทน "ค่าเฉลี่ยของมูลค่าจากทุกวิธี" — [Valuation Methods - Three Main Approaches to Value a Business (CFI)]
- Wall Street Prep ระบุชุดมาตรฐาน: DCF, LBO, Comparable Company, Precedent Transactions, 52-week high/low และตัวเลือก Liquidation, Sum-of-the-Parts โดย WSP ไม่ได้ listing analyst targets — [Football Field Valuation Chart - Excel Tutorial + Example - Wall Street Prep]
- จุดประสงค์ของ chart คือ sanity-check หลายวิธีเทียบกัน เช่น comps อาจสูงในตลาดแรง ขณะที่ DCF ต่ำกว่า และใช้ใน fairness opinion ด้วย — [Football Field Valuation Chart - Excel Tutorial + Example - Wall Street Prep]
- ลักษณะของแต่ละวิธีตาม CFI: DCF เป็น intrinsic ละเอียดสุดและต้องใช้สมมติฐานมากสุด (CFI อ้างว่ามักให้ผลแม่นสุดเพราะความพยายามที่ใส่) รองรับหลาย scenario และ sensitivity; comps เทียบ multiples เช่น P/E, EV/EBITDA โดย EBITDA multiple ใช้บ่อยสุด; precedent transactions รวม takeover premium เป็นมูลค่า en bloc แต่เก่าเร็ว และใช้น้อยกว่า comps — [Valuation Methods - Three Main Approaches to Value a Business (CFI)]
- ฝั่ง REIT: trading comps สะท้อนมูลค่าหุ้นแบบไม่มีอำนาจควบคุม ส่วน transaction comps สะท้อนราคาที่จ่ายเพื่อควบคุมจึงมี control/acquisition premium — [REIT Valuation Methods - Financial Edge Training]

**กำหนดปลายล่าง/บนของแท่ง**

- คำถามต่อยืนยันว่า excerpt ของ WSP และ CFI **ไม่ได้ระบุ** วิธีกำหนดปลายแท่งด้วย percentile (25th/75th) หรือ min/max ในตัว chart notebook ตอบว่า "does not explicitly state" ดังนั้นข้อความใน log ก่อนหน้า (football-field.md) ว่า comps ใช้ min/25th ถึง max/75th และ DCF ใช้ WACC สูง/terminal growth ต่ำเป็นปลายล่าง ไม่มีหลักฐานรองรับใน excerpt ให้ถือว่า **ไม่พบ**
- สิ่งที่ source อื่นแสดงเป็นแนวปฏิบัติเรื่อง DCF range (ไม่ได้เรียกว่า football field): ใช้ตาราง sensitivity สองตัวแปร ตัวอย่างคือ discount rate เทียบ terminal EBITDA multiple เปลี่ยนทีละ 1.0x รอบ 5.0x ปลาย "absolute bottom" คือ discount rate สูงสุดกับ multiple ต่ำสุด และปลายล่างนี้เป็นค่าที่ใกล้ราคาตลาดหลัง IPO ที่สุด ช่วง DCF ของ Volcom ในงานนี้คือ 34.6 ถึง 72.1 (ตัวเลขตัวอย่างของ source ห้ามนำไปใช้) — [Examining IPO Valuation Methods - NYU Stern]
- Lockheed Martin: ทำ sensitivity ของ WACC กับ long-term growth และคำนวณ DCF จากประมาณการนักวิเคราะห์แบบ average, low, high ได้ implied price ต่ำ/เฉลี่ย/สูง — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ช่วงของ comps/precedents คือ implied price จาก multiple ของ peer คูณตัวชี้วัดของบริษัท (เช่น EPS, EBITDA) — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]; ตำรากล่าวขั้นตอนเลือกตัวชี้วัด คำนวณ multiple ของ peer แบบ average/median/other แล้วคูณกับบริษัทเป้าหมาย — [Business Analysis and Valuation - docenti.unina.it]

**อ่านราคาปัจจุบันเทียบ chart**

- excerpt ของ WSP/CFI ไม่ได้อธิบายการตีความเส้นราคาปัจจุบันตรง ๆ (ยกเว้นเป้าหมาย sanity-check) สิ่งที่มี source รองรับคือตัวอย่างการเทียบมูลค่ากับราคา: DCF จากประมาณการเฉลี่ย (ฐานที่ผู้เขียนปรับ) ได้ 484.94 สูงกว่าราคาตลาดจึงสรุปว่าตลาดประเมินต่ำไป แต่ DCF 804.12 สูงกว่าราคา 465.31 มากจนผู้เขียนเห็นว่าไม่น่าเป็นจริง และ scenario low-estimate ได้ 461.13 สรุปว่าแพงเล็กน้อย จึงอ่านผลร่วมกับ sensitivity — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ตัวอย่าง IPO: ปลายล่างของช่วง DCF ใกล้ผลงานตลาดจริง ช่วยลด "money left on the table" — [Examining IPO Valuation Methods - NYU Stern]

**การรวม/ถ่วงน้ำหนัก 3 วิธี**

- คำถามต่อยืนยัน: WSP และ CFI **ไม่ได้ระบุสูตรถ่วงน้ำหนัก** DCF/comps/precedents CFI แสดงเส้นเฉลี่ยของทุกวิธีแบบไม่ถ่วงน้ำหนัก — [Valuation Methods - Three Main Approaches to Value a Business (CFI)]
- แนวคิดการรวมจาก source อื่น: ใช้ relative valuation เสริมหลังทำ DCF เพื่อเพิ่มความแม่นและความน่าเชื่อถือ (Fernández อ้างโดย source) การพึ่ง DCF อย่างเดียวไม่แข็งแรงพอ — [VALUATION OF LOCKHEED MARTIN CORPORATION USING DISCOUNTED CASH FLOW AND RELATIVE VALUATION METHODS - Digikogu]
- ในงาน IPO การเฉลี่ย multiple ที่แม่นสุดกับผล DCF ช่วยลด mispricing ให้บริษัทที่ถูกตั้งราคาผิดมากที่สุด แต่ไม่ดีกว่ากรณีที่ตั้งราคาถูกอยู่แล้ว และอ้าง Spence ว่าควรใช้หลายวิธี (ปกติ 3 วิธี) ได้ช่วงมูลค่าแล้วใช้ดุลยพินิจเลือกค่า — [Examining IPO Valuation Methods - NYU Stern]
- นักวิเคราะห์เสนอให้ใช้หลายแนวทางพร้อมกันเพื่อผลที่เชื่อถือได้ — [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK: A CASE STUDY OF LUMINOR BANK AS - Digikogu]
- การถ่วงน้ำหนักแบบ probability ที่ source มีเป็นของ scenario ภายใน DCF ของ cyclical (50% วงจรเดิม, 50% breakout) ไม่ใช่การถ่วงข้ามวิธี — [How to value cyclical companies - McKinsey]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Valuation Methods - Three Main Approaches to Value a Business (CFI) | "The orange dotted line in the middle represents the average valuation from all the methods." |
| Valuation Methods - Three Main Approaches to Value a Business (CFI) | "the range of prices analysts have for the stock" |
| Football Field Valuation Chart - Wall Street Prep | "sanity-check various methodologies against one another" |
| Examining IPO Valuation Methods - NYU Stern | "obtain a range of values" |
| VALUATION OF LOCKHEED MARTIN ... - Digikogu | "relying, for instance, only on DCF would mean" (ประโยคต่อไม่ยก) |

## สิ่งที่ไม่พบใน notebook

- วิธีกำหนดปลายแท่งด้วย percentile หรือ min/max ที่ source ระบุตรง ๆ สำหรับ trading comps และ precedents (ที่ log ก่อนหน้าเขียนว่า 25th/75th ไม่มีหลักฐานรองรับ)
- วิธีกำหนดปลายแท่ง DCF สำหรับ football field โดยเฉพาะ (มีแต่แนวปฏิบัติ sensitivity จาก source อื่น)
- วิธีอ่านเส้นราคาปัจจุบันที่ source football field ระบุตรง ๆ (มีเฉพาะตัวอย่างเทียบมูลค่ากับราคาใน Lockheed Martin และ IPO)
- น้ำหนักถ่วงที่ควรให้ DCF/comps/precedents ตามบริบท (เช่น sell-side M&A ให้ precedents มากกว่า): notebook พูดไว้ในคำตอบแรกแต่ไม่มี citation จึงตัดออก
- ขั้นตอนสร้างใน Excel ไม่ได้ถามซ้ำรอบนี้ ข้อมูลอยู่ใน log football-field.md เดิม (ส่วน percentile ในนั้นให้ถือว่าไม่ยืนยัน)
