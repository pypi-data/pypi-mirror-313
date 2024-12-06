from typing import Optional, List

from boto3.dynamodb.conditions import Key

from documente_shared.domain.entities.document_process import DocumentProcess
from documente_shared.domain.enums import DocumentProcessStatus
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

    def filter(self, statuses: List[DocumentProcessStatus]) -> List[DocumentProcess]:
        items = []

        for status in statuses:
            response = self._table.query(
                IndexName='status',
                KeyConditionExpression=Key('status').eq(status.value),
            )
            status_items = response.get('Items', [])
            items.extend(status_items)

        return [
            DocumentProcess.from_dict(item)
            for item in items
        ]
