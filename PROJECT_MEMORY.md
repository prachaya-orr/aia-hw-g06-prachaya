# PROJECT_MEMORY.md

> ความจำระยะยาวของโปรเจกต์ AI อ่านไฟล์นี้ก่อนเริ่มงานทุกครั้ง ผู้สอนอ่านเพื่อดูว่าคุณเจออะไรมาและเรียนรู้อะไร
> ห้ามวาง error ยาว ๆ ที่อาจมี key หรือข้อมูลส่วนตัว ให้สรุปสั้น ๆ แทน

## กฎที่ได้จากบทเรียน

> กฎ 1 บรรทัด ที่ AI ต้องทำตามจากนี้ไป

- เปลี่ยนชื่อ repo บน GitHub ก่อน แล้วค่อยแก้ `origin` ในเครื่อง และเช็กด้วย `git ls-remote origin` ทุกครั้ง
- brief สั่ง `--mode deep` ต้องใช้ deep ทุกรอบที่ค้น source ห้ามลดเป็น fast เอง
- คำตอบของ NotebookLM ต้องตรวจกับ `cited_text` ทุกข้อ ประโยคไหนไม่มีข้อความใน source รองรับให้ย้ายไป "ไม่พบใน notebook"
- งบจาก yfinance ต้องจับคู่ตามวันสิ้นงวด ไม่ใช่ตามลำดับคอลัมน์ และคอลัมน์ที่ว่างทั้งปีห้ามเติมเอง
- ห้ามใช้ Free Cash Flow ของ Yahoo แทน FCFF ให้คำนวณจาก EBIT ตามสูตรใน playbook
- สูตร Excel ที่เป็นฟังก์ชันรุ่นใหม่ (เช่น PERCENTILE.INC) ต้องเขียนเป็น `_xlfn.` ใน openpyxl และรัน `python -m valuation verify` ทุกครั้งหลังแก้สูตร
- ผล valuation ที่ห่างจากราคาตลาดหลายเท่า ให้ไล่หาสมมติฐานที่ผิดก่อนเชื่อผล
- ห้าม commit ไฟล์ล็อกของ Office (`~$*`) เพราะมีชื่อผู้ใช้ในเครื่อง
- ห้ามใช้ `enterpriseToEbitda` ของ Yahoo ให้คิด EV/EBITDA เองจากงบรายปีด้วยนิยามเดียวกันทั้งบริษัทเป้าหมายและ peer
- เปลี่ยนโครง JSON ของข้อมูลดิบเมื่อไร ต้องเพิ่ม `SCHEMA_VERSION` ใน `fetch.py`
- หุ้นอุตสาหกรรมใหม่ ต้องเพิ่ม Yahoo industry ใน `industry_map` ของ `config.yaml` ก่อน fetch และตรวจ ticker ต่างประเทศจากชื่อใน `longName` (หุ้นมาเลเซียบน Yahoo ใช้รหัสตัวเลข เช่น IHH = 5225.KL)
- บริษัทที่มีเงินลงทุนในบริษัทร่วม/JV หรืออสังหาฯ เพื่อการลงทุนมาก ใช้ Operating Income แทน EBIT ของ Yahoo แล้วใส่ `non_operating_assets` เพื่อไม่ให้นับซ้ำ
- ใส่ `.nojekyll` แล้ว GitHub Pages ไม่แปลง .md เป็นหน้าเว็บ ต้องมี `index.html` ที่ root และลิงก์ไฟล์ .md ไปหน้า GitHub (`/blob/main/...`)

## บันทึกปัญหา

> เพิ่มต่อท้าย ห้ามลบของเก่า

### 2026-10-31 · เปลี่ยนชื่อ repo แล้ว remote หาไม่เจอ

- **เจออะไร:** `git ls-remote origin` ขึ้น `Repository not found` หลังแก้ URL ของ `origin` เป็น `aia-hw-g06-prachaya`
- **สาเหตุ:** แก้ URL ในเครื่องก่อน ขณะที่ repo บน GitHub ยังชื่อ `aia-hw-prachaya` อยู่
- **แก้อย่างไร:** เปลี่ยนชื่อบน GitHub ด้วย `gh repo rename aia-hw-g06-prachaya` แล้ว `git fetch` ผ่าน
- **ลองวิธีไหนแล้วไม่เวิร์ก:** ให้ AI รัน `gh repo rename` ครั้งแรกถูกระบบ permission บล็อก ต้องให้ผู้เรียนสั่งยืนยันอีกครั้งจึงรันได้ · ย้ายโฟลเดอร์ระหว่างที่ session เปิดอยู่ทำให้ session เดิมหาโฟลเดอร์ไม่เจอ ต้องเปิดโฟลเดอร์ใหม่เป็นที่ทำงาน

