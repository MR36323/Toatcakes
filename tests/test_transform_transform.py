from utils.transform_transform import (
    create_dim_staff,
    create_dim_counterparty,
    create_dim_currency,
    create_dim_design,
    create_dim_location,
    create_dim_date,
    create_fact_sales_order,
)
import pandas as pd
import pandas.core.frame
import pytest
import numpy as np


class TestCreateDimStaff:
    @pytest.fixture
    def test_data(scope="function"):
        return (
            [
                {
                    "staff_id": 1,
                    "first_name": "Jeremie",
                    "last_name": "Franey",
                    "department_id": 2,
                    "email_address": "jeremie.franey@terrifictotes.com",
                    "created_at": 1,
                    "last_updated": 1,
                },
                {
                    "staff_id": 2,
                    "first_name": "Deron",
                    "last_name": "Beier",
                    "department_id": 1,
                    "email_address": "deron.beier@terrifictotes.com",
                    "created_at": 2,
                    "last_updated": 1,
                },
            ],
            [
                {
                    "department_id": 1,
                    "department_name": "Sales",
                    "location": "Manchester",
                    "manager": "Richard Roma",
                    "created_at": 2,
                    "last_updated": 2,
                },
                {
                    "department_id": 2,
                    "department_name": "Purchasing",
                    "location": "Manchester",
                    "manager": "Naomi Lapaglia",
                    "created_at": 2,
                    "last_updated": 2,
                },
            ],
        )

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_staff(test_data[0], test_data[1])
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_staff(test_data[0], test_data[1])
        assert set(result_df.columns.values) == {
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        }

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_staff(test_data[0], test_data[1])
        assert type(result_df.loc[0]["staff_id"]) == np.int64
        assert type(result_df.loc[0]["first_name"]) == str
        assert type(result_df.loc[0]["last_name"]) == str
        assert type(result_df.loc[0]["department_name"]) == str
        assert type(result_df.loc[0]["location"]) == str
        assert type(result_df.loc[0]["email_address"]) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_staff(test_data[0], test_data[1])
        row_list_0 = result_df.loc[0, :].values.tolist()
        row_list_1 = result_df.loc[1, :].values.tolist()
        assert row_list_0 == [
            1,
            "Jeremie",
            "Franey",
            "jeremie.franey@terrifictotes.com",
            "Purchasing",
            "Manchester",
        ]
        assert row_list_1 == [
            2,
            "Deron",
            "Beier",
            "deron.beier@terrifictotes.com",
            "Sales",
            "Manchester",
        ]


class TestCreateDimCounterparty:
    @pytest.fixture
    def test_data(scope="function"):
        return (
            [
                {
                    "counterparty_id": 1,
                    "counterparty_legal_name": "Fahey and Sons",
                    "legal_address_id": 15,
                    "commercial_contact": "Micheal Toy",
                    "delivery_contact": "Mrs. Lucy Runolfsdottir",
                    "created_at": 1,
                    "last_updated": 1,
                }
            ],
            [
                {
                    "address_id": 15,
                    "address_line_1": "test_line_1",
                    "address_line_2": "test_line_2",
                    "district": "test_district",
                    "city": "test_city",
                    "postal_code": "test_code",
                    "country": "test_country",
                    "phone": "test_phone",
                    "created_at": 2,
                    "last_updated": 2,
                }
            ],
        )

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_counterparty(test_data[0], test_data[1])
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_counterparty(test_data[0], test_data[1])
        assert set(result_df.columns.values) == {
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        }

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_counterparty(test_data[0], test_data[1])
        assert type(result_df.loc[0]["counterparty_id"]) == np.int64
        assert type(result_df.loc[0]["counterparty_legal_name"]) == str
        assert type(result_df.loc[0]["counterparty_legal_address_line_1"]) == str
        assert type(result_df.loc[0]["counterparty_legal_address_line_2"]) == str
        assert type(result_df.loc[0]["counterparty_legal_district"]) == str
        assert type(result_df.loc[0]["counterparty_legal_city"]) == str
        assert type(result_df.loc[0]["counterparty_legal_postal_code"]) == str
        assert type(result_df.loc[0]["counterparty_legal_country"]) == str
        assert type(result_df.loc[0]["counterparty_legal_phone_number"]) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_counterparty(test_data[0], test_data[1])
        row_list_0 = result_df.loc[0, :].values.tolist()
        assert row_list_0 == [
            1,
            "Fahey and Sons",
            "test_line_1",
            "test_line_2",
            "test_district",
            "test_city",
            "test_code",
            "test_country",
            "test_phone",
        ]


