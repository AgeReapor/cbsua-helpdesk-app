# System Architecture

**Architecture style:** Single shared Frappe Helpdesk deployment with phased office onboarding.  
**System of record for tickets:** Frappe Helpdesk.  
**Customization principle:** Configure native Helpdesk capabilities first; add a CBSUA app extension only for verified gaps.

## 1. Architecture principles

1. Frappe Helpdesk is the ticketing application; do not recreate its ticket engine.
2. Frappe Framework provides the underlying application, authentication, permissions, persistence, and background processing.
3. One deployment serves multiple office teams.
4. ICT is the only active office in Phase 1.
5. Office-level access isolation is a release gate, not an assumption.
6. Custom fields and configuration should be preferred over custom ticket services.
7. Version compatibility must be pinned and verified before implementation.

## 2. C4 Level 1 — System context

```mermaid
flowchart TB
    Customer["CBSUA Clients / Requesters"]
    ICT["ICT Office Personnel"]
    Registrar["Registrar Personnel"]
    Admissions["Admissions Personnel"]
    Cashier["Cashier Personnel"]
    Admin["System Administrator"]

    System["CBSUA Ticketing and Queueing System<br/>(Frappe Helpdesk)"]

    Customer -->|"Submit and track permitted tickets"| System
    ICT -->|"Manage ICT tickets"| System
    Registrar -.->|"Future office onboarding"| System
    Admissions -.->|"Future office onboarding"| System
    Cashier -.->|"Future office onboarding"| System
    Admin -->|"Configure and administer platform"| System
```

## 3. C4 Level 2 — Container view

The diagram is logical. Exact deployment topology (single server, separate workers, managed database, object storage, and reverse proxy) is a deployment decision to be finalized.

```mermaid
flowchart TB
    Customer["Customer Browser"]
    Agent["Agent / Manager Browser"]
    Admin["Administrator Browser"]

    subgraph Platform["CBSUA Frappe / Helpdesk Deployment"]
        Proxy["HTTPS Reverse Proxy"]
        HelpdeskUI["Helpdesk v16 Vue app<br/>/helpdesk (agent and customer routes)"]
        Desk["Frappe Desk / administration"]
        App["Frappe Helpdesk Application"]
        Framework["Frappe Framework"]
        Workers["Background Workers / Scheduler"]
        Redis[("Redis")]
        DB[("MariaDB")]
        Files[("Private / Public File Storage")]
    end

    Mail["Institutional Email Service"]

    Customer --> Proxy
    Agent --> Proxy
    Admin --> Proxy
    Proxy --> HelpdeskUI
    Proxy --> Desk
    HelpdeskUI --> App
    Desk --> Framework
    App --> Framework
    Framework --> DB
    Framework --> Redis
    Redis --> Workers
    App --> Files
    Workers <--> Mail
    App <--> Mail
```

Email is an optional integration for the initial release unless stakeholders require email-to-ticket intake or outbound email notifications at launch.

## 4. C4 Level 3 — Logical Helpdesk components

```mermaid
flowchart TB
    subgraph Interfaces["Frappe Helpdesk Interfaces"]
        CustomerUI["Customer Portal"]
        AgentUI["Agent Interface"]
        AdminUI["Frappe Desk / Administration"]
    end

    subgraph Helpdesk["Frappe Helpdesk Capabilities"]
        Ticket["Ticket records and lifecycle"]
        Customer["Customer / Contact records"]
        Team["Teams / Agent Groups"]
        Assignment["Assignment configuration"]
        SLA["SLA configuration"]
        Conversation["Replies and internal comments"]
        Views["Ticket lists, filters, and reports"]
        Forms["Ticket types, templates, and custom fields"]
    end

    subgraph Framework["Frappe Framework Services"]
        Authentication["Authentication and sessions"]
        Authorization["Roles and permissions"]
        Persistence[("Database")]
        Jobs["Background jobs and scheduler"]
    end

    CustomerUI --> Ticket
    AgentUI --> Ticket
    AdminUI --> Forms
    AgentUI --> Authentication
    AdminUI --> Authentication
    Authentication --> Authorization
    Ticket --> Customer
    Ticket --> Team
    Ticket --> Assignment
    Ticket --> SLA
    Ticket --> Conversation
    Ticket --> Views
    Ticket --> Persistence
    Customer --> Persistence
    Team --> Persistence
    Assignment --> Persistence
    SLA --> Persistence
    Jobs --> Persistence
```

