import pandas as pd
from typing import List, Optional
from enum import Enum, IntEnum
from pydantic import BaseModel, Field
from pprint import pprint
from db import Medical_Database
import math

replace_nan = lambda value: 0 if math.isnan(value) else value


class Gender(Enum):
    Male = "M"
    Female = "F"
    Unisex = "U"


class Decision(Enum):
    Yes = "Y"
    Maybe = "M"
    No = "N"


class DAC_Reference(BaseModel):
    # Address ID - Unique identifier for the practice location; offices within the same building, but varied by suite or floor, will have the same Address ID aside from the final two characters
    address_id: str = Field(max_length=25)  # type - (string) | length - (25)


class DAC_Medical_Assignment(BaseModel):
    # Clinician accepts Medicare Assignment - Indicator for whether clinician accepts Medicare approved amount as payment in full Y = Clinician accepts Medicare approved amount as payment in full M = Clinician may accept Medicare Assignment
    clinician_accepts_medicare_assignment: (
        Decision  # type - (string (Y/M)) | length - (1)
    )

    # Group accepts Medicare Assignment - Indicator for whether group accepts Medicare approved amount as payment in full Y = Group accepts Medicare approved amount as payment in full M = Group may accept Medicare Assignment
    group_accepts_medicare_assignment: Decision  # type - (string (Y/M)) | length - (1)


class DAC_Medical_Credentials(BaseModel):
    # Pri_spec Primary specialty Primary medical specialty reported by the individual
    # clinician in the selected enrollment
    primary_specialty: str = Field(max_length=60)  # type - (string) | length - (60)

    # Sec_spec_1 Secondary specialty 1 First secondary medical specialty reported by the
    # individual clinician in the selected enrollment
    secondary_specialty_one: str = Field(
        max_length=60
    )  # type - (string) | length - (60)

    # Sec_spec_2 Secondary specialty 2 Second secondary medical specialty reported by the
    # individual clinician in the selected enrollment
    secondary_specialty_two: str = Field(
        max_length=60
    )  # type - (string) | length - (60)

    # Sec_spec_3 Secondary specialty 3 Third secondary medical specialty reported by the
    # individual clinician in the selected enrollment
    secondary_specialty_three: str = Field(
        max_length=60
    )  # type - (string) | length - (60)

    # Sec_spec_4 Secondary specialty 4 Fourth secondary medical specialty reported by the
    # individual clinician in the selected enrollment
    secondary_specialty_four: str = Field(
        max_length=60
    )  # type - (string) | length - (60)

    # Sec_spec_all All secondary specialties All secondary medical specialty reported by the
    # individual clinician in the selected enrollment
    all_secondary_specialties: str = Field(
        max_length=200
    )  # type - (string) | length - (200)


class DAC_Medical_Practice(BaseModel):
    # Telehealth - Indicator for whether clinician offers telehealth services over video and/or audio Y = Medicare fee-for-service claims indicate that clinician offers telehealth services
    telehealth: str  # type - (string) | length - (1)

    # Facility Name - Legal organization name of the group practice that the individual clinician works with – will be blank if the address is not linked to a group
    facility_name: str = Field(max_length=70)  # type - (string) | length - (70)

    # Group PAC ID - Unique group ID assigned by PECOS to the group that the individual clinician works with – will be blank if the address is not linked to a group
    group_pac_id: int  # type - (string) | length - (10)

    # Number of group members - Total number of individual clinicians affiliated with the group based on Group Practice PAC ID
    number_of_group_members: int  # type - (numeric) | length - (8)

    # Line 1 Street Address - Group or individual's line 1 address
    address_line_one: str = Field(max_length=55)  # type - (string) | length - (55)

    # Line 2 Street Address - Group or individual's line 2 address
    address_line_two: str = Field(max_length=55)  # type - (string) | length - (55)

    # Marker of address line 2 suppression - Marker that the address as reported may be incomplete
    address_incompletion_marker: str  # type - (string) | length - (1)

    # City/Town - Group or individual's city
    city: str = Field(max_length=30)  # type - (string) | length - (30)

    # State - Group or individual's state
    state: str = Field(max_length=2)  # type - (string) | length - (2)

    # Zip Code - Group or individual's ZIP code (9 digits when available)
    zip_code: str = Field(max_length=15)  # type - (string) | length - (15)

    # Telephone Number - Phone number is listed only when there is a single phone number available for the address
    # had to remove the max length field
    telephone_number: str  # type - (string) | length - (15)

    medical_credentials: DAC_Medical_Credentials

    medical_assignment: DAC_Medical_Assignment

    # reference ID
    reference: DAC_Reference


class DAC_Medical_Professional(BaseModel):
    # NPI - Unique clinician ID assigned by NPPES
    npi: int  # type - (string) | length - (10)

    # PAC ID - Unique individual clinician ID assigned by PECOS
    ind_pac_id: int  # type - (string) | length - (10)

    # Clinician Enrollment ID - Unique ID for the clinician enrollment that is the source for the data in the observation
    ind_enrl_id: str = Field(max_length=15)  # type - (string) | length - (15)

    # Provider Last Name - Individual clinician last name
    provider_last_name: str = Field(max_length=35)  # type - (string) | length - (35)

    # Provider First Name - Individual clinician first name
    provider_first_name: str = Field(max_length=25)  # type - (string) | length - (25)

    # Provider Middle Name - Individual clinician middle name
    provider_middle_name: Optional[str] = Field(
        max_length=25
    )  # type - (string) | length - (25)
    # Suffix - Individual clinician suffix
    suffix: Optional[str] = Field(max_length=10)  # type - (string) | length - (10)

    # Gender - Individual clinician gender
    gender: Gender  # type - (string (M/F/U)) | length - (1)

    # Credential - Medical credential such as MD, DO, DPM, etc.
    credentials: str = Field(max_length=3)  # type - (string) | length - (3)

    # Medical School Name - Individual clinician’s medical school
    medical_school: str = Field(max_length=100)  # type - (string) | length - (100)

    # Grd_yr Graduation year Individual clinician’s medical school graduation year
    graduation_year: int  # type - (numeric) | length - (4)

    # Medical Practices - Medical Practices that this medical professional has worked at
    medical_practices: List[DAC_Medical_Practice]