class TestCreateDimCurrency:

    def test_output_is_of_type_dataframe(self):

        test_input = [
            {
                "currency_id": 1,
                "currency_code": "GBP",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "currency_id": 2,
                "currency_code": "USD",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "currency_id": 3,
                "currency_code": "EUR",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
        ]

        response = create_dim_currency(test_input)
        assert isinstance(response, pd.DataFrame)

    def test_correct_clmn_names_are_returned(self):

        test_input = [
            {
                "currency_id": 1,
                "currency_code": "GBP",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "currency_id": 2,
                "currency_code": "USD",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "currency_id": 3,
                "currency_code": "EUR",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
        ]

        response = create_dim_currency(test_input)
        assert list(response.columns) == [
            "currency_id",
            "currency_code",
            "currency_name",
        ]

    def test_handles_currency_name_not_in_dictionary(self):

        test_input = [
            {
                "currency_id": 1,
                "currency_code": "JPY",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "currency_id": 2,
                "currency_code": "EUR",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
        ]

        response = create_dim_currency(test_input)
        print(list(response["currency_name"]))
        assert list(response["currency_name"]) == ["Unknown", "Euro"]


class TestCreateDimDesign:

    @pytest.fixture
    def test_data(scope="function"):
        return [
            {
                "design_id": 8,
                "created_at": 1,
                "design_name": "Wooden",
                "file_location": "/usr",
                "file_name": "wooden-20220717-npgz.json",
                "last_updated": 1,
            },
            {
                "design_id": 51,
                "created_at": 2,
                "design_name": "Bronze",
                "file_location": "/private",
                "file_name": "bronze-20221024-4dds.json",
                "last_updated": 2,
            },
        ]

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_design(test_data)
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_design(test_data)
        assert set(result_df.columns.values) == {
            "design_id",
            "design_name",
            "file_location",
            "file_name",
        }

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_design(test_data)
        assert type(result_df.loc[0]["design_id"]) == np.int64
        assert type(result_df.loc[0]["design_name"]) == str
        assert type(result_df.loc[0]["file_location"]) == str
        assert type(result_df.loc[0]["file_name"]) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_design(test_data)
        row_list_0 = result_df.loc[0, :].values.tolist()
        row_list_1 = result_df.loc[1, :].values.tolist()
        assert row_list_0 == [8, "Wooden", "/usr", "wooden-20220717-npgz.json"]
        assert row_list_1 == [51, "Bronze", "/private", "bronze-20221024-4dds.json"]


class TestCreateDimLocation:
    @pytest.fixture
    def test_data(scope="function"):
        return [
            {
                "address_id": 1,
                "address_line_1": "test_1",
                "address_line_2": "test_2",
                "district": "test_district",
                "city": "test_city",
                "postal_code": "test_code",
                "country": "test_country",
                "phone": "test_number",
                "created_at": 1,
                "last_updated": 1,
            }
        ]

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_location(test_data)
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_location(test_data)
        assert set(result_df.columns.values) == {
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        }

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_location(test_data)
        assert type(result_df.loc[0]["location_id"]) == np.int64
        assert type(result_df.loc[0]["address_line_1"]) == str
        assert type(result_df.loc[0]["address_line_2"]) == str
        assert type(result_df.loc[0]["district"]) == str
        assert type(result_df.loc[0]["city"]) == str
        assert type(result_df.loc[0]["postal_code"]) == str
        assert type(result_df.loc[0]["country"]) == str
        assert type(result_df.loc[0]["phone"]) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_location(test_data)
        row_list_0 = result_df.loc[0, :].values.tolist()
        assert row_list_0 == [
            1,
            "test_1",
            "test_2",
            "test_district",
            "test_city",
            "test_code",
            "test_country",
            "test_number",
        ]


class TestCreateDimDate:

    def test_output_is_of_type_dataframe(self):
        test_input = [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            }
        ]
        response = create_dim_date(test_input)
        assert isinstance(response, pd.DataFrame)

    def test_correct_clmn_names_are_returned(self):
        test_input = [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            }
        ]
        response = create_dim_date(test_input)
        assert list(response.columns) == [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]

    def test_correct_number_of_values(self):
        test_input = [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            }
        ]
        assert len(create_dim_date(test_input)) == 3

    def test_correct_values(self):
        test_input = [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            }
        ]
        expected = pd.DataFrame(
            {
                "date_id": ["2022-11-03", "2022-11-07", "2022-11-08"],
                "year": [2022, 2022, 2022],
                "month": [11, 11, 11],
                "day": [3, 7, 8],
                "day_of_week": [4, 1, 2],
                "day_name": ["Thursday", "Monday", "Tuesday"],
                "month_name": ["November", "November", "November"],
                "quarter": [4, 4, 4],
            }
        )
        pd.testing.assert_frame_equal(create_dim_date(test_input), expected)


class TestCreateFactSalesOrder:
    @pytest.fixture
    def test_data(scope="function"):
        return [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-04 14:20:49.962000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            },
            {
                "sales_order_id": 3,
                "created_at": "2022-12-03 14:20:49.962000",
                "last_updated": "2022-12-04 14:20:49.962000",
                "design_id": 4,
                "staff_id": 10,
                "counterparty_id": 4,
                "units_sold": 65839,
                "unit_price": "2.91",
                "currency_id": 3,
                "agreed_delivery_date": "2022-11-06",
                "agreed_payment_date": "2022-11-07",
                "agreed_delivery_location_id": 19,
            },
        ]

    def test_output_is_of_type_dataframe(self, test_data): ...

    def test_correct_clmn_names(self): ...

    def test_correct_clmn_data_types(self): ...

    def test_correct_data_values(self): ...

    def test_new_sales_record_id_given_new_sales_order_id(self): ...

    def test_new_sales_record_id_given_update_to_record_with_same_sales_order_id(
        self,
    ): ...


class TestLatestGetSalesRecordId:

    def test_gets_latest_record_id_if_already_present(self): ...

    def test_raises_exception_if_record_id_not_already_present(self): ...


class TestUpdateLatestSalesRecordId:

    def test_update_latest_record_id_if_already_present(self): ...

    def test_update_latest_record_id_if_not_already_present(self): ...
