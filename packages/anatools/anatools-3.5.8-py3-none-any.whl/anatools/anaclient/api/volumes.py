"""
Volumes API calls.
"""

def getVolumes(self, organizationId=None, workspaceId=None, volumeId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getVolumes",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "volumeId": volumeId
            },
            "query": """query 
                getVolumes($organizationId: String, $workspaceId: String, $volumeId: String) {
                    getVolumes(organizationId: $organizationId, workspaceId: $workspaceId, volumeId: $volumeId) {
                        volumeId
                        name
                        description
                        organization
                        organizationId
                        permission
                        createdAt
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getVolumes")


def getManagedVolumes(self, organizationId, volumeId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedVolumes",
            "variables": {
                "organizationId": organizationId,
                "volumeId": volumeId
            },
            "query": """query 
                getManagedVolumes($organizationId: String, $volumeId: String) {
                    getManagedVolumes(organizationId: $organizationId, volumeId: $volumeId) {
                        volumeId
                        organizationId
                        name
                        description
                        createdAt
                        updatedAt
                        organizations {
                            organizationId
                            name
                            permission
                        }
                    }
                }"""})
    return self.errorhandler(response, "getManagedVolumes")


def getVolumeData(self, volumeId, keys=[], dir=None, recursive=False, offset=None, limit=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getVolumeData",
            "variables": {
                "volumeId": volumeId,
                "keys": keys,
                "dir": dir,
                "recursive": recursive,
                "offset": offset,
                "limit": limit
            },
            "query": """query 
                getVolumeData($volumeId: String!, $keys: [String], $dir: String, $recursive: Boolean, $limit: Int, $offset: Int) {
                    getVolumeData(volumeId: $volumeId, keys: $keys, dir: $dir, recursive: $recursive, limit: $limit, offset: $offset){
                        keys {
                            key
                            size
                            updatedAt
                            hash
                            url
                        }
                        pageInfo {
                            totalItems
                            offset
                            limit
                        }
                    }
                }"""})
    return self.errorhandler(response, "getVolumeData")


def createManagedVolume(self, organizationId, name, description=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedVolume",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                createManagedVolume($organizationId: String!, $name: String!, $description: String) {
                    createManagedVolume(organizationId: $organizationId, name: $name, description: $description)
                }"""})
    return self.errorhandler(response, "createManagedVolume")


def deleteManagedVolume(self, volumeId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedVolume",
            "variables": {
                "volumeId": volumeId,
            },
            "query": """mutation 
                deleteManagedVolume($volumeId: String!) {
                    deleteManagedVolume(volumeId: $volumeId)
                }"""})
    return self.errorhandler(response, "deleteManagedVolume")


def editManagedVolume(self, volumeId, name=None, description=None, permission=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedVolume",
            "variables": {
                "volumeId": volumeId,
                "name": name,
                "description": description,
                "permission": permission
            },
            "query": """mutation 
                editManagedVolume($volumeId: String!, $name: String, $description: String, $permission: String) {
                    editManagedVolume(volumeId: $volumeId, name: $name, description: $description, permission: $permission)
                }"""})
    return self.errorhandler(response, "editManagedVolume")


def putVolumeData(self, volumeId, key, size):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "putVolumeDataV2",
            "variables": {
                "volumeId": volumeId,
                "key": key,
                "size": size,
            },
            "query": """mutation 
                putVolumeDataV2($volumeId: String!, $key: String!, $size: Float!) {
                    putVolumeDataV2(volumeId: $volumeId, key: $key, size: $size){
                        key
                        uploadId
                        volumeId
                        partSize
                        urls
                    }
                }"""})
    return self.errorhandler(response, "putVolumeDataV2")


def putVolumeDataFinalizer(self, volumeId, uploadId, key, parts):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "putVolumeDataV2Finalizer",
            "variables": {
                "volumeId": volumeId,
                "uploadId": uploadId,
                "key": key,
                "parts": parts,
            },
            "query": """mutation 
                putVolumeDataV2Finalizer($volumeId: String!, $uploadId: String!, $key: String!, $parts: [MultipartInput!]) {
                    putVolumeDataV2Finalizer(volumeId: $volumeId, uploadId: $uploadId, key: $key, parts: $parts)
                }"""})
    return self.errorhandler(response, "putVolumeDataV2Finalizer")


def deleteVolumeData(self, volumeId, keys=[]):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteVolumeData",
            "variables": {
                "volumeId": volumeId,
                "keys": keys
            },
            "query": """mutation 
                deleteVolumeData($volumeId: String!, $keys: [String]!) {
                    deleteVolumeData(volumeId: $volumeId, keys: $keys)
                }"""})
    return self.errorhandler(response, "deleteVolumeData")


def mountVolumes(self, volumes):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "mountVolumes",
            "variables": {
                "volumes": volumes
            },
            "query": """mutation 
                mountVolumes($volumes: [String]!) {
                    mountVolumes(volumes: $volumes){
                        keys
                        rw
                        credentials {
                            accesskeyid
                            accesskey
                            sessiontoken
                        }
                    }
                }"""})
    return self.errorhandler(response, "mountVolumes")