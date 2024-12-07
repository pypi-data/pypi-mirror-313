"""
GAN Functions
"""
import os
from anatools.anaclient.helpers import multipart_upload_file
from anatools.lib.download import download_file

def get_gan_models(self, organizationId=None, workspaceId=None, modelId=None):
    """Retrieve information about GAN models
    
    Parameters
    ----------
    organizationId : str
        Organization ID that owns the models
    workspaceId : str
        Workspace ID that contains the models
    modelId : str
        Model ID to retrieve information for. 
    
    Returns
    -------
    list[dict]
        GAN Model information.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANModels(organizationId=organizationId, workspaceId=workspaceId, modelId=modelId)
    

def get_gan_datasets(self, datasetId=None, gandatasetId=None, workspaceId=None):
    """Retrieve information about GAN dataset jobs.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to retrieve information for. 
    gandatasetId : str
        Gan dataset ID to retrieve.
    workspaceId : str
        Workspace ID where the dataset exists.

    Returns
    -------
    list[dict]
        Information about the GAN Dataset.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANDatasets(workspaceId=workspaceId, datasetId=datasetId, gandatasetId=gandatasetId)


def create_gan_dataset(self, modelId, datasetId, workspaceId=None):
    """Create a new GAN dataset based off an existing dataset. This will start a new job.
    
    Parameters
    ----------
    modelId : str
        Model ID to use for the GAN.
    datasetId : str
        Dataset ID to input into the GAN. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    str
        The datsetId for the GAN Dataset job.
    """
    if self.check_logout(): return
    if modelId is None: raise ValueError("ModelId must be provided.")
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createGANDataset(workspaceId=workspaceId, datasetId=datasetId, modelId=modelId)


def delete_gan_dataset(self, datasetId, workspaceId=None):
    """Deletes a GAN dataset job.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID for the GAN dataset. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    bool
        Returns true if the GAN dataset was successfully deleted.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteGANDataset(workspaceId=workspaceId, datasetId=datasetId)


def create_managed_gan(self, name, description, modelfile, flags=None, organizationId=None):
    """Uploades a GAN model to the microservice. The model will be owned by the specified organization.
    If organizationId is not given the model will be owned by that of the analcient.
    
    Parameters
    ----------
    name : str
        A name for model.
    description : str
        Details about the model.
    modelfile : str
        The file of the model - relative to the local directry.
    flags : str
        Parameters for use when running the model.
    organizationId : str
        Id of organization that owns the model, that of the anaclient if not given.
    
    Returns
    -------
    modleId : str
        The unique identifier for this model.
    """
    if self.check_logout(): return
    if modelfile is None: raise ValueError("Filename must be defined.")
    if description is None: description = ''
    if organizationId is None: organizationId = self.organization
    if not os.path.exists(modelfile): raise Exception(f'Could not find file: {modelfile}')
    self.refresh_token()

    filesize = os.path.getsize(modelfile)
    fileinfo = self.ana_api.createManagedGAN(organizationId=organizationId, name=name, size=filesize, description=description, flags=flags)
    modelId = fileinfo['modelId']

    parts = multipart_upload_file(modelfile, fileinfo["partSize"], fileinfo["urls"], f"Uploading gan model {modelfile}")
    self.refresh_token()
    finalize_success = self.ana_api.createManagedGANFinalizer(organizationId, fileinfo['uploadId'], fileinfo['key'], parts)
    if not finalize_success:
        raise Exception(f"Failed to upload dataset {modelfile}.")
    else:
        print(f"\x1b[1K\rUpload completed successfully!", flush=True)
        return modelId


def delete_gan_model(self, modelId):
    """Delete the GAN model and remove access to it from all shared organizations.
    This can only be done by a user in the organization that owns the model.
    
    Parameters
    ----------
    modelId : str
        The ID of a specific GAN model.
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.deleteGANModel(modelId=modelId)

def get_managed_gans(self, organizationId=None, modelId=None):
    """Retrieves the managed GANs for an organization.
    
    Parameters
    ----------
    organizationId : str
        The ID of the organization that the managed GAN belongs to.
    modelId : str
        The ID of a specific model.

    Returns
    -------
    list[dict]
        Model Info
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getManagedGANs(organizationId=organizationId, modelId=modelId)

def edit_managed_gan(self, modelId, name=None, description=None, flags=None):
    """Edits the name, description, and flags of a managed gan.
    
    Parameters
    ----------
    modelId: str
        The modelId that will be updated.
    name : str
        The new name of the managed gan. Note: this name needs to be unique per organization.
    description : str
        Description of the managed gan
    flags : str
        Flags for the model
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    if name is None and description is None and flags is None: return
    return self.ana_api.editManagedGAN(modelId=modelId, name=name, description=description, flags=flags)

def delete_managed_gan(self, modelId):
    """Removes the managed map
    
    Parameters
    ----------
    modelId : str
        The ID of a specific Model to delete.
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.deleteManagedGAN(modelId=modelId)


def download_managed_gan(self, modelId, localDir=None):
    """Download the managed gan model file from your organization.
    
    Parameters
    ----------
    modelId : str
       ModelId to download.
    localDir : str
        Path for where to download the gan model. If none is provided, current working directory will be used.
    
    Returns
    -------
    str
        The name of the managed gan model that got downloaded.
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('modelId must be specified.')
    if localDir is None: localDir = os.getcwd()

    url = self.ana_api.downloadManagedGAN(modelId=modelId)
    fname = url.split('?')[0].split('/')[-1]
    return download_file(url=url, fname=fname, localDir=localDir) 