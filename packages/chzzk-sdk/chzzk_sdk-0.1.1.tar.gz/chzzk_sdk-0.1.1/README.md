# chzzk-sdk

네이버 라이브 스트리밍 서비스 치치직(CHZZK)의 비공식 API 라이브러리.<br/>
공부 목적으로 만들었으며, 참조한 레포는 하단의 `References`에 명시했습니다.

- 로그인 (쿠키 사용)
- 검색 (채널, 영상, 생방송)
- 채널 정보 조회
- 방송 상태 및 상세 정보 조회
- 채팅 보내기
- 이벤트 구독
  - 연결 상태 (on_connect, on_disconnect)
  - 채팅 (on_chat)
  - 방송 상태 (on_broadcast_open, on_broadcast_close)
  - 후원 (on_donation)
  - 구독 (on_subscription)
  - 상단 고정 (on_pin, on_unpin)
  - 시스템 메시지 (on_system_message)
  - 메시지 관리
  - 그 외 (on_recent_chat, on_notice, on_blind, on_mission_pending, on_mission_approved, on_mission_rejected, on_mission_completed)
- 채팅 커맨드 생성 `@client.commands(name="커맨드이름")`
- 관리 (채팅 제한, 상단 고정 설정)

# Requirements

- Python 3.11+

# Installation

```commandline
pip install chzzk-sdk
```

# Example

```py
import asyncio

from chzzk import ChzzkChat, Chzzk
from chzzk.model import ChatMessage

from dotenv import dotenv_values


env = dotenv_values(".env")
chzzk = Chzzk().from_data(auth=env.get("AUTH"), session=env.get("SESSION"))
chat = ChzzkChat(chzzk=chzzk, prefix="!") # commands를 위한 prefix 지정


@chat.event
async def on_connect():
    print(f"on_connect")
    await chat.send_chat("on_connect test")


@chat.event
async def on_chat(message: ChatMessage):
    print(f"on_chat: {message.content}")

    
@chat.commands(name="공지")
async def notice(message: ChatMessage, *args):
    await chat.pin_message(message=message)


# name가 없으면, 함수이름이 커맨드 명령어 이름이 됨.
@chat.commands()
async def 공지해제(*args):
    await chat.unpin_message()


@chat.commands(name="덧셈")
async def plus(message: ChatMessage, *args):
    nums = list(map(lambda x: int(x), args))
    await chat.send_chat(f"덧셈 결과: {sum(nums)}")


async def main():
    channels = await chzzk.search.channels("갈대s")
    channel_id = channels[0].channel.channel_id
    await chat.run(channel_id=channel_id)

if __name__ == "__main__":
    asyncio.run(main())
```

# References

- [jonghwanhyeon/python-chzzk](https://github.com/jonghwanhyeon/python-chzzk?tab=readme-ov-file)
- [kimcore/chzzk](https://github.com/kimcore/chzzk)
- [gunyu1019/chzzkpy](https://github.com/gunyu1019/chzzkpy)