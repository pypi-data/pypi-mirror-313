from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)


from .module_imports import key


@headers({"Ocp-Apim-Subscription-Key": key})
class _Events(Consumer):
    """Inteface to Events resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def sent_emails(self):
        """Inteface to Sent Emails resource for the RockyRoad API."""
        return self._Sent_Emails(self)

    def portal_logs(self):
        """Inteface to Portal Logs resource for the RockyRoad API."""
        return self._Portal_Logs(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class _Sent_Emails(Consumer):
        """Inteface to Sent Emails resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("events/sent-emails")
        def list(
            self,
            limit: Query = None,
            order: Query = None,
            recipient: Query = None,
            reply_to: Query = None,
            subject: Query = None,
        ):
            """This call will return list of Sent Emails."""

        @returns.json
        @http_get("events/sent-emails/{uid}")
        def get(self, uid: str):
            """This call will get the Sent Email for the specified uid."""

        @delete("events/sent-emails/{uid}")
        def delete(self, uid: str):
            """This call will delete the Sent Email for the specified uid."""

        @returns.json
        @json
        @post("events/sent-emails")
        def insert(self, sent_email_object: Body):
            """This call will create the Sent Email with the specified parameters."""

        @json
        @patch("events/sent-emails/{uid}")
        def update(self, uid: str, sent_email_object: Body):
            """This call will update the Sent Email with the specified parameters."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class _Portal_Logs(Consumer):
        """Inteface to Portal Logs resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("events/portal-logs")
        def list(
            self,
            limit: Query = None,
            order: Query = None,
            login_email: Query = None,
            message: Query = None,
            event_data: Query = None,
            company: Query = None,
            user_uid: Query = None,
            subdomain: Query = None,
            environment: Query = None,
        ):
            """This call will return list of Portal Logs."""

        @returns.json
        @http_get("events/portal-logs/last-login-statistics")
        def last_login_statistics(
            self,
            user_role: Query = None,
            company_uid: Query = None,
        ):
            """This call will return list of the last login time for users."""
