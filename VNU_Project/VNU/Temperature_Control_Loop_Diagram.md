graph TD
    subgraph Greenhouse Environment
        A[Temperature]
    end

    subgraph Controller Logic
        B(Greenhouse Controller)
        C{Compare Temp vs Optimal Range}
        D[Optimal Range (Setpoint)]
    end

    subgraph Sensing
        E[Temperature Sensor]
    end

    subgraph Actuators
        F[Heater]
        G[Cooling Fan]
    end

    A -- Measured by --> E
    E -- Sends Reading --> C
    D -- Provides Setpoint --> C
    C -- Makes Decision --> B
    
    B -- Temp Too Low --> F
    B -- Temp Too High --> G
    
    F -- Heats --> A
    G -- Cools --> A

    style A fill:#ffadad,stroke:#333,stroke-width:2px
    style B fill:#9cf,stroke:#333,stroke-width:2px
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#cfc,stroke:#333,stroke-width:2px
    style F fill:#f2b5a8,stroke:#333,stroke-width:2px
    style G fill:#a8d8f2,stroke:#333,stroke-width:2px
