from telemetry.providers import MockTelemetryProvider


class TelemetryManager:
    provider_classes = {'mock': MockTelemetryProvider}

    def __init__(self):
        self._providers = {}

    def provider_for(self, rig):
        provider_class = self.provider_classes.get(rig.provider, MockTelemetryProvider)
        if rig.id not in self._providers or not isinstance(self._providers[rig.id], provider_class):
            self._providers[rig.id] = provider_class()
        return self._providers[rig.id]

    def read(self, rig):
        return self.provider_for(rig).read(rig)

    def close(self):
        for provider in self._providers.values():
            provider.close()
        self._providers.clear()
