# GCP Deployment Architecture

## Overview

This document describes the architecture for deploying the MCP Server on Google Cloud Platform (GCP) using Cloud Run, with security measures like VPC Service Controls and proper ingress/egress rules.

## Components

1. **Cloud Run Services**:
   - `mcp-server`: Main API service
   - `mcp-streamlit`: Web interface
   - `opa-service`: Open Policy Agent

2. **Cloud Storage**:
   - Data buckets for file storage
   - Policy bundles for OPA

3. **Networking**:
   - VPC Network
   - VPC Service Controls perimeter
   - Load Balancer for external access

4. **Security**:
   - Identity and Access Management (IAM)
   - VPC Service Controls
   - Ingress/Egress rules

## Diagram

```
                            ┌─────────────────────┐
                            │   Internet Users    │
                            └──────────┬──────────┘
                                       │
                            ┌──────────▼──────────┐
                            │  Cloud Load Balancer │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
         ┌──────────▼──────────┐    ┌──▼──┐    ┌──────────▼──────────┐
         │   MCP Streamlit     │    │ VPC │    │     MCP Server      │
         │     (Cloud Run)     │    │ SC  │    │      (Cloud Run)    │
         └─────────────────────┘    └──┬──┘    └─────────────────────┘
                                      │
                            ┌─────────▼─────────┐
                            │   OPA Service     │
                            │    (Cloud Run)    │
                            └─────────┬─────────┘
                                      │
                            ┌─────────▼─────────┐
                            │  Policy Bundles   │
                            │  (Cloud Storage)  │
                            └───────────────────┘

                            ┌─────────────────────┐
                            │   Data Storage      │
                            │  (Cloud Storage)    │
                            └─────────────────────┘
```

## Detailed Component Descriptions

### 1. Cloud Run Services

#### MCP Server (API)
- Deployed as a Cloud Run service
- Handles all API requests for CSV/Excel processing and authentication
- Communicates with OPA Service for policy evaluation
- Uses IAM for authentication and authorization

#### MCP Streamlit (Web Interface)
- Deployed as a Cloud Run service
- Provides the user interface for the application
- Communicates with MCP Server API
- Only allows authenticated users with proper roles

#### OPA Service
- Deployed as a Cloud Run service
- Evaluates policies for access control
- Loads policy bundles from Cloud Storage
- Communicates with MCP Server for policy decisions

### 2. Cloud Storage

#### Data Storage Buckets
- Store uploaded CSV/Excel files
- Controlled access via IAM and VPC SC
- Versioned for audit purposes

#### Policy Bundles
- Store OPA policy files
- Mounted to OPA service as read-only
- Version controlled in Git alongside application code

### 3. Networking

#### VPC Network
- Isolated network for all services
- Private service access for internal communication
- Cloud NAT for controlled egress to internet

#### VPC Service Controls (VPC SC)
- Security perimeter to prevent data exfiltration
- Controls access to Cloud Storage buckets
- Limits lateral movement between services

#### Load Balancer
- Single entry point for external traffic
- SSL termination
- Content-based routing to different Cloud Run services

### 4. Security

#### IAM
- Service accounts for each Cloud Run service
- Role-based access control (RBAC) for users
- Principle of least privilege applied to all resources

#### Ingress/Egress Rules
- Ingress: Only allow traffic from Load Balancer
- Egress: Controlled access to GCP services and internet
- VPC Firewall rules for additional security layers

## Data Flow

1. **User Authentication**
   - User accesses Streamlit UI through Load Balancer
   - Streamlit service authenticates user with IAM
   - JWT token generated for session

2. **File Processing**
   - User uploads CSV/Excel file via Streamlit UI
   - Streamlit service forwards request to MCP Server API
   - MCP Server processes file and stores in Cloud Storage
   - Results sent back to user through Streamlit UI

3. **Policy Evaluation**
   - For each request, MCP Server calls OPA Service
   - OPA Service evaluates policies using bundles from Cloud Storage
   - Access decision returned to MCP Server
   - MCP Server enforces decision in response

4. **Data Storage**
   - Files stored in Cloud Storage buckets
   - Protected by VPC SC and IAM policies
   - Versioned for audit trail