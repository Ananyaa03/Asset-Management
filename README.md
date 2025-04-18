# Asset-Management
A simple and efficient Asset Management system built with FastAPI and MongoDB, providing CRUD APIs to manage and track company assets.

**Note on the Base Model:** This project currently represents a base model for the Asset Management API. The Pydantic models (`Asset`, `AssetInDB`) and potentially some of the API logic are designed as a starting point. They will be further adapted and refined based on the structure and content of the actual dataset received. Expect updates to the models and potentially the API endpoints to accurately reflect the data.

## Features

* **Create Asset:** Add new asset records to the database.
* **Get Asset by ID:** Retrieve details of a specific asset using its unique ID.
* **Get Employee Assets:** Fetch a list of all assets assigned to a particular employee.
* **Update Asset:** Modify the details of an existing asset.
* **Delete Asset:** Remove an asset record from the database.

## Technologies Used

* **FastAPI:** A modern, high-performance web framework for building APIs with Python.
* **Pydantic:** A data validation and settings management library using Python type hints.
* **Motor:** An asynchronous Python driver for MongoDB.
* **MongoDB:** A NoSQL document database.

## Prerequisites

* Python 3.7+
* pip (Python package installer)
* MongoDB installed and running (default local connection at `mongodb://localhost:27017` is assumed).

## Installation

1.  **Clone the repository** (if you have one, otherwise just proceed to the next step for a new project):
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS and Linux
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file with the following content if it doesn't exist)*:
    ```
    fastapi
    uvicorn
    motor
    pydantic
    bson
    ```

## Configuration

* **MongoDB Connection:** The MongoDB connection URL and database name are defined in the script:
    ```python
    MONGODB_URL = "mongodb://localhost:27017"
    DATABASE_NAME = "asset_management_db"
    ASSET_COLLECTION_NAME = "assets"
    ```
    You can modify these variables in the main Python file (`main.py` or the name of your FastAPI application file) to match your MongoDB setup.

## Running the Application

1.  **Navigate to the project directory** in your terminal.

2.  **Run the FastAPI application using Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    *(Replace `main` with the name of your Python file if it's different, and `app` with the name of your FastAPI application instance)*.

3.  **Access the API documentation:** Once the application is running, you can access the automatically generated interactive API documentation at `http://127.0.0.1:8000/docs` or `http://localhost:8000/docs`.

## API Endpoints

### Create a New Asset

* **Endpoint:** `/assets/`
* **Method:** `POST`
* **Request Body (JSON):**
    ```json
    {
      "employee_id": "EMP001",
      "asset_names": ["Laptop", "Monitor"],
      "asset_id": ["LAP-001", "MON-002"],
      "purchase_date": "2023-01-15",
      "serial_number": "SN12345",
      "condition": "Good"
    }
    ```
* **Response (JSON):** Returns the newly created asset details, including its unique `id` in the database.
    ```json
    {
      "employee_id": "EMP001",
      "asset_names": ["Laptop", "Monitor"],
      "asset_id": ["LAP-001", "MON-002"],
      "purchase_date": "2023-01-15",
      "serial_number": "SN12345",
      "condition": "Good",
      "id": "6440b5e7e7b2b8a7c9d3f0e1"
    }
    ```
* **Status Code:** `201 Created`

### Get Asset by ID

* **Endpoint:** `/assets/{asset_id}`
* **Method:** `GET`
* **Path Parameter:** `asset_id` (the unique ID of the asset in the database)
* **Response (JSON):** Returns the details of the requested asset.
    ```json
    {
      "employee_id": "EMP001",
      "asset_names": ["Laptop", "Monitor"],
      "asset_id": ["LAP-001", "MON-002"],
      "purchase_date": "2023-01-15",
      "serial_number": "SN12345",
      "condition": "Good",
      "id": "6440b5e7e7b2b8a7c9d3f0e1"
    }
    ```
* **Status Codes:**
    * `200 OK`: Asset found.
    * `404 Not Found`: Asset with the given ID does not exist.
    * `400 Bad Request`: Invalid asset ID format.

### Get Assets by Employee ID

* **Endpoint:** `/employees/{employee_id}/assets/`
* **Method:** `GET`
* **Path Parameter:** `employee_id` (the ID of the employee)
* **Response (JSON):** Returns a list of all assets assigned to the specified employee.
    ```json
    [
      {
        "employee_id": "EMP001",
        "asset_names": ["Laptop", "Monitor"],
        "asset_id": ["LAP-001", "MON-002"],
        "purchase_date": "2023-01-15",
        "serial_number": "SN12345",
        "condition": "Good",
        "id": "6440b5e7e7b2b8a7c9d3f0e1"
      },
      {
        "employee_id": "EMP001",
        "asset_names": ["Keyboard"],
        "asset_id": ["KEY-005"],
        "purchase_date": "2023-03-20",
        "serial_number": "SN67890",
        "condition": "Excellent",
        "id": "6440b6a1e7b2b8a7c9d3f0e2"
      }
    ]
    ```
* **Status Code:** `200 OK`

### Update an Existing Asset

* **Endpoint:** `/assets/{asset_id}`
* **Method:** `PUT`
* **Path Parameter:** `asset_id` (the unique ID of the asset to update)
* **Request Body (JSON):** The fields to update. Only the provided fields will be modified.
    ```json
    {
      "condition": "Fair"
    }
    ```
* **Response (JSON):** Returns the updated asset details.
    ```json
    {
      "employee_id": "EMP001",
      "asset_names": ["Laptop", "Monitor"],
      "asset_id": ["LAP-001", "MON-002"],
      "purchase_date": "2023-01-15",
      "serial_number": "SN12345",
      "condition": "Fair",
      "id": "6440b5e7e7b2b8a7c9d3f0e1"
    }
    ```
* **Status Codes:**
    * `200 OK`: Asset updated successfully.
    * `404 Not Found`: Asset with the given ID does not exist.
    * `400 Bad Request`: Invalid asset ID format or no fields to update.

### Delete an Asset

* **Endpoint:** `/assets/{asset_id}`
* **Method:** `DELETE`
* **Path Parameter:** `asset_id` (the unique ID of the asset to delete)
* **Response (JSON):**
    ```json
    {
      "message": "Asset deleted successfully"
    }
    ```
* **Status Codes:**
    * `200 OK`: Asset deleted successfully.
    * `404 Not Found`: Asset with the given ID does not exist.
    * `400 Bad Request`: Invalid asset ID format.

## Contributing

Contributions are welcome! Please feel free to submit pull requests with bug fixes, new features, or improvements.
