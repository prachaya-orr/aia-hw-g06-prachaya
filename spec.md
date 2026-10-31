---
title: Valuation Deep Research · football field ต่อหุ้น
owner: prachaya
status: draft
updated: 2026-10-31
---

# Spec

## 1. Goal · อยากตัดสินใจเรื่องอะไร

ตัดสินว่าราคาหุ้นรายตัว (ใส่ ticker อะไรก็ได้ เริ่มที่ CPALL.BK) ถูกหรือแพงกว่ามูลค่ายุติธรรม โดยใช้วิธี valuation ที่ค้นคว้ามาจาก NotebookLM ว่าเหมาะกับธุรกิจนั้น แล้วเทียบหลายวิธีใน football field เดียว

## 2. Material questions · 3–5 คำถามที่เปลี่ยนการตัดสินใจ

1. วิธี valuation ไหนเหมาะกับธุรกิจนี้ และวิธีไหนไม่ควรใช้ (เช่น ธนาคารไม่ใช้ DCF FCFF)
2. ราคาตลาดปัจจุบันอยู่ต่ำกว่า ในช่วง หรือสูงกว่าช่วงมูลค่าที่หลายวิธีซ้อนทับกัน
3. สมมติฐานไหนทำให้มูลค่าเปลี่ยนมากที่สุด (WACC, terminal growth, margin) และช่วงที่สมเหตุสมผลคือเท่าไร
4. peer ที่ใช้เทียบ multiple เป็นธุรกิจเดียวกันจริงหรือไม่

## 3. Trust sources · แหล่งข้อมูลที่อนุญาต

| แหล่ง | ใช้ตอบคำถามข้อ |
|---|---|
| NotebookLM notebook "Valuation Methods" (รายชื่อ source อยู่ใน `research/sources.md`) | 1, 3 |
| Yahoo Finance ผ่าน yfinance · ราคา, จำนวนหุ้น, งบการเงินรายปี, beta, 52w range, multiple ของ peer | 2, 3, 4 |
| ThaiBMA · อัตราผลตอบแทนพันธบัตรรัฐบาล 10 ปี (risk-free rate หุ้นไทย) | 3 |
| Yahoo Finance `^TNX` · US Treasury 10 ปี (risk-free rate หุ้นสหรัฐ) | 3 |
| Damodaran Online · equity risk premium และ country risk premium | 3 |

กติกา: ทุกตัวเลขต้องมี source และวันที่ หาไม่ได้ให้เว้นว่างและบอก ห้ามเดา

## 4. Output · หน้าตาผลงานที่ต้องการ

ต่อหุ้น 1 ตัว ได้ 2 ไฟล์:
- **Excel** ชีต Inputs (ทุกค่ามี source + วันที่), Historical, WACC, DCF, Sensitivity, Comps, Football field และ Sources โดยใช้สูตรจริงให้แก้สมมติฐานแล้วเห็นผลทันที
- **HTML** อธิบาย valuation ทีละขั้น: วิธีที่เลือกและเหตุผล (อ้าง NotebookLM), สูตร → ตัวเลขที่ใส่ → ผล, ตารางสมมติฐานทั้งหมด, sensitivity และ football field chart

ไฟล์ที่ต้องได้: `output/<TICKER>/<TICKER>_valuation.xlsx` · `output/<TICKER>/<TICKER>_valuation.html` · `research/playbook.md`

## 5. Success criteria · รู้ได้อย่างไรว่างานผ่าน

- [ ] รัน `python -m valuation run <TICKER>` คำสั่งเดียวได้ทั้ง Excel และ HTML
- [ ] ทุกตัวเลขใน Inputs และตารางสมมติฐานมี source และวันที่
- [ ] วิธีที่เลือกต่อหุ้นมีเหตุผลอ้างอิงจาก NotebookLM พร้อม citation
- [ ] Excel คำนวณใหม่แล้วได้มูลค่าต่อหุ้นตรงกับ HTML (ต่างกันไม่เกิน 0.5%)
- [ ] ดู football field แล้วตอบได้ใน 1 นาทีว่าราคาปัจจุบันถูกหรือแพงเมื่อเทียบกับแต่ละวิธี
