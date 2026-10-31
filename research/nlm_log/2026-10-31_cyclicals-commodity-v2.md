# Valuation ของบริษัท cyclical (รอบ 2): McKinsey scenarios เทียบ normalized earnings ของ Damodaran

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 1d71157f-b02c-428e-9dd0-2ee559d5c21d
- **หมายเหตุ:** ถามหลังเพิ่ม source "How to value cyclical companies - McKinsey" ใน log เดิม `2026-10-31_cyclicals-commodity.md` มีแหล่งเดียวคือ Damodaran (2009) ส่วนที่เป็น Damodaran ด้านล่างจึงสรุปสั้นและเน้นเฉพาะจุดใหม่

## คำถาม

How should cyclical companies be valued according to McKinsey's article 'How to value cyclical companies'? Cover: (1) probabilistic scenarios of the cycle versus normal-cycle or new-trend assumptions; (2) how McKinsey compares this with using normalized earnings or mid-cycle values; (3) what base year or starting point to use for the forecast; (4) how multiples (P/E, EV/EBITDA) behave across the cycle and why the market does not simply capitalize current earnings. Say clearly which points come from McKinsey versus Damodaran's Ups and Downs paper.

## คำตอบสรุป

**ส่วนที่มาจาก McKinsey (ใหม่ทั้งหมด)**

- ไม่มีใครพยากรณ์วัฏจักรกำไรของอุตสาหกรรมได้แม่นยำ พยากรณ์เดี่ยวใดๆ ย่อมผิด McKinsey จึงแนะนำให้ใช้วิธี multiple-scenario แบบ probabilistic เพื่อเลี่ยงกับดักของพยากรณ์เดียว — [How to value cyclical companies - McKinsey]
- กรอบ 4 ขั้นตอนแบบ 2 scenario (ใช้กับมากกว่า 2 scenario ได้): (1) สร้างและประเมิน scenario "normal cycle" จากข้อมูลวัฏจักรในอดีต โดยดูเส้นแนวโน้มระยะยาวของกำไรจากการดำเนินงาน กระแสเงินสด และ ROIC (2) สร้างและประเมิน scenario "new trend line" ที่ถือว่าผลงานล่าสุดคือแนวโน้มระยะยาวใหม่ (3) เขียนเหตุผลเชิงเศรษฐศาสตร์ของแต่ละ scenario เช่น อุปสงค์ การเข้า-ออกของผู้เล่น เทคโนโลยี (4) ให้น้ำหนักความน่าจะเป็นและคำนวณมูลค่าถ่วงน้ำหนัก — [How to value cyclical companies - McKinsey]
- ตัวอย่างของ source: บริษัทที่ดูเหมือนอยู่ที่จุดสูงสุดของวัฏจักร ให้น้ำหนัก 50% ว่าวัฏจักรจะเป็นไปตามอดีตแล้วขาลง และ 50% ว่าจะหลุดจากวัฏจักรไปสู่แนวโน้มใหม่ มูลค่าคือค่าเฉลี่ยถ่วงน้ำหนักของสอง scenario (ตัวเลข 50/50 เป็นตัวอย่างประกอบ ไม่ใช่กฎ) — [How to value cyclical companies - McKinsey]
- ค่า continuing value ต้องตั้งบนระดับกำไร normalized คือจุดบนเส้นแนวโน้มกระแสเงินสดระยะยาวของบริษัท ไม่ใช่จุดสูงสุดหรือต่ำสุด — [How to value cyclical companies - McKinsey]
- ใน scenario new-trend ไม่ต้องกังวลมากกับการจำลองความเป็นวัฏจักรในอนาคต แต่วัฏจักรยังสำคัญต่อความอยู่รอดทางการเงิน (solvency) — [How to value cyclical companies - McKinsey]
- scenario ที่ได้ให้ทั้งค่าประมาณมูลค่าและกรอบขอบเขตของมูลค่า ผู้บริหารใช้ขอบเขตนี้ปรับกลยุทธ์ได้ — [How to value cyclical companies - McKinsey]
- สำหรับอุตสาหกรรมที่ผูกกับ commodity การเริ่มโมเดลจากรายได้อาจไม่ดีที่สุด ตัวอย่างโรงงานโพลีเอทิลีน: ให้โมเดลปริมาณและ crack spread (ส่วนต่างราคาผลิตภัณฑ์กับต้นทุนวัตถุดิบ) แล้วหักค่าใช้จ่ายดำเนินงาน — [How to value cyclical companies - McKinsey]
- ผลการศึกษาของ McKinsey กับ 15 บริษัทที่มีวัฏจักร 4 ปี: ราคาหุ้นผันผวนมากกว่าที่ DCF คาด ซึ่งชี้ว่าตลาดมีอคติ anchoring กับกำไรปัจจุบัน และราคาตลาดไม่ได้ตามเส้น perfect foresight หรือ zero foresight แต่ตามเส้นผสมที่ใกล้ 50-50 มากกว่า — [How to value cyclical companies - McKinsey]
- ถ้ามี perfect foresight ค่า DCF จะผันผวนน้อยกว่ากำไรมาก เพราะปีกระแสเงินสดสูงหักล้างปีต่ำ มีเพียงแนวโน้มระยะยาวที่สำคัญ — [How to value cyclical companies - McKinsey]
- consensus forecast ของนักวิเคราะห์ไม่ทำนายวัฏจักรกำไร แต่คาดการณ์เส้นขึ้นเรียบๆ source ให้คำอธิบายว่านักวิเคราะห์มีแรงจูงใจเลี่ยงการทำนายขาลง (ประเด็นนี้เป็นสมมติฐานที่ source เสนอ ไม่ใช่ข้อสรุปที่ยืนยันแล้ว) — [How to value cyclical companies - McKinsey]
- ผลงานในอดีตต้องตีความตามตำแหน่งในวัฏจักร ผลงานที่แย่ลงอาจเป็นแค่ช่วงอื่นของวัฏจักร ไม่ใช่แนวโน้มลบระยะยาว — [How to value cyclical companies - McKinsey]

