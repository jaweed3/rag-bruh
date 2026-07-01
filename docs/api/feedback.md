# POST /feedback

Rate a query response for quality monitoring.

## Request

```json
{
  "query_id": "uuid-from-query-response",
  "rating": 4,
  "corrected_response": "optional corrected answer"
}
```

## Response

```json
{
  "status": "received"
}
```

Rating is 1-5. Stored in `queries` table for eval dataset.
