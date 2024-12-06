from enum import Enum


class InstanceRentedBusinessStatus(str, Enum):
    IN_QUEUE: str = 'IN_QUEUE'
    CREATING: str = 'CREATING'
    ONLINE: str = 'ONLINE'
    TERMINATING: str = 'TERMINATING'
    STOPPED: str = 'STOPPED'
    STOPPING: str = 'STOPPING'
    STARTING: str = 'STARTING'
    REBOOTING: str = 'REBOOTING'
    DELETED: str = 'DELETED'
    RENTAL_ERROR: str = 'RENTAL_ERROR'
    UNKNOWN: str = 'UNKNOWN'
    ALL: str = 'ALL'
