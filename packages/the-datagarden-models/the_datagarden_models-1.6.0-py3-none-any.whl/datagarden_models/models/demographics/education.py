from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class PercentagesByAgeGenderBaseKeys:
    MALE = "male"
    FEMALE = "female"
    TOTAL = "total"


class PercentagesByAgeGenderLegends:
    AGE_GENDER_MALE = "Percentage of males in with given education level. "
    AGE_GENDER_FEMALE = "Percentage of females with education level. "
    AGE_GENDER_TOTAL = "Percentage of males and females with education level. "


L1a = PercentagesByAgeGenderLegends


class PercentagesByAgeGender(DataGardenSubModel):
    male: dict = Field(default_factory=dict, description=L1a.AGE_GENDER_MALE)
    female: dict = Field(default_factory=dict, description=L1a.AGE_GENDER_FEMALE)
    total: dict = Field(default_factory=dict, description=L1a.AGE_GENDER_TOTAL)


class CountByAgeGenderLegends:
    AGE_GENDER_MALE = "Number of males in with given education level. "
    AGE_GENDER_FEMALE = "Number of females with education level. "
    AGE_GENDER_TOTAL = "Number of males and females with education level. "


L1b = CountByAgeGenderLegends


class CountByAgeGender(DataGardenSubModel):
    male: dict = Field(default_factory=dict, description=L1b.AGE_GENDER_MALE)
    female: dict = Field(default_factory=dict, description=L1b.AGE_GENDER_FEMALE)
    total: dict = Field(default_factory=dict, description=L1b.AGE_GENDER_TOTAL)


class Isced2011EducationLevelKeys:
    ISCED_2011_5TO8 = "isced_2011_5to8"
    ISCED_2011_5_COUNT = "isced_2011_5_count"
    ISCED_2011_6_COUNT = "isced_2011_6_count"
    ISCED_2011_7_COUNT = "isced_2011_7_count"
    ISCED_2011_8_COUNT = "isced_2011_8_count"


class Isced2011EducationLevelLegends:
    ISCED_2011_5TO8 = (
        "Level 5 up to and including level 8 of the "
        "ISCED 2011 International Standard Classification of Education."
    )
    ISCED_2011_5_COUNT = (
        "Count for Level 5 (Short cycle tertiary) education of the "
        "ISCED 2011 International Standard Classification of Education."
    )
    ISCED_2011_6_COUNT = (
        "Count for Level 6 (Bachelor's or equivalent) education of the "
        "ISCED 2011 International Standard Classification of Education."
    )
    ISCED_2011_7_COUNT = (
        "Count for Level 7 (Master's or equivalent) education of the "
        "ISCED 2011 International Standard Classification of Education."
    )
    ISCED_2011_8_COUNT = (
        "Count for Level 8 (Doctoral or equivalent) education of the "
        "ISCED 2011 International Standard Classification of Education."
    )


L2 = Isced2011EducationLevelLegends


class Isced2011EducationLevel(DataGardenSubModel):
    isced_2011_5to8: PercentagesByAgeGender = Field(
        default_factory=PercentagesByAgeGender, description=L2.ISCED_2011_5TO8
    )
    isced_2011_5_count: CountByAgeGender = Field(
        default_factory=CountByAgeGender, description=L2.ISCED_2011_5_COUNT
    )
    isced_2011_6_count: CountByAgeGender = Field(
        default_factory=CountByAgeGender, description=L2.ISCED_2011_6_COUNT
    )
    isced_2011_7_count: CountByAgeGender = Field(
        default_factory=CountByAgeGender, description=L2.ISCED_2011_7_COUNT
    )
    isced_2011_8_count: CountByAgeGender = Field(
        default_factory=CountByAgeGender, description=L2.ISCED_2011_8_COUNT
    )


class EducationV1Legends:
    ISCED_2011_BY_AGE_GENDER = (
        "Percentage or count of and age gender group with a given education level. "
        "see https://uis.unesco.org/sites/default/files/documents/international-standard-classification-of-education-isced-2011-en.pdf"
        " for detailed explenation of the education levels."
    )


L3 = EducationV1Legends


class Education(DataGardenSubModel):
    isced_2011_by_age_gender: Isced2011EducationLevel = Field(
        default_factory=Isced2011EducationLevel, description=L3.ISCED_2011_BY_AGE_GENDER
    )


class EducationV1Keys(
    PercentagesByAgeGenderBaseKeys,
    Isced2011EducationLevelKeys,
):
    ISCED_2011_BY_AGE_GENDER = "isced_2011_by_age_gender"
