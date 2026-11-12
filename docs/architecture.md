# CBSUA Digital Helpdesk — System Architecture and UML Models

**Document ID:** CBSUA-ARCH-001  
**Status:** Architecture baseline for stakeholder and technical validation  
**Version:** 1.0  
**Date:** 2026-11-12

> **Modeling note:** C4 views are expressed as Mermaid flowcharts with explicit C4 level labels because Mermaid's broadly supported syntax does not provide native C4 rendering in all GitHub Markdown contexts. Domain entities, relationships and behavior use Mermaid `erDiagram`, `classDiagram`, `sequenceDiagram` and `stateDiagram-v2`. These are logical models, not physical database schema or verified runtime topology.

## 1. Architectural overview

The CBSUA Digital Helpdesk is a shared ticketing service based on Frappe Helpdesk. The target local hosting model uses CBSUA Pilot to manage local host, bench, site, app acquisition/validation and runtime operations.

| Concern | Primary owner | Responsibility |
|---|---|---|
| Local host and orchestration | CBSUA Pilot | Host setup, benches, sites, apps, validation, tasks and local services |
| Framework runtime | Frappe | Request lifecycle, authentication, authorization primitives, persistence and jobs |
| Ticketing product | Frappe Helpdesk | Requester/agent experience, tickets, teams, assignment, SLA and reports |
| Product dependency | Frappe Telephony | Dependency required by inspected Helpdesk metadata; telephony feature scope is separate |
| Institutional behavior | CBSUA Helpdesk extension | CBSUA-specific configuration and justified extensions only |

### 1.1 Architecture principles

1. Keep Pilot, Frappe, Helpdesk, Telephony and CBSUA extension responsibilities separate.
2. Use native Helpdesk capabilities before custom development.
3. ICT is the only enabled operational office in Phase 1.
4. Future offices remain disabled until approval and isolation tests pass.
5. Enforce authorization server-side; UI filtering alone is insufficient.
6. Pin immutable source revisions and validate the full app set together.
7. Treat conceptual diagrams as logical views until verified against the selected Helpdesk revision.
8. Do not equate local hosting with production readiness.

## 2. C4 Level 1 — System context

**Purpose:** Show people and external systems interacting with the CBSUA Digital Helpdesk.

~~~mermaid
flowchart TB
    Requester["Person: CBSUA requester<br/>Submits and follows permitted requests"]
    ICTAgent["Person: ICT agent<br/>Processes assigned ICT tickets"]
    ICTManager["Person: ICT manager<br/>Monitors queue and coordinates work"]
    PlatformAdmin["Person: Platform administrator<br/>Manages platform and site"]
    FutureStaff["Person: Future office personnel<br/>Not enabled in Phase 1"]

    Helpdesk["Software system: CBSUA Digital Helpdesk<br/>Shared ticket intake, queue, communication and resolution"]

    Mail["External system: Institutional email<br/>Optional intake and/or notification channel"]
    Pilot["Platform control plane: CBSUA Pilot<br/>Local hosting and app/site operations"]

    Requester -->|"Submit requests; view authorized updates"| Helpdesk
    ICTAgent -->|"Review, assign, communicate and resolve"| Helpdesk
    ICTManager -->|"Monitor workload; reassign and escalate"| Helpdesk
    PlatformAdmin -->|"Administer users, site and configuration"| Helpdesk
    FutureStaff -.->|"Future onboarding only"| Helpdesk
    Helpdesk <-->|"Approved email integration, if enabled"| Mail
    PlatformAdmin -->|"Privileged host/bench/site administration"| Pilot
    Pilot -->|"Hosts and operates the application runtime"| Helpdesk
~~~

**Boundary:** Requesters, agents and managers use Helpdesk. Platform administrators use Pilot for host/bench/site operations and supported Frappe administration for application/site configuration. Pilot is not a ticketing user interface or business workflow engine.

### 2.1 Actor responsibilities

| Actor | Phase 1 | Primary capabilities |
|---|---|---|
| Requester | Active | Submit ticket; view permitted ticket and communication |
| ICT agent | Active | Work assigned/team tickets; reply; comment internally; update status |
| ICT manager | Active | Monitor ICT queue; assign/reassign/escalate within authority |
| Platform administrator | Active | Provision staff and administer platform/site |
| Registrar/Admissions/Cashier staff | Not provisioned | Future office onboarding only |

## 3. C4 Level 2 — Container view

**Purpose:** Show the principal runtime containers and data stores. This is a logical deployment view; the final production topology is not yet approved.

