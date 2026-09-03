# 1주차 노트 검수 진행 (loop 작업용, 사이트 빌드 제외 파일)

작성/검수 가이드 요약:
- 톤: 학부/대학원생 대상, 억지 비유·유아 말투 배제. 소리 내 읽어 술술.
- 흐름: 문단·절 사이 인과·징검다리. Problem → 이 개념이 등장할 수밖에 없던 이유.
- 전방 참조("이번 주 N번째 노트에서 다룬다") 과다 → 제거·축약. 각 노트 "정리" 절은 유지.
- 시각화: 자작 SVG 남발 금지. 병목 지점에 공식/논문/검증된 블로그의 좋은 레퍼런스 시각자료를 찾아 출처 밝혀 인용. 없을 때만 자작.

## 체크리스트

- [x] 01-introduction.mdx — 수업 소개
- [x] 01a-transformer.mdx — Transformer 구조
- [x] 01b-bert-vs-gpt.mdx — BERT vs GPT, decoder-only 수렴
- [x] 01c-decoder-only-llm.mdx — decoder-only LLM 한 바퀴 (Llama 3 8B)
- [x] 01d-llm-inference.mdx — prefill/decode, memory wall, KV cache

전 항목 완료 → loop 종료.

## 검수 메모

- **01-introduction**: 여러 차례 사용자 트림을 거쳐 흐름·분량 모두 정제됨. 수정 없이 통과.
- **01a**: "이번 주 N번째 노트에서 …" 식 전방 참조 5곳 제거/축약. LLM full form 을 §2 Sidenote
  첫 등장으로 이동. §10 말미 KV-cache 예고를 일반 서술로 완화. Wikimedia 아키텍처 그림
  라이선스(CC BY-SA 3.0, Yuening Jia) 재확인 — 표기 정확. 파라미터 비중 표현을 01c(70%)와 통일.
- **01b**: §5 리스트의 "(네 번째 노트)" 제거. 나머지는 흐름·톤 양호, 표·수식 검증 통과.
- **01c**: §3 GQA·§6 KV cache 전방 참조를 "다음 노트"로 축약. Byte-level BPE 설명에서
  "UTF-8 = 8비트 인코딩"이라는 부정확한 표현을 "1–4바이트로 표현"으로 교정. Llama 3 8B
  파라미터 분해 표(41.9M/176M/6.98B/0.53B → 8.03B, FFN 70%·attn 17%·emb 13%) 재계산 일치.
  블록 SVG 는 노트 수식과 정확히 대응하고 CC 라이선스 대체 그림이 없어 유지.
- **01d**: MHA/GQA/MQA 자작 SVG → **GQA 원논문(Ainslie et al. 2023, EMNLP) Figure 2** 로 교체
  (ACL Anthology CC BY 4.0, arXiv HTML v3 이미지 직접 참조). 캐시·roofline 수치(128 KiB/token,
  1/16/32 GiB, intensity≈1, ridge≈300, MLA 576원소≈57배) 전부 재검증 일치. roofline SVG 는
  decode/prefill 지점을 직접 표시한 맞춤 도식이라 유지. 미래 주차(2·3·6·7주차) 참조는
  범위 경계로서 유지.
- 로컬 빌드 검증 불가(milab-pnu/lectures 쓰기 차단) → 각주 정의 매칭, 단독 줄 Sidenote,
  한 줄 $$, heading 수식, MDX 중괄호를 수동 점검. push 후 CI(check-lecture-notes.mjs)가 최종 확인.
