import uuid
from homeassistant import config_entries
from homeassistant.helpers.storage import Store
from homeassistant.helpers import selector
import voluptuous as vol
from .const import (DOMAIN, CONF_FOLDER_PATHS, CONF_FILTER, CONF_SORT, CONF_RECURSIVE, DEFAULT_FILTER, DEFAULT_SORT, DEFAULT_RECURSIVE, SORT_OPTIONS)

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.sensors"


class FileTrackConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Auto-setup: geen formulier nodig, activeert FileTrack direct."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="FileTrack", data={})

    @staticmethod
    def async_get_options_flow(config_entry):
        return FileTrackOptionsFlow(config_entry)


class FileTrackOptionsFlow(config_entries.OptionsFlow):
    """Options flow. Updated menu with add/remove control based on modern entity linking"""

    def __init__(self, config_entry):
        self._config_entry = config_entry
        self._to_remove = []

    async def async_step_init(self, user_input=None):
        return self.async_show_menu(
            step_id="init",
            menu_options=["add_sensor", "remove_sensor"]
        )

    async def async_step_add_sensor(self, user_input=None):
        if user_input is not None:
            store = Store(self.hass, STORAGE_VERSION, STORAGE_KEY)
            stored = await store.async_load() or {"sensors": []}
            new_sensor = {
                "id": uuid.uuid4().hex,
                "name": user_input["name"],
                CONF_FOLDER_PATHS: user_input[CONF_FOLDER_PATHS],
                CONF_FILTER: user_input.get(CONF_FILTER, DEFAULT_FILTER),
                CONF_SORT: user_input.get(CONF_SORT, DEFAULT_SORT),
                CONF_RECURSIVE: user_input.get(CONF_RECURSIVE, DEFAULT_RECURSIVE),
            }
            
            stored["sensors"].append(new_sensor)
            await store.async_save(stored)
            await self.hass.config_entries.async_reload(self._config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required(CONF_FOLDER_PATHS): str,
            vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): str,
            vol.Optional(CONF_SORT, default=DEFAULT_SORT): vol.In(SORT_OPTIONS),
            vol.Optional(CONF_RECURSIVE, default=DEFAULT_RECURSIVE): bool,
        })
        return self.async_show_form(step_id="add_sensor", data_schema=data_schema)

    async def async_step_remove_sensor(self, user_input=None):
        store = Store(self.hass, STORAGE_VERSION, STORAGE_KEY)
        stored = await store.async_load() or {"sensors": []}
        sensors = stored.get("sensors", [])

        if not sensors:
            return self.async_abort(reason="no_sensors")
            
        if user_input is not None:
            self._to_remove = user_input.get("sensors", [])
            if not self._to_remove:
                return self.async_abort(reason="cancelled")
            return await self.async_step_confirm()

        options = [{"value": s["name"], "label": s["name"]} for s in sensors]
        return self.async_show_form(
            step_id="remove_sensor",
            data_schema=vol.Schema({
                vol.Required("sensors"): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=options, multiple=True)
                )
            }),
        )

    async def async_step_confirm(self, user_input=None):
        if user_input is not None:
            if user_input.get("confirm"):
                for name in self._to_remove:
                    await self._do_remove(name)
                await self.hass.config_entries.async_reload(self._config_entry.entry_id)
                return self.async_create_entry(title="", data={})
            return self.async_abort(reason="cancelled")

        names = "\n".join(f"• {n}" for n in self._to_remove)
        return self.async_show_form(
            step_id="confirm",
            data_schema=vol.Schema({
                vol.Required("confirm", default=False): bool,
            }),
            description_placeholders={"names": names},
        )

    async def _do_remove(self, name):
        store = Store(self.hass, STORAGE_VERSION, STORAGE_KEY)
        stored = await store.async_load() or {"sensors": []}

        match = next((s for s in stored["sensors"] if s["name"] == name), None)
        if not match:
            return

        sensor_id = match["id"]

        from homeassistant.helpers import entity_registry as er
        registry = er.async_get(self.hass)
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, sensor_id)
        if entity_id:
            registry.async_remove(entity_id)

        stored["sensors"] = [s for s in stored["sensors"] if s["id"] != sensor_id]
        await store.async_save(stored)