### 2026-10-31 · รอบเสริมของ NotebookLM ใช้ fast แทน deep

- **เจออะไร:** รอบค้น source เสริม (multiples, REIT, cyclical, football field) ใช้ `nlm research --mode fast` ได้แค่ 10 รายการ
- **สาเหตุ:** AI เลือก fast เองเพื่อให้เร็ว ทั้งที่ brief สั่ง deep
- **แก้อย่างไร:** ผู้เรียนทักท้วง จึงค้นใหม่แบบ deep ได้ 43 รายการ เลือก import 13 รายการ notebook รวมเป็น 32 source
- **ลองวิธีไหนแล้วไม่เวิร์ก:** source ของ ibinterviewquestions import ไม่ได้ทั้งแบบ research import และเพิ่มด้วย URL (เว็บไม่ให้ NotebookLM ดึงหน้า)

### 2026-10-31 · NotebookLM ตอบเกินหลักฐาน

- **เจออะไร:** log รอบแรกของ football field บอกว่าปลายแท่ง comps ใช้ percentile 25/75 และ PEG มีสูตร แต่ตรวจซ้ำแล้วไม่มีข้อความใน source รองรับ
- **สาเหตุ:** NotebookLM เติมความรู้ทั่วไปเข้ามาในคำตอบ แม้ citation จะชี้ไปที่ source
- **แก้อย่างไร:** ถามซ้ำแบบเจาะจง (log `-v2`) ให้ agent เทียบกับ `cited_text` แล้วย้ายข้อที่ไม่มีหลักฐานไปไว้ใน "ไม่พบใน notebook"

### 2026-10-31 · ข้อมูล yfinance ที่ต้องระวัง

- **เจออะไร:**
  - งบรายปีของ CPALL ปี 2021 ว่างทั้งคอลัมน์ และงบกระแสเงินสดมีแค่ 4 ปี ขณะที่งบอื่นมี 5 ปี
  - `enterpriseToEbitda` ของ CPALL จาก yfinance คือ 12.98 แต่หน้าเว็บ Yahoo แสดง 10.67
  - Free Cash Flow ของ Yahoo = OCF + Capex ไม่ใช่ FCFF
  - ticker ที่ไม่มีจริง yfinance ไม่ error แต่คืน info ที่ไม่มี `quoteType`
  - `totalDebt` และ `totalCash` ใน info เป็นค่าไตรมาสล่าสุด ไม่ใช่ปีงบ
- **สาเหตุ:** ข้อมูลของ Yahoo มาจากหลายตาราง อัปเดตไม่พร้อมกัน และ yfinance ไม่ตรวจความถูกต้องให้
- **แก้อย่างไร:** เก็บค่าว่างเป็น null พร้อมเหตุผล · จับคู่งวดตามวันที่ · ตรวจ `quoteType` ทุก ticker · ใช้งบรายปีแทน info สำหรับหนี้และเงินสด · EV/EBITDA ของ peer ยังไม่ได้แก้ (ดูรอบ 5)

### 2026-10-31 · Excel ขึ้น #NAME? ในชีต Comps

- **เจออะไร:** LibreOffice คำนวณ P25/P50/P75 ของ peer แล้วได้ `#NAME?` ทุกช่อง
- **สาเหตุ:** openpyxl เขียนสูตรตามตัวอักษร ฟังก์ชันที่เพิ่มใน Excel 2010 อย่าง `PERCENTILE.INC` ต้องมี prefix `_xlfn.` ในไฟล์ xlsx
- **แก้อย่างไร:** เปลี่ยนเป็น `_xlfn.PERCENTILE.INC` แล้ว `verify` ได้ค่าตรงกับ Python ทั้งหมด

### 2026-10-31 · DCF ได้ ฿293 ต่อหุ้น จากราคา ฿43.75

- **เจออะไร:** ใช้ beta ของ Yahoo (0.44) ได้ cost of equity 4.9% WACC 3.8% และ DCF สูงเกินราคาเกือบ 7 เท่า
- **สาเหตุ:** regression beta ของหุ้นตัวเดียวมี standard error สูง (playbook §3) และ Rf ของไทยต่ำ ทำให้ WACC ใกล้ terminal growth
- **แก้อย่างไร:** ใช้ bottom-up beta จากตาราง unlevered beta ของ Damodaran (Retail Grocery ตลาดเกิดใหม่ 0.856) relever ด้วย D/E ของ CPALL ได้ 1.63 แล้วปรับ Rf, Kd, terminal value และ minority interest ตาม playbook ได้ WACC 6.49%

