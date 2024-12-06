from typing import Literal, Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenModel, DataGardenModelLegends

from .period_totals import WeatherPeriodTotalsV1, WeatherPeriodTotalsV1Keys

TEMP_SCALES: Literal["CELSIUS", "FAHRENHEID"]


class WeatherV1Keys(WeatherPeriodTotalsV1Keys):
    MIN_TEMP = "min_temp"
    MAX_TEMP = "max_temp"
    MEAN_TEMP = "mean_temp"
    RAIN_FALL_MM = "rain_fall_mm"
    SEA_LEVEL_PRESSURE_HPA = "sea_level_pressure_hpa"
    CLOUD_COVER_OKTA = "cloud_cover_okta"
    TEMP_SCALE = "temp_scale"
    WIND_DIRECTION = "wind_direction"
    WIND_SPEED_M_S = "wind_speed_m_s"
    MAX_WIND_GUST_M_S = "max_wind_gust_m_s"
    SUN_HOURS = "sun_hours"
    SNOW_DEPTH_CM = "snow_depth_cm"
    RADIATION_PER_SQUARE_M = "radiation_per_square_m"
    HUMIDITY = "humidity"
    DATAGARDEN_MODEL_NAME = "WeatherData"
    PERIOD_TOTALS = "period_totals"


class WeatherV1Legends(DataGardenModelLegends):
    MODEL_LEGEND: str = "Weather data for a region. "
    MIN_TEMP = "minimum temperature"
    MAX_TEMP = "maximum temperature"
    MEAN_TEMP = "mean temperature"
    TEMP_SCALE = "unit of temperature(Celsius or Fahrenheit)"
    RAIN_FALL_MM = "rainfall in mm"
    SEA_LEVEL_PRESSURE_HPA = "sea level pressure in hPa"
    CLOUD_COVER_OKTA = "cloud cover in oktas"
    WIND_DIRECTION = "wind direction in degrees"
    WIND_SPEED_M_S = "wind speed in m/s"
    MAX_WIND_GUST_M_S = "max wind gust in m/s"
    SUN_HOURS = "sun hours"
    SNOW_DEPTH_CM = "snow depth in cm"
    RADIATION_PER_SQUARE_M = "radiation per square meter in W/m²"
    HUMIDITY = "humidity in %"
    PERIOD_TOTALS = "Weather totals for the period"


L = WeatherV1Legends


class WeatherObservationV1(DataGardenModel):
    datagarden_model_version: str = Field("v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION)
    min_temp: Optional[float] = Field(None, ge=-70, le=70, description=L.MIN_TEMP)
    max_temp: Optional[float] = Field(None, ge=-70, le=70, description=L.MAX_TEMP)
    mean_temp: Optional[float] = Field(None, ge=-70, le=70, description=L.MEAN_TEMP)
    rain_fall_mm: Optional[float] = Field(None, ge=0, description=L.RAIN_FALL_MM)
    sea_level_pressure_hpa: Optional[float] = Field(
        None, ge=850, le=1100, description=L.SEA_LEVEL_PRESSURE_HPA
    )
    cloud_cover_okta: Optional[int] = Field(None, ge=0, le=8, description=L.CLOUD_COVER_OKTA)
    temp_scale: Literal["CELSIUS", "FAHRENHEID"] = Field("CELSIUS", description=L.TEMP_SCALE)
    wind_direction: Optional[int] = Field(None, ge=0, le=359, description=L.WIND_DIRECTION)
    wind_speed_m_s: Optional[float] = Field(None, ge=0, le=110, description=L.WIND_SPEED_M_S)
    max_wind_gust_m_s: Optional[float] = Field(None, ge=0, le=110, description=L.MAX_WIND_GUST_M_S)
    sun_hours: Optional[float] = Field(None, ge=0, le=24, description=L.SUN_HOURS)
    snow_depth_cm: Optional[float] = Field(None, ge=0, le=10000, description=L.SNOW_DEPTH_CM)
    radiation_per_square_m: Optional[float] = Field(
        None, ge=-100, le=2000, description=L.RADIATION_PER_SQUARE_M
    )
    humidity: Optional[float] = Field(None, ge=0, le=100, description=L.HUMIDITY)
    period_totals: Optional[WeatherPeriodTotalsV1] = Field(None, description=L.PERIOD_TOTALS)

    class Meta:
        exclude_fields_in_has_values_check: list[str] = [WeatherV1Keys.TEMP_SCALE]
