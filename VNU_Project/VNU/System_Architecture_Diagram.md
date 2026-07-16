graph TD
    subgraph "User Interface (Client-Side)"
        A[Web Browser - HTML/CSS/JS]
        B[Voice Command Interface]
    end

    subgraph "Backend Server (Flask)"
        C[RESTful API Endpoints]
        D[Flask Application - app.py]
    end

    subgraph "Core Logic"
        E[Greenhouse Controller]
    end

    subgraph "Simulated Environment"
        F[Sensors]
        G[Actuators]
        H[ROS Simulation - RX200 Robot]
    end

    A -- HTTP Requests (Fetch API) --> C
    B -- Processes Voice --> A
    
    C -- Calls Functions --> D
    D -- Orchestrates --> E

    E -- Manages State & Logic --> F
    E -- Manages State & Logic --> G
    E -- Manages State & Logic --> H

    F -- Provides Data --> E
    G -- Provides Data --> E
    H -- Provides Data --> E
    
    E -- Returns Status --> D
    D -- Sends JSON Response --> C
    C -- Updates UI --> A

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:2px
    style E fill:#9cf,stroke:#333,stroke-width:2px
    style F fill:#cfc,stroke:#333,stroke-width:2px
    style G fill:#cfc,stroke:#333,stroke-width:2px
    style H fill:#cfc,stroke:#333,stroke-width:2px
