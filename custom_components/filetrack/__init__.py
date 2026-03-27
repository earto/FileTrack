import os
import uuid
import logging
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.storage import Store
from homeassistant.helpers import config_validation as cv, discovery
from .const import DOMAIN, CONF_FOLDER_PATHS, CONF_FILTER, CONF_SORT, CONF_RECURSIVE, DEFAULT_FILTER, DEFAULT_SORT, DEFAULT_RECURSIVE

_LOGGER = logging.getLogger(__name__)
STORAGE_KEY = f"{DOMAIN}.sensors"
STORAGE_VERSION = 1

ADD_SENSOR_SCHEMA = vol.Schema({
    vol.Required("name"): cv.string,
    vol.Required(CONF_FOLDER_PATHS): cv.string,
    vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): cv.string,
    vol.Optional(CONF_SORT, default=DEFAULT_SORT): cv.string,
    vol.Optional(CONF_RECURSIVE, default=DEFAULT_RECURSIVE): cv.boolean,
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Initialiseer FileTrack en registreer de add_sensor service."""
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    stored = await store.async_load() or {"sensors": []}

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["store"] = store
    hass.data[DOMAIN]["stored"] = stored
    hass.data[DOMAIN]["add_entities"] = None

    async def handle_add_sensor(call: ServiceCall) -> None:
        name = call.data["name"].strip()
        folder = call.data[CONF_FOLDER_PATHS].strip().rstrip("/")
        filter_term = call.data.get(CONF_FILTER, DEFAULT_FILTER)
        sort = call.data.get(CONF_SORT, DEFAULT_SORT)
        recursive = call.data.get(CONF_RECURSIVE, DEFAULT_RECURSIVE)

        if not os.path.isdir(folder):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                _LOGGER.error("FileTrack: map aanmaken mislukt %s: %s", folder, e)
                raise ValueError(f"Kan map niet aanmaken: {folder}") from e

        sensor_id = uuid.uuid4().hex

        sensor_config = {
            "id": sensor_id,
            "name": name,
            CONF_FOLDER_PATHS: folder,
            CONF_FILTER: filter_term,
            CONF_SORT: sort,
            CONF_RECURSIVE: recursive,
        }
        stored["sensors"].append(sensor_config)
        await store.async_save(stored)

        add_entities = hass.data[DOMAIN].get("add_entities")
        if add_entities:
            from .sensor import FileTrackSensor
            add_entities([FileTrackSensor(folder, name, filter_term, sort, recursive, sensor_id)], True)
        else:
            _LOGGER.warning("FileTrack: sensor platform nog niet geladen, sensor verschijnt na herstart")

    hass.services.async_register(DOMAIN, "add_sensor", handle_add_sensor, schema=ADD_SENSOR_SCHEMA)

    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True
