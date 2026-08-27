---
title: 최적화 기초
week: 2
order: 0
---

## 경사하강법

파라미터 갱신 규칙:

$$\theta \leftarrow \theta - \eta \, \nabla_\theta \mathcal{L}(\theta)$$

- $\eta$: 학습률(learning rate)
- 미니배치 SGD, 모멘텀, Adam 으로 확장

![학습률에 따른 수렴/발산 개념도](./assets/diagram.png)

위 그림처럼 학습률이 크면 발산한다.

## 실습

간단한 2차 함수에서 학습률에 따른 수렴/발산을 관찰한다.
