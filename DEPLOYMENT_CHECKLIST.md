# Production Deployment Checklist

## Security

- [ ] Generate new SECRET_KEY
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

- [ ] Set DEBUG=False in .env
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set SECURE_SSL_REDIRECT=True
- [ ] Set SECURE_HSTS_SECONDS=31536000
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True

## Database

- [ ] Migrate from SQLite to PostgreSQL (recommended)
- [ ] Configure database backups
- [ ] Test restore process
- [ ] Set up database monitoring

## Media & Static Files

- [ ] Configure media storage (S3, Azure Blob, etc. optional)
- [ ] Set proper permissions on media folder
- [ ] Test static file serving
- [ ] Enable CDN if available

## SSL/HTTPS

- [ ] Obtain SSL certificate (Let's Encrypt recommended)
- [ ] Configure Nginx SSL paths
- [ ] Enable HSTS headers
- [ ] Test certificate renewal process

## Nginx Configuration

- [ ] Update server_name with your domain
- [ ] Configure SSL certificate paths
- [ ] Set proper rate limits
- [ ] Enable compression
- [ ] Add security headers

## Email Configuration

- [ ] Configure email backend (SendGrid, AWS SES, etc.)
- [ ] Set ADMIN_EMAIL
- [ ] Test email sending
- [ ] Configure error notifications

## Environment Variables

- [ ] All sensitive data in .env
- [ ] Never commit secrets
- [ ] Use environment variables for:
  - SECRET_KEY
  - API KEYS (AI providers)
  - Database credentials
  - Email settings
  - AWS/Azure credentials

## Monitoring

- [ ] Set up error tracking (Sentry recommended)
- [ ] Configure logging
- [ ] Set up health checks
- [ ] Monitor disk space
- [ ] Monitor CPU/memory usage

## Backups

- [ ] Daily database backups
- [ ] Test backup restoration
- [ ] Store backups securely
- [ ] Document backup procedure

## Performance

- [ ] Enable caching (Redis optional)
- [ ] Optimize database queries
- [ ] Set up CDN for static files
- [ ] Monitor response times
- [ ] Load test the application

## API Security

- [ ] Add rate limiting
- [ ] Implement API authentication (JWT)
- [ ] Log API requests
- [ ] Monitor for abuse
- [ ] Document API endpoints

## Update & Maintenance

- [ ] Keep Django updated
- [ ] Update dependencies regularly
- [ ] Security patches immediately
- [ ] Test updates in staging first
- [ ] Plan maintenance windows

## Documentation

- [ ] Document deployment process
- [ ] Create runbooks
- [ ] Document scaling strategy
- [ ] Create disaster recovery plan
- [ ] Document API integration

## Testing

- [ ] Test all features in staging
- [ ] Load testing
- [ ] Security testing
- [ ] Cross-browser testing
- [ ] Mobile testing

## Domain & DNS

- [ ] Configure DNS records
- [ ] Test domain resolution
- [ ] Set up email MX records (if email enabled)
- [ ] Configure SPF/DKIM records (if email enabled)

## Monitoring & Alerts

- [ ] Set up uptime monitoring
- [ ] Configure alert notifications
- [ ] Monitor error rates
- [ ] Track performance metrics
- [ ] Review logs regularly

## Sample Production .env

```env
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
DJANGO_SETTINGS_MODULE=rohit_mobile_project.settings
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://user:password@host:5432/dbname

AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIzaSy...
ANTHROPIC_API_KEY=sk-ant-...

SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Deployment Command

```bash
# Build image
docker build -t rohit-mobile:latest .

# Push to registry
docker tag rohit-mobile:latest your-registry/rohit-mobile:latest
docker push your-registry/rohit-mobile:latest

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Health Checks

After deployment, verify:

- [ ] Customer site loads
- [ ] Admin dashboard accessible
- [ ] API endpoints responding
- [ ] Static files loading
- [ ] Media files accessible
- [ ] Database queries working
- [ ] AI detection functional
- [ ] Inventory manager working
- [ ] SSL certificate valid
- [ ] Error logging working

---

**Last Updated**: March 14, 2026
