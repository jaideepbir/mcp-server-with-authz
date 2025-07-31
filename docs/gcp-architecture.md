# GCP Deployment Architecture for MCP Server

## Overview

This document describes the architecture for deploying the Model Context Protocol (MCP) Server on Google Cloud Platform (GCP) using Cloud Run, with security measures like VPC Service Controls and proper ingress/egress rules.

## Components

1. **Cloud Run Services**:
   - `mcp-server`: Main MCP service implementing the Model Context Protocol
   - `opa-service`: Open Policy Agent for policy evaluation

2. **Cloud Storage**:
   - Data buckets for file storage
   - Policy bundles for OPA

3. **Networking**:
   - VPC Network
   - VPC Service Controls perimeter
   - Load Balancer for external access (if needed)

4. **Security**:
   - Identity and Access Management (IAM)
   - VPC Service Controls
   - Ingress/Egress rules

## Diagram

```
                            ┌─────────────────────┐
                            │   LLM Applications  │
                            │   (Claude Desktop,  │
                            │    Custom Apps, etc)│
                            └──────────┬──────────┘
                                       │
                            ┌──────────▼──────────┐
                            │  Cloud Load Balancer │
                            │     (if required)    │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
         ┌──────────▼──────────┐    ┌──▼──┐    ┌──────────▼──────────┐
         │   MCP Server        │    │ VPC │    │     OPA Service     │
         │    (Cloud Run)      │    │ SC  │    │      (Cloud Run)    │
         └─────────────────────┘    └──┬──┘    └─────────────────────┘
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

#### MCP Server
- Deployed as a Cloud Run service
- Implements the Model Context Protocol
- Provides tools for CSV/Excel processing and policy evaluation
- Communicates with OPA Service for policy evaluation
- Uses IAM for authentication and authorization

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
- Optional entry point for external traffic
- SSL termination
- Content-based routing to different Cloud Run services

### 4. Security

#### IAM
- Service accounts for each Cloud Run service
- Role-based access control (RBAC) for users
- Principle of least privilege applied to all resources

#### Ingress/Egress Rules
- Ingress: Controlled access from LLM applications
- Egress: Controlled access to GCP services and internet
- VPC Firewall rules for additional security layers

## Data Flow

1. **LLM Application Connection**
   - LLM application connects to MCP Server through Model Context Protocol
   - Authentication happens through IAM or custom token system

2. **Tool Usage**
   - LLM requests to use a tool (e.g., CSV reader, policy evaluator)
   - MCP Server processes the request
   - Results sent back to LLM through MCP protocol

3. **Policy Evaluation**
   - For requests requiring authorization, MCP Server calls OPA Service
   - OPA Service evaluates policies using bundles from Cloud Storage
   - Access decision returned to MCP Server
   - MCP Server enforces decision in response

4. **Data Storage**
   - Files are stored in Cloud Storage buckets
   - Protected by VPC SC and IAM policies
   - Versioned for audit trail