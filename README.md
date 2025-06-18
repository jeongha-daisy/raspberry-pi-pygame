# 🎮 라즈베리파이 2D 게임

센서와 조이스틱을 활용해 만든 **라즈베리파이 기반 실시간 인터랙티브 2D 게임**입니다.

버튼, 조도, 진동, 소리 센서를 활용하여 다양한 아이템을 발동하고, 조이스틱을 통해 캐릭터를 조작하며 장애물을 피합니다.

<br><br>

## 💭 시스템 개요

- **입력:** 조이스틱, 버튼, 조도 센서, 진동 센서, 소리 센서
- **처리**: 클라이언트 센서 처리는 Python, 게임 로직 처리 및 렌더링은 Python +  Pygame 라이브러리
- **통신:** 2채널(센서, 조이스틱) TCP소켓 통신
- **출력:** 센서 입력은 클라이언트(라즈베리파이)에서 서버(게임 PC)로 실시간 전송, 게임 화면은 서버에서 출력

<br><br>


## 💭 게임 설명

<img width="534" alt="image" src="https://github.com/user-attachments/assets/3ab8f4c2-60a3-4bb5-bebc-9e3adc436be7" />


장애물을 피하며 가능한 오랫동안 버텨서 높은 점수를 얻는 것이 게임의 목표입니다.

게임을 진행하며 아이템을 이용해 장애물을 회피할 수 있습니다. 각 아이템은 날아오는 장애물 사이에서 얻을 수 있으며 아이템의 능력은 센서를 통해 발동됩니다.

<img width="400" alt="image" src="https://github.com/user-attachments/assets/d22864ff-dc9a-49c1-b078-69c7ea75bca8" /> <img width="400" alt="image" src="https://github.com/user-attachments/assets/bf0e3ab7-3747-4e85-be4e-82d7b10215a7" />


조이스틱으로 캐릭터를 조작합니다. 아래는 각 센서에 해당하는 아이템의 능력입니다. 해당 아이템을 소유하고 센서를 인식할 경우 아이템의 효과가 발휘됩니다. 


<table>
  <tr>
    <td><img width="50" alt="image" src="https://github.com/user-attachments/assets/37374e63-2a51-419c-90c7-5c80296678e8" /></td>
    <td>
      입력: 버튼 누름 <br>
      효과: 장애물 정지 (Freeze)
    </td>
  </tr>
</table>

<table>
  <tr>
    <td><img width="50" alt="image" src="https://github.com/user-attachments/assets/1c651f4c-6884-49ec-aad4-9e8a02b5f831" /></td>
    <td>
      입력: 조도센서에서 그림자 감지<br>
      효과: 쉴드 생성 (Shield)
    </td>
  </tr>
</table>

<table>
  <tr>
    <td><img width="50" alt="image" src="https://github.com/user-attachments/assets/0d2d11fd-ea2e-4b28-a534-a8ad7af0d8a3" /></td>
    <td>
      입력: 충격 감지 센서에서 충격 감지<br>
      효과: 장애물 제거 (Clear All)
    </td>
  </tr>
</table>

<table>
  <tr>
    <td><img width="50" alt="image" src="https://github.com/user-attachments/assets/94a65b0e-7f17-49fd-82f7-fe00295c56f4" /></td>
    <td>
      입력: 사운드 감지 센서에서 사운드 감지<br>
      효과: 장애물 느리게 (Slow)
    </td>
  </tr>
</table>

<br><br>

## 💭 시스템 구조

센서 입력 → Raspberry Pi 처리 → TCP 전송 → 게임 서버 반영
<br>
<img width="534" alt="image" src="https://github.com/user-attachments/assets/dc02583e-cd69-4ad6-b496-98af5890f651" />

- 센서 이벤트 및 조이스틱 데이터는 각각 별도의 소켓으로 전송됩니다. (2채널)
- 서버는 자동 복구 구조로, 연결 끊겨도 다시 수신 가능합니다.
- 클라이언트는 라즈베리파이 전원 연결 시 자동 실행되도록 systemd에 등록하였습니다.

<br><br>

## 💭 부품 설명

센서와 조이스틱은 브레드보드 위에 직접 구성되어 있으며, 모든 부품은  Raspberry Pi와 연결되어 있습니다. 

- Raspberry Pi 4
- ADC 모듈 (**PCF8591)**
    - 아날로그 신호 기반의 조이스틱 값을 읽기 위함
- 조이스틱 모듈
- 버튼
- 충격 센서
- 사운드 감지 센서
- 조도 센서

<br><br>

## 💭 프로젝트 차별점

### 다양한 센서를 활용

- 일반적인 임베디드 게임 프로젝트:
    - 조이스틱 모듈 & 버튼 모듈을 활용하거나 특정 센서 한, 두개를 메인 입력으로 사용
- 본 프로젝트:
    - 네 가지 다양한 물리 센서를 활용하여 게임 내의 고유한 아이템 능력과 연동
    - 변화를 게임 플레이에 적극적으로 반영. 센서의 입력이 실시간으로 게임에 영향을 미치는 인터랙션 강조

### 멀티스레드 구조

- 본 프로젝트: 센서/조이스틱 입력을 TCP로 실시간 전송
    - 센서 포트 / 조이스틱 포트 분리
    - 센서는 이벤트가 발생할 때만 전송하지만, 조이스틱은 값을 계속 **읽어서 전송 하기 때문에**

### 실사용 고려

- systemd 통한 자동 실행
- 클라이언트/서버 끊김 복구 가능
- 추후 컨트롤러 케이스 제작으로 실환경에서의 작동을 기대

<br><br>

## 💭 실행 방법

### 클라이언트 (라즈베리파이)

타겟 서버(PC)의 IP 주소로 수정 후 실행합니다. 

```bash
python client.py
```

> ※ systemd 등록으로 자동 실행되도록 설정 가능합니다다.
> 
> 
> `/etc/systemd/system/client.service`에 등록
> 

### 서버 (PC)

본 PC의 IP 주소로 수정 후 실행합니다. (pygame 설치 필요)

```bash
python main_game.py
```

> pyinstaller를 이용하여 exe로 내보낸 후 실행 가능합니다.
> 

<br><br>

## 💭 시연 영상

(추가 예정)
