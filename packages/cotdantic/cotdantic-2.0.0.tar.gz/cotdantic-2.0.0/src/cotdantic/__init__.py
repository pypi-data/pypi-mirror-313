__version__ = '2.0.0'

from .models import (
	Point,
	Contact,
	Link,
	Status,
	Group,
	Takv,
	Track,
	PrecisionLocation,
	Alias,
	Image,
	Detail,
	EventBase,
	Event,
	CotBase,
)

from . import converters
from .cot_types import atom

LOCATION = (38.691420, -77.134600)


def __event_to_bytes(self: EventBase) -> bytes:
	return converters.model2proto(self)


@classmethod
def __event_from_bytes(cls: EventBase, proto: bytes) -> EventBase:
	return converters.proto2model(cls, proto)


EventBase.__bytes__ = __event_to_bytes
EventBase.to_bytes = __event_to_bytes
EventBase.from_bytes = __event_from_bytes
