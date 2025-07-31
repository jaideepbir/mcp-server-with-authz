# Advanced policy
package advanced

default allow = false

# Admins can do anything
allow {
    input.user.role == "admin"
}

# Users can read any document
allow {
    input.user.role == "user"
    input.action == "read"
}

# Users can write to documents in their department
allow {
    input.user.role == "user"
    input.action == "write"
    input.user.department == input.document.department
}