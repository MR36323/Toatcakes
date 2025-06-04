from utils.transform_transform import (
    create_dim_staff, 
    create_dim_counterparty, 
    create_dim_currency, 
    create_dim_design, 
    create_dim_location, 
    create_dim_date, 
    create_fact_sales_order
)
import pandas as pd
import pandas.core.frame
import datetime
import pytest
import numpy as np


class TestCreateDimStaff:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...
    
    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...


class TestCreateDimCounterparty:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...


class TestCreateDimCurrency:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...


class TestCreateDimDesign:
    @pytest.fixture
    def test_data(scope='function'):
        return [{'design_id': 8, 'created_at': datetime.datetime(2022, 11, 3, 14, 20, 49, 962000), 'design_name': 'Wooden', 'file_location': '/usr', 'file_name': 'wooden-20220717-npgz.json', 'last_updated': datetime.datetime(2022, 11, 3, 14, 20, 49, 962000)}, {'design_id': 51, 'created_at': datetime.datetime(2023, 1, 12, 18, 50, 9, 935000), 'design_name': 'Bronze', 'file_location': '/private', 'file_name': 'bronze-20221024-4dds.json', 'last_updated': datetime.datetime(2023, 1, 12, 18, 50, 9, 935000)}]

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_design(test_data)
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_design(test_data)
        assert list(result_df.columns.values) == ['design_id', 'design_name', 'file_location', 'file_name']

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_design(test_data)
        assert type(result_df.loc[0]['design_id']) == np.int64
        assert type(result_df.loc[0]['design_name']) == str
        assert type(result_df.loc[0]['file_location']) == str
        assert type(result_df.loc[0]['file_name']) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_design(test_data)
        row_list_0 = result_df.loc[0, :].values.tolist()
        row_list_1 = result_df.loc[1, :].values.tolist()
        assert row_list_0 == [8, 'Wooden', '/usr', 'wooden-20220717-npgz.json']
        assert row_list_1 == [51, 'Bronze', '/private', 'bronze-20221024-4dds.json']


class TestCreateDimLocation:
    @pytest.fixture
    def test_data(scope='function'):
        return [{'address_id': 1, 'address_line_1':'test_1', 'address_line_2': 'test_2', 'district': 'test_district', 'city': 'test_city', 'postal_code': 'test_code', 'country': 'test_country', 'phone': 'test_number', 'created_at': datetime.datetime(2022, 11, 3, 14, 20, 49, 962000), 'last_updated': datetime.datetime(2022, 11, 4, 14, 20, 49, 962000)}]

    def test_output_is_of_type_dataframe(self, test_data):
        result_df = create_dim_location(test_data)
        assert type(result_df) == pandas.core.frame.DataFrame

    def test_correct_clmn_names(self, test_data):
        result_df = create_dim_location(test_data)
        assert list(result_df.columns.values) == ['location_id', 'address_line_1', 'address_line_2', 'district', 'city', 'postal_code', 'country', 'phone']

    def test_correct_clmn_data_types(self, test_data):
        result_df = create_dim_location(test_data)
        assert type(result_df.loc[0]['location_id']) == np.int64
        assert type(result_df.loc[0]['address_line_1']) == str
        assert type(result_df.loc[0]['address_line_2']) == str
        assert type(result_df.loc[0]['district']) == str
        assert type(result_df.loc[0]['city']) == str
        assert type(result_df.loc[0]['postal_code']) == str
        assert type(result_df.loc[0]['country']) == str
        assert type(result_df.loc[0]['phone']) == str

    def test_correct_data_values(self, test_data):
        result_df = create_dim_location(test_data)
        row_list_0 = result_df.loc[0, :].values.tolist()
        assert row_list_0 == [1, 'test_1', 'test_2', 'test_district', 'test_city', 'test_code','test_country', 'test_number']

    

class TestCreateDimDate:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...    


class TestCreateFactSalesOrder:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...

    def test_new_sales_record_id_given_new_sales_order_id(self):
        ...

    def test_new_sales_record_id_given_update_to_record_with_same_sales_order_id(self):
        ...


class TestLatestGetSalesRecordId:

    def test_gets_latest_record_id_if_already_present(self):
        ...

    def test_raises_exception_if_record_id_not_already_present(self):
        ...


class TestUpdateLatestSalesRecordId:

    def test_update_latest_record_id_if_already_present(self):
        ...

    def test_update_latest_record_id_if_not_already_present(self):
        ...