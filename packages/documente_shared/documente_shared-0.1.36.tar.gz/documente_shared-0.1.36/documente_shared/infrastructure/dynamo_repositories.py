from typing import Optional

from documente_shared.domain.entities.document_process import DocumentProcess
from documente_shared.domain.repositories import DocumentProcessRepository
from documente_shared.infrastructure.dynamo_table import DynamoDBTable



class DynamoDocumentProcessRepository(
    DynamoDBTable,
    DocumentProcessRepository,
):
    def find(self, digest: str) -> Optional[DocumentProcess]:
        item = self.get(key={'digest': digest})
        if item:
            return DocumentProcess.from_dict(item)
        return None

    def persist(self, instance: DocumentProcess) -> DocumentProcess:
        self.put(instance.to_simple_dict)
        return instance

    def remove(self, instance: DocumentProcess):
        self.delete(key={'digest': instance.digest})