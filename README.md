# Permission_Graph

Graph:
nodes - representing the different entities. 
edges - representing the relationship between different nodes. 

Task 1 - Build a Permission Graph From Static Data
1. Parse a file containing JSON-formatted lines representing permission policies in GCP.
2. Build a code that represents a graph containing different entities (Identities and Resources) and the links between entities.

Task 2 - Resource hierarchy
Given a Resource, return all the hierarchy of the resource
Input: Resource unique ID
Output: a list of of all the ancestors of the resource (in order starting from the given resource)

Task 3 - Who has what
Given an Identity, return all the resources that identity has permissions on.
Input: Identity unique ID
Output: a list of tuples of all the Resources that the Identity has permissions on.
Each tuple should be as following: (Resource name, Resource type, Role)

Task 4 - What has who
Given a Resource, return all the Identities that have permissions on that resource.
Input: Resource unique ID
Output: a list of tuples of all the Identities that have permissions on the Resource
Each tuple should be as following: (Identity name, Role)

Task 5 - Downloading User Data From Google
Output:
1. Fetch the list of all users in the organization.
2. Fetch the list of all groups in the organization.
3. Fetch the list of users in each group.

Task 6 - Identities Enrichment (Bonus)
Answer previous tasks, but this time don’t stop at the identity level.
1. For user->resource walks, go through groups a user belongs to and are granted with permissions.
2. For resource->user walks, return the list of actual users