### 2026-10-31 · ไฟล์ล็อกของ Excel โผล่ใน git status

- **เจออะไร:** `output/CPALL.BK/~$CPALL.BK_valuation.xlsx` ขึ้นเป็นไฟล์ใหม่ตอน `/save`
- **สาเหตุ:** เปิดไฟล์ Excel ค้างไว้ Excel จึงสร้างไฟล์ล็อกที่มีชื่อผู้ใช้ในเครื่อง
- **แก้อย่างไร:** เพิ่ม `~$*` ใน `.gitignore`

### 2026-10-31 · EV/EBITDA ของ Yahoo ใช้นิยามไม่ตรงกัน

- **เจออะไร:** `enterpriseToEbitda` ของ CPALL คือ 12.98 แต่หน้าเว็บ Yahoo แสดง 10.67 ส่วน 2912.TW ได้ 13.65 เท่า แต่คิดเองจากงบได้ 7.37 เท่า
- **สาเหตุ:** Yahoo ใช้ EV ที่รวมหนี้สัญญาเช่าและ minority interest แต่หารด้วย `ebitda` ย้อนหลัง 12 เดือนที่ยังหักค่าเช่า (CPALL ฿76 พันล้าน เทียบงบรายปีหลัง IFRS 16 ฿91.6 พันล้าน)
- **แก้อย่างไร:** คิด EV/EBITDA เองจากงบรายปี: (มูลค่าตลาด + Total Debt + Minority Interest − Cash) ÷ EBITDA ได้ CPALL 10.62 เท่า ใกล้กับหน้าเว็บ และใช้นิยามเดียวกันกับ peer ทุกตัว

### 2026-10-31 · pipeline ล้มเมื่อลอง ticker อื่น (AAPL)

- **เจออะไร:** `run AAPL` ขึ้น `KeyError: 'rating_table'` แล้วต่อด้วย `TypeError` ตอนคูณ minority interest
- **สาเหตุ:** ไฟล์ดิบของ AAPL ดึงไว้ก่อนเพิ่มตาราง rating และ pipeline ไม่ได้ดึงใหม่ · AAPL ไม่มีรายการ Minority Interest ในงบ ค่าจึงเป็น None
- **แก้อย่างไร:** เพิ่ม `SCHEMA_VERSION` ให้ดึงใหม่เองเมื่อไฟล์เก่ากว่า · ร่างสมมติฐานนับ minority และ lease ที่ไม่มีในงบเป็น 0 · `load()` แจ้งชื่อ input ที่ยังไม่มีค่าแทนการ error กลางการคำนวณ

### 2026-10-31 · ใช้ pipeline กับ BDMS.BK (โรงพยาบาล)

- **เจออะไร:**
  - ticker `IHH.KL` และ `KPJ.KL` ไม่ error แต่ได้ info ว่างทุกช่อง
  - Yahoo industry ของ BDMS (`Medical Care Facilities`) ยังไม่มีใน `industry_map` ถ้า fetch เลย unlevered beta จะเป็น null
  - WACC ของ BDMS ได้ 4.89% และ terminal value เป็น 85% ของ EV DCF จึงสูงกว่า P/E และ EV/EBITDA
- **สาเหตุ:** Yahoo ใช้รหัสตัวเลขกับหุ้นมาเลเซีย (IHH = 5225.KL, KPJ = 5878.KL) · beta อุตสาหกรรมโรงพยาบาลตลาดเกิดใหม่ต่ำ (0.646) และ BDMS หนี้น้อย ประกอบกับ Rf ไทยหลังหัก default spread เหลือ 0.80%
- **แก้อย่างไร:** ค้นรหัสที่ถูกแล้วตรวจจาก `longName` · เพิ่ม mapping ใน `config.yaml` ก่อน fetch · WACC ต่ำไม่ได้แก้ แต่ทดลองเปลี่ยนสมมติฐานทีละข้อ พบว่าถ้าใช้ beta ≈ 1 ตามที่ playbook §4 บอกสำหรับช่วง terminal DCF เหลือ ฿16.88–20.18 บันทึกเป็นข้อจำกัดใน `research/BDMS.BK_method_choice.md`

### 2026-10-31 · STPI.BK: DCF ติดลบและห่างจากราคามาก

