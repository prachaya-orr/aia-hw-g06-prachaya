# Workflow ของโปรแกรม (ภาพรวม)

> ลำดับการทำงานตั้งแต่ค้นวิธี valuation จนได้ Excel และ HTML ของหุ้น 1 ตัว อัปเดต 2026-11-03 (หลังทำ CPALL, BDMS, STPI และร่าง CCET)
> มี 2 แผนภาพ: **workflow** บอกว่าต้องตัดสินใจอะไรตรงไหน ส่วน **sequence diagram** บอกว่าใครส่งอะไรให้ใคร
> GitHub แสดงแผนภาพ mermaid ในไฟล์นี้ให้เอง

## 1. Workflow: จุดตัดสินใจของหุ้น 1 ตัว

```mermaid
flowchart TD
    START(["ผู้เรียนสั่ง valuation TICKER"]) --> MAP{"Yahoo industry มีใน<br/>industry_map ของ config.yaml?"}
    MAP -- ไม่มี --> ADDMAP["เปิดไฟล์ beta ของ Damodaran<br/>เพิ่ม mapping ที่ตรงธุรกิจ"] --> PEERS
    MAP -- มี --> PEERS["หา candidate peer จาก Yahoo<br/>คัดตามเกณฑ์ playbook §9<br/>ตัดตัวผิดปกติ / ขาดทุน / ส่วนทุนติดลบ"]
    PEERS --> FETCH["fetch TICKER --peers ...<br/>→ data/raw/TICKER.json"]
    FETCH --> DRAFT["draft TICKER<br/>→ assumptions/TICKER.yaml (status: draft)"]
    DRAFT --> TYPE{"ธุรกิจแบบไหน<br/>playbook §1"}

    TYPE -- "ธนาคาร / การเงิน" --> BANK["DDM, FCFE, excess return, P/BV<br/>ห้าม FCFF และ EV/EBITDA"]
    TYPE -- "ค้าปลีก สัญญาเช่ามาก<br/>(CPALL)" --> LEASE["DCF FCFF นับ lease เป็นหนี้<br/>+ EV/EBITDA, P/E"]
    TYPE -- "โตเต็มที่ กำไรนิ่ง<br/>(BDMS)" --> MATURE["DCF 2-stage<br/>+ P/E, EV/EBITDA"]
    TYPE -- "cyclical กำไรขึ้นลง<br/>(STPI, CCET)" --> CYC["normalize margin เฉลี่ยตลอดรอบ<br/>รายได้โตเท่า g · EV/EBITDA บนตัวเลข normalize"]

    BANK --> RULES
    LEASE --> RULES
    MATURE --> RULES
    CYC --> RULES

    RULES["ตรวจกฎความสอดคล้อง<br/>• beta แบบ bottom-up ไม่ใช้ regression beta<br/>• g ≤ Rf หลังหัก default spread<br/>• ROC ช่วง terminal = WACC<br/>• capex < D&A → ตั้ง capex = D&A<br/>• EPS ≤ 0 → ตัด P/E<br/>• ปันผล ÷ FCFE นอก 80–110% → ตัด DDM"]
    RULES --> XH{"มีเงินลงทุนในบริษัทร่วม/JV<br/>หรืออสังหาฯ เพื่อการลงทุนมาก?"}
    XH -- มี --> NOA["ใช้ Operating Income แทน EBIT ของ Yahoo<br/>ใส่ non_operating_assets ใน bridge (§2)"] --> MC
    XH -- ไม่มี --> MC["เขียน research/TICKER_method_choice.md<br/>วิธีที่เลือก + เหตุผล + ข้อเสนอให้ยืนยัน"]

    MC --> RUN1["run TICKER (ร่าง)"]
    RUN1 --> FAR{"ผลห่างจากราคาตลาด<br/>หลายเท่า?"}
    FAR -- ใช่ --> HUNT["ไล่หาสมมติฐานที่ผิดก่อนเชื่อผล<br/>ทดลองเปลี่ยนทีละข้อ แล้วบันทึกสาเหตุ"] --> ASK
    FAR -- ไม่ --> ASK{"ผู้เรียนยืนยันข้อเสนอ?"}
    ASK -- แก้ --> EDIT["แก้ YAML ตามที่ผู้เรียนเลือก"] --> RUN1
    ASK -- ยืนยัน --> REV["status: reviewed<br/>run TICKER อีกครั้ง"]
    REV --> VER{"verify TICKER<br/>Excel ต่างจาก Python ≤ 0.5%?"}
    VER -- ไม่ผ่าน --> FIX["แก้สูตร Excel<br/>(เช่น _xlfn. ของฟังก์ชันรุ่นใหม่)"] --> REV
    VER -- ผ่าน --> HTML["เปิด HTML ตรวจ football field<br/>และหน้าจอมือถือ"]
    HTML --> SAVE["/save: ตรวจ key → prompts.md<br/>→ PROJECT_MEMORY.md → commit → push"]
    SAVE --> END(["จบรอบ"])

    classDef decide fill:#fff4d6,stroke:#c99a2e,color:#3d2c00
    classDef rule fill:#e8eefc,stroke:#5b7bd5,color:#14234f
    classDef warn fill:#fde8e8,stroke:#c95454,color:#4a1010
    class MAP,TYPE,XH,FAR,ASK,VER decide
    class RULES,NOA rule
    class HUNT,FIX warn
```

