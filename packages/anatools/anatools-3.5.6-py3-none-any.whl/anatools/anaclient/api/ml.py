"""
ML API calls.
"""

def getMLArchitectures(self):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMLArchitectures",
            "query": """query 
                getMLArchitectures {
                    getMLArchitectures {
                        architectureId
                        name
                        description
                        annotations
                        hyperparameters {
                            name
                            field
                            type
                            description
                            default
                            min
                            max
                            step
                            options
                        }
                        createdAt
                        createdBy
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getMLArchitectures")


def getMLModels(self, workspaceId, datasetId=None, modelId=None, cursor=None, limit=None):
    if limit is None: limit = 100
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMLModels",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "modelId": modelId,
                "cursor": cursor,
                "limit": limit
            },
            "query": """query 
                getMLModels ($workspaceId: String!, $datasetId: String, $modelId: String, $cursor: String, $limit: Int) {
                    getMLModels (workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId, cursor: $cursor, limit: $limit) {
                        workspaceId
                        modelId
                        datasetId
                        architectureId
                        architecture
                        name
                        description
                        parameters
                        status
                        metrics
                        createdAt
                        createdBy
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getMLModels")


def createMLModel(self, workspaceId, datasetId, architectureId, name, description=None, parameters=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers,
        json = {
            "operationName": "createMLModel",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "architectureId": architectureId,
                "name": name,
                "description": description,
                "parameters": parameters
            },
            "query": """mutation 
                createMLModel ($workspaceId: String!, $datasetId: String!, $architectureId: String!, $name: String, $description: String, $parameters: String) {
                    createMLModel (workspaceId: $workspaceId, datasetId: $datasetId, architectureId: $architectureId, name: $name, description: $description, parameters: $parameters)
                }"""})
    return self.errorhandler(response, "createMLModel")


def deleteMLModel(self, workspaceId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteMLModel",
            "variables": {
                "workspaceId": workspaceId,
                "modelId": modelId,
            },
            "query": """mutation 
                deleteMLModel ($workspaceId: String!, $modelId: String!) {
                    deleteMLModel (workspaceId: $workspaceId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteMLModel")


def editMLModel(self, workspaceId, modelId, name=None, description=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editMLModel",
            "variables": {
                "workspaceId": workspaceId,
                "modelId": modelId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                editMLModel ($workspaceId: String!, $modelId: String!, $name: String, $description: String) {
                    editMLModel (workspaceId: $workspaceId, modelId: $modelId, name: $name, description: $description)
                }"""})
    return self.errorhandler(response, "editMLModel")


def downloadMLModel(self, workspaceId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "downloadMLModel",
            "variables": {
                "workspaceId": workspaceId,
                "modelId": modelId
            },
            "query": """mutation 
                downloadMLModel ($workspaceId: String!, $modelId: String!) {
                    downloadMLModel (workspaceId: $workspaceId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "downloadMLModel")


def uploadMLModel(self, workspaceId, architectureId, name, size, description=None, parameters=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "uploadMLModel",
            "variables": {
                "workspaceId": workspaceId,
                "architectureId": architectureId,
                "name": name,
                "size": size,
                "description": description,
                "parameters": parameters
            },
            "query": """mutation 
                uploadMLModel ($workspaceId: String!, $architectureId: String!, $name: String!, $size: Float!, $description: String, parameters: String) {
                    uploadMLModel (workspaceId: $workspaceId, architectureId: $architectureId, name: $name, size: $size, description: $description, parameters: $parameters) {
                        key
                        modelId
                        uploadId
                        partSize
                        urls
                    }
                }"""})
    return self.errorhandler(response, "uploadMLModel")


def uploadMLModelFinalizer(self, workspaceId, key, uploadId, parts):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "uploadMLModelFinalizer",
            "variables": {
                "workspaceId": workspaceId,
                "key": key,
                "uploadId": uploadId,
                "parts": parts
            },
            "query": """mutation 
                uploadMLModelFinalizer ($workspaceId: String!, $key: String!, $uploadId: String, $parts: [MultipartInput!]) {
                    uploadMLModelFinalizer (workspaceId: $workspaceId, key: $key, uploadId: $uploadId, parts: $parts)
                }"""})
    return self.errorhandler(response, "uploadMLModelFinalizer")



def getMLInferences(self, workspaceId, inferenceId, datasetId=None, modelId=None, cursor=None, limit=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMLInferences",
            "variables": {
                "workspaceId": workspaceId,
                "inferenceId": inferenceId,
                "datasetId": datasetId,
                "modelId": modelId,
                "cursor": cursor,
                "limit": limit
            },
            "query": """query 
                getMLInferences ($workspaceId: String!, $datasetId: String, $modelId: String, $cursor: String, $limit: Int) {
                    getMLInferences (workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId, cursor: $cursor, limit: $limit) {
                        workspaceId
                        inferenceId
                        datasetId
                        dataset
                        modelId
                        model
                        status
                        metrics
                        createdAt
                        createdBy
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getMLInferences")


def getMLInferenceMetrics(self, workspaceId, inferenceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMLInferenceMetrics",
            "variables": {
                "workspaceId": workspaceId,
                "inferenceId": inferenceId
            },
            "query": """query 
                getMLInferenceMetrics ($workspaceId: String!, $inferenceId: String!) {
                    getMLInferenceMetrics (workspaceId: $workspaceId, inferenceId: $inferenceId)
                }"""})
    return self.errorhandler(response, "getMLInferenceMetrics")


def createMLInference(self, workspaceId, datasetId, modelId, mapId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createMLInference",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "modelId": modelId,
                "mapId": mapId
            },
            "query": """mutation 
                createMLInference ($workspaceId: String!, $datasetId: String!, $modelId: String!, $mapId: String) {
                    createMLInference (workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId, mapId: $mapId)
                }"""})
    return self.errorhandler(response, "createMLInference")


def deleteMLInference(self, workspaceId, inferenceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteMLInference",
            "variables": {
                "workspaceId": workspaceId,
                "inferenceId": inferenceId
            },
            "query": """mutation 
                deleteMLInference ($workspaceId: String!, $inferenceId: String!) {
                    deleteMLInference (workspaceId: $workspaceId, inferenceId: $inferenceId)
                }"""})
    return self.errorhandler(response, "deleteMLInference")


def downloadMLInference(self, workspaceId, inferenceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "downloadMLInference",
            "variables": {
                "workspaceId": workspaceId,
                "inferenceId": inferenceId
            },
            "query": """mutation 
                downloadMLInference ($workspaceId: String!, $inferenceId: String!) {
                    downloadMLInference (workspaceId: $workspaceId, inferenceId: $inferenceId)
                }"""})
    return self.errorhandler(response, "downloadMLInference")
