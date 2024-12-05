from django.conf import settings

from .identity.factory import IdentityFactory


def get_identity_data(identity_type, identity_number, image=None, user_id=None):
    factory = IdentityFactory()
    if hasattr(settings, 'PYKOLO_DEFAULT_IDENTITY_SERVICE'):
        identity_service = settings.PYKOLO_DEFAULT_IDENTITY_SERVICE
    else:
        identity_service = 'MOCK'
    service = factory.get_service(identity_service)
    match identity_type:
        case 'BVN':
            identity_response = service.lookup_bvn(identity_number)
        case 'NIN':
            identity_response = service.lookup_nin(identity_number)
        case 'BVN_SELFIE':
            identity_response = service.lookup_bvn_with_image(identity_number, image)
        case 'ADVANCED_BVN':
            identity_response = service.lookup_advanced_bvn(identity_number)
        case _:
            identity_response = None

    if identity_response:
        identity_response_data = identity_response.to_dict()
        return identity_response_data

    return None
