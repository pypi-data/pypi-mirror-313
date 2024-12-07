"""
Members API calls.
"""

def getMembers(self, organizationId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMembers",
            "variables": {
                "organizationId": organizationId,
            },
            "query": """query 
                getMembers($organizationId: String) {
                    getMembers(organizationId: $organizationId) {
                        organizationId
                        userId
                        email
                        name
                        role
                    }
                }"""})
    return self.errorhandler(response, "getMembers")

def getInvitations(self, organizationId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getInvitations",
            "variables": {
                "organizationId": organizationId,
            },
            "query": """query 
                getInvitations($organizationId: String) {
                    getInvitations(organizationId: $organizationId) {
                        createdAt
                        email
                        organizationId
                        role
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getInvitations")


def addMember(self, email, role=None, organizationId=None, workspaceId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addMember",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "email": email,
                "role": role
            },
            "query": """mutation 
                addMember($organizationId: String, $workspaceId: String, $email: String!, $role: String) {
                    addMember(organizationId: $organizationId, workspaceId: $workspaceId, email: $email, role: $role)
                }"""})
    return self.errorhandler(response, "addMember")


def removeMember(self, email, organizationId=None, workspaceId=None, invitationId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeMember",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "email": email,
                "invitationId":invitationId
            },
            "query": """mutation 
                removeMember($organizationId: String, $workspaceId: String, $email: String!, $invitationId: String) {
                    removeMember(organizationId: $organizationId, workspaceId: $workspaceId, email: $email, invitationId: $invitationId)
                }"""})
    return self.errorhandler(response, "removeMember")


def editMember(self, email, organizationId, role):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editMember",
            "variables": {
                "organizationId": organizationId,
                "email": email,
                "role": role
            },
            "query": """mutation 
                editMember($organizationId: String!, $email: String!, $role: String!) {
                    editMember(organizationId: $organizationId, email: $email, role: $role)
                }"""})
    return self.errorhandler(response, "editMember")
