# 1주차 노트 검수 진행 (loop 작업용, 사이트 빌드 제외 파일)

작성/검수 가이드 요약:
- 톤: 학부/대학원생 대상, 억지 비유·유아 말투 배제. 소리 내 읽어 술술.
- 흐름: 문단·절 사이 인과·징검다리. Problem → 이 개념이 등장할 수밖에 없던 이유.
- 전방 참조("이번 주 N번째 노트에서 다룬다") 과다 → 노트 끝 hand-off 1개만 남기고 정리(cut). 각 노트의 "정리" 절은 유지.
- 시각화: 자작 SVG 남발 금지. 병목 지점에 공식/논문/검증된 블로그의 좋은 레퍼런스 시각자료를 찾아 출처 밝혀 인용. 없을 때만 자작.
- 완료: 파일 저장 후 아래 체크. 전부 [x] 면 loop 종료.

## 체크리스트

- [x] 01-introduction.mdx — 수업 소개
- [x] 01a-transformer.mdx — Transformer 구조
- [ ] 01b-bert-vs-gpt.mdx — BERT vs GPT, decoder-only 수렴
- [ ] 01c-decoder-only-llm.mdx — decoder-only LLM 한 바퀴 (Llama 3 8B)
- [ ] 01d-llm-inference.mdx — prefill/decode, memory wall, KV cache

## 메모

- 01-introduction: 여러 차례 사용자 트림을 거쳐 흐름·분량 모두 정제됨. 수정 없이 검수 통과.
- 01a: 전방 참조("이번 주 세 번째/네 번째 노트에서 …") 5곳 제거 또는 내부 절 참조로 축약.
  §10 말미 KV-cache 예고를 "긴 context 에서 이 항을 다루는 게 이후 inference 의 중심 문제"로
  일반화. LLM full form 을 §2 Sidenote 첫 등장으로 이동. Wikimedia 아키텍처 그림 라이선스
  (CC BY-SA 3.0, Yuening Jia) 재확인 — 표기 정확. SVG 없음, 외부 그림·영상 4개 모두 출처·라이선스 적정.
