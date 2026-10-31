# Workflow ของโปรแกรม (ภาพรวม)

> ลำดับการทำงานตั้งแต่ค้นวิธี valuation จนได้ Excel และ HTML ของหุ้น 1 ตัว อัปเดต 2026-10-31
> GitHub แสดงแผนภาพ mermaid ในไฟล์นี้ให้เอง

## Sequence diagram

```mermaid
sequenceDiagram
    autonumber
    actor U as ผู้เรียน
    participant C as Claude (session หลัก)
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
    U->>C: ขอวิธี valuation ที่ถูกต้อง
    C->>R: ส่งคำถาม (DCF, WACC, multiples, IFRS 16 ...)
    R->>N: nlm notebook query valuation-methods --json --new-conversation
    N-->>R: คำตอบ + citation (cited_text)
    R->>R: ตัดประโยคที่ไม่มีหลักฐาน → "ไม่พบใน notebook"
    R-->>C: research/nlm_log/*.md
    C->>C: รวมเป็น research/playbook.md
    end

    rect rgba(120, 200, 150, 0.15)
    Note over U,SRC: 2. ดึงข้อมูลดิบ
    U->>CLI: fetch TICKER --peers ... --minority-proxy ...
    CLI->>F: fetch.main()
    F->>SRC: Yahoo: info, งบรายปี 3 งบ, ปันผล
    alt ticker ลงท้าย .BK
        F->>SRC: ThaiBMA พันธบัตร 10 ปี
    else หุ้นอื่น
        F->>SRC: Yahoo ^TNX
    end
    F->>SRC: Damodaran: ERP/CRP, unlevered beta, ตาราง rating
    F->>SRC: peer: P/E + งบรายปี (คิด EV/EBITDA เอง)
    F->>SRC: minority proxy: P/BV ของบริษัทลูก
    F-->>CLI: data/raw/TICKER.json (ทุกค่ามี source, url, asof)
    end

    rect rgba(230, 180, 90, 0.18)
    Note over U,A: 3. ร่างและรีวิวสมมติฐาน
    U->>CLI: draft TICKER
    CLI->>A: write_draft(raw)
    A-->>U: assumptions/TICKER.yaml (status: draft)
    C->>C: อ่าน playbook + ข้อมูลดิบ
    C-->>U: research/TICKER_method_choice.md + ข้อเสนอ
    U->>C: ยืนยัน (peer, capex, ROC, g)
    C->>A: แก้ YAML → status: reviewed
    end

    rect rgba(200, 130, 200, 0.15)
    Note over U,O: 4. คำนวณและสร้างผลงาน
    U->>CLI: run TICKER
    CLI->>F: ensure_raw() ดึงใหม่ถ้า schema / peer / proxy เปลี่ยน
    CLI->>A: load() แปลง from: เป็นค่าพร้อมที่มา
    A-->>CLI: Assumptions (ขาดค่า = แจ้งชื่อ input)
    CLI->>M: run(a, peers)
    M->>M: WACC (Rf − default spread, bottom-up beta, synthetic rating)
    M->>M: DCF FCFF + sensitivity · comps P/E, EV/EBITDA · DDM · 52 สัปดาห์
    M-->>CLI: ช่วง low/base/high + steps + คำเตือน
    CLI->>O: excel.build() / html.build()
    O-->>U: output/TICKER/ .xlsx (สูตรจริง) · .html · results.json
    end

    rect rgba(220, 120, 120, 0.15)
    Note over U,V: 5. ตรวจ Excel เทียบ Python
    U->>CLI: verify TICKER
    CLI->>V: soffice --convert-to xlsx (คำนวณสูตรใหม่)
    V-->>CLI: ค่าจาก named cells (x_wacc, x_dcf_base ...)
    CLI-->>U: เทียบ results.json ต่างได้ไม่เกิน 0.5%
    end

    rect rgba(150, 150, 150, 0.15)
    Note over U,G: 6. บันทึกงาน
    U->>C: /save
    C->>C: ตรวจ key / ข้อมูลส่วนตัว
    C->>C: เขียน prompts.md + PROJECT_MEMORY.md
    C->>G: commit "รอบ N: ..." แล้ว push
    end
```

## ไฟล์ที่เกี่ยวข้องในแต่ละขั้น

| ขั้น | โค้ด / คำสั่ง | ไฟล์ที่ได้ |
|---|---|---|
| 1. ค้นวิธี | `.claude/agents/valuation-researcher.md` · `nlm` CLI | `research/nlm_log/*.md` · `research/playbook.md` · `research/sources.md` |
| 2. ดึงข้อมูล | `valuation/fetch.py` · `config.yaml` | `data/raw/<TICKER>.json` (ไม่ commit) |
| 3. สมมติฐาน | `valuation/assumptions.py` | `assumptions/<TICKER>.yaml` · `research/<TICKER>_method_choice.md` |
| 4. คำนวณ | `valuation/pipeline.py` · `methods.py` · `excel.py` · `html.py` · `templates/report.html` | `output/<TICKER>/<TICKER>_valuation.xlsx` · `.html` · `_results.json` |
| 5. ตรวจ | `valuation/verify.py` (ต้องมี LibreOffice) | ผลเทียบในเทอร์มินัล |
| 6. บันทึก | `.claude/commands/save.md` | `prompts.md` · `PROJECT_MEMORY.md` · commit บน GitHub |

## คำสั่งที่ใช้บ่อย

```bash
.venv/bin/python -m valuation run CPALL.BK
```

```bash
.venv/bin/python -m valuation verify CPALL.BK
```

หุ้นตัวใหม่: `draft <TICKER>` → รีวิว `assumptions/<TICKER>.yaml` (เพิ่ม peers, methods, method_reasons) → `run <TICKER>` → `verify <TICKER>`
