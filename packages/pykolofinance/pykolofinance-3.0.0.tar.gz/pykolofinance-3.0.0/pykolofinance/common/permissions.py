import logging
from django.conf import settings
from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsSuperAdmin(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Super Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'Super Admin')


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'Admin')


class IsAdminViewOnly(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'Admin View Only')


class IsAgentUser(permissions.BasePermission):
    """Allows access only to agents. """
    message = "Only Agent are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Agent')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsDivisionalHead(permissions.BasePermission):
    """Allows access only to agents. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Divisional Head')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAgentNetworkManager(permissions.BasePermission):
    """Allows access only to Agent Network Manager. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Agent Network Manager')


class IsRegionalHead(permissions.BasePermission):
    """Allows access only to Regional Head. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Regional Head')


class IsRelationshipOfficer(permissions.BasePermission):
    """Allows access only to Relationship Officer. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Relationship Officer')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsMerchant(permissions.BasePermission):
    """Allows access only to Merchant. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Merchant')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperAgent(permissions.BasePermission):
    """Allows access only to Super Agent. """
    message = "Only Divisional Head are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Super Agent')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsHeadOfOperations(permissions.BasePermission):
    """Allows access only to Head of Operations. """
    message = "Only Head of Operations are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Head of Operations')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAccounts(permissions.BasePermission):
    """Allows access only to Accounts. """
    message = "Only Accounts are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Accounts')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsReconciliation(permissions.BasePermission):
    """Allows access only to CSO. """
    message = "Only Reconciliation are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Reconciliation')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsMaComm(permissions.BasePermission):
    """Allows access only to MaComm. """
    message = "Only MaComm are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'MaComm')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsCustomerSupportSupervisor(permissions.BasePermission):
    """Allows access only to Customer Support Supervisor. """
    message = "Only Customer Support Supervisor are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Customer Support Supervisor')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsCustomerSupportOfficer(permissions.BasePermission):
    """Allows access only to Customer Support Officer. """
    message = "Only Customer Support Officer are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Customer Support Officer')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsHeadInternalControl(permissions.BasePermission):
    """Allows access only to Head Internal Control. """
    message = "Only Head Internal Control are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Head Internal Control')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsInternalControlOfficer(permissions.BasePermission):
    """Allows access only to Internal Control Officer. """
    message = "Only Internal Control Officer are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Internal Control Officer')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSafeIPAddress(permissions.BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """

    @staticmethod
    def get_client_ip(request):
        ip_addresses = [request.META.get('REMOTE_ADDR', ''), request.META.get('HTTP_X_FORWARDED_FOR', '')]
        return [addr for addr in ip_addresses if addr]

    def has_permission(self, request, view):

        remote_addresses = self.get_client_ip(request)
        logger.info({'remote_addresses': remote_addresses})
        if not settings.DEBUG:
            return any(element in remote_addresses for element in settings.ATHENA_SAFE_LIST_IPS)
        return True