from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class EventsCaller(Component):
    def mount(self):
        self.emit('event_name', {'something': 1})

    def set_event(self):
        self.emit('another_event', {'else': 2})

    def method_without_event_emitting(self):
        pass

    def inline_template(self):
        return """
            <div>
                I call events!
            </div>
        """


class ComponentWithListener(Component):
    received_event_payload = {}

    def some_event_name(self, payload):
        self.received_event_payload = payload

    def inline_template(self):
        return """
            <div>
                Event called:
                <div>{{ received_event_name }}</div>
                <div>{{ received_event_payload }}</div>
            </div>
        """


class LazyComponentEventReceiver(Component):
    received_event_payload = {}

    def some_event_name(self, payload):
        self.received_event_payload = payload

    def inline_template(self):
        return """
            <div>
                Event called:
                <div>{{ received_event_name }}</div>
                <div>{{ received_event_payload }}</div>
            </div>
        """


class EventsTest(SilicaTestCase):
    def test_event_is_called_from_mount(self):
        (
            SilicaTest(component=EventsCaller)
            .assertEventEmitted('event_name', {'something': 1})
        )

    def test_event_is_called_from_message(self):
        request = (
            SilicaTest(component=EventsCaller)
            .call('set_event')
            .assertEventEmitted('another_event', {'else': 2})
        )

        (request
            .call('method_without_event_emitting')
            .assertEventNotEmitted('another_event')
         )

    def test_an_event_listener_is_called_and_payload_received(self):
        (
            SilicaTest(component=ComponentWithListener)
            .emit('some_event_name', {'something': 1})
            .assertSee("{'something': 1}")
        )

    def test_emitting_event_to_one_component_name(self):
        (
            SilicaTest(component=ComponentWithListener)
            .emit_to('some_event_name', {'something': 1})
            .assertSee("{'something': 1}")
        )

    def test_emitting_event_to_one_component_name_only(self):
        # Needs browser testing
        pass

    def test_emitting_event_to_multiple_components_with_same_name(self):
        # Needs browser testing
        pass

    def test_emitting_events_to_lazy_components(self):
        # Not really able to test properly, need browser testing
        (
            SilicaTest(component=LazyComponentEventReceiver, lazy=True)
            .emit('some_event_name', {'something': 1})
            .assertSee("{'something': 1}")
        )

    def test_emitting_events_from_lazy_components(self):
        pass