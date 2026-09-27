# Auth Microservice

A production-ready authentication microservice built with FastAPI, featuring JWT token-based authentication, secure password hashing, and persistent database storage.

## Features

- 🔐 JWT token-based authentication
- 🔒 Bcrypt password hashing with passlib
- 💾 Persistent SQLAlchemy database (SQLite by default)
- ✅ Input validation with Pydantic
- 📚 Auto-generated API documentation (Swagger UI)
- 🌍 Environment-based configuration
- 🐳 Docker support

## Prerequisites

- Docker installed (for containerized deployment)
- Python 3.10+ (for local development)

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd auth-microservice
   ```

2. **Create virtual environment**
   ```bash
   cd authenticator
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the service**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
   ```

The API will be available at `http://localhost:8080`

### Docker Deployment

Use the provided setup script:

```bash
./setup.sh
```

This will:
- Build the Docker image as `poc-authenticator`
- Run the container on `localhost:3210`

Or manually:
```bash
docker build . -t auth-microservice
docker run -p 8080:8080 -e SECRET_KEY=your-secret-key auth-microservice
```

## Configuration

Create a `.env` file in the `authenticator/` directory (see `.env.example`):

```env
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./test.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Environment Variables

- `SECRET_KEY`: JWT signing key (⚠️ Change in production!)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)

## API Endpoints

### Authentication

#### Register
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "created_at": "2024-09-27T10:30:00"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Protected Endpoints

#### Get Protected Resource
```http
GET /private
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Hello john_doe",
  "username": "john_doe"
}
```

### Public Endpoints

#### Health Check
```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

#### Free Endpoint
```http
GET /free
```

**Response (200 OK):**
```json
{
  "message": "This is a free endpoint"
}
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

## Database

The service uses SQLAlchemy ORM with SQLite by default. To use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/authdb
```

Or MySQL:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/authdb
```

## Security Notes

⚠️ **Important**: This is a POC implementation. For production:

1. **Change `SECRET_KEY`** - Generate a strong secret and keep it secure
2. **Use HTTPS** - Always use HTTPS in production
3. **Enable CORS properly** - Configure CORS settings based on your requirements
4. **Use environment variables** - Never commit secrets to version control
5. **Database credentials** - Secure your database connection string
6. **Token expiration** - Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` based on your security policy
7. **Rate limiting** - Consider adding rate limiting for authentication endpoints
8. **Input validation** - Current validation is basic; enhance as needed

## Development

### Project Structure
```
authenticator/
├── main.py           # FastAPI application and endpoints
├── auth.py           # Authentication handler (JWT, password hashing)
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic request/response schemas
├── config.py         # Configuration management
├── database.py       # Database setup and session management
├── requirements.txt  # Python dependencies
└── .env.example      # Example environment variables
```

### Testing the API

Using curl:
```bash
# Register
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Login
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Access protected endpoint
curl -H "Authorization: Bearer <token>" http://localhost:8080/private
```

## Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Refresh tokens
- [ ] Role-based access control (RBAC)
- [ ] OAuth2 integration
- [ ] API key authentication
- [ ] Request logging and monitoring
- [ ] Database migrations (Alembic)
- [ ] Comprehensive test suite
- [ ] Rate limiting

## License

MIT

## Support

For issues and questions, please create an issue in the repository.
