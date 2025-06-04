from utils.transform_transform import (
    create_dim_staff, 
    create_dim_counterparty, 
    create_dim_currency, 
    create_dim_design, 
    create_dim_location, 
    create_dim_date, 
    create_fact_sales_order
)
import json
import pandas as pd


# class TestCreateDimStaff:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...
    
#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...


# class TestCreateDimCounterparty:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...

#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...


class TestCreateDimCurrency:
    
    def test_output_is_of_type_dataframe(self):

        test_input = [{"currency_id": 1, "currency_code": "GBP", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 2, "currency_code": "USD", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 3, "currency_code": "EUR", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}]

        response = create_dim_currency(test_input)
        assert isinstance(response, pd.DataFrame)

    def test_correct_clmn_names_are_returned(self):
        
        test_input = [{"currency_id": 1, "currency_code": "GBP", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 2, "currency_code": "USD", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 3, "currency_code": "EUR", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}]

        response = create_dim_currency(test_input)
        assert list(response.columns) == ['currency_id', 'currency_code', 'currency_name']

    def test_handles_currency_name_not_in_dictionary(self):

        test_input = [{"currency_id": 1, "currency_code": "JPY", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}, {"currency_id": 2, "currency_code": "EUR", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}]

        response = create_dim_currency(test_input)
        print(list(response["currency_name"]))
        assert list(response["currency_name"]) == ["Unknown", "Euro"]


# class TestCreateDimDesign:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...

#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...


# class TestCreateDimLocation:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...

#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...
    

# class TestCreateDimDate:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...

#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...    


# class TestCreateFactSalesOrder:
    
#     def test_output_is_of_type_dataframe(self):
#         ...

#     def test_correct_clmn_names(self):
#         ...

#     def test_correct_clmn_data_types(self):
#         ...

#     def test_correct_data_values(self):
#         ...

#     def test_new_sales_record_id_given_new_sales_order_id(self):
#         ...

#     def test_new_sales_record_id_given_update_to_record_with_same_sales_order_id(self):
#         ...


# class TestLatestGetSalesRecordId:

#     def test_gets_latest_record_id_if_already_present(self):
#         ...

#     def test_raises_exception_if_record_id_not_already_present(self):
#         ...


# class TestUpdateLatestSalesRecordId:

#     def test_update_latest_record_id_if_already_present(self):
#         ...

#     def test_update_latest_record_id_if_not_already_present(self):
#         ...