"""API Module"""

class api:
    
    def __init__(self, url, status_url, headers, verbose=False):
        import requests
        self.url = url
        self.status_url = status_url
        self.headers = headers
        self.verbose = verbose
        self.session = requests.Session()

    def login(self, email, password):
        response = self.session.post(
            url = self.url, 
            json = {
                "operationName": "signIn",
                "variables": {
                    "email": email,
                    "password": password
                },
                "query": """mutation 
                    signIn($email: String!, $password: String!) {
                        signIn(email: $email, password: $password) {
                            uid
                            idtoken
                            expires
                        }
                    }"""})
        if 'errors' in response.json(): return False
        return self.errorhandler(response, "signIn")

    def getSystemNotifications(self):
        response = self.session.post(
            url = self.status_url, 
            json = {
                "operationName": "getSystemNotifications",
                "variables": {},
                "query": """query 
                    getSystemNotifications {
                        getSystemNotifications {
                            message
                            notificationId
                        }
                    }"""})
        if 'errors' in response.json(): return False
        return self.errorhandler(response, "getSystemNotifications")

    def getSystemStatus(self, serviceId=None):
        response = self.session.post(
            url = self.status_url, 
            json = {
                "operationName": "getSystemStatus",
                "variables": {
                    "serviceId": serviceId
                },
                "query": """query 
                    getSystemStatus($serviceId: String) {
                        getSystemStatus(serviceId: $serviceId) {
                            serviceId
                            serviceName
                            description
                            status
                            type
                            updatedAt
                            createdAt
                        }
                    }"""})
        if 'errors' in response.json(): return False
        return self.errorhandler(response, "getSystemStatus")

    def close(self):
        self.session.close()

    from .handlers      import errorhandler
    from .organizations import getOrganizations, editOrganization
    from .channels      import getChannels, getManagedChannels, getChannelDeployment, createManagedChannel, deleteManagedChannel, editManagedChannel, deployManagedChannel, setChannelGraph, getChannelDocumentation, uploadChannelDocumentation
    from .volumes       import getVolumes, getManagedVolumes, createManagedVolume, deleteManagedVolume, editManagedVolume, getVolumeData, putVolumeData, putVolumeDataFinalizer, deleteVolumeData, mountVolumes
    from .members       import getMembers, addMember, removeMember, editMember, getInvitations
    from .workspaces    import getWorkspaces, createWorkspace, deleteWorkspace, editWorkspace
    from .graphs        import getGraphs, createGraph, deleteGraph, editGraph, downloadGraph, getDefaultGraph
    from .datasets      import getDatasets, createDataset, deleteDataset, editDataset, downloadDataset, cancelDataset, datasetUpload, datasetUploadFinalizer, getDatasetRuns, getDatasetLog
    from .analytics     import getAnalytics, getAnalyticsTypes, createAnalytics, deleteAnalytics
    from .annotations   import getAnnotations, getAnnotationFormats, getAnnotationMaps, createAnnotation, downloadAnnotation, deleteAnnotation, getManagedMaps, createManagedMap, editManagedMap, deleteManagedMap, downloadManagedMap
    from .gan           import getGANModels, getGANDatasets, createGANDataset, deleteGANDataset, createManagedGAN, createManagedGANFinalizer, deleteGANModel, getManagedGANs, editManagedGAN, deleteManagedGAN, addGANOrganization, removeGANOrganization, downloadManagedGAN
    from .umap          import getUMAPs, createUMAP, deleteUMAP
    from .api_keys      import getAPIKeys, createAPIKey, deleteAPIKey, getAPIKeyData, getAPIKeyContext
    from .llm           import getLLMResponse, createLLMPrompt, deleteLLMPrompt, getLLMBaseChannels, getLLMChannelNodeTypes
    from .editor        import createRemoteDevelopment, deleteRemoteDevelopment, listRemoteDevelopment, startRemoteDevelopment, stopRemoteDevelopment
    from .ml            import getMLArchitectures, getMLModels, createMLModel, deleteMLModel, editMLModel, downloadMLModel, uploadMLModel, uploadMLModelFinalizer, getMLInferences, getMLInferenceMetrics, createMLInference, deleteMLInference, downloadMLInference
    from .inpaint       import getInpaints, getInpaintLogs, createInpaint, deleteInpaint