from mtmai.config import Settings
from mtmai.config import settings as base_settings


class SettingsManager:
    __instance: Settings = base_settings

    @staticmethod
    def get_settings() -> Settings:
        return SettingsManager.__instance

    @staticmethod
    def set_settings(settings: Settings) -> None:
        SettingsManager.__instance = settings
