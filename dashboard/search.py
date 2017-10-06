from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, String, Nested, Integer
from elasticsearch import Elasticsearch

connections.create_connection(update_all_types=True)


class TaskES(DocType):
    name = String()
    description = Text()
    priority = Integer()
    author_id = Integer()
    marked_done_id = Integer()
    attachments = Nested(properties={'link': String(),
                                     'filename': String()})

    class Meta:
        index = 'tasks'


def index_to_es(task):
    es = Elasticsearch()
    if not es.indices.exists(index='tasks'):
        # create index if it does not exists already
        TaskES.init()
    es_document = TaskES(
            meta={'id': task.id},
            name=task.name,
            description=task.description,
            priority=task.priority,
            author_id=task.author.pk,
            marked_done_id=task.done_user.pk,
            attachments=task.list_documents()
            )
    es_document.save()
