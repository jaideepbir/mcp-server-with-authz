# Attribute-based policy
package attribute_based

default allow = false

# Admins can do anything
allow {
    input.user.role == "admin"
}

# Users can access documents based on clearance level
allow {
    input.user.role == "user"
    input.user.clearance_level >= input.document.classification_level
}

# Special access for users in the same group as the document
allow {
    input.user.role == "user"
    input.user.groups[_] == input.document.group
}