~~~mermaid
flowchart TB
    subgraph Users["User devices"]
      BrowserRequester["Requester browser"]
      BrowserStaff["Agent / manager browser"]
      BrowserAdmin["Administrator browser"]
    end

    subgraph Host["CBSUA managed local host"]
      Pilot["CBSUA Pilot<br/>Admin UI + CLI + task orchestration"]
      subgraph Bench["Pilot-managed bench / shared app environment"]
        Proxy["Local web entry point<br/>Production proxy/TLS to be finalized"]
        Frappe["Frappe Framework<br/>Web runtime and application services"]
        Helpdesk["Frappe Helpdesk<br/>Ticketing product"]
        Telephony["Frappe Telephony<br/>Declared product dependency"]
        Extension["CBSUA Helpdesk extension<br/>Institution-specific behavior"]
        Workers["Background workers / scheduler"]
      end
      DB[("Site database")]
      Redis[("Redis / queue services")]
      Files[("Site file storage<br/>Private and public files")]
    end

    Email["Institutional email service<br/>Optional integration"]

    BrowserRequester --> Proxy
    BrowserStaff --> Proxy
    BrowserAdmin --> Proxy
    Proxy --> Frappe
    Frappe --> Helpdesk
    Helpdesk --> Extension
    Helpdesk --> Telephony
    Frappe --> DB
    Helpdesk --> DB
    Extension --> DB
    Frappe --> Redis
    Redis --> Workers
    Workers --> DB
    Helpdesk --> Files
    Workers <-->|"If configured"| Email
    Pilot -->|"Creates/manages bench and site"| Bench
    Pilot -->|"Coordinates local processes/tasks"| Workers
~~~

### 3.1 Container responsibilities

| Container | Responsibility | State |
|---|---|---|
| Pilot control plane | Host/bench/site/app lifecycle, app validation, process/task operations | Host and bench configuration |
| Frappe web runtime | HTTP request lifecycle and framework services | Site configuration and application state |
| Helpdesk application | Ticket, customer, team, assignment and SLA behavior | Ticketing records |
| Telephony app | Helpdesk dependency/integration capabilities | Telephony-specific records if enabled |
| CBSUA extension | Approved institution-specific fields, hooks, policy or reports | CBSUA extension records/configuration |
| Workers/scheduler | Asynchronous work and scheduled tasks | Queue state and job execution |
| Site database | Durable structured application records | Persistent relational data |
| Redis/queues | Cache and job queue support | Transient/cache/queue data |
| Site file storage | Ticket attachments and related files | Uploaded documents |

**Important:** An app repository present in a bench is not necessarily installed on a site. App acquisition, dependency validation, and site installation are distinct operations managed through Pilot.

## 4. C4 Level 3 — Logical component view

**Purpose:** Decompose the Helpdesk product boundary into responsibilities. Component labels are capability-level abstractions, not guaranteed class names or DocTypes.

~~~mermaid
flowchart TB
    subgraph Interfaces["Presentation components"]
      CustomerPortal["Requester portal"]
      AgentWorkspace["Agent workspace"]
      ManagerViews["Manager queue and reports"]
      AdminWorkspace["Frappe administration"]
    end

    subgraph Product["Frappe Helpdesk product capabilities"]
      Intake["Ticket intake and reference"]
      TicketCore["Ticket lifecycle and classification"]
      CustomerRecords["Requester/customer association"]
      TeamQueue["Team queue and membership"]
      Assignment["Assignment and reassignment"]
      Conversation["Customer replies and internal comments"]
      ServicePolicy["SLA and working-calendar policy"]
      Notification["Notification orchestration"]
      Reporting["Filters, lists and reports"]
    end

    subgraph Extension["CBSUA extension boundary"]
      CBSUAPolicy["CBSUA-specific validation/policy<br/>Only for verified gaps"]
      CBSUAConfig["CBSUA fixtures and configuration"]
      CBSUAReports["Institution-specific reports<br/>Only if native reports are insufficient"]
    end

    subgraph Framework["Frappe framework services"]
      Identity["Authentication and sessions"]
      Permission["Roles, permissions and access checks"]
      ORM["Document / persistence services"]
      Events["Hooks, events and background jobs"]
      Files["File and attachment services"]
    end

    CustomerPortal --> Intake
    CustomerPortal --> TicketCore
    AgentWorkspace --> TicketCore
    ManagerViews --> Reporting
    AdminWorkspace --> CBSUAConfig

    Intake --> CustomerRecords
    Intake --> TicketCore
    TicketCore --> TeamQueue
    TicketCore --> Assignment
    TicketCore --> Conversation
    TicketCore --> ServicePolicy
    TicketCore --> Notification
    TicketCore --> Reporting

    CBSUAPolicy -.->|"Extension only where needed"| TicketCore
    CBSUAConfig -.-> TeamQueue
    CBSUAReports -.-> Reporting

    CustomerPortal --> Identity
    AgentWorkspace --> Identity
    ManagerViews --> Identity
    Identity --> Permission
    TicketCore --> Permission
    TicketCore --> ORM
    CustomerRecords --> ORM
    TeamQueue --> ORM
    Assignment --> ORM
    Conversation --> ORM
    Conversation --> Files
    Notification --> Events
    ServicePolicy --> Events
