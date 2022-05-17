import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
@dataclass
class LogMsg:
    delay_ms: int
    msg: str
    level: str = "DEBUG"

    def __str__(self):
        return f'[{self.level:<6}]  {self.msg}'

msgs = [
    LogMsg(100, 'starting caspal.ch header generation...', 'INFO'),
    LogMsg(129, f'Version: deadbeef-{datetime.now()}, on x86_64'),
    LogMsg(1200, 'preparing context for info on site header...', 'INFO'),
    LogMsg(672, 'scanning for updated hooks and plugins...'),
    LogMsg(992, '    nothing in: ./funcs'),
    LogMsg(992, '    nothing in: ./plugins'),
    LogMsg(532, '    nothing in: ./hooks'),
    LogMsg(411, '    nothing in: /etc/defaults/caspal-ch-banner-gibberish/hooks'),

]
took_ms = sum(m.delay_ms for m in msgs)
msgs += [
    LogMsg(123, f'building context finished sucessfully in {took_ms} ms', 'INFO'),
    LogMsg(54, 'building header for site....', 'INFO'),
    LogMsg(345, 'Successfully generated gibberish logs! Enjoy the rest of the page'),
    LogMsg(200, 'Context:'),
    LogMsg(500, '    - User: Pascal Bättig'),
    LogMsg(1549,'    - Roles: Cloud, DevOps, SRE'),
    LogMsg(172, '    - Site: caspal.ch'),
]

now = datetime.now()
for msg in msgs:
    print(f'{now.isoformat()}  {msg}')
    now += timedelta(milliseconds=msg.delay_ms)
