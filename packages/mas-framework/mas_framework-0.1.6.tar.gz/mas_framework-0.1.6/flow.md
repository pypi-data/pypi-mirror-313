```mermaid
graph TD
    subgraph "Core System"
        D[Discovery Service]
        T[Transport Service]
        R[Registry]
    end

    subgraph "Message Flow Patterns"
        %% Core -> Agent -> Core Pattern
        C1[Core System] -->|1. Command/Request| A1[Agent A]
        A1 -->|2. Response/Ack| C1
        
        %% Agent -> Core -> Agent Pattern
        A2[Agent B] -->|1. Request| C2[Core System]
        C2 -->|2. Response/Ack| A2
        
        %% Agent <-> Agent Pattern
        A3[Agent C] -->|1. Direct Message| A4[Agent D]
        A4 -.->|2. Optional Response| A3
    end

    subgraph "Message Processing"
        T -->|Validate Message| V[Message Validation]
        V -->|Check Recipient| R
        V -->|Deduplicate| DD[Deduplication Layer]
        DD -->|Route Message| RT[Message Router]
        RT -->|Deliver| RCP[Recipient]
    end

    subgraph "State Management"
        R -->|Track Agent Status| ST[Status Tracker]
        ST -->|Update Last Seen| LS[Last Seen]
        ST -->|Monitor Health| H[Health Check]
    end

    subgraph "Error Handling"
        E[Error Handler]
        RT -->|Failed Delivery| E
        V -->|Invalid Message| E
        DD -->|Duplicate Detected| E
        E -->|Notify Sender| NS[Sender]
    end

    %% Message Flow Rules
    classDef rule fill:#f9f,stroke:#333,stroke-width:2px
    class MFR rule

    %% Message Types & Validation Rules
    1. Each message must have:
       - Unique ID
       - Timestamp
       - Sender ID
       - Target ID
       - Message Type
       - Payload

    2. Message Routing Rules:
       - Discovery Service only processes registration and discovery requests
       - Transport Service handles all message routing
       - Registry maintains agent state and validates recipients
       - Messages are deduplicated based on Message ID and timestamp

    3. State Management:
       - Agents must be registered before sending/receiving messages
       - Agent status is tracked (ACTIVE/INACTIVE)
       - Last seen timestamp is updated with each interaction

    4. Error Handling:
       - Invalid messages are rejected with error response
       - Undeliverable messages trigger error notification
       - Duplicate messages are dropped silently
       - Connection issues trigger reconnection flow

    5. Security Rules:
       - Agents can only send messages if authenticated
       - Messages are validated against sender's permissions
       - Direct agent-to-agent messages must be authorized