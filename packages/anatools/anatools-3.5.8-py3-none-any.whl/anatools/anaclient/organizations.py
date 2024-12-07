"""
Organization Functions
"""

def get_organization(self):
    """Get organization id of current organization. 
    
    Returns
    -------
    str
        Organization ID of current workspace.
    """
    if self.check_logout(): return
    return self.organization


def set_organization(self, organizationId, workspaceId=None):
    """Set the organization (and optionally a workspace) to the one you wish to work in.
    
    Parameters
    ----------
    organizationId : str
        Organization ID for the organization you wish to work in.
    workspaceId : str
        Workspace ID for the workspace you wish to work in. Uses default workspace if this is not set.
    """
    from anatools.lib.print import print_color
    if self.check_logout(): return
    if not self.user: 
        print_color("Cannot change organization while using API Key", 'ffff00')
        return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    workspaceSet = False
    self.workspaces = self.ana_api.getWorkspaces()
    if len(self.workspaces) == 0: 
        self.workspace = None
        print("No workspaces available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); 
        return
        
    for workspace in self.workspaces:
        if organizationId == workspace['organizationId']:
            if workspaceId is None or workspaceId == workspace['workspaceId']:
                self.workspace = workspace['workspaceId']
                self.organization = workspace['organizationId']
                workspaceSet = True
                break
    if not workspaceSet: raise Exception('Could not find organization or workspace specified.')
    print(f'Organization set to {self.organization}.')
    print(f'Workspace set to {self.workspace}.')
    return


def get_organizations(self, organizationId=None):
    """Shows the organizations the user belongs to and the user's role in that organization.
    
    Returns
    -------
    list[dict]
        Information about the organizations you belong to. 
    """  
    if self.check_logout(): return
    if organizationId is None and self.user is None: organizationId = self.organization
    if organizationId is None:
        self.organizations = self.ana_api.getOrganizations(organizationId)
        return self.organizations
    else:
        organizations = self.ana_api.getOrganizations(organizationId)
        return organizations


def edit_organization(self, name, organizationId=None):
    """Update the organization name. Uses current organization if no organizationId provided.
    
    Parameters
    ----------
    name : str
        Name to update organization to.
    organizationId : str
        Organization Id to update.
    
    Returns
    -------
    bool
        True if organization was edited successfully, False otherwise.
    """  
    if self.check_logout(): return
    if name is None: return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.editOrganization(organizationId, name)


def get_organization_members(self, organizationId=None):
    """Get users of an organization.
    
    Parameters
    ----------
    organizationId : str
        Organization ID. Defaults to current if not specified.
    
    Returns
    -------
    list[dict]
        Information about users of an organization.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getMembers(organizationId=organizationId)

def get_organization_invites(self, organizationId=None):
    """Get invitations of an organization.
    
    Parameters
    ----------
    organizationId : str
        Organization ID. Defaults to current if not specified.
    
    Returns
    -------
    list[dict]
        Information about invitations of an organization.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getInvitations(organizationId=organizationId)


def add_organization_member(self, email, role, organizationId=None):
    """Add a user to an existing organization.
    
    Parameters
    ----------
    email: str
        Email of user to add.
    role : str
        Role for user. 
    organizationId : str
        Organization ID to add members too. Uses current if not specified.
    
    Returns
    -------
    str
        Response status if user got added to workspace succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if role is None: raise ValueError("Role must be provided.")
    if organizationId is None: organizationId = self.organization
    return self.ana_api.addMember(email=email, role=role, organizationId=organizationId, workspaceId=None)


def remove_organization_member(self, email, organizationId=None):
    """Remove a member from an existing organization.
    
    Parameters
    ----------
    email : str
        Member email to remove.
    organizationId: str
        Organization ID to remove member from. Removes from current organization if not specified.
    
    Returns
    -------
    str
        Response status if member got removed from organization succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if organizationId is None: organizationId = self.organization
    return self.ana_api.removeMember(email=email, organizationId=organizationId, workspaceId=None)

def remove_organization_invitation(self, email, organizationId=None, invitationId=None ):
    """Remove a invitation from an existing organization.
    
    Parameters
    ----------
    email : str
        Invitation email to remove.
    organizationId: str
        Organization ID to remove member from. Removes from current organization if not specified.
    invitationId: str
        Invitation ID to remove invitation from. Removes from current organization if not specified.
    
    Returns
    -------
    str
        Response status if member got removed from organization succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if invitationId is None: raise ValueError("No invitation found.")
    if organizationId is None: organizationId = self.organization
    return self.ana_api.removeMember(email=email, organizationId=organizationId, workspaceId=None, invitationId=invitationId)


def edit_organization_member(self, email, role, organizationId=None):
    """Edit a member's role. 
    
    Parameters
    ----------
    email : str
        Member email to edit.
    role: str
        Role to assign. 
    organizationId: str
        Organization ID to remove member from. Edits member in current organization if not specified.
    
    Returns
    -------
    str
        Response if member got edited succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if role is None: raise ValueError("Role must be provided.")
    if organizationId is None: organizationId = self.organization
    return self.ana_api.editMember(email=email, role=role, organizationId=organizationId)
