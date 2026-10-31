# Valuation ของบริษัท cyclical และ commodity

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** bcb1d561-2e75-4e4b-a255-5bfbada610ab

## คำถาม

How should cyclical and commodity companies be valued? Cover normalized earnings, mid-cycle margins, commodity price assumptions, and which multiples are misleading at cycle peaks and troughs.

## คำตอบสรุป

source ที่ notebook ใช้ตอบข้อนี้มีเพียงแหล่งเดียว คือ [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern] (Damodaran, 2009) ทุกข้อด้านล่างจึงมาจาก source นี้

**ปัญหาหลัก**

- มูลค่าของบริษัท cyclical/commodity ขึ้นกับตัวแปรมหภาค (ราคาสินค้าโภคภัณฑ์หรือการเติบโตทางเศรษฐกิจ) มากกว่าลักษณะเฉพาะของบริษัท และมี operating leverage สูง กำไรจึงแกว่งแรงกว่ารายได้ — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- base-year fixation: ถ้าฐานปีล่าสุดอยู่ที่จุดสูงสุดของวัฏจักรจะประเมินมูลค่าสูงเกินจริง ถ้าอยู่ที่จุดต่ำสุดจะประเมินต่ำเกินจริง และ input อื่นนอกจากกำไรก็เบี้ยวตามวัฏจักรด้วย — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- แนวทางของ source: การพยายามพยากรณ์วัฏจักรรอบหน้าไร้ประโยชน์และอันตราย ควร normalize กำไรและกระแสเงินสดข้ามวัฏจักรแทน — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**Normalized earnings และ mid-cycle margin**

- ปีปกติของบริษัท cyclical คือจุดกลางวัฏจักร ส่วนบริษัท commodity คือปีที่ราคาสะท้อนราคาที่แท้จริงตามอุปสงค์อุปทาน และ source ยอมรับว่าการนิยาม "ปกติ" มีความเป็นอัตนัย — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- เทคนิค normalize สำหรับบริษัท cyclical มี 3 แบบ (1) ค่าเฉลี่ยสัมบูรณ์ตามเวลา (เฉลี่ยกำไรหลายปี) ซึ่งเข้าใจง่ายแต่ประเมินต่ำถ้าบริษัทโตขึ้นระหว่างช่วงนั้น (2) ค่าเฉลี่ยเชิงสัมพัทธ์ คือเฉลี่ย margin หรือผลตอบแทนต่อทุนข้ามวัฏจักรแล้วคูณกับรายได้หรือเงินลงทุนปัจจุบัน และใช้อัตราส่วนต่อรายได้หรือ book capital กับ capex และ working capital (3) ค่าเฉลี่ยของ sector สำหรับบริษัทที่มีประวัติสั้นหรือเปลี่ยนแปลงการดำเนินงาน — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ช่วงที่ source กล่าวถึงสำหรับการเฉลี่ยกำไรคือ 5 ถึง 10 ปี — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ข้อผิดพลาดที่พบบ่อย: normalize ไม่ครบ (incomplete normalization) คือ normalize เฉพาะกำไร แต่ปล่อย return on capital, reinvestment, ต้นทุนเงินทุน และสัดส่วนหนี้ไว้ที่ระดับของปีปัจจุบัน ต้อง normalize ทั้งหมดให้สอดคล้องกัน — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- อย่านับซ้ำ: ถ้าปรับกำไรขึ้นสู่ระดับ normalized แล้ว ไม่ควรใส่อัตราเติบโตสูงซ้ำบนฐานนั้น — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**สมมติฐานราคา commodity**

- ใช้ราคา normalized จากค่าเฉลี่ยย้อนหลังที่ปรับเงินเฟ้อ หรือจากการวิเคราะห์อุปสงค์อุปทานระยะยาว (ต้นทุนการผลิตส่วนเพิ่ม) — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ใช้ราคาจากตลาด futures/forward สำหรับกระแสเงินสดระยะใกล้ เพื่อตัดมุมมองของนักวิเคราะห์ออก (ถ้าใช้ราคา normalized เช่น 100 เหรียญเทียบกับราคาตลาด 45 เหรียญ ผลมูลค่าจะสะท้อนมุมมองต่อราคาน้ำมันเท่าๆ กับมุมมองต่อบริษัท) — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ทางเลือก: ให้อัตราเติบโตเป็นกลไกพากลับสู่ภาวะปกติ คือใส่การเติบโตต่ำหรือติดลบที่จุดสูงสุดของวัฏจักร และสูงที่จุดต่ำสุด พร้อมให้ margin ค่อยๆ กลับสู่ระดับ normalized ในระยะยาว — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ทางเลือก: scenario analysis และ Monte Carlo simulation ของราคาสินค้า และ real options สำหรับแหล่งสำรองที่ยังไม่ได้พัฒนา (บวก premium เข้ากับ DCF) — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**Multiples ที่ทำให้เข้าใจผิดที่จุดสูงสุดและต่ำสุด**

- P/E ของบริษัท cyclical/commodity จะต่ำที่สุดตอนวัฏจักรขึ้นสูงสุด และสูงที่สุดตอนวัฏจักรต่ำสุด ซึ่งดูสวนทาง แต่สะท้อนว่าตลาดประเมินมูลค่าระยะยาว source ยกตัวอย่าง P/E 6 เท่าอาจ "สมเหตุสมผล" ที่จุดสูงสุด และ 15 เท่าที่จุดต่ำสุด ดังนั้น P/E ต่ำที่จุดสูงสุดไม่ได้แปลว่าถูก — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ตอนกำไรติดลบ P/E คำนวณไม่ได้ การขยับขึ้นไปใช้ EV/EBITDA หรือ revenue multiple จึงนิ่งกว่าและคำนวณได้ แต่ source เตือนว่าเป็น "false stability" เพราะผู้ลงทุนยังสนใจกำไรและกระแสเงินสดสุดท้าย และความผันผวนของ margin กับ capital intensity ที่ต่างกันระหว่างบริษัทไม่ถูกจับ — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- วิธีที่ถูกกว่า: ใช้ multiple กับกำไร normalized (เฉลี่ย 5-10 ปี) และต้องเทียบ multiple กับตำแหน่งในวัฏจักร — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "far better to normalize earnings and cash flows across the cycle" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "we will consistently under estimate their values" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "tend to have high operating leverage (high fixed costs)" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "average earnings over a period (5 to 10 years)" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "multiples of earnings ... will bottom out at the peak of the cycle" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "False Stability" |

## สิ่งที่ไม่พบใน notebook

- ไม่มีตัวเลข mid-cycle margin หรือราคา commodity normalized ของบริษัท/อุตสาหกรรมจริง (source เป็นบทความวิธีการ ปี 2009 ใช้ตัวอย่างเก่า เช่น ราคาน้ำมันเดือนมีนาคม 2009)
- notebook ตอบจาก source เดียว จึงไม่มีมุมมองเปรียบเทียบจากหลายผู้เขียน
- ข้อความ "ปรับ target multiple ให้ต่ำตอนจุดสูงสุดและสูงตอนจุดต่ำสุด" เป็นการตีความของ notebook จากประเด็นเรื่อง P/E ที่กลับด้านตามวัฏจักร ไม่ใช่คำแนะนำที่ source ระบุเป็นขั้นตอนตรงๆ
