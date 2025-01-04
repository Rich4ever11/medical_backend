import sqlite3
import traceback


class Medical_Database:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path, isolation_level=None)
        self.create_tables()

    def create_tables(self):
        print("[o] Creating Medical Tables...")
        self.connection.execute("""DROP TABLE IF EXISTS medical_professional;""")
        self.connection.execute(
            """
            CREATE TABLE medical_professional (
                npi INTEGER PRIMARY KEY,
                ind_pac_id INTEGER NOT NULL UNIQUE,
                ind_enrl_id TEXT NOT NULL,
                provider_last_name TEXT NOT NULL,
                provider_first_name TEXT NOT NULL,
                provider_middle_name TEXT NOT NULL,
                suffix TEXT NOT NULL,
                gender TEXT NOT NULL,
                
                credentials TEXT NOT NULL,
                medical_school TEXT NOT NULL,
                graduation_year INTEGER NOT NULL
        )"""
        )
        self.connection.execute("""DROP TABLE IF EXISTS medical_practice;""")
        self.connection.execute(
            """
            CREATE TABLE medical_practice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telehealth TEXT NOT NULL,
                facility_name TEXT NOT NULL,
                group_pac_id TEXT NOT NULL,
                number_of_group_members INTEGER NOT NULL,
                address_line_one TEXT NOT NULL,
                address_line_two TEXT NOT NULL,
                address_incompletion_marker TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                telephone_number TEXT NOT NULL,
                
                primary_specialty TEXT NOT NULL,
                secondary_specialty_one TEXT NOT NULL,
                secondary_specialty_two TEXT NOT NULL,
                secondary_specialty_three TEXT NOT NULL,
                secondary_specialty_four TEXT NOT NULL,
                all_secondary_specialties TEXT NOT NULL,
                
                group_accepts_medicare_assignment TEXT NOT NULL,
                clinician_accepts_medicare_assignment TEXT NOT NULL,
                
                address_id TEXT NOT NULL,
                
                
                npi INTEGER NOT NULL,
                FOREIGN KEY (npi) 
                    REFERENCES medical_professional (npi) 
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
        )"""
        )
        print("[+] Success: Medical Tables Created")
        print()

    def add_medical_professional(
        self,
        npi: int,
        ind_pac_id: int,
        ind_enrl_id: str,
        provider_last_name: str,
        provider_first_name: str,
        provider_middle_name: str,
        suffix: str,
        gender: str,
        credentials: str,
        medical_school: str,
        graduation_year: int,
    ):
        try:
            parameters = (
                npi,
                ind_pac_id,
                ind_enrl_id,
                provider_last_name,
                provider_first_name,
                provider_middle_name,
                suffix,
                gender,
                credentials,
                medical_school,
                graduation_year,
            )
            print("[o] Inserting Medical Professional Into DB:")
            print("\tparameters - ", parameters)
            self.connection.execute(
                """INSERT INTO medical_professional (npi, ind_pac_id, ind_enrl_id, provider_last_name, provider_first_name, provider_middle_name, suffix, gender, credentials, medical_school, graduation_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                parameters,
            )
            print("[+] Successfully Added a Medical Professional")
        except Exception:
            print(traceback.format_exc())
            print("[-] Failed to Add new Medical Professional")

    def add_medical_practice(
        self,
        npi: int,
        telehealth: str,
        facility_name: str,
        group_pac_id: str,
        number_of_group_members: int,
        address_line_one: str,
        address_line_two: str,
        address_incompletion_marker: str,
        city: str,
        state: str,
        zip_code: str,
        telephone_number: str,
        primary_specialty: str,
        secondary_specialty_one: str,
        secondary_specialty_two: str,
        secondary_specialty_three: str,
        secondary_specialty_four: str,
        all_secondary_specialties: str,
        group_accepts_medicare_assignment: str,
        clinician_accepts_medicare_assignment: str,
        address_id: str,
    ):
        try:
            parameters = (
                telehealth,
                facility_name,
                group_pac_id,
                number_of_group_members,
                address_line_one,
                address_line_two,
                address_incompletion_marker,
                city,
                state,
                zip_code,
                telephone_number,
                npi,
                primary_specialty,
                secondary_specialty_one,
                secondary_specialty_two,
                secondary_specialty_three,
                secondary_specialty_four,
                all_secondary_specialties,
                group_accepts_medicare_assignment,
                clinician_accepts_medicare_assignment,
                address_id,
            )
            print("[o] Inserting Medical Practice Into DB:")
            print("\tparameters - ", parameters)
            self.connection.execute(
                """INSERT INTO medical_practice (telehealth, 
                    facility_name, 
                    group_pac_id, 
                    number_of_group_members, 
                    address_line_one, 
                    address_line_two, 
                    address_incompletion_marker, 
                    city, 
                    state, 
                    zip_code, 
                    telephone_number, 
                    npi, 
                    primary_specialty,
                    secondary_specialty_one, 
                    secondary_specialty_two,
                    secondary_specialty_three, 
                    secondary_specialty_four, 
                    all_secondary_specialties, 
                    group_accepts_medicare_assignment, 
                    clinician_accepts_medicare_assignment, 
                    address_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                parameters,
            )
            print("[+] Successfully Added a Medical Practice")
        except Exception:
            print(traceback.format_exc())
            print("[-] Failed to Add new Medical Practice")
