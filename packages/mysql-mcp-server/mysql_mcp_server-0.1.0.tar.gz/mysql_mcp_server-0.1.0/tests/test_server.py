import pytest
import os
from unittest.mock import patch, MagicMock
from mysql.connector import Error
from pydantic import AnyUrl

# Set test environment variables
os.environ.update({
    "MYSQL_HOST": "localhost",
    "MYSQL_USER": "test_user",
    "MYSQL_PASSWORD": "test_password",
    "MYSQL_DATABASE": "test_db"
})

# Import after setting environment variables
from mysql_mcp_server.server import (
    list_resources,
    read_resource,
    list_tools,
    call_tool
)

@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.fetchall.return_value = [("table1",), ("table2",)]
    cursor.description = [("column1",), ("column2",)]
    return cursor

@pytest.fixture
def mock_connection(mock_cursor):
    conn = MagicMock()
    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = mock_cursor
    return conn

@pytest.mark.asyncio
async def test_list_resources(mock_connection):
    with patch('mysql.connector.connect', return_value=mock_connection):
        resources = await list_resources()
        assert len(resources) == 2
        assert resources[0].uri == "mysql://table1/data"
        assert resources[1].uri == "mysql://table2/data"

@pytest.mark.asyncio
async def test_read_resource(mock_connection):
    mock_connection.cursor().__enter__().fetchall.return_value = [
        (1, "data1"),
        (2, "data2")
    ]
    
    with patch('mysql.connector.connect', return_value=mock_connection):
        result = await read_resource(AnyUrl("mysql://test_table/data"))
        assert "column1,column2" in result
        assert "1,data1" in result
        assert "2,data2" in result

@pytest.mark.asyncio
async def test_list_tools():
    tools = await list_tools()
    assert len(tools) == 1
    assert tools[0].name == "execute_sql"
    assert "query" in tools[0].inputSchema["properties"]

@pytest.mark.asyncio
async def test_call_tool_select(mock_connection):
    mock_connection.cursor().__enter__().fetchall.return_value = [
        (1, "test_data")
    ]
    
    with patch('mysql.connector.connect', return_value=mock_connection):
        result = await call_tool("execute_sql", {"query": "SELECT * FROM test_table"})
        assert len(result) == 1
        assert "column1,column2" in result[0].text
        assert "1,test_data" in result[0].text

@pytest.mark.asyncio
async def test_call_tool_show_tables(mock_connection):
    mock_connection.cursor().__enter__().fetchall.return_value = [
        ("table1",),
        ("table2",)
    ]
    
    with patch('mysql.connector.connect', return_value=mock_connection):
        result = await call_tool("execute_sql", {"query": "SHOW TABLES"})
        assert len(result) == 1
        assert "Tables_in_test_db" in result[0].text
        assert "table1" in result[0].text
        assert "table2" in result[0].text

@pytest.mark.asyncio
async def test_call_tool_invalid():
    with pytest.raises(ValueError):
        await call_tool("invalid_tool", {})

@pytest.mark.asyncio
async def test_call_tool_missing_query():
    with pytest.raises(ValueError):
        await call_tool("execute_sql", {})

@pytest.mark.asyncio
async def test_database_error(mock_connection):
    mock_connection.cursor().__enter__().execute.side_effect = Error("Test error")
    
    with patch('mysql.connector.connect', return_value=mock_connection):
        result = await call_tool("execute_sql", {"query": "SELECT * FROM test_table"})
        assert "Error executing query: Test error" in result[0].text