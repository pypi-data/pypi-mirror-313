"""
Inpaint Functions
"""

def get_inpaints(self, volumeId, inpaintId=None):
    """Fetches the inpaint jobs in the volume.
    
    Parameters
    ----------
    volumeId : str
        Volume ID
    inpaintId : str
        Inpaint ID

    Returns
    -------
    dict
        Inpaint jobs info
    """
    if self.check_logout(): return
    cursor = None
    limit = 100
    jobs = []
    response = True
    while response != []:
        response = self.ana_api.getInpaints(volumeId, inpaintId, cursor, limit)
        if len(response): 
            cursor = response[-1]['inpaintId']
            jobs += response
    return jobs


def get_inpaint_logs(self, volumeId, inpaintId):
    """ Fetches the logs for the inpaint job.
    
    Parameters
    ----------
    volumeId : str
        Volume ID
    inpaintId : str
        Inpaint ID

    Returns
    -------
    str
        logs
    """
    if self.check_logout(): return
    return self.ana_api.getInpaintLogs(volumeId=volumeId, inpaintId=inpaintId)


def create_inpaint(self, volumeId, location, files=[], destination=None):
    """Creates an inpaint job.
    
    Parameters
    ----------
    volumeId : str
        Volume ID
    location : str
        Directory location of the input files
    files : list
        List of files to inpaint, leave empty to inpaint all files in directory
    destination : str
        Destination of the inpaint

    Returns
    -------
    str
        Inpaint ID
    """
    if self.check_logout(): return
    return self.ana_api.createInpaint(volumeId=volumeId, location=location, files=files, destination=destination)


def delete_inpaint(self, volumeId, inpaintId):
    """Deletes or cancels an inpaint job.
    
    Parameters
    ----------
    volumeId : str
        Volume ID
    inpaintId : str
        Inpaint ID
    
    Returns
    -------
    bool
        Success / Failure
    """
    if self.check_logout(): return
    return self.ana_api.deleteInpaint(volumeId, inpaintId)
