from abc import ABC, abstractmethod
from typing import Optional

from documente_shared.domain.entities.document_process import DocumentProcess


class DocumentProcessRepository(ABC):

    @abstractmethod
    def find(self, digest: str) ->Optional[DocumentProcess]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, instance: DocumentProcess) -> DocumentProcess:
        raise NotImplementedError

    @abstractmethod
    def remove(self, instance: DocumentProcess):
        raise NotImplementedError