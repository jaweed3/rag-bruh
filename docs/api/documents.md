# GET /documents

List all indexed documents.

## Response

```json
{
  "documents": [
    { "doc_id": "uuid", "title": "Python Programming", "author": "John Smith", "created_at": "..." }
  ]
}
```

# DELETE /documents/{doc_id}

Remove a document and its chunks from Qdrant + PostgreSQL.

## Response

```json
{
  "doc_id": "uuid",
  "status": "deleted"
}
```
