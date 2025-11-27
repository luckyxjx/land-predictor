# API Setup Guide

## Environment Configuration

### 1. Setup Environment File
```bash
make setup-env
# or
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` file with your actual API keys:

#### Real Estate APIs
- **99acres**: Register at https://www.99acres.com/api
- **MagicBricks**: Contact https://www.magicbricks.com/api-access
- **Housing.com**: Apply at https://housing.com/developers

#### Government APIs
- **RERA**: https://rera.gov.in/api-documentation
- **Registrar**: Contact state registrar offices

#### Market Data APIs
- **RBI**: https://api.rbi.org.in/docs
- **NSE**: https://www.nseindia.com/api

### 3. API Rate Limits

| API | Free Tier | Paid Tier |
|-----|-----------|-----------|
| 99acres | 100/hour | 1000/hour |
| MagicBricks | 200/hour | 2000/hour |
| Housing.com | 150/hour | 1500/hour |
| RERA | 50/hour | 500/hour |

### 4. Test Configuration
```bash
make config
```

## API Integration Steps

### Step 1: Get API Keys
1. Register with each service
2. Verify email/phone
3. Apply for API access
4. Wait for approval (1-7 days)
5. Get API keys

### Step 2: Update Configuration
```bash
# Edit .env file
ACRES_99_API_KEY=your_actual_key_here
MAGICBRICKS_API_KEY=your_actual_key_here
```

### Step 3: Test APIs
```bash
make api-test
```

### Step 4: Start Streaming
```bash
make producer  # Uses real API data
```

## Security Best Practices

1. **Never commit .env files**
2. **Use different keys for dev/prod**
3. **Rotate keys regularly**
4. **Monitor API usage**
5. **Set up alerts for quota limits**

## Troubleshooting

### Common Issues

**API Key Invalid**
- Check key format
- Verify account status
- Check API permissions

**Rate Limit Exceeded**
- Reduce request frequency
- Upgrade to paid tier
- Implement better caching

**Connection Timeout**
- Check internet connection
- Verify API endpoint URLs
- Increase timeout values

### Debug Commands
```bash
# Check configuration
make config

# Test individual APIs
python src/data/real_estate_api.py

# Validate data
make validate
```

## Production Deployment

### Environment Variables
```bash
# Production .env
ACRES_99_API_KEY=prod_key_here
MAGICBRICKS_API_KEY=prod_key_here
GLOBAL_RATE_LIMIT=5000
DAILY_REQUEST_LIMIT=50000
```

### Monitoring
- Set up API usage alerts
- Monitor error rates
- Track data quality metrics
- Log all API calls

### Scaling
- Use multiple API keys
- Implement request queuing
- Add caching layers
- Use CDN for static data