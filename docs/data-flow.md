# Data Flow in MCP Server on GCP

## Overview

This document describes the data flow within the MCP Server application when deployed on Google Cloud Platform (GCP).

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              External Users                                │
└─────────────────────────┬───────────────────────────────────────────────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │  Authentication │
                 │                 │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │   Streamlit     │
                 │   Web UI        │
                 │                 │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │   Load Balancer │
                 │                 │
                 └────────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│                │ │             │ │                 │
│  MCP Server    │ │ OPA Service │ │ Cloud Storage   │
│  (Cloud Run)   │ │ (Cloud Run) │ │ (Buckets)       │
│                │ │             │ │                 │
│ ┌────────────┐ │ │ ┌─────────┐ │ │ ┌─────────────┐ │
│ │            │ │ │ │         │ │ │ │             │ │
│ │   Auth     │ │ │ │ Policy  │ │ │ │   Policy    │ │
│ │   Module   │ │ │ │ Engine  │ │ │ │   Bundles   │ │
│ │            │ │ │ │         │ │ │ │             │ │
│ └────────────┘ │ │ └─────────┘ │ │ └─────────────┘ │
│                │ │             │ │                 │
│ ┌────────────┐ │ │             │ │ ┌─────────────┐ │
│ │            │ │ │             │ │ │             │ │
│ │   CSV      │ │ │             │ │ │   Data      │ │
│ │  Reader    │ │ │             │ │ │   Files     │ │
│ │            │ │ │             │ │ │             │ │
│ └────────────┘ │ │             │ │ └─────────────┘ │
│                │ │             │ │                 │
│ ┌────────────┐ │ │             │ │                 │
│ │            │ │ │             │ │                 │
│ │   CSV      │ │ │             │ │                 │
│ │ Analyzer   │ │ │             │ │                 │
│ │            │ │ │             │ │                 │
│ └────────────┘ │ │             │ │                 │
│                │ │             │ │                 │
└────────────────┘ └─────────────┘ └─────────────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │     Audit       │
                 │     Logs        │
                 │                 │
                 └─────────────────┘
```

## Detailed Data Flow

### 1. User Access and Authentication

1. User accesses the application through a browser
2. Request is routed through Cloud Load Balancer
3. Streamlit Web UI service handles the initial request
4. User authenticates with credentials
5. Authentication module in MCP Server validates credentials
6. JWT token is generated and returned to user
7. Token is stored in browser session

### 2. Tool Selection and File Upload

1. Authenticated user selects a tool (CSV Reader, CSV Analyzer, or OPA Evaluator)
2. For CSV tools, user uploads a file or selects a sample
3. Streamlit UI sends file to MCP Server API
4. File is temporarily stored in memory or forwarded directly to processing modules

### 3. CSV/Excel Processing

#### CSV Reader
1. MCP Server receives file from Streamlit UI
2. CSV Reader module parses the file
3. Data is structured and returned to Streamlit UI
4. Streamlit UI displays data in a table format

#### CSV Analyzer
1. MCP Server receives file from Streamlit UI
2. CSV Analyzer module performs statistical analysis
3. Plotly is used to generate visualizations
4. Results and visualizations are returned to Streamlit UI
5. Streamlit UI displays analysis results and charts

### 4. Policy Evaluation (OPA)

1. For each request requiring authorization, MCP Server calls OPA Service
2. Request context and user information are sent to OPA
3. OPA Service evaluates policies using bundles from Cloud Storage
4. Decision (allow/deny) is returned to MCP Server
5. MCP Server enforces the decision

### 5. Data Storage

1. Uploaded files are stored in Cloud Storage buckets
2. Access to buckets is controlled by IAM policies
3. VPC Service Controls prevent unauthorized data exfiltration
4. Files are versioned for audit purposes

### 6. Audit and Logging

1. All requests are logged by Cloud Run services
2. OPA decisions are logged for audit purposes
3. Logs are sent to Cloud Logging
4. Logs are retained for compliance and troubleshooting

## Security Considerations

1. All communication between services is encrypted
2. VPC Service Controls isolate sensitive data
3. IAM policies enforce least privilege access
4. Ingress is limited to Load Balancer only
5. Egress is controlled through Cloud NAT and firewall rules
6. Secrets are managed through Secret Manager
7. Regular security scans are performed on container images

## Scaling Considerations

1. Cloud Run automatically scales based on request volume
2. Cloud Storage provides unlimited storage capacity
3. Load Balancer distributes traffic efficiently
4. VPC allows for private service communication
5. Caching can be implemented for frequently accessed data