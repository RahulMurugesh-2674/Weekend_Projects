
# Import TestClient to send HTTP requests to the FastAPI application during testing.
from fastapi.testclient import TestClient

# Import the main module to access and reset the employee list.
from app import main

# Import the FastAPI application that will be tested.
from app.main import app

# Import pytest to use fixtures for test setup and isolation.
import pytest


# Create a test client to interact with the API without starting a server.
client = TestClient(app)


# Test whether the health-check endpoint returns a successful response.
def test_health_check():
    # Send a GET request to the health endpoint.
    response = client.get("/health")

    # Verify that the HTTP status code indicates success.
    assert response.status_code == 200

    # Verify that the response contains the expected health status.
    assert response.json() == {"status": "healthy"}


# Test whether the API retrieves the employee list successfully.
def test_get_employees():
    # Send a GET request to retrieve all employees.
    response = client.get("/employees")

    # Verify that the request was successful.
    assert response.status_code == 200

    # Verify that the response data is a list.
    assert isinstance(response.json(), list)

    # Verify that the list contains at least one employee.
    assert len(response.json()) >= 1


# Test whether a new employee can be created successfully.
def test_create_employees():
    # Send a POST request with the new employee's details.
    response = client.post(
        "/employees",
        json={"id": 5, "name": "David", "department": "BME"}
    )

    # Verify that the employee creation request succeeded.
    assert response.status_code == 200

    # Verify that the response contains the newly created employee's name.
    assert response.json()["name"] == "David"


# Test whether an existing employee can be deleted successfully.
def test_delete_employees():
    # Send a DELETE request to remove the employee with ID 1.
    response = client.delete("/employees/1")

    # Verify that the deletion request succeeded.
    assert response.status_code == 200

    # Verify that the response contains the deleted employee's name.
    assert response.json()["employee"]["name"] == "Arun"


# Test whether an existing employee can be updated successfully.
def test_put_employees():
    # Send a PUT request with the updated details for employee ID 1.
    response = client.put(
        "/employees/1",
        json={"id": 1, "name": "christo", "department": "BME"}
    )

    # Verify that the update request succeeded.
    assert response.status_code == 200

    # Verify that the response contains the expected employee ID.
    assert response.json()["id"] == 1


# Create an automatic fixture that runs before every test.
# This prevents changes made by one test from affecting the next test.
@pytest.fixture(autouse=True)
def reset_employees():
    # Restore the original employee records before each test.
    # Slice assignment updates the existing list instead of creating a new list.
    main.employees[:] = [
        {
            "id": 1,
            "name": "Arun",
            "department": "Testing"
        },
        {
            "id": 2,
            "name": "Priya",
            "department": "DevOps"
        }
    ]
