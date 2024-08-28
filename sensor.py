import logging
import aiohttp
from homeassistant.helpers.entity import Entity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    async with aiohttp.ClientSession() as session:
        geh = GeWebsocketClient(username=config_entry.data["username"], password=config_entry.data["password"], region=config_entry.data["region"])
        try:
            await geh.async_get_credentials_and_run(session)
        except Exception as e:
            _LOGGER.error(f"Error setting up GE Appliances integration: {e}")
            return False

        sensors = []
        for appliance in geh.appliances:
            for attribute, value in appliance.attributes.items():
                sensors.append(GeHomeSensor(appliance.name, attribute, value))

        async_add_entities(sensors, True)

class GeHomeSensor(Entity):
    def __init__(self, device_name, attribute, value):
        self._device_name = device_name
        self._attribute = attribute
        self._value = value

    @property
    def name(self):
        return f"{self._device_name}_{self._attribute}"

    @property
    def state(self):
        return self._value

    @property
    def unique_id(self):
        return f"{self._device_name}_{self._attribute}"