- **เจออะไร:** DCF ร่างแรกของ STPI ไม่บวกเงินลงทุนได้ −฿0.46 ต่อหุ้น · ΔNWC ÷ Δรายได้ในร่างได้ −83% · CAGR รายได้ −3.18%
- **สาเหตุ:** โมเดลไม่มีช่องบวก cross holdings ตาม playbook §2 ขณะที่ STPI ถือสินทรัพย์ที่ไม่ใช่การดำเนินงาน ฿5,170 ล้าน (51% ของมูลค่าตลาด) · รายได้แบบโครงการขึ้นลง ทำให้สูตรเฉลี่ยในร่างใช้ไม่ได้
- **แก้อย่างไร:** เพิ่ม input `non_operating_assets` (ค่าเริ่มต้น 0) · ใช้ Operating Income แทน EBIT · normalize margin 4 ปี, รายได้โตเท่า g, NWC จากสัดส่วนในงบดุล · ผลยังต่ำกว่าราคาเพราะ ROC ในอดีต 1.99% ต่ำกว่า WACC ไม่ใช่ความผิดของสูตร

### 2026-10-31 · CCET.BK: beta และ peer เปลี่ยนผลมาก

- **เจออะไร:** Yahoo industry `Computer Hardware` ยังไม่มี mapping ทำให้ unlevered beta เป็น null · DCF ร่าง ฿1.02 ต่ำกว่าราคา ฿7.95 มาก · fetch และ LibreOffice verify รอบแรกถูก sandbox บล็อก และคำสั่งวิเคราะห์ scenario แบบ one-liner ผิด shell quoting สองครั้ง
- **สาเหตุ:** ต้องจับคู่ชื่ออุตสาหกรรมของ Yahoo กับ Damodaran เอง · bottom-up beta ของ `Computers/Peripherals` ตลาดเกิดใหม่สูงถึง 1.618 (relever เป็น 1.946) เทียบ Yahoo regression beta 0.657 · CCET ซื้อขายที่ P/E และ EV/EBITDA ประมาณสองเท่าของมัธยฐาน peer · sandbox ไม่มี DNS/สิทธิ์ให้ LibreOffice ทำงานครบ · one-liner ใช้ single quote ซ้อนกัน
- **แก้อย่างไร:** ตรวจ `betaemerg.xls` แล้วเพิ่ม mapping ที่ตรงชื่อ · ทดสอบ beta, ERP, growth และ margin ทีละตัวก่อนเชื่อผล · ใช้ peer ฮาร์ดแวร์/EMS ไต้หวัน 5 ตัวแทนหุ้นชิ้นส่วนไทย · ขอสิทธิ์เครือข่ายและ LibreOffice ตามปกติ · แก้คำสั่งวิเคราะห์ให้เก็บค่าจาก dict ในตัวแปรแทนการซ้อน quote

### 2026-11-04 · ตรวจ mermaid ใน browser pane ไม่ได้เมื่อเปิดไฟล์ local

- **เจออะไร:** เปิดหน้า HTML ทดสอบ mermaid จาก `file://` ใน browser pane แล้วรัน JavaScript ไม่ได้ (pane แสดงไฟล์ local เป็น static snapshot)
- **สาเหตุ:** pane ไม่ให้ใช้ page tools กับไฟล์ local
- **แก้อย่างไร:** เปิดผ่าน `python3 -m http.server` ชั่วคราวด้วย `.claude/launch.json` ตรวจเสร็จแล้วหยุด server และลบ `launch.json` ทิ้ง

### 2026-11-04 · GitHub Pages ขึ้น 404 หลังกด Save

- **เจออะไร:** หลังผู้เรียนกด Save ใน Settings → Pages แล้ว `gh api .../pages` ยังตอบ 404 และ `has_pages: false` ไปอีกพักหนึ่ง จากนั้นงาน `pages-build-deployment` อยู่ในคิว GitHub Actions ราว 10 นาที เว็บจึงขึ้น 404
- **สาเหตุ:** GitHub บันทึกการตั้งค่าและเริ่ม deploy ไม่ทันที
- **แก้อย่างไร:** ไม่ต้องแก้อะไร รอจน `gh run view <id>` เป็น `completed success` แล้วตรวจลิงก์ด้วย `curl` แบบไม่ล็อกอิน
- **ลองวิธีไหนแล้วไม่เวิร์ก:** สั่งเปิด Pages ซ้ำผ่าน `gh api -X POST .../pages` ได้ 409 "already enabled" · browser pane ไม่ได้ล็อกอิน GitHub จึงเปิดหน้า Settings ไม่ได้