## 2. Sequence diagram: ใครส่งอะไรให้ใคร

```mermaid
sequenceDiagram
    autonumber
    actor U as ผู้เรียน
    participant C as AI (Claude / Codex)
    participant R as valuation-researcher<br/>(subagent)
    participant N as NotebookLM<br/>"Valuation Methods"
    participant CLI as python -m valuation
    participant F as fetch.py
    participant SRC as Yahoo / ThaiBMA /<br/>Damodaran
    participant A as assumptions.py
    participant M as methods.py
    participant O as excel.py / html.py
    participant V as verify.py<br/>(LibreOffice)
    participant G as git / GitHub

    rect rgba(120, 160, 220, 0.15)
    Note over U,N: 1. ค้นวิธี valuation (ทำครั้งเดียว ใช้ร่วมทุกหุ้น)
    U->>C: ขอวิธี valuation ที่อ้างอิงได้
    C->>R: ส่งคำถาม (DCF, WACC, multiples, cyclical, IFRS 16 ...)
    R->>N: nlm notebook query valuation-methods --json --new-conversation
    N-->>R: คำตอบ + citation (cited_text)
    R->>R: ตัดประโยคที่ไม่มีหลักฐาน → "ไม่พบใน notebook"
    R-->>C: research/nlm_log/*.md
    C->>C: รวมเป็น research/playbook.md (§1–§14)
    end

    rect rgba(120, 200, 150, 0.15)
    Note over U,SRC: 2. เตรียมและดึงข้อมูลดิบ
    U->>C: valuation TICKER
    C->>SRC: ดู industry และ candidate peer จาก Yahoo
    opt industry ยังไม่มีใน config.yaml
        C->>C: เพิ่ม industry_map ให้ตรงชื่อในไฟล์ beta ของ Damodaran
    end
    C->>CLI: fetch TICKER --peers ... [--minority-proxy ...]
    CLI->>F: fetch.main()
    F->>SRC: Yahoo: info, งบรายปี 3 งบ, ปันผล
    alt ticker ลงท้าย .BK
        F->>SRC: ThaiBMA พันธบัตร 10 ปี
    else หุ้นอื่น
        F->>SRC: Yahoo ^TNX
    end
    F->>SRC: Damodaran: ERP/CRP, unlevered beta อุตสาหกรรม, ตาราง rating
    F->>SRC: peer: P/E, P/BV + งบรายปี (คิด EV/EBITDA เอง)
    F-->>CLI: data/raw/TICKER.json (ทุกค่ามี source, url, asof)
    end

    rect rgba(230, 180, 90, 0.18)
    Note over U,A: 3. ร่างสมมติฐานและเลือกวิธี
    C->>CLI: draft TICKER
    CLI->>A: write_draft(raw)
    A-->>C: assumptions/TICKER.yaml (status: draft)
    C->>C: จัดประเภทธุรกิจตาม playbook §1 · normalize ถ้า cyclical (§8)
    C->>A: แก้ YAML: methods, peers, เหตุผล, non_operating_assets ...
    C->>CLI: run TICKER (ผลร่าง)
    opt ผลห่างจากราคาหลายเท่า
        C->>M: ทดลองเปลี่ยนสมมติฐานทีละข้อ หาสาเหตุ
    end
    C-->>U: research/TICKER_method_choice.md + ข้อเสนอให้ยืนยัน
    U->>C: ยืนยันตามร่าง / ขอแก้
    C->>A: status: reviewed
    end

    rect rgba(200, 130, 200, 0.15)
    Note over U,O: 4. คำนวณและสร้างผลงาน
    C->>CLI: run TICKER
    CLI->>F: ensure_raw() ดึงใหม่ถ้า schema / peer / proxy เปลี่ยน
    CLI->>A: load() แปลง from: เป็นค่าพร้อมที่มา (input ใหม่ที่ไม่มีในไฟล์ใช้ค่าเริ่มต้น)
    A-->>CLI: Assumptions (ขาดค่า = แจ้งชื่อ input)
    CLI->>M: run(a, peers)
    M->>M: WACC (Rf − default spread, bottom-up beta, synthetic rating)
    M->>M: DCF FCFF + sensitivity · comps P/E, EV/EBITDA, P/BV · DDM · 52 สัปดาห์
    M-->>CLI: ช่วง low/base/high + steps + คำเตือน
    CLI->>O: excel.build() / html.build()
    O-->>U: output/TICKER/ .xlsx (สูตรจริง) · .html · results.json
    end

    rect rgba(220, 120, 120, 0.15)
    Note over U,V: 5. ตรวจ Excel เทียบ Python
    C->>CLI: verify TICKER
    CLI->>V: soffice --convert-to xlsx (คำนวณสูตรใหม่)
    V-->>CLI: ค่าจาก named cells (x_wacc, x_dcf_base ...)
    CLI-->>C: เทียบ results.json ต่างได้ไม่เกิน 0.5%
    end

    rect rgba(150, 150, 150, 0.15)
    Note over U,G: 6. บันทึกงาน
    U->>C: /save
    C->>C: ตรวจ key / ข้อมูลส่วนตัว / ไฟล์ที่ไม่ได้สร้างเอง
    C->>C: เขียน prompts.md + PROJECT_MEMORY.md
    C->>G: commit "รอบ N: ..." แล้ว push
    end
```

