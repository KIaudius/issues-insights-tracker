# Issues & Insights Tracker

A full-stack application for tracking issues and insights with role-based access control, real-time updates, and analytics.

## Features

- **Multi-Role Authentication**: ADMIN, MAINTAINER, and REPORTER roles with different permissions
- **Issue Management**: Create, read, update, delete issues with workflow states
- **Real-Time Updates**: WebSocket integration for live updates
- **File Attachments**: Secure file upload and storage
- **Comments**: Discussion threads on issues
- **Dashboard**: Analytics and statistics visualization
- **Background Jobs**: Automated statistics aggregation
- **API Documentation**: Auto-generated Swagger UI
- **Comprehensive Testing**: Backend unit tests and E2E tests

## Bonus Features

- **PDF/Image Preview**: Preview uploaded documents and images
- **Dark Mode**: Toggle between light and dark themes
- **Advanced Validation**: Robust input validation using Pydantic v2

## Tech Stack

### Frontend
- **SvelteKit**: SSR-enabled frontend framework
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts for the dashboard
- **PDF.js**: PDF rendering in the browser

### Backend
- **FastAPI**: High-performance Python API framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **APScheduler**: Task scheduling for background jobs
- **WebSockets**: Real-time communication

### Database
- **PostgreSQL 15+**: Relational database

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **API Layer**: FastAPI routes and endpoints
- **Service Layer**: Business logic and validation
- **Data Access Layer**: Database models and CRUD operations
- **Schema Layer**: Pydantic models for validation and serialization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/issues-insights-tracker.git
   cd issues-insights-tracker
   ```

2. Create a `.env` file with the required environment variables (see `.env.example`).

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/api/docs

## Development

### Backend Development

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload

# Run tests
pytest backend/tests
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

API documentation is available at `/api/docs` when the application is running. It provides a comprehensive overview of all available endpoints, request/response schemas, and authentication requirements.

## Testing

### Backend Tests

```bash
pytest backend/tests
```

### E2E Tests

```bash
cd frontend
npm run test:e2e
```

## Deployment

The application is containerized and can be deployed to any platform that supports Docker.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SvelteKit](https://kit.svelte.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [PostgreSQL](https://www.postgresql.org/)
