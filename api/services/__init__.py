from .filepress import FilePressService
from .gdtot import GDTOTService

def get_service(service_name):
    services = {
        'filepress': FilePressService(),
        'gdtot': GDTOTService()
    }
    return services.get(service_name) 