# Data Flow in MCP Server on GCP

## Overview

This document describes the data flow within the MCP Server application when deployed on Google Cloud Platform (GCP), following the Model Context Protocol.

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LLM Applications                                     │
│              (Claude Desktop, Custom Apps, etc)                             │
└─────────────────────────┬───────────────────────────────────────────────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │  Authentication │
                 │     (IAM)       │
                 │                 │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │                 │
                 │   MCP Protocol  │
                 │     Server      │
                 │                 │
                 └────────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│                │ │             │ │                 │
│  MCP Tools     │ │ OPA Service │ │ Cloud Storage   │
│  (File Ops,    │ │ (Cloud Run) │ │ (Buckets)       │
│   Policy Eval) │ │             │ │                 │
│                │ │ ┌─────────┐ │ │ ┌─────────────┐ │
│ ┌────────────┐ │ │ │ Policy  │ │ │ │             │ │
│ │            │ │ │ │ Engine  │ │ │ │   Policy    │ │
│ │   CSV      │ │ │ │         │ │ │ │   Bundles   │ │
│ │  Reader    │ │ │ └─────────┘ │ │ │             │ │
│ │            │ │ │             │ │ └─────────────┘ │
│ └────────────┘ │ │             │ │                 │
│                │ │             │ │ ┌─────────────┐ │
│ ┌────────────┐ │ │             │ │ │             │ │
│ │            │ │ │             │ │ │   Data      │ │
│ │   CSV      │ │ │             │ │ │   Files     │ │
│ │ Analyzer   │ │ │             │ │ │             │ │
│ │            │ │ │             │ │ └─────────────┘ │
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

### 1. LLM Application Connection

1. LLM application (e.g., Claude Desktop) connects to MCP Server
2. Connection is authenticated through IAM or custom token system
3. MCP protocol handshake establishes communication channel

### 2. Tool Discovery

1. LLM application requests list of available tools
2. MCP Server responds with tool definitions:
   - CSV/Excel Reader
   - CSV/Excel Analyzer
   - Data Filter
   - Data Sort
   - OPA Policy Evaluator
3. LLM can also access file resources through MCP resource interface

### 3. Tool Usage

#### CSV/Excel Processing
1. LLM requests to use CSV Reader tool with file path parameter
2. MCP Server reads file from Cloud Storage
3. Data is parsed and structured
4. Results are returned to LLM through MCP protocol

#### Data Analysis
1. LLM requests to use CSV Analyzer tool with file path parameter
2. MCP Server performs statistical analysis on the data
3. Results are returned to LLM through MCP protocol

#### Data Manipulation
1. LLM requests to use Filter or Sort tools with parameters
2. MCP Server applies the requested operations
3. Results are returned to LLM through MCP protocol

### 4. Policy Evaluation (OPA)

1. When LLM requests an action that requires authorization, MCP Server calls OPA Service
2. Request context and user information are sent to OPA
3. OPA Service evaluates policies using bundles from Cloud Storage
4. Decision (allow/deny) is returned to MCP Server
5. MCP Server enforces the decision and responds to LLM

### 5. Resource Access

1. LLM can request access to file resources through MCP resource interface
2. MCP Server retrieves file content from Cloud Storage
3. Content is returned to LLM through MCP protocol

### 6. Data Storage

1. Files are stored in Cloud Storage buckets
2. Access to buckets is controlled by IAM policies
3. VPC Service Controls prevent unauthorized data exfiltration
4. Files are versioned for audit purposes

### 7. Audit and Logging

1. All MCP protocol interactions are logged
2. OPA decisions are logged for audit purposes
3. Logs are sent to Cloud Logging
4. Logs are retained for compliance and troubleshooting

## Security Considerations

1. All communication between services is encrypted
2. VPC Service Controls isolate sensitive data
3. IAM policies enforce least privilege access
4. Ingress is limited to authorized LLM applications
5. Egress is controlled through Cloud NAT and firewall rules
6. Secrets are managed through Secret Manager
7. Regular security scans are performed on container images

## Scaling Considerations

1. Cloud Run automatically scales based on request volume
2. Cloud Storage provides unlimited storage capacity
3. Load Balancer distributes traffic efficiently (if used)
4. VPC allows for private service communication
5. Caching can be implemented for frequently accessed data