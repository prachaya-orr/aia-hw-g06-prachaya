# Stock-based compensation และ employee options ใน valuation

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** fbac498f-a964-4abf-b688-6571408fc309

## คำถาม

"How should stock-based compensation and employee stock options be treated in valuation? Compare treating SBC as an expense versus adding it back, dilution of share count, and treasury stock method versus option pricing value of outstanding options."

## คำตอบสรุป

- Wall Street มักจะ add back SBC โดยอ้างว่าเป็น non-cash แต่ source มองว่าผิด เพราะละเลยต้นทุนจาก dilution ทำให้ overvalue โดยเฉพาะบริษัทที่ออก SBC มาก — [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep]
- Damodaran: SBC ไม่เหมือน depreciation แต่เป็นการจ่ายค่าตอบแทนเป็นหุ้น (in-kind) ถ้าบริษัทขายหุ้นให้ตลาดแล้วเอาเงินมาจ่ายพนักงาน ก็จะนับเป็นค่าใช้จ่ายเงินสด จึงไม่ควร add back — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]
- ผลกระทบสองชั้นต่อมูลค่า: (1) การให้ SBC ต่อเนื่องทำให้ cash flow ในอนาคตต่ำลง จึงต้อง forecast SBC เป็นค่าใช้จ่ายและไม่ add back (2) options ที่ออกไปแล้วและยังไม่หมดอายุเป็นสิทธิเรียกร้องเพิ่มเติมบนมูลค่า equity ต้องหักมูลค่า options ออกก่อนหารด้วยจำนวนหุ้นจริง — [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets], [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences - NYU Stern]
- แนวทางทำ forecast: ประมาณมูลค่า SBC เป็น % ของรายได้แล้วใส่เป็นค่าใช้จ่าย และกฎบัญชีปัจจุบันบังคับให้บันทึก SBC เป็นค่าใช้จ่ายอยู่แล้ว การ extrapolate margin ในอดีตจึงรวม SBC แล้ว — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ไม่ถือว่า double counting: การลด earnings ตาม SBC ในอนาคต และการหักมูลค่า options เก่าที่ค้างอยู่ เป็นคนละผลกัน (ตัวอย่าง Twitter) — [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]
- Restricted stock: ที่ให้ไปแล้วให้นับรวมในจำนวนหุ้นปัจจุบัน ไม่มี deadweight cost แยกต่างหาก — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets]
- วิธีจัดการ options เดิมมี 3 แบบหลัก (1) Fully diluted shares: หาร equity value ด้วยหุ้นหลัง exercise ทั้งหมด ง่ายแต่ไม่ใส่เงินที่ได้จากการ exercise และไม่รวม time premium ทำให้ได้มูลค่าต่อหุ้นต่ำเกิน — [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences - NYU Stern]
- (2) Treasury stock method: บวกเงินที่ได้จากการ exercise (exercise price x จำนวน options) เข้า equity value แล้วหารด้วยหุ้น diluted แต่ไม่คิด time premium ของ options และมีปัญหากับ out-of-the-money options ทำให้มูลค่าต่อหุ้นสูงเกิน — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences - NYU Stern]
- (3) Option pricing: ประมาณมูลค่า options ที่ยังค้างอยู่ (เช่น Black-Scholes ปรับ dilution) หักออกจาก equity value แล้วหารด้วยจำนวนหุ้น primary เป็นวิธีที่ source แนะนำ ได้ค่าสูงกว่า diluted-share และต่ำกว่า treasury stock method — [Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences - NYU Stern], [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ข้อควรระวังของ option pricing สำหรับ employee options: ระยะยาวทำให้สมมติฐาน variance คงที่ไม่แม่น, ทำให้เกิด dilution, มักถูก exercise ก่อนครบกำหนด และต้อง vest ก่อน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ตัวอย่างตัวเลข (Wall Street Prep): แนว Damodaran ที่ไม่ add back SBC ให้ enterprise value ต่ำกว่าแนว analyst ทั่วไป ($40m เทียบ $50m) และแนวที่ดีที่สุดคือหัก SBC ใน FCF + หักมูลค่า options จาก equity + นับเฉพาะหุ้นจริงและ restricted stock — [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep]
- มุมมองของ Wall Street Prep: ฝั่งหารจำนวนหุ้น แนว Wall Street ยอมรับได้ถ้านับ unvested restricted stock ด้วย ปัญหาหลักคือการเพิกเฉย SBC ในอนาคต — [Stock Based Compensation (SBC) | Journal Entry + Examples - Wall Street Prep]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Aswath Damodaran Updated: January 2026 - NYU Stern | "you should not be adding them back." |
| Stock Based Compensation (SBC) \| Journal Entry + Examples - Wall Street Prep | "systematically overvaluing businesses by ignoring this expense" |
| Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets | "Deadweight effect of past compensation" |
| Employee Stock Options (ESOPs) and Restricted Stock ... - NYU Stern | "The correct approach to dealing with options is to estimate the value" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "The treasury stock approach fails to consider the time premium on the options." |

## สิ่งที่ไม่พบใน notebook

- ไม่พบตัวเลขเกณฑ์ว่า SBC สูงเท่าไรของรายได้จึงถือว่ามีนัยสำคัญ
- ไม่พบแนวทางเฉพาะสำหรับ SBC ใน multiple-based valuation (notebook ถามกลับเรื่อง option-adjusted P/E แต่ไม่ได้ให้คำตอบที่มี citation)
- ตารางเปรียบเทียบสามวิธีใน notebook เป็นการจัดรูปของ notebook เอง เนื้อหาข้างต้นใช้เฉพาะส่วนที่มี citation รองรับ