~~~

### 4.1 Extension rules

- Do not create a second ticket engine.
- Do not put CBSUA-only business policy into Pilot or the generic Helpdesk fork.
- Do not duplicate native Helpdesk entities without a demonstrated need.
- Every extension must cite an SRS requirement, explain why native configuration is insufficient, and include compatibility, migration and test evidence.

## 5. Domain model — UML and entity-relationship model

### 5.1 Conceptual ER model

**Purpose:** Describe the institutional ticket domain and its cardinalities. This model is conceptual and does not prescribe exact database table names.

~~~mermaid
erDiagram
    OFFICE ||--o{ SERVICE_TEAM : contains
    USER ||--o{ TEAM_MEMBERSHIP : has
    SERVICE_TEAM ||--o{ TEAM_MEMBERSHIP : includes
    CUSTOMER ||--o{ CONTACT : has
    CONTACT ||--o{ TICKET : submits
    OFFICE ||--o{ TICKET : owns
    SERVICE_TEAM ||--o{ TICKET : receives
    USER o|--o{ TICKET : assigned_to
    TICKET ||--o{ TICKET_MESSAGE : contains
    USER ||--o{ TICKET_MESSAGE : authors
    TICKET ||--o{ TICKET_EVENT : records
    USER o|--o{ TICKET_EVENT : performs
    SERVICE_POLICY ||--o{ TICKET : governs
    TICKET ||--o{ ATTACHMENT_REFERENCE : references

    OFFICE {
      string office_id PK
      string office_code UK
      string office_name
      boolean enabled
    }
    SERVICE_TEAM {
      string team_id PK
      string team_name
      string office_id FK
      boolean enabled
    }
    USER {
      string user_id PK
      string email UK
      boolean enabled
    }
    TEAM_MEMBERSHIP {
      string membership_id PK
      string user_id FK
      string team_id FK
      string role
    }
    CUSTOMER {
      string customer_id PK
      string display_name
    }
    CONTACT {
      string contact_id PK
      string customer_id FK
      string email
      string identity_reference
    }
    TICKET {
      string ticket_id PK
      string reference UK
      string subject
      string description
      string status
      string priority
      string category
      string office_id FK
      string team_id FK
      string requester_id FK
      string assignee_id FK
      string service_policy_id FK
      datetime created_at
      datetime resolved_at
    }
    TICKET_MESSAGE {
      string message_id PK
      string ticket_id FK
      string author_id FK
      string visibility
      text body
      datetime created_at
    }
    TICKET_EVENT {
      string event_id PK
      string ticket_id FK
      string actor_id FK
      string event_type
      text event_data
      datetime occurred_at
    }
    SERVICE_POLICY {
      string policy_id PK
      string policy_name
      string response_target
      string resolution_target
      string calendar_id
    }
    ATTACHMENT_REFERENCE {
      string attachment_id PK
      string ticket_id FK
      string file_reference
      string visibility
    }
~~~

### 5.2 Entity definitions and rules

| Entity | Meaning | Key rules |
|---|---|---|
| Office | Institutional service boundary | Only ICT enabled in Phase 1; future offices disabled by default |
| Service Team | Operational group handling tickets | Belongs to one office; membership controls staff scope |
| User | Authenticated staff/platform identity | Disabled identities cannot use agent functions |
| Team Membership | Association between user and team | Membership alone is not a substitute for complete record-level authorization |
| Customer | Requesting person/organization record | Exact mapping to Helpdesk customer model must be validated |
| Contact | Requester contact/identity record | Must support the approved requester identity policy |
| Ticket | Unit of service work | Has requester, office/team scope, status, priority and unique reference |
| Ticket Message | Conversation entry | Must distinguish customer-visible reply from internal-only content |
| Ticket Event | Auditable lifecycle/assignment event | Records important state and ownership changes where supported |
| Service Policy | Response/resolution policy and calendar | ICT policy approved before production |
| Attachment Reference | Link to file storage | Visibility follows ticket authorization and attachment policy |

### 5.3 UML class model

~~~mermaid
classDiagram
    class Office {
      +officeId
      +officeCode
      +name
      +enabled
    }
    class ServiceTeam {
      +teamId
      +name
      +enabled
    }
    class User {
      +userId
      +email
      +enabled
    }
    class TeamMembership {
      +membershipId
      +role
    }
    class Customer {
      +customerId
      +displayName
    }
    class Contact {
      +contactId
      +email
    }
    class Ticket {
      +ticketId
      +reference
      +subject
      +description
      +status
      +priority
      +createdAt
      +resolvedAt
    }
    class TicketMessage {
      +messageId
      +body
      +visibility
      +createdAt
    }
    class TicketEvent {
      +eventId
      +eventType
      +occurredAt
    }
    class ServicePolicy {
      +policyId
      +responseTarget
      +resolutionTarget
      +calendarId
    }
    class AttachmentReference {
      +attachmentId
      +fileReference
      +visibility
    }

    Office "1" --> "0..*" ServiceTeam : owns
    ServiceTeam "1" --> "0..*" TeamMembership : has
    User "1" --> "0..*" TeamMembership : joins
    Customer "1" --> "0..*" Contact : has
    Contact "1" --> "0..*" Ticket : requests
    Office "1" --> "0..*" Ticket : owns
    ServiceTeam "0..1" --> "0..*" Ticket : queues
    User "0..1" --> "0..*" Ticket : assigned agent
    Ticket "1" *-- "0..*" TicketMessage : conversation
    Ticket "1" *-- "0..*" TicketEvent : history
    Ticket "1" *-- "0..*" AttachmentReference : attachments
    ServicePolicy "0..1" --> "0..*" Ticket : applies to
    User "1" --> "0..*" TicketMessage : authors
    User "0..1" --> "0..*" TicketEvent : performs
~~~

### 5.4 Mapping to Helpdesk implementation

The model is deliberately independent of exact Frappe DocType names. Before implementation, the technical team must map each concept to:
1. an existing native Helpdesk DocType/field;
2. a supported Frappe framework entity; or
3. a CBSUA extension entity/field only where a documented gap exists.

The team must not create separate Office, Customer, Contact, Ticket or Team records if the selected Helpdesk release already provides the required entity and relationship.

## 6. Ticket lifecycle — UML state machine

~~~mermaid
stateDiagram-v2
    [*] --> New: Request submitted
    New --> Queued: ICT routing applied
    Queued --> Assigned: Agent assigned
    Assigned --> InProgress: Work begins
    InProgress --> WaitingForRequester: Additional information requested
    WaitingForRequester --> InProgress: Requester responds
    InProgress --> Resolved: Resolution recorded
    Resolved --> Closed: Approved closure rule met
    Resolved --> InProgress: Reopened, if permitted
    Closed --> [*]
~~~

**Validation note:** These are conceptual states. Exact status names, transitions and reopen/closure behavior must be mapped to the pinned Helpdesk release and approved by the ICT service owner.

## 7. Ticket submission and processing — UML sequence

~~~mermaid
sequenceDiagram
    autonumber
    actor Requester
    participant Portal as Helpdesk requester portal
    participant HD as Helpdesk application
    participant Auth as Frappe identity/permission services
    participant DB as Site database
    participant ICT as ICT team queue
    actor Agent as ICT agent
    participant Notify as Notification service

    Requester->>Portal: Submit ICT request
    Portal->>HD: Create ticket request
    HD->>Auth: Validate requester and allowed intake
    Auth-->>HD: Identity/access decision
    HD->>DB: Persist ticket and reference
    DB-->>HD: Ticket created
    HD->>ICT: Route to ICT queue
    HD->>Notify: Trigger configured acknowledgement
    Notify-->>Requester: Ticket reference/status notification
    Agent->>HD: Open authorized ICT queue
    HD->>Auth: Check role, membership and ticket scope
    Auth-->>HD: Permit/deny
    HD-->>Agent: Display authorized ticket
    Agent->>HD: Assign and process ticket
    HD->>DB: Persist assignment/status/history
    Agent->>HD: Send reply or internal comment
    HD->>DB: Persist message with visibility
    HD->>Notify: Send customer-visible notification when configured
    Notify-->>Requester: Permitted update
    Agent->>HD: Record resolution
    HD->>DB: Persist resolution and event
~~~

## 8. Authorization model — decision flow

~~~mermaid
flowchart TD
    Start["User requests ticket or action"]
    Authn{"Authenticated where required?"}
    Role{"Role permits action?"}
    Membership{"Active team membership?"}
    Scope{"Ticket office/team within scope?"}
    Visibility{"Message / attachment visibility permits access?"}
    Permit["Permit requested operation"]
    Deny["Deny operation"]
    Audit["Record event where supported"]

    Start --> Authn
    Authn -->|"No"| Deny
    Authn -->|"Yes"| Role
    Role -->|"No"| Deny
    Role -->|"Yes"| Membership
    Membership -->|"No, if team action requires it"| Deny
    Membership -->|"Yes / not applicable"| Scope
    Scope -->|"No"| Deny
    Scope -->|"Yes"| Visibility
    Visibility -->|"No"| Deny
    Visibility -->|"Yes"| Permit
    Permit --> Audit
    Deny --> Audit
~~~

### 8.1 Mandatory authorization test surface

The team must test:
- queue/list visibility;
- direct ticket URL;
- global search;
- reports and dashboards;
- customer-visible versus internal comments;
- private/public attachments and download URLs;
- assignment, reassignment and escalation;
- export and bulk operations;
- disabled staff accounts;
- revoked team membership;
- manager versus platform-administrator privilege.

## 9. Office onboarding — activity flow

~~~mermaid
flowchart TD
    Start["Office onboarding requested"]
    Approve{"Sponsor and office owner approve?"}
    Discover["Document services, categories and required fields"]
    Policy["Approve identity, priority, calendar and service targets"]
    Team["Configure office team and staff membership"]
    Access["Configure and test authorization boundaries"]
    Route["Configure intake destination and routing"]
    Report["Configure views and reports"]
    Verify["Run workflow, notification and cross-office tests"]
    Accept{"Office owner accepts evidence?"}
    Enable["Enable office destination"]
    Remediate["Fix findings and repeat tests"]
    Reject["Keep office disabled"]

    Start --> Approve
    Approve -->|"No"| Reject
    Approve -->|"Yes"| Discover --> Policy --> Team --> Access --> Route --> Report --> Verify --> Accept
    Accept -->|"Yes"| Enable
    Accept -->|"No"| Remediate --> Verify
~~~

## 10. Deployment and trust boundaries

### 10.1 Logical environment tiers

| Environment | Purpose | Data policy |
|---|---|---|
| Local development | Developer implementation and debugging | Synthetic data |
| Integration/acceptance | Cross-app, workflow, authorization and UAT validation | Synthetic or specifically approved test data |
| Production | Institutional service | Approved real data under institutional policy |

### 10.2 Trust boundaries

- Pilot Admin UI/CLI is a privileged host-administration surface.
- Helpdesk requester and staff interfaces have different authorization levels.
- Platform administrators have broader privileges than office managers.
- A team membership or hidden UI element does not prove data isolation.
- Secrets must not be committed to Git.
- Attachments inherit the ticket's authorization and privacy policy.
- Local host success does not prove production security, resilience or availability.

## 11. Architecture decisions and open points

| ID | Decision / question | Status |
|---|---|---|
| ADR-A01 | Pilot owns local host, bench, site and app lifecycle | Accepted target |
| ADR-A02 | Frappe is the framework; Helpdesk is the ticketing product | Accepted |
| ADR-A03 | CBSUA extension owns only institution-specific gaps | Accepted |
| ADR-A04 | ICT is the only active Phase 1 destination | Accepted |
| ADR-A05 | Native Helpdesk configuration is preferred | Accepted |
| ADR-A06 | Exact Frappe/Helpdesk/Telephony/Python revision set | Open, blocking |
| ADR-A07 | Exact native DocType mapping for conceptual entities | Open, implementation discovery |
| ADR-A08 | Customer authentication and anonymous submission policy | Open |
| ADR-A09 | Complete office/team authorization behavior | Open, security gate |
| ADR-A10 | Production host/site topology, backup and monitoring | Open |
| ADR-A11 | Whether Telephony features are enabled in Phase 1 | Open |

## 12. Related requirements

- [SRS](SRS.md) — business context, problems, needs, functional and non-functional requirements.
- [Traceability matrix](traceability-matrix.md) — problem → need → requirement → architecture/test.
- [Workflows](workflows.md) — operational scenarios and exception cases.
- [Pilot architectural handoff](handoff/README.md) — local hosting and repository boundaries.
