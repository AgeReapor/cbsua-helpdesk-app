# Ticketing Workflows

## 1. Phase 1 ICT ticket lifecycle

```mermaid
flowchart TD
    A["Customer submits ICT ticket"]
    B["Helpdesk creates ticket and reference"]
    C["Ticket enters ICT team queue"]
    D["ICT agent is assigned"]
    E["Agent reviews and works ticket"]
    F{"Information needed?"}
    G["Ask customer for information"]
    H["Customer responds"]
    I["Record resolution"]
    J["Notify customer"]
    K["Close ticket under approved rule"]

    A --> B --> C --> D --> E --> F
    F -->|"Yes"| G --> H --> E
    F -->|"No"| I --> J --> K
```

The exact status values and transitions must be aligned to the selected Helpdesk version. The diagram describes the intended business process, not a claim that these exact status labels are built in.

## 2. Assignment workflow

```mermaid
flowchart TD
    Ticket["New ICT ticket"]
    Queue["ICT team queue"]
    Choice{"Assignment method"}
    Manual["ICT manager / authorized agent assigns"]
    Auto["Configured Helpdesk assignment rule"]
    Agent["Assigned ICT agent"]
    Work["Agent processes ticket"]

    Ticket --> Queue --> Choice
    Choice -->|"Manual"| Manual --> Agent
    Choice -->|"Automatic, if validated"| Auto --> Agent
    Agent --> Work
```

Automatic assignment is optional until the team confirms workload and fairness rules and validates the feature in the pinned release.

## 3. Escalation workflow

```mermaid
flowchart TD
    Active["Ticket being processed"]
    Trigger{"Escalation condition met?"}
    Continue["Continue normal processing"]
    Manager["Notify / route to ICT manager"]
    Reassign["Review priority, ownership, or specialist"]
    Resume["Continue processing with updated ownership"]

    Active --> Trigger
    Trigger -->|"No"| Continue
    Trigger -->|"Yes"| Manager --> Reassign --> Resume
```

Escalation triggers (age, priority, SLA risk, or specialist need) and manager actions must be approved by ICT.

## 4. Future office onboarding workflow

```mermaid
flowchart TD
    Start["Office approved for onboarding"]
    Discover["Confirm services, ticket categories, and request fields"]
    Targets["Approve priorities, working calendar, and service targets"]
    Team["Create office Helpdesk team and membership"]
    Access["Configure roles and office-level access restrictions"]
    Route["Configure intake destination and routing"]
    Reports["Configure office views and reports"]
    Test["Test isolation, assignment, notifications, and workflow"]
    Gate{"Office owner accepts?"}
    Activate["Enable office destination"]
    Fix["Resolve findings and retest"]

    Start --> Discover --> Targets --> Team --> Access --> Route --> Reports --> Test --> Gate
    Gate -->|"Yes"| Activate
    Gate -->|"No"| Fix --> Test
```

## 5. Customer access policy

Before production, stakeholders must choose one of the following policies:

- Authenticated customer accounts only.
- Anonymous submission with secure reference-based follow-up.
- A mixed model with defined eligibility and safeguards.

The implementation must verify that a customer can only see tickets they are authorized to access. The policy must also address identity verification, sensitive attachments, retention, and account recovery.

## 6. Operational exception cases to test

- Ticket submitted with missing or invalid required information.
- Ticket routed to an unavailable or disabled team.
- Agent account disabled while tickets remain assigned.
- Ticket reassigned to another agent or team.
- Customer replies after a ticket is resolved or closed.
- Duplicate or repeated ticket submissions.
- Attachment rejected due to type or size policy.
- Notification delivery failure.
- SLA calendar boundary, holiday, and after-hours behavior.
- Unauthorized user attempts to open a ticket directly.
