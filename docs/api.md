# MCP Server API Documentation

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

To obtain a token, make a POST request to `/api/auth/login` with a valid authorization header.

## CSV/Excel Reader

### Read File
```
POST /api/csv-reader/read
```

Upload a CSV or Excel file to read its contents.

**Request:**
- Form data with file field containing the file

**Response:**
```json
{
  "data": [...],  // Array of row objects
  "columns": [...],  // Array of column names
  "rows": 0  // Number of rows
}
```

## CSV/Excel Analyzer

### Analyze File
```
POST /api/csv-analyzer/analyze
```

Analyze a CSV or Excel file and get statistical summary.

**Request:**
- Form data with file field containing the file

**Response:**
```json
{
  "summary": {...},  // Statistical summary
  "columns": [...],  // Array of column names
  "rows": 0  // Number of rows
}
```

### Visualize Data
```
POST /api/csv-analyzer/visualize
```

Generate a Plotly visualization from CSV/Excel data.

**Request:**
- Form data with file field containing the file
- Additional form fields:
  - chart_type: bar, line, scatter, or histogram
  - x_column: column name for X-axis
  - y_column: column name for Y-axis (required for bar, line, scatter)

**Response:**
```json
{
  "chart": "...",  // JSON representation of Plotly chart
  "columns": [...]  // Array of column names
}
```

## OPA Client

### List Policies
```
GET /api/opa/policies
```

Get a list of available policies.

**Response:**
```json
{
  "policies": ["simple", "advanced", "attribute_based"]
}
```

### Evaluate Policy
```
POST /api/opa/evaluate
```

Evaluate a policy with input data.

**Request:**
```json
{
  "policy": "simple",  // Policy name
  "input": {...}  // Input data for policy evaluation
}
```

**Response:**
```json
{
  "allowed": true,  // Whether access is allowed
  "policy": "simple",
  "input": {...}
}
```