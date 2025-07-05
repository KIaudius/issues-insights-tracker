# Architecture Decision Record (ADR)

## 1. Technology Stack Selection

### Context
The Issues & Insights Tracker requires a robust, scalable, and secure technology stack that supports real-time updates, role-based access control, and efficient data processing.

### Decision
We've selected the following technology stack:
- **Frontend**: SvelteKit with SSR and Tailwind CSS
- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL 15+
- **Containerization**: Docker Compose

### Rationale
- **SvelteKit**: Offers excellent performance with minimal bundle size, built-in SSR for SEO and performance, and a reactive programming model that simplifies state management.
- **FastAPI**: Provides high performance, automatic OpenAPI documentation, built-in validation via Pydantic, and native async support for WebSockets and background tasks.
- **PostgreSQL**: Mature, feature-rich database with excellent support for complex queries, transactions, and JSON data types.
- **Docker Compose**: Simplifies deployment and ensures consistency across development and production environments.

### Consequences
- Positive: High developer productivity, excellent performance, comprehensive documentation.
- Negative: Team members need to be familiar with multiple technologies.

## 2. Authentication and Authorization

### Context
The application requires secure authentication and strict role-based access control (RBAC) with three distinct roles: ADMIN, MAINTAINER, and REPORTER.

### Decision
Implement OAuth2 with PKCE flow using JWT tokens for authentication and custom permission dependencies for authorization.

### Rationale
- OAuth2 with PKCE is a secure authentication flow suitable for SPA applications.
- JWT tokens provide a stateless authentication mechanism with built-in expiration.
- Custom permission dependencies allow for fine-grained access control at the API route level.

### Consequences
- Positive: Secure, stateless authentication with clear separation of roles.
- Negative: Need to manage token refresh and secure storage on the client side.

## 3. Real-Time Updates

### Context
The application requires real-time updates for issue changes, comments, and attachments to provide a collaborative experience.

### Decision
Implement WebSockets for real-time communication with a subscription-based model for specific issues.

### Rationale
- WebSockets provide a persistent connection for real-time updates.
- Subscription-based model reduces unnecessary traffic by only sending updates for issues that users are actively viewing.
- FastAPI has built-in support for WebSockets, making implementation straightforward.

### Consequences
- Positive: Real-time updates improve user experience and collaboration.
- Negative: Requires managing WebSocket connections and handling reconnection scenarios.

## 4. Database Schema Design

### Context
The database schema needs to support complex relationships between users, issues, comments, attachments, and statistics.

### Decision
Implement a normalized relational schema with appropriate foreign key constraints and indexes.

### Rationale
- Normalized schema reduces data redundancy and ensures data integrity.
- Foreign key constraints enforce referential integrity.
- Indexes improve query performance for common access patterns.

### Consequences
- Positive: Data integrity, efficient queries for common operations.
- Negative: Complex queries may require joins across multiple tables.

## 5. File Upload and Storage

### Context
The application needs to support secure file uploads and storage for issue attachments.

### Decision
Implement server-side validation of file types and sizes, store files in a structured directory hierarchy, and serve them through a protected endpoint.

### Rationale
- Server-side validation prevents malicious file uploads.
- Structured directory hierarchy (by issue ID) organizes files logically.
- Protected endpoint ensures only authorized users can access files.

### Consequences
- Positive: Secure file storage with proper access control.
- Negative: Need to manage disk space and implement cleanup for deleted issues.

## 6. Background Processing

### Context
The application requires background processing for statistics aggregation and potentially other tasks.

### Decision
Implement APScheduler for scheduled tasks and run it in a separate worker container.

### Rationale
- APScheduler provides a flexible scheduling system with persistent job storage.
- Separate worker container isolates background processing from the web server.

### Consequences
- Positive: Reliable background processing without affecting API performance.
- Negative: Additional container to manage and monitor.

## 7. Testing Strategy

### Context
The application requires comprehensive testing to ensure reliability and correctness.

### Decision
Implement unit tests for backend components with pytest, and E2E tests for frontend with Playwright.

### Rationale
- Unit tests verify individual components in isolation.
- E2E tests verify the complete user flow across frontend and backend.
- Both pytest and Playwright have excellent support for async code and mocking.

### Consequences
- Positive: High test coverage ensures reliability and simplifies refactoring.
- Negative: Maintaining comprehensive test suite requires ongoing effort.

## 8. Containerization Strategy

### Context
The application needs to be easily deployable and scalable.

### Decision
Use Docker Compose with separate services for frontend, backend, worker, and database.

### Rationale
- Separate services allow independent scaling and updates.
- Docker Compose simplifies local development and testing.
- Container-based deployment is supported by most cloud providers.

### Consequences
- Positive: Consistent environment across development and production.
- Negative: Container orchestration adds complexity compared to simpler deployment options.
