"""
API Keys calls.
"""

def getAPIKeyContext(self, apiKey):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAPIKeyContext",
            "variables": {
                "apiKey": apiKey
            },
            "query": """query getAPIKeyContext($apiKey: String!) {
                            getAPIKeyContext(apiKey: $apiKey) {
                                createdAt
                                expiresAt
                                name
                                organizationId
                            }

                            }"""})
    return self.errorhandler(response, "getAPIKeyContext")


def getAPIKeys(self):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAPIKeys",
            "query": """query getAPIKeys {
                            getAPIKeys {
                                createdAt
                                expiresAt
                                name
                                organizationId
                            }
                        }"""})
    return self.errorhandler(response, "getAPIKeys")


def createAPIKey(self, name, expires, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createAPIKey",
            "variables": {
                "name": name,
                "organizationId": organizationId,
                "expiresAt": expires
            },
            "query": """mutation createAPIKey($name: String!, $organizationId: String!, $expiresAt: String) {
                            createAPIKey(name: $name, organizationId: $organizationId, expiresAt: $expiresAt)
                        }"""})
    return self.errorhandler(response, "createAPIKey")


def deleteAPIKey(self, name):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteAPIKey",
            "variables": {
                "name": name
            },
            "query": """mutation deleteAPIKey($name: String!) {
                            deleteAPIKey(name: $name)
                        }"""})
    return self.errorhandler(response, "deleteAPIKey")


def getAPIKeyData(self, name):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAPIKeyData",
            "variables": {
                "name": name
            },
            "query": """query getAPIKeyData($name: String!) {
                            getAPIKeyData(name: $name) {
                                createdAt
                                expiresAt
                                name
                                organizationId
                            }
                        }"""})
    return self.errorhandler(response, "getAPIKeyData")
