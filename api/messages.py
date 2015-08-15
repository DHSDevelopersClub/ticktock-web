"""Endpoints messages."""
__author__ = "Alexander Otavka"
__copyright__ = "Copyright (C) 2015 DHS Developers Club"

from datetime import datetime

from protorpc import messages, message_types
import endpoints


class CalendarProperties(messages.Message):
    """
    Data for certain properties of a calendar.

    :type calendar_id: str
    :type name: str
    :type hidden: bool
    :type color: str
    :type link: str
    """
    calendar_id = messages.StringField(1, required=True)
    name = messages.StringField(2)
    hidden = messages.BooleanField(3)
    color = messages.StringField(4)
    link = messages.StringField(5)

CALENDAR_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    CalendarProperties,
    calendar_id=messages.StringField(1, required=True)
)


class CalendarCollection(messages.Message):
    """
    Pageable array of calendar messages.

    :type items: list[Calendar]
    :type next_page_token: str
    """
    items = messages.MessageField(CalendarProperties, 1, repeated=True)
    next_page_token = messages.StringField(2)


class EventSettings(messages.Message):
    """Settings for an event."""
    pass


class EventProperties(messages.Message):
    """
    Data for certain properties of events.

    :type event_id: str
    :type calendar_id: str
    :type name: str
    :type start_date: datetime
    :type end_date: datetime
    :type starred: bool
    :type hidden: bool
    :type link: str
    :type settings: EventSettings
    """
    event_id = messages.StringField(1, required=True)
    calendar_id = messages.StringField(2, required=True)
    name = messages.StringField(3)
    start_date = message_types.DateTimeField(4)
    end_date = message_types.DateTimeField(5)
    starred = messages.BooleanField(6)
    hidden = messages.BooleanField(7)
    link = messages.StringField(8)
    settings = messages.MessageField(EventSettings, 9)

EVENT_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    EventProperties,
    event_id=messages.StringField(1, required=True),
    calendar_id=messages.StringField(2, required=True)
)


class EventCollection(messages.Message):
    """
    Pageable array of event messages.

    :type items: list[Event]
    :type next_page_token: str
    """
    items = messages.MessageField(EventProperties, 1, repeated=True)
    next_page_token = messages.StringField(2)


class Settings(messages.Message):
    """Settings for a user."""
    pass


class SearchQuery(messages.Message):
    """
    Search query with various optional filters.

    :type search: str
    :type only_hidden: bool
    :type page_token: str
    :type timezone: str

    :cvar search: A generic search string.
    :cvar only_hidden: Either show only hidden, or show no hidden items.
    :cvar page_token: For queries to large data sets.
    :cvar timezone: For event searches, not yet implemented.
    """
    search = messages.StringField(1)
    only_hidden = messages.BooleanField(2)
    # TODO: implement paging (get all the data for forever, then memcache it)
    page_token = messages.StringField(3)
    # FUTURE: implement timezones.
    timezone = messages.StringField(4)

EVENT_SEARCH_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    SearchQuery,
    calendar_id=messages.StringField(5, required=True)
)