# Dockerfile for OPA client
FROM openpolicyagent/opa:latest

# Copy policy files
COPY policies/ /policies/

# Expose port
EXPOSE 8181

# Run OPA server with decision logging
CMD ["run", "--server", "--log-format=json", "--log-level=info", "/policies"]