## ไฟล์ที่เกี่ยวข้องในแต่ละขั้น

| ขั้น | โค้ด / คำสั่ง | ไฟล์ที่ได้ |
|---|---|---|
| 1. ค้นวิธี | `.claude/agents/valuation-researcher.md` (Codex ใช้ `.codex/agents/valuation-researcher.toml`) · `nlm` CLI | `research/nlm_log/*.md` · `research/playbook.md` · `research/sources.md` |
| 2. ดึงข้อมูล | `valuation/fetch.py` · `config.yaml` (industry_map) | `data/raw/<TICKER>.json` (ไม่ commit) |
| 3. สมมติฐาน | `valuation/assumptions.py` | `assumptions/<TICKER>.yaml` · `research/<TICKER>_method_choice.md` |
| 4. คำนวณ | `valuation/pipeline.py` · `methods.py` · `excel.py` · `html.py` · `templates/report.html` | `output/<TICKER>/<TICKER>_valuation.xlsx` · `.html` · `_results.json` |
| 5. ตรวจ | `valuation/verify.py` (ต้องมี LibreOffice) | ผลเทียบในเทอร์มินัล |
| 6. บันทึก | `.claude/commands/save.md` | `prompts.md` · `PROJECT_MEMORY.md` · commit บน GitHub |

## หุ้นที่ผ่าน workflow นี้แล้ว

| หุ้น | ประเภทธุรกิจ (§1) | วิธีที่ใช้ | สถานะ |
|---|---|---|---|
| CPALL.BK | ค้าปลีก สัญญาเช่ามาก | DCF FCFF, P/E, EV/EBITDA, 52 สัปดาห์ | reviewed |
| BDMS.BK | โตเต็มที่ (โรงพยาบาล) | DCF FCFF, P/E, EV/EBITDA, 52 สัปดาห์ | reviewed |
| STPI.BK | cyclical + เงินลงทุนมาก | DCF normalize + non_operating_assets, EV/EBITDA normalize, P/BV, 52 สัปดาห์ | reviewed |
| CCET.BK | cyclical (ฮาร์ดแวร์/EMS) | DCF normalize, P/E, EV/EBITDA, 52 สัปดาห์ | draft |

## คำสั่งที่ใช้บ่อย

```bash
.venv/bin/python -m valuation run CPALL.BK
```

```bash
.venv/bin/python -m valuation verify CPALL.BK
```

หุ้นตัวใหม่: เพิ่ม industry_map ถ้ายังไม่มี → `fetch <TICKER> --peers ...` → `draft <TICKER>` → แก้ `assumptions/<TICKER>.yaml` และเขียน `research/<TICKER>_method_choice.md` → `run <TICKER>` → ผู้เรียนยืนยัน → `status: reviewed` → `run` → `verify`
