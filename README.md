# iot-repo-3
IoT 프로젝트 3조 저장소. 팔팔이
---
> ### IoT 기술 기반 스마트 물류 시스템을 구현합니다. 물류 자동화 및 센서 기반 물류 상태 실시간 모니터링을 제공합니다.

<br />

## 🤖 프로젝트 소개
<details markdown="1">
  <summary><h3>Iot 기반 스마트 물류 시스템</h3></h3></summary>
  <li>물류 산업은 점차 대형화, 복잡화되고 있으며, 효율적인 운영 체계 구축이 필수적인 과제로 대두되고 있다.</li>
  <li>본 프로젝트는 IoT 센서, 실시간 데이터에 기반하여 물류 프로세스 자동화를 목표로 한다.</li>
  <li>제안된 시스템은 물류 관리의 최적화와 자원 활용 효율성을 향상시킬 수 있을 것으로 기대된다.</li>
</details>
<br />

## 🧠 구성원 및 역할
|이름|업무|
|:---|:---|
|임시온|- 데이터베이스 설계 및 구현<br> - PyQT UI 구현 <br> - git 관리|
|최희재|- 컨베이어 구동 기능 구현<br> - 택배 감지 및 분류 기능 구현<br> - 시스템 구성도 설계|
|조나온|- QR 코드 인식 기능 구현<br> - 시퀀스 다이어 그램 제작<br> - Confluence 문서 관리|
|김진재|- Serial 통신 구현<br> - UI base code 제작 <br> - 모니터링 기능 구현|
|문세희|- 프로젝트 운영 및 관리|
<br />

## 🖥️ 활용 기술
|구분|상세|
|:---|:---|
|개발환경|<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" /> |
|IDE| <img src="https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" /> <img src="https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white" /> |
|언어| <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c++&logoColor=white" /> |
|DB|<img src="https://img.shields.io/badge/Amazon_RDS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" /> <img src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" />|
|협업| <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" /> <img src="https://img.shields.io/badge/confluence-172B4D?style=for-the-badge&logo=confluence&logoColor=white" /> <img src="https://img.shields.io/badge/jira-0052CC?style=for-the-badge&logo=jira&logoColor=white" /> <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white" />||
<br />

#### Hardware
    제어 보드 : arduino uno
    사용 언어 : cpp
    
    (사용 센서)
    - CMOS QR 코드 스캐너 모듈 2D Barcode Scanner USB
    - 2A L298 모터드라이버 모듈
    - 28BYJ-48 ULN2003 Step Moter
    - ULN2003 Step Moter Driver
    - 기어박스장착모터 (NP01D-288)
    - TCRT5000 적외선 IR 센서
    
    (통신 방식)
    - Serial 통신

#### PC
    사용 언어 : Python

    사용 모듈 : Serial, Pyqt5,, requests, threading



## System Requirements
| **주 기능**            | **상세 기능**                     | **설명**                                                                 | **개발 우선 순위** |
|-------------------------|-----------------------------------|--------------------------------------------------------------------------|--------------------|
| 구동 기능              | 컨베이어 벨트 단방향 구동 기능    | 컨베이어 벨트 동작                                                      | 1                  |
|                       | 구동 속도 조절 기능              | 컨베이어 벨트 구동 속도를 사용자 입력으로 제어                          | 3                  |
| 택배 구분 기능        | 택배 주소지 기준에 따라 분류함    | 택배 주소지 기준에 따라 분류                                             | 1                  |
| 택배 분류 기능        | 물리적으로 다른 분류함으로 구분함 | 물리적으로 다른 분류함으로 구분                                          | 1                  |
| 정지 기능              | 컨베이어 벨트 정지               | 컨베이어 벨트 동작 정지                                                 | 1                  |
| 모니터링 기능          | 컨베이어 시스템 모니터링 기능     | 컨베이어 동작 횟수, 시간, 시작/종료 시각, 처리 갯수 등의 통계 시각화 및 실시간 화면 표시 | 1                  |
| 원격 제어 기능         | 컨베이어 벨트 원격 제어 기능      | 원격으로 동작/정지 및 속도 제어                                          | 1                  |
| 자동녹화기능           | 컨베이어 벨트 정지/동작 시 녹화   | 컨베이어 벨트 정지/동작 시 자동 녹화                                    | 2                  |
| 상태 표시 기능         | 시스템 상태 표시 기능            | 시스템의 정지/동작/부팅 상태를 표시                                      | 2                  |
| 위험요소 감지 기능     | 위험 요소 감지 기능              | 컨베이어 근처 위험 요소(사람 등)를 감지                                  | 2                  |
| 택배 경로 추적        | 택배 경로 추적 기능              | 택배의 이동 경로 추적 및 확인                                           | 4                  |


## System Scenario
![Screenshot from 2024-11-22 17-07-20](https://github.com/user-attachments/assets/a8b33987-5d5c-4605-a793-2a25f352bec3)


## Design
[UI 설계](https://www.figma.com/design/2HPsWyqSAlxDfTQgQZTUDu/Team3?node-id=0-1&t=DpAPZBAEqeQ5pgbb-1)

## 결과

#### 바코드 기능 시연

[![YouTube Video](https://img.youtube.com/vi/reqIpaoSUK0/0.jpg)](https://www.youtube.com/watch?v=reqIpaoSUK0)


#### 분류기 기능 시연
[![YouTube Video](https://img.youtube.com/vi/Vg6thNHTn-g/0.jpg)](https://youtu.be/Vg6thNHTn-g)


#### 전체 기능 시연
[![YouTube Video](https://img.youtube.com/vi/iGdT6jQyY-w/0.jpg)](https://youtu.be/iGdT6jQyY-w)



