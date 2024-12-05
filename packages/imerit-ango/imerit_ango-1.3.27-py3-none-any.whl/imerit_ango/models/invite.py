from typing import List

from imerit_ango.models.enums import ProjectRoles, OrganizationRoles


class Invitation:
    def __init__(self, to: List[str], organizationRole: OrganizationRoles, projectId: str, projectRole: ProjectRoles):
        self.to = to
        self.organizationRole = organizationRole
        self.projectId = projectId
        self.projectRole = projectRole

    def toDict(self):
        return {
            'to': self.to,
            'organizationRole': self.organizationRole.value,
            'projectId': self.projectId,
            'projectRole': self.projectRole.value
        }

class RoleUpdate:
    def __init__(self, email: str, organizationRole: OrganizationRoles):
        self.email = email
        self.organizationRole = organizationRole

    def toDict(self):
        return {
            'email': self.email,
            'organizationRole': self.organizationRole.value
        }

class ProjectMember:
    def __init__(self, email: str, projectRole: ProjectRoles):
        self.email = email
        self.projectRole = projectRole

    def toDict(self):
        return {
            'to': self.email,
            'projectRole': self.projectRole.value
        }