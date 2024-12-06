"""
API Keys Functions
"""


def get_api_keys(self):
    """Queries the api keys associated with user's account. This call will return data only when logged in with email/password.
    
    Parameters
    ----------
    
    Returns
    -------
    [dict]
        Names of API keys associated with user's account.
    """
    if self.check_logout(): return
    return self.ana_api.getAPIKeys()


def get_api_key_data(self, name):
    """Returns information about specific api key. This call will return data only when logged in with email/password.
    
    Parameters
    ----------
    name: str
        Name of the API Key. 
    
    Returns
    -------
    [dict]
        Information about API Key
    """
    if self.check_logout(): return
    return self.ana_api.getAPIKeyData(name=name)


def create_api_key(self, name, expires=None, organizationId=None):
    """Creates a new API Key for the user account for the current organization. User will only see this key once, so make sure to save it.
        To use the api key on login, ensure it is set as an environment variable called RENDEREDAI_API_KEY on next use of `anatools` or send it as an init parameter called APIKey.
        This call can only be used when logged in with email/password.
    
    Parameters
    ----------
    name: str
        Name of the API Key. 
    organizationId: str
        Organization ID to set the API Key access at. If no organization is provided, it will use the current context.
    expires : str
        Expiration date to set for the API Key. If none provided, a default expiration a week out will get set. 
        
    Returns
    -------
    str
        API Key in plain-text or failure message about API key creation
    """
    if self.check_logout(): return
    if name is None: return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.createAPIKey(name=name, expires=expires, organizationId=organizationId)

def delete_api_key(self, name):
    """Deletes the API key from user account. This call can only be used when logged in with email/password.
    
    Parameters
    ----------
    name: str
        Name of the API Key to delete.
        
    Returns
    -------
    bool
        Success or failure message about API key deletion
    """
    if self.check_logout(): return
    if name is None: return
    return self.ana_api.deleteAPIKey(name=name)
