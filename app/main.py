
# Import FastAPI to create the API and HTTPException to return HTTP errors.
from fastapi import FastAPI, HTTPException

# Import BaseModel to validate incoming request data.
from pydantic import BaseModel


# Initialize the FastAPI application.
app = FastAPI(title="Employee Management API")


# Define the structure and data types required for an employee.
# FastAPI uses this model to validate incoming request bodies.
class Employee(BaseModel):
    id: int
    name: str
    department: str


# Temporary in-memory storage for employee records.
# Data will reset when the application restarts.
employees = [
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


# Health-check endpoint to verify that the API is running.
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# GET: Retrieve all employee records.
@app.get("/employees")
def get_employees():
    return employees


# GET: Retrieve one employee using their employee ID.
@app.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: int):

    # Search for an employee whose ID matches the requested ID.
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    # Return HTTP 404 if no matching employee is found.
    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


# POST: Create a new employee record.
@app.post("/employees")
def create_employee(employee: Employee):

    # Convert the validated Pydantic model into a dictionary.
    new_employee = employee.model_dump()

    # Add the new employee to the in-memory list.
    employees.append(new_employee)

    # Return the newly created employee record.
    return new_employee


# PUT: Update an existing employee using their ID.
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: Employee):

    # Enumerate provides both the list index and employee record.
    for index, employee in enumerate(employees):

        # Check whether the current employee matches the requested ID.
        if employee["id"] == employee_id:

            # Replace the existing record with the updated data.
            # The list index is used to update the correct employee.
            employees[index] = updated_employee.model_dump()

            # Return the updated employee record.
            return employees[index]

    # Return HTTP 404 if the employee does not exist.
    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


# DELETE: Remove an employee using their ID.
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    # Enumerate provides the index and employee record.
    for index, employee in enumerate(employees):

        # Find the employee that matches the requested ID.
        if employee["id"] == employee_id:

            # Remove the employee and keep the deleted record.
            deleted_employee = employees.pop(index)

            # Return a confirmation message and the deleted record.
            return {
                "message": "Employee details deleted",
                "employee": deleted_employee
            }

    # Return HTTP 404 if the employee does not exist.
    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
