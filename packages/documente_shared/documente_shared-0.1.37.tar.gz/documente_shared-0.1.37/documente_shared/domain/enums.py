from documente_shared.domain.base_enum import BaseEnum


class DocumentProcessStatus(BaseEnum):
    PENDING = 'PENDING'
    ENQUEUED = 'ENQUEUED'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    DELETED = 'DELETED'
    CANCELLED = 'CANCELLED'


class DocumentProcessCategory(BaseEnum):
    CIRCULAR = 'CIRCULAR'


class DocumentProcessSubCategory(BaseEnum):
    CC_COMBINADA = 'CC_COMBINADA'
    CC_NORMATIVA = 'CC_NORMATIVA'


