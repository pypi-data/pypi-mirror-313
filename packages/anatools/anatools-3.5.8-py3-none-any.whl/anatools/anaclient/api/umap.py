"""
GAN API calls.
"""

def getUMAPs(self, umapId, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getUMAPs",
            "variables": {
                "workspaceId": workspaceId,
                "umapId": umapId,
                "datasetId": datasetId
            },
            "query": """query 
                getUMAPs($workspaceId: String!, $datasetId: String, $umapId: String) {
                    getUMAPs(workspaceId: $workspaceId, datasetId: $datasetId, umapId: $umapId) {
                        umapId
                        workspaceId
                        name
                        datasets {
                            dataset
                            datasetId
                        }
                        samples
                        seed
                        status
                        results
                        createdAt
                        createdBy
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getUMAPs")


def createUMAP(self, datasetIds, samples, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createUMAP",
            "variables": {
                "workspaceId": workspaceId,
                "datasetIds": datasetIds,
                "samples": samples
            },
            "query": """mutation 
                createUMAP($workspaceId: String!, $datasetIds: [String]!, $samples: [Int]!) {
                    createUMAP(workspaceId: $workspaceId, datasetIds: $datasetIds, samples: $samples)
                }"""})
    return self.errorhandler(response, "createUMAP")


def deleteUMAP(self, umapId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteUMAP",
            "variables": {
                "workspaceId": workspaceId,
                "umapId": umapId,
            },
            "query": """mutation 
                deleteUMAP($workspaceId: String!, $umapId: String!) {
                    deleteUMAP(workspaceId: $workspaceId, umapId: $umapId)
                }"""})
    return self.errorhandler(response, "deleteUMAP")

