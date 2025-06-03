from utils.transform_transfrom import (
    create_dim_staff, 
    create_dim_counterparty, 
    create_dim_currency, 
    create_dim_design, 
    create_dim_location, 
    create_dim_date, 
    create_fact_sales_order
)


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
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...


class TestCreateDimLocation:
    
    def test_output_is_of_type_dataframe(self):
        ...

    def test_correct_clmn_names(self):
        ...

    def test_correct_clmn_data_types(self):
        ...

    def test_correct_data_values(self):
        ...
    

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