if __name__ == "__main__":
    print("[o] Loading CSV File...")
    csv_data = pd.read_csv("./data/DAC_NationalDownloadableFile.csv")
    db_class = Medical_Database(db_path="database/medical_test.db")
    med_dict = dict()
    for key, value in csv_data.iterrows():
        csv_row = value.to_dict()
        csv_row_medical_professional_npi = int(csv_row["NPI"])

        dac_medical_practice = DAC_Medical_Practice(
            telehealth=str(csv_row["Telehlth"]),
            facility_name=str(csv_row["Facility Name"]),
            group_pac_id=int(replace_nan(csv_row["org_pac_id"])),
            number_of_group_members=int(replace_nan(csv_row["num_org_mem"])),
            address_line_one=str(csv_row["adr_ln_1"]),
            address_line_two=str(csv_row["adr_ln_2"]),
            address_incompletion_marker=str(csv_row["ln_2_sprs"]),
            city=str(csv_row["City/Town"]),
            state=str(csv_row["State"]),
            zip_code=str(csv_row["ZIP Code"]),
            telephone_number=str(int(replace_nan(csv_row["Telephone Number"]))),
            medical_credentials=DAC_Medical_Credentials(
                primary_specialty=str(csv_row["pri_spec"]),
                secondary_specialty_one=str(csv_row["sec_spec_1"]),
                secondary_specialty_two=str(csv_row["sec_spec_2"]),
                secondary_specialty_three=str(csv_row["sec_spec_3"]),
                secondary_specialty_four=str(csv_row["sec_spec_4"]),
                all_secondary_specialties=str(csv_row["sec_spec_all"]),
            ),
            medical_assignment=DAC_Medical_Assignment(
                group_accepts_medicare_assignment=str(csv_row["grp_assgn"]),
                clinician_accepts_medicare_assignment=str(csv_row["ind_assgn"]),
            ),
            reference=DAC_Reference(address_id=str(csv_row["adrs_id"])),
        )

        pprint(csv_row)
        print("==========================================================")
        if csv_row_medical_professional_npi not in med_dict:
            dac_med_professional = DAC_Medical_Professional(
                npi=int(csv_row["NPI"]),
                ind_pac_id=int(csv_row["Ind_PAC_ID"]),
                ind_enrl_id=str(csv_row["Ind_enrl_ID"]),
                provider_last_name=str(csv_row["Provider Last Name"]),
                provider_first_name=str(csv_row["Provider First Name"]),
                provider_middle_name=str(csv_row["Provider Middle Name"]),
                suffix=str(csv_row["suff"]),
                gender=str(csv_row["gndr"]),
                credentials=str(csv_row["Cred"]),
                medical_school=str(csv_row["Med_sch"]),
                graduation_year=(int(replace_nan(csv_row["Grd_yr"]))),
                medical_practices=[],
            )
            dac_med_professional.medical_practices.append(dac_medical_practice)
            med_dict[dac_med_professional.npi] = dac_med_professional
            db_class.add_medical_professional(
                npi=dac_med_professional.npi,
                ind_pac_id=dac_med_professional.ind_pac_id,
                ind_enrl_id=dac_med_professional.ind_enrl_id,
                provider_last_name=dac_med_professional.provider_last_name,
                provider_first_name=dac_med_professional.provider_first_name,
                provider_middle_name=dac_med_professional.provider_middle_name,
                suffix=dac_med_professional.suffix,
                gender=dac_med_professional.gender.value,
                credentials=dac_med_professional.credentials,
                medical_school=dac_med_professional.medical_school,
                graduation_year=dac_med_professional.graduation_year,
            )
        else:
            med_dict[csv_row_medical_professional_npi].medical_practices.append(
                dac_medical_practice
            )

        db_class.add_medical_practice(
            npi=csv_row_medical_professional_npi,
            telehealth=dac_medical_practice.telehealth,
            facility_name=dac_medical_practice.facility_name,
            group_pac_id=dac_medical_practice.group_pac_id,
            number_of_group_members=dac_medical_practice.number_of_group_members,
            address_line_one=dac_medical_practice.address_line_one,
            address_line_two=dac_medical_practice.address_line_two,
            address_incompletion_marker=dac_medical_practice.address_incompletion_marker,
            city=dac_medical_practice.city,
            state=dac_medical_practice.state,
            zip_code=dac_medical_practice.zip_code,
            telephone_number=dac_medical_practice.telephone_number,
            primary_specialty=dac_medical_practice.medical_credentials.primary_specialty,
            secondary_specialty_one=dac_medical_practice.medical_credentials.secondary_specialty_one,
            secondary_specialty_two=dac_medical_practice.medical_credentials.secondary_specialty_two,
            secondary_specialty_three=dac_medical_practice.medical_credentials.secondary_specialty_three,
            secondary_specialty_four=dac_medical_practice.medical_credentials.secondary_specialty_four,
            all_secondary_specialties=dac_medical_practice.medical_credentials.all_secondary_specialties,
            group_accepts_medicare_assignment=dac_medical_practice.medical_assignment.group_accepts_medicare_assignment.value,
            clinician_accepts_medicare_assignment=dac_medical_practice.medical_assignment.clinician_accepts_medicare_assignment.value,
            address_id=dac_medical_practice.reference.address_id,
        )
