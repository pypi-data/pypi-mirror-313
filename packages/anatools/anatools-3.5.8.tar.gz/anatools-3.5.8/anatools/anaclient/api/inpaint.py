"""
Inpaint API calls.
"""

def getInpaints(self, volumeId, inpaintId=None, cursor=None, limit=None):
    if limit is None: limit = 100
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getInpaints",
            "variables": {
                "volumeId": volumeId,
                "inpaintId": inpaintId,
                "cursor": cursor,
                "limit": limit
            },
            "query": """query 
                getInpaints($volumeId: String!, $inpaintId: String, $cursor: String, $limit: Int) {
                    getInpaints(volumeId: $volumeId, inpaintId: $inpaintId, cursor: $cursor, limit: $limit) {
                    volumeId
                    inpaintId
                    status
                    location
                    destination
                    createdBy
                    createdAt
                    updatedBy
                    updatedAt
                }
            }"""})
    return self.errorhandler(response, "getInpaints")


def getInpaintLogs(self, volumeId, inpaintId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getInpaintLogs",
            "variables": {
                "volumeId": volumeId,
                "inpaintId": inpaintId
            },
            "query": """query 
                getInpaintLogs($volumeId: String!, $inpaintId: String!) {
                    getInpaintLogs(volumeId: $volumeId, inpaintId: $inpaintId) {
                        volumeId
                        inpaintId
                        log
                        state
                    }
                }"""})
    return self.errorhandler(response, "getInpaintLogs")


def createInpaint(self, volumeId, location, files=[], destination=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createInpaint",
            "variables": {
                "volumeId": volumeId,
                "location": location,
                "files": files,
                "destination": destination
            },
            "query": """mutation 
                createInpaint($volumeId: String!, $location: String!, $files: [String], $destination: String) {
                    createInpaint(volumeId: $volumeId, location: $location, files: $files, destination: $destination)
                }"""})
    return self.errorhandler(response, "createInpaint")


def deleteInpaint(self, volumeId, inpaintId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteInpaint",
            "variables": {
                "volumeId": volumeId,
                "inpaintId": inpaintId
            },
            "query": """mutation 
                deleteInpaint($volumeId: String!, $inpaintId: String!) {
                    deleteInpaint(volumeId: $volumeId, inpaintId: $inpaintId)
                }"""})
    return self.errorhandler(response, "deleteInpaint")