**เทียบกับ Damodaran (จุดที่ใหม่หรือเน้นต่างจาก log เดิม)**

- จุดต่างหลัก: Damodaran มองว่าการพยายามพยากรณ์วัฏจักรรอบหน้าไร้ประโยชน์และอันตราย ควร normalize กำไรข้ามวัฏจักร ส่วน McKinsey เน้นถ่วงน้ำหนักความน่าจะเป็นของ scenario แทนการเชื่อ normalized ค่าเดียว (การเทียบสองมุมนี้เป็นการจัดเรียงของ notebook โดยสองบทความไม่ได้อ้างถึงกัน) — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern], [How to value cyclical companies - McKinsey]
- จุดร่วม: ทั้งสองให้ค่าระยะยาว (terminal/continuing value) ตั้งบนระดับ normalized ไม่ใช่ peak หรือ trough — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern], [How to value cyclical companies - McKinsey]
- Damodaran ก็รองรับแนวทาง probabilistic: scenario analysis (boom, stagnation, recession) ใช้ค่าคาดหวังหรือช่วงมูลค่า และ simulation ของตัวแปรมหภาค เพราะกำไรของบริษัทเหล่านี้ขึ้นกับตัวแปรมหภาคไม่กี่ตัว — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ปีฐาน (base year): Damodaran เตือน base year fixation คือปีปัจจุบันที่ตกที่จุดสูงสุดทำให้ประเมินสูงเกิน ที่จุดต่ำสุดทำให้ประเมินต่ำเกิน และ margin, ROC, capex, working capital, ต้นทุนเงินทุนก็เบี้ยวตามวัฏจักรด้วย — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ใหม่จาก Damodaran: ปีปกติของบริษัท cyclical คือจุดกลางวัฏจักร ถ้าใช้ค่าเฉลี่ยกำไรควรเฉลี่ยยาวพอครอบคลุมวัฏจักรเต็มรอบ ซึ่งวัฏจักรเศรษฐกิจยาวได้ตั้งแต่ 2-3 ปีถึงมากกว่า 10 ปี และข้อเสียคือเฉลี่ยค่าสัมบูรณ์จะประเมินผิดถ้าบริษัทโตขึ้นระหว่างช่วงนั้น — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- วิธีประนีประนอม (adaptive growth): ให้กำไรระยะสั้นตามวัฏจักรปัจจุบัน (ประมาณ 6 เดือนถึงสองปี) แล้วใช้อัตราเติบโตพากลับสู่ระดับ normalized ระยะยาว — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- Multiples: ที่จุดสูงสุดของวัฏจักร multiple ของกำไรต่ำสุด และสูงสุดที่จุดต่ำสุด เพราะตลาดตีมูลค่าระยะยาว P/E 6 เท่าอาจ fair ที่จุดสูงสุด และ 15 เท่าที่ trough ได้ ถ้าเปรียบเทียบกันในจุดเดียวกันของวัฏจักร — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- EV/EBITDA และ EV/Revenue คำนวณได้และนิ่งกว่าเมื่อกำไรติดลบ แต่ Damodaran เรียกว่า "False Stability" — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]
- ใหม่: เมื่อ normalize แล้ว บริษัทที่กำไรเสี่ยงกว่าควรเทรดที่ multiple ของกำไร normalized ต่ำกว่า และบริษัทที่มีศักยภาพเติบโตสูงกว่าควรได้ multiple สูงกว่า — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| How to value cyclical companies - McKinsey | "any single forecast of performance must be wrong" |
| How to value cyclical companies - McKinsey | "a point on the company's long-term cash flow trend line" |
| How to value cyclical companies - McKinsey | "What ultimately matters is the crack spread, not the revenues" |
| How to value cyclical companies - McKinsey | "market prices exhibit the bias of anchoring on current earnings" |
| How to value cyclical companies - McKinsey | "the market does not follow either the perfect-foresight or the zero-foresight path" |
| How to value cyclical companies - McKinsey | "The consensus forecasts do not predict the earnings cycle at all" |
| How to value cyclical companies - McKinsey | "Only the long-term trend really matters" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "a normal year would be one that represents the mid-point of the cycle" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "far better to normalize earnings and cash flows across the cycle" |
| Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern | "False Stability" |

