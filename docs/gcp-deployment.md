# GCP Deployment Guide for MCP Server

## Overview

This guide provides instructions for deploying the Model Context Protocol (MCP) Server application on Google Cloud Platform (GCP) using Cloud Run services.

## Prerequisites

1. Google Cloud SDK installed and configured
2. Docker installed
3. Project created in GCP with billing enabled
4. Required APIs enabled:
   - Cloud Run API
   - Cloud Storage API
   - VPC Service Controls API
   - IAM API

## Deployment Steps

### 1. Set up Environment

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Set region
export REGION="us-central1"

# Authenticate with gcloud
gcloud auth login

# Set project
gcloud config set project $PROJECT_ID
```

### 2. Enable Required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  storage.googleapis.com \
  accesscontextmanager.googleapis.com \
  iam.googleapis.com
```

### 3. Create Cloud Storage Buckets

```bash
# Create bucket for data files
gsutil mb -l $REGION gs://$PROJECT_ID-mcp-data/

# Create bucket for policy bundles
gsutil mb -l $REGION gs://$PROJECT_ID-mcp-policies/
```

### 4. Upload Policy Bundles

```bash
# Copy policies to policy bucket
gsutil cp policies/* gs://$PROJECT_ID-mcp-policies/
```

### 5. Build and Deploy Services

#### Build Docker Images

```bash
# Build MCP Server image
docker build -t gcr.io/$PROJECT_ID/mcp-server .
docker push gcr.io/$PROJECT_ID/mcp-server

# OPA service uses official image, so no build needed
```

#### Deploy to Cloud Run

```bash
# Deploy OPA service
gcloud run deploy opa-service \
  --image openpolicyagent/opa:latest-rootless \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "OPA_URL=http://localhost:8181" \
  --port 8181

# Deploy MCP Server
gcloud run deploy mcp-server \
  --image gcr.io/$PROJECT_ID/mcp-server \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "OPA_URL=https://opa-service-url"
```

### 6. Set up VPC Service Controls

```bash
# Create access policy
gcloud access-context-manager policies create \
  --organization YOUR_ORG_ID \
  --title "MCP Access Policy"

# Create service perimeter
gcloud access-context-manager perimeters create mcp-perimeter \
  --policy ACCESS_POLICY_ID \
  --title "MCP Perimeter" \
  --resources "projects/$PROJECT_ID" \
  --restricted-services "run.googleapis.com","storage.googleapis.com"
```

### 7. Configure IAM Permissions

```bash
# Create service accounts
gcloud iam service-accounts create mcp-server-sa \
  --display-name "MCP Server Service Account"

# Grant permissions to service accounts
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mcp-server-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### 8. Set up Load Balancer (Optional)

```bash
# This is only needed if you want to expose the service publicly
# Create a serverless network endpoint group
gcloud compute network-endpoint-groups create mcp-neg \
  --region=$REGION \
  --network-endpoint-type=serverless \
  --cloud-run-service=mcp-server

# Create load balancer components (backend service, url map, etc.)
# Refer to GCP documentation for complete load balancer setup
```

## Environment Variables

### MCP Server
- `OPA_URL`: URL of the OPA service

## Monitoring and Logging

1. Cloud Run automatically integrates with Cloud Logging
2. Enable Cloud Monitoring for custom metrics
3. Set up alerting policies for critical metrics
4. Use Cloud Trace for distributed tracing

## Security Best Practices

1. Use VPC Service Controls to prevent data exfiltration
2. Implement least privilege IAM policies
3. Enable audit logging for all services
4. Regularly scan container images for vulnerabilities
5. Use Secret Manager for sensitive configuration
6. Implement proper ingress/egress controls

## Scaling Considerations

1. Cloud Run automatically scales based on request volume
2. Configure maximum instances to control costs
3. Use Cloud Storage for unlimited file storage
4. Implement caching for frequently accessed data
5. Monitor resource usage and adjust as needed

## Integration with LLM Applications

To connect LLM applications to your deployed MCP server:

1. For Claude Desktop:
   ```bash
   uv run mcp install src/mcp_server.py
   ```

2. For custom applications:
   - Use the MCP Python client library to connect to your Cloud Run service
   - Handle authentication appropriately (IAM or custom tokens)

## Troubleshooting

1. Check Cloud Logging for error messages
2. Verify service connectivity using curl from Cloud Shell
3. Ensure all required APIs are enabled
4. Check IAM permissions for service accounts
5. Validate VPC Service Controls configuration