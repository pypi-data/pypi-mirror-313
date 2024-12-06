
from gautomator.extensions.gamelogic.events.user_event import UserEvent
from gautomator.extensions.unrealengine.events.actor_realtime_trace_event import ActorRealtimeTraceEvent


class GameEventType:

    USER_EVENT = UserEvent()
    ACTOR_REALTIME_TRACE_EVENT = ActorRealtimeTraceEvent()