This is a conceptual mapping of product capabilities, not a promise that every box is a separate deployable service or DocType. Validate actual feature names and availability against the pinned Helpdesk release.

## 5. Office queue and routing model

```mermaid
flowchart TD
    Intake["Ticket submitted"]
    Identify["Determine responsible office"]
    ICT{"Phase 1: ICT destination"}
    ICTTeam["ICT Helpdesk Team"]
    Future["Future approved office destinations"]
    Queue["Office team queue"]
    Assign["Manual or configured automatic assignment"]
    Agent["Authorized office agent"]
    Work["Respond, investigate, update"]
    Resolve["Resolve and close"]

    Intake --> Identify --> ICT
    ICT -->|"Enabled"| ICTTeam --> Queue
    ICT -.->|"Not enabled in Phase 1"| Future
    Queue --> Assign --> Agent --> Work --> Resolve
```

For Phase 1, the customer intake experience must not expose future office destinations. The office/team association must be stored or derived consistently and used by access-control rules and reporting.

## 6. Conceptual data model

```mermaid
erDiagram
    USER ||--o{ TEAM_MEMBER : joins
    TEAM ||--o{ TEAM_MEMBER : includes
    TEAM ||--o{ HD_TICKET : receives
    USER ||--o{ HD_TICKET : assigned_agent
    CUSTOMER ||--o{ CONTACT : has
    CONTACT ||--o{ HD_TICKET : requester
    SLA_POLICY ||--o{ HD_TICKET : applies_to

    USER {
        string id
        string email
        boolean enabled
    }
    TEAM {
        string id
        string office_code
    }
    TEAM_MEMBER {
        string user_id
        string team_id
    }
    CUSTOMER {
        string id
        string display_name
    }
    CONTACT {
        string id
        string email
        string customer_id
    }
    HD_TICKET {
        string id
        string subject
        string office_code
        string ticket_type
        string priority
        string status
        string team_id
        string assigned_agent
        datetime created_at
        datetime resolved_at
    }
    SLA_POLICY {
        string id
        string response_target
        string resolution_target
    }
```

This model is conceptual only. It is not a statement of exact Helpdesk database schema. The implementation must inspect the selected release's DocTypes and use native fields wherever possible. `office_code` may be a custom field or a value derived from an approved team-to-office mapping. Avoid duplicating native records.

## 7. Authorization boundary

```mermaid
flowchart TD
    Request["Authenticated staff request"]
    Role["Evaluate Helpdesk role"]
    Team["Evaluate team membership"]
    Scope["Evaluate ticket office/team scope"]
    Allowed{"Authorized?"}
    Permit["Permit requested action"]
    Deny["Deny access and record as appropriate"]

    Request --> Role --> Team --> Scope --> Allowed
    Allowed -->|"Yes"| Permit
    Allowed -->|"No"| Deny
```

Required tests include direct ticket URL access, list filtering, search, reports, attachments, comments, assignment changes, and manager-level actions. Hiding a ticket from a list is not sufficient if it remains accessible through another route.

## 8. Deployment considerations

- Pin mutually compatible Frappe Framework and Frappe Helpdesk versions.
- Use HTTPS in production.
- Separate development, test/staging, and production environments where feasible.
- Back up the database and file storage together.
- Test restore procedures before production acceptance.
- Restrict administrative access.
- Document worker, scheduler, email, and storage configuration.
- Keep CBSUA customizations in version control and cover them with automated or repeatable tests.

## 9. Architecture decisions requiring validation

- Exact supported Frappe and Helpdesk release pair.
- Native team-level permission behavior and whether office isolation needs an extension.
- Customer portal authentication and anonymous ticket policy.
- Email intake and notification requirements.
- Whether an explicit Office DocType is needed or team metadata is sufficient.
- Reporting capabilities and whether custom reports are required.
