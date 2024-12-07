from lisa.globalfit.framework.bus import MessageStream
from lisa.globalfit.framework.msg.subjects import Subject

STREAM_INFRA = MessageStream(name="infra", subjects=[Subject("infra.>")])
