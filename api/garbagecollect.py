"""Clear out old or unbound datastore entities."""

import logging

from google.appengine.ext import ndb
from oauth2client.appengine import CredentialsNDBModel
from endpoints import NotFoundException
import webapp2

import gapiutils
import authutils
import models
import strings

__author__ = "Alexander Otavka"
__copyright__ = "Copyright (C) 2015 DHS Developers Club"


class GarbageCollector(webapp2.RequestHandler):
    """Respond to chron job by ensuring the event database is clean."""

    def get(self):
        unbound_count = 0
        old_count = 0
        for user_entity in models.get_user_query().iter(keys_only=True):
            user_id = user_entity.key.string_id()
            cred_entity = ndb.Key(CredentialsNDBModel, user_id).get()
            service = authutils.get_service(authutils.CALENDAR_API_NAME,
                                            authutils.CALENDAR_API_VERSION,
                                            cred_entity.credentials)
            events_query = models.Event.query(ancestor=user_entity.key)

            for event in events_query.iter(keys_only=True):
                event_id = event.key.string_id()
                cal_id = event.key.parent().string_id()

                try:
                    gapiutils.get_event(service, cal_id, event_id, "UTC",
                                        validation_only=True)
                except NotFoundException:
                    logging.info(strings.LOGGING_DELETE_UNBOUND_EVENT
                                 .format(event_id=event_id, calendar_id=cal_id,
                                         user_id=user_id))
                    event.key.delete()
                    unbound_count += 1
                    continue
                except gapiutils.OldEventError:
                    logging.info(strings.LOGGING_DELETE_OLD_EVENT
                                 .format(event_id=event_id, calendar_id=cal_id,
                                         user_id=user_id))
                    event.key.delete()
                    old_count += 1
                    continue

        self.response.write(strings.LOGGING_GARBAGE_COLLECTION_SUMMARY
                            .format(old=old_count, unbound=unbound_count,
                                    total=(old_count + unbound_count)))


collectors = webapp2.WSGIApplication([
    ("/_ah/garbagecollect/go", GarbageCollector),
])