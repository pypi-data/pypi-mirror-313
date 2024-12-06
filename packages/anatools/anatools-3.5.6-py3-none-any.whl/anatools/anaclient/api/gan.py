"""
GAN API calls.
"""

def getGANModels(self, organizationId, workspaceId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANModels",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "modelId": modelId
            },
            "query": """query 
                getGANModels($organizationId: String, $workspaceId: String, $modelId: String) {
                    getGANModels(organizationId: $organizationId, workspaceId: $workspaceId, modelId: $modelId){
                        modelId
                        name
                        description
                    }
                }"""})
    return self.errorhandler(response, "getGANModels")


def getGANDatasets(self, datasetId, workspaceId, gandatasetId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANDatasets",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "gandatasetId": gandatasetId
            },
            "query": """query 
                getGANDatasets$workspaceId: String!, $datasetId: String, $gandatasetId: String) {
                    getGANDatasets(workspaceId: $workspaceId, datasetId: $datasetId, gandatasetId: $gandatasetId) {
                        createdAt
                        createdBy
                        datasetId
                        description
                        model
                        modelId
                        name
                        parentId
                        status
                        updatedAt
                        updatedBy
                        workspaceId
                    }
                }"""})
    return self.errorhandler(response, "getGANDatasets")


def createGANDataset(self, modelId, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "modelId": modelId,
            },
            "query": """mutation 
                createGANDataset($workspaceId: String!, $datasetId: String!, $modelId: String!) {
                    createGANDataset(workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "createGANDataset")


def deleteGANDataset(self, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId
            },
            "query": """mutation 
                deleteGANDataset($workspaceId: String!, $datasetId: String!) {
                    deleteGANDataset(workspaceId: $workspaceId, datasetId: $datasetId)
                }"""})
    return self.errorhandler(response, "deleteGANDataset")


def createManagedGAN(self, organizationId, name, size, description, flags):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedGANV2",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "size": size,
                "description": description,
                "flags": flags,
            },
            "query": """mutation 
                createManagedGANV2($organizationId: String!, $name: String!, $size: Float!, $description: String!, $flags: String) {
                    createManagedGANV2(organizationId: $organizationId, name: $name, size: $size, description: $description, flags: $flags){
                        key
                        uploadId
                        modelId
                        partSize
                        urls
                    }
                }"""})
    return self.errorhandler(response, "createManagedGANV2")

def createManagedGANFinalizer(self, organizationId, uploadId, key, parts):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedGANV2Finalizer",
            "variables": {
                "organizationId": organizationId,
                "uploadId": uploadId,
                "key": key,
                "parts": parts,
            },
            "query": """mutation 
                createManagedGANV2Finalizer($organizationId: String!, $uploadId: String!, $key: String!, $parts: [MultipartInput!]) {
                    createManagedGANV2Finalizer(organizationId: $organizationId, uploadId: $uploadId, key: $key, parts: $parts)
                }"""})
    return self.errorhandler(response, "createManagedGANV2Finalizer")


def deleteGANModel(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANModel",
            "variables": {
                "modelId": modelId,
            },
            "query": """mutation 
                deleteGANModel($modelId: String!) {
                    deleteGANModel(modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteGANModel")


def getManagedGANs(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedGANs",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """query 
                getManagedGANs($organizationId: String!, $modelId: String) {
                    getManagedGANs(organizationId: $organizationId, modelId: $modelId) {
                        createdAt
                        createdBy
                        description
                        modelId
                        name
                        organizationId
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getManagedGANs")

def editManagedGAN(self, modelId, name=None, description=None, flags=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedGAN",
            "variables": {
                "modelId": modelId,
                "name": name,
                "description": description,
                "flags": flags
            },
            "query": """mutation 
                editManagedGAN($modelId: String!, $name: String, $description: String, $flags: String) {
                    editManagedGAN(modelId: $modelId, name: $name, description: $description, flags: $flags)
                }"""})
    return self.errorhandler(response, "editManagedGAN")

def deleteManagedGAN(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedGAN",
            "variables": {
                "modelId": modelId,
            },
            "query": """mutation 
                deleteManagedGAN($modelId: String!) {
                    deleteManagedGAN(modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteManagedGAN")

def addGANOrganization(self, modelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addGANOrganization",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """mutation 
                addGANOrganization($organizationId: String!, $modelId: String!) {
                    addGANOrganization(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "addGANOrganization")


def removeGANOrganization(self, modelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeGANOrganization",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """mutation 
                removeGANOrganization($organizationId: String!, $modelId: String!) {
                    removeGANOrganization(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "removeGANOrganization")


def downloadManagedGAN(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "downloadManagedGAN",
            "variables": {
                "modelId": modelId
            },
            "query": """mutation 
                downloadManagedGAN($modelId: String!) {
                    downloadManagedGAN(modelId: $modelId) 
                }"""})
    return self.errorhandler(response, "downloadManagedGAN")
