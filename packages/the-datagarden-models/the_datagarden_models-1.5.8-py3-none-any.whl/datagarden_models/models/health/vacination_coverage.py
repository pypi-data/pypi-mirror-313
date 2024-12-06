from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class VaccinationDetailsKeys:
    GRADE = "grade"
    LOCAL_NAME = "local_name"
    GLOBAL_VACCINE_NAME = "global_vaccine_name"
    TARGET_POPULATION = "target_population"


class VaccinationDetailsLegends:
    GRADE = "Grade of vaccination per type of vaccine."
    LOCAL_NAME = "Local name of the vaccination."
    GLOBAL_NAME = "Standard name code of the vaccination."
    TARGET_POPULATION = "Target population of the vaccination."


class VaccinationDetails(DataGardenSubModel):
    grade: float
    local_name: Optional[str] = None
    global_vaccine_name: Optional[str] = None
    target_population: Optional[int] = None


class VaccinationCoverageKeys(VaccinationDetailsKeys):
    GRADE_PER_TYPE = "grade_per_type"


class VaccinationCoverageLegends:
    GRADE_PER_TYPE = "Grade of vaccination per type of vaccine. " "Type will ususally be a regional key."


L = VaccinationCoverageLegends


class VaccinationCoverage(DataGardenSubModel):
    grade_per_type: Optional[dict[str, VaccinationDetails]] = Field(
        default=None, description=L.GRADE_PER_TYPE
    )