## สิ่งที่ไม่พบใน notebook

- **McKinsey ไม่ได้พูดถึง multiples (P/E, EV/EBITDA) ตามวัฏจักรโดยตรง:** ส่วนพฤติกรรม multiple ทั้งหมดมาจาก Damodaran ประโยคของ notebook ที่ว่า McKinsey "แสดงว่าการใช้ market multiple คงที่กับกำไรปัจจุบันให้มูลค่าผิดเพี้ยน" ไม่มี cited_text รองรับตรงๆ จึงตัดทิ้ง สิ่งที่ McKinsey แสดงจริงคือราคาหุ้นผันผวนเกิน DCF เพราะ anchoring กับกำไรปัจจุบัน
- **ประโยค "McKinsey เตือนว่า normalized earnings ค่าเดียวอันตราย" เป็นการตีความของ notebook:** ที่ source พูดคือพยากรณ์เดี่ยวใดๆ ย่อมผิด และ continuing value ของ McKinsey เองใช้ระดับกำไร normalized ข้อความไม่ได้ตำหนิ normalized earnings โดยตรง
- **McKinsey ไม่ให้ตัวเลขแนะนำจำนวนปีฐาน/ช่วงเฉลี่ยกำไร** และไม่ให้ตัวเลข mid-cycle margin หรือน้ำหนักความน่าจะเป็นที่แนะนำ (50/50 เป็นเพียงตัวอย่างและผลทดสอบกับตลาด)
- ไม่มี source ที่บอกวิธีกำหนดน้ำหนัก scenario ให้เป็นรูปธรรมนอกจากบอกให้ใช้เหตุผลเชิงเศรษฐศาสตร์และความน่าจะเป็นของมัน
- ไม่มีตัวเลขเฉพาะบริษัท cyclical ไทย และกลุ่มตัวอย่าง 15 บริษัทของ McKinsey ที่ cited_text ระบุคือบริษัทวัฏจักร 4 ปีในอุตสาหกรรมโลหะปฐมภูมิและอุปกรณ์ขนส่ง (ตลาดและช่วงเวลาไม่ปรากฏใน cited_text) ไม่ควรสรุปทั่วไปกับทุกอุตสาหกรรม
