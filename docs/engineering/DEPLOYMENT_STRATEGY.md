# DEPLOYMENT_STRATEGY.md

# AQVERA — Deployment Strategy

## Deployment Model (PROPOSED)

Private, self-hosted operation via Docker Compose. Suitable for a solo developer and controlled evaluation. Not a public SaaS initially.

## Deployment Architecture

```
Docker Compose (single host)
├── Frontend container (Next.js)
├── Backend API container (FastAPI)
├── PostgreSQL container (primary database)
├── Redis container (background queue)
├── Worker container (document processing, AI tasks)
└── MinIO container (S3-compatible object storage)
```

## Environment Variables (PROPOSED)

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| REDIS_URL | Redis connection string |
| STORAGE_ENDPOINT | S3-compatible endpoint |
| STORAGE_BUCKET | Bucket name |
| STORAGE_ACCESS_KEY | Access key (encrypted at rest) |
| STORAGE_SECRET_KEY | Secret key (encrypted at rest) |
| AI_PROVIDER__* | AI provider credentials (encrypted) |
| SECRET_KEY | Application secret (session signing, password pepper) |
| ENCRYPTION_KEY | Key for encrypting stored credentials |
| CORS_ORIGINS | Allowed frontend origins |
| LOG_LEVEL | Logging level |
| MAX_FILE_SIZE | Max upload size (bytes) |

## Secret Management (PROPOSED)

- Secrets stored in environment variables or .env (development).
- Production: secret manager or encrypted environment file.
- API keys encrypted at rest in database (`credentials_encrypted`).
- Never commit secrets to version control.

## Scaling Approach

- Vertical scaling (larger single host) first.
- Horizontal scaling only if demonstrated requirement.
- No Kubernetes, no service mesh, no complex eventing.

## Backup Strategy (PROPOSED)

- PostgreSQL: regular `pg_dump` backups.
- Object Storage: versioning or periodic backup.
- Encrypted credentials: backed up with encryption key.

## Rollback

- Database migrations are forward-only for production; rollback scripts kept for development.
- Application version rollback via Docker image tags.

## Health Checks

- Database connectivity.
- Redis connectivity.
- AI provider availability (circuit breaker state).
- Worker queue health.

## Future Public Access Requirements (DEFERRED)

Before opening to external students:
- DDoS protection and WAF.
- Public-facing authentication (OAuth).
- Data residency and regional deployment.
- Penetration test.
- Privacy policy and terms of service.
- Regulatory assessment (do not claim compliance without evidence).
