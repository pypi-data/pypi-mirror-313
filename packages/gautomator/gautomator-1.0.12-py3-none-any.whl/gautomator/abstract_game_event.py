from gautomator.common.exceptions import NotImplementedException


class AbstractGameEvent:


    @property
    def event_type(self) -> str:
        raise NotImplementedException

    async def enable(self):
        raise NotImplementedException

    async def disable(self):
        raise NotImplementedException

    @property
    def event_class(self):
        raise NotImplementedException