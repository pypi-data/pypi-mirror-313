from typing import Literal, Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenModelLegends, DataGardenSubModel

TEMP_SCALES: Literal["CELSIUS", "FAHRENHEID"]


class WeatherPeriodTotalsV1Keys:
    DAYS_WITH_PRECIPITATION = "days_with_precipitation"
    DAYS_WITH_SNOW = "days_with_snow"
    DAYS_WITH_SUN = "days_with_sun"
    TOTAL_PRECIPITATION_MM = "total_precipitation_mm"
    TOTAL_SNOW_CM = "total_snow_cm"
    TOTAL_SUN_HOURS = "total_sun_hours"
    DAYS_WITH_WEATHER_DATA = "days_with_weather_data"
    DAYS_WITH_METRIC_DATA = "days_with_metric_data"
    VALUE = "value"


class WeatherPeriodTotalsV1Legends(DataGardenModelLegends):
    DAYS_WITH_PRECIPITATION = "days with precipitation > 0 mm"
    DAYS_WITH_SNOW = "days with snow > 0 cm"
    DAYS_WITH_SUN = "days with sun > 0 hours"
    TOTAL_PRECIPITATION_MM = "total precipitation in mm for the period"
    TOTAL_SNOW_CM = "total snow in cm for the period"
    TOTAL_SUN_HOURS = "total sun hours"
    DAYS_WITH_WEATHER_DATA = "number of days for which weather data is available during the period"
    DAYS_WITH_METRIC_DATA = "number of days for which metric data is available during the period"
    VALUE = "value of metric"


L = WeatherPeriodTotalsV1Legends


class Total(DataGardenSubModel):
    value: Optional[float] = Field(None, ge=0, description=L.VALUE)
    days_with_metric_data: Optional[int] = Field(None, ge=0, description=L.DAYS_WITH_METRIC_DATA)


class TotalInt(DataGardenSubModel):
    value: Optional[int] = Field(None, ge=0, description=L.VALUE)
    days_with_metric_data: Optional[int] = Field(None, ge=0, description=L.DAYS_WITH_METRIC_DATA)


class WeatherPeriodTotalsV1(DataGardenSubModel):
    days_with_precipitation: Optional[TotalInt] = Field(None, description=L.DAYS_WITH_PRECIPITATION)
    days_with_snow: Optional[TotalInt] = Field(None, description=L.DAYS_WITH_SNOW)
    days_with_sun: Optional[TotalInt] = Field(None, description=L.DAYS_WITH_SUN)
    total_precipitation_mm: Optional[Total] = Field(None, description=L.TOTAL_PRECIPITATION_MM)
    total_snow_cm: Optional[Total] = Field(None, description=L.TOTAL_SNOW_CM)
    total_sun_hours: Optional[Total] = Field(None, description=L.TOTAL_SUN_HOURS)
    days_with_weather_data: Optional[int] = Field(None, ge=0, description=L.DAYS_WITH_WEATHER_DATA)

    @property
    def is_empty(self) -> bool:
        return all(
            getattr(self, field) is None
            for field in self.model_fields
            if field not in ["temp_scale", "datagarden_model_version"]
        )

    def __bool__(self) -> bool:
        return not self.is_empty
