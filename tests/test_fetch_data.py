from utils.fetch_data import make_connection,close_connection,get_data
from pg8000.exceptions import InterfaceError
from datetime import datetime
import pytest
from unittest.mock import Mock, patch

class TestGetData:
    def test_get_data_fetch_data_for_staff_table(self):
        mock_columns = [
            {'name': 'staff_id'}, {'name': 'first_name'}, {'name': 'last_name'},
            {'name': 'department_id'}, {'name': 'email_address'}, {'name': 'created_at'}, {'name': 'last_updated'}
        ]
        mock_rows = [
            (1, 'Jeremie', 'Franey', 2, 'jeremie.franey@terrifictotes.com',
            datetime(2022, 11, 3, 14, 20, 51, 563000), datetime(2022, 11, 3, 14, 20, 51, 563000)),
            (2, 'Deron', 'Beier', 6, 'deron.beier@terrifictotes.com',
            datetime(2022, 11, 3, 14, 20, 51, 563000), datetime(2022, 11, 3, 14, 20, 51, 563000))
        ]
        mock_conn = Mock()
        mock_conn.columns = mock_columns
        mock_conn.run.return_value = mock_rows
        query = "SELECT * FROM staff"
        result = get_data(mock_conn, query, 'staff')
        
        assert isinstance(result, dict)
        assert 'staff' in result
        assert isinstance(result['staff'], list)
        assert len(result['staff']) == 2
        for row in result['staff']:
            assert isinstance(row, dict)
            assert 'staff_id' in row 
            assert 'first_name' in row
            assert 'last_name' in row 
            assert 'department_id' in row
            assert 'email_address' in row 
            assert 'last_updated' in row
            assert isinstance(row['staff_id'], int)
            assert isinstance(row['first_name'], str)
            assert isinstance(row['last_name'], str)
            assert isinstance(row['department_id'], int)
            assert isinstance(row['email_address'], str)
            assert isinstance(row['created_at'], datetime)
            assert isinstance(row['last_updated'], datetime)

    def test_get_data_run_raises_exception(self):
        pass

class TestMakeConnection:
    @patch("utils.fetch_data.Connection")
    def test_make_connection_returns_a_connection_object(self, mock_connection):
        mock_conn = Mock()
        mock_connection.return_value = mock_conn
        conn = make_connection()
        assert conn is mock_conn
        close_connection(conn)

    @patch("utils.fetch_data.Connection")
    def test_make_connection_raises_exception(self, mock_connection):
        mock_connection.side_effect = Exception("test error")
        conn = make_connection()
        assert conn is None

class TestCloseConnections:
    def test_close_connection_raises_exception(self):
        mock_conn = Mock()
        mock_conn.close.side_effect = Exception("test error")
        with pytest.raises(Exception):
            close_connection(mock_conn)

    def test_close_connection_raises_interface_error(self):
        mock_conn = Mock()
        mock_conn.close.side_effect = InterfaceError("test error")
        with pytest.raises(InterfaceError):
            close_connection(mock_conn)

        
    def test_close_connection_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            close_connection(None)
