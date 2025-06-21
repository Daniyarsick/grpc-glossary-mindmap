# Glossary Service with gRPC and MindMap Frontend

This project implements a glossary service using gRPC and provides a web-based frontend to visualize the terms as a mind map.

The project is fully containerized using Docker, allowing for easy setup and deployment.

## Project Structure

```
.
├── docker-compose.yml
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── glossary_service
│   ├── Dockerfile
│   ├── glossary_pb2.py
│   ├── glossary_pb2_grpc.py
│   ├── requirements.txt
│   └── server.py
└── proto
    └── glossary.proto
```

- **`proto/`**: Contains the Protocol Buffers definition file (`glossary.proto`) for the gRPC service.
- **`glossary_service/`**: Contains the Python backend, including the gRPC server, a Flask REST API gateway, and its Dockerfile.
- **`frontend/`**: Contains the static HTML, CSS, and JavaScript files for the mind map visualization.
- **`docker-compose.yml`**: Defines the services, networks, and volumes for the Docker application.

## How to Run

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running.

### Steps

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Build and run the application using Docker Compose:**
    ```sh
    docker-compose up --build
    ```
    This command will build the Docker image for the glossary service and start the container.

3.  **Access the application:**
    -   **Frontend (MindMap)**: Open your web browser and navigate to [http://localhost:8080](http://localhost:8080).
    -   **gRPC Service**: The gRPC server is available on port `50051`.
    -   **REST API**: The REST API is available under the `/api` path.

## API Endpoints (REST Gateway)

- `GET /api/terms`: Retrieves a list of all glossary terms.
- `GET /api/terms/{term_id}`: Retrieves a single term by its ID.

## Containerization Choices

For this project, **Docker** was chosen as the containerization format. Here's a brief analysis in the context of Russian alternatives:

- **Docker:** It is the de-facto international standard for containerization. It has a vast ecosystem, extensive documentation, and widespread community support. Docker Hub is a massive public registry for images. For most use cases, it's the most straightforward and well-supported choice.

- **Domestic Russian Alternatives:** As of my last update, there aren't any widely adopted, production-ready containerization platforms from Russia that directly compete with Docker's core functionality (like `containerd` and `runc`). While there are Russian cloud platforms that *use* container technology (like Yandex Cloud with its Managed Kubernetes), the underlying container runtime is typically based on the same open-source components as Docker. The value they add is in management, orchestration, and integration into their specific cloud ecosystem.

For a project aimed at quick deployment on an arbitrary platform, sticking to the global standard (Docker) is the most practical choice. It ensures maximum compatibility with hosting providers, CI/CD tools, and developer machines both within and outside of Russia.
