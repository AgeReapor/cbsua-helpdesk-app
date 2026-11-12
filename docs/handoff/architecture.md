# Target Architecture

## 1. Architectural intent

Adopt a **Pilot-managed Frappe platform with Helpdesk as the ticketing product and a narrow CBSUA extension boundary**.

Pilot owns local hosting and operational lifecycle. Frappe owns framework services. Helpdesk owns ticketing capabilities. Telephony supplies a product dependency. The CBSUA app owns only institution-specific behavior that cannot be safely delivered through supported Helpdesk configuration.

The logical deployment may begin on one local development host. Do not confuse that topology with production readiness.

## 2. System context

~~~mermaid
flowchart TB
  Requester["CBSUA requester"]
  Agent["ICT helpdesk agent"]
  Manager["ICT service manager"]
  Admin["Platform administrator"]
  subgraph Host["CBSUA managed local host"]
    Pilot["CBSUA Pilot<br/>Admin UI + CLI"]
    Bench["Pilot-managed bench"]
    Site["CBSUA Helpdesk site"]
    Frappe["CBSUA Frappe Framework"]
    HD["CBSUA Helpdesk"]
    Tel["CBSUA Telephony"]
    Ext["CBSUA Helpdesk extension"]
    DB[("Site database")]
    Redis[("Redis / queues")]
    Files[("Site files")]
  end
  Requester --> Site
  Agent --> Site
  Manager --> Site
  Admin --> Pilot
  Pilot --> Bench
  Bench --> Frappe
  Bench --> HD
  Bench --> Tel
  Bench --> Ext
  Site --> Frappe
  Site --> HD
  Site --> Tel
  Site --> Ext
  Frappe --> DB
  Frappe --> Redis
  HD --> DB
  Ext --> DB
  HD --> Files
~~~

Pilot manages benches, sites, apps, local processes and operational tasks. End users interact with Helpdesk, not Pilot's Admin UI. The Admin UI is a privileged platform-administration surface and must be access-restricted separately from Helpdesk roles.

## 3. Repository and runtime layers

| Layer | Repository | Responsibility |
|---|---|---|
| Host control plane | cbsua-app-pilot | CLI, Admin UI, bench/site lifecycle, app staging and validation, local services |
| Framework | cbsua-app-frappe | Frappe request lifecycle, DocTypes, authentication, permissions, persistence and jobs |
| Product | cbsua-app-helpdesk | Ticket intake, customer/agent interfaces, ticket lifecycle, teams, assignment, SLA and reports |
| Product dependency | cbsua-app-telephony | Telephony integration DocTypes and provider adapters required by Helpdesk metadata |
| Institutional extension | cbsua-helpdesk-app | CBSUA-specific fields, hooks, fixtures/configuration, policy extensions, reports and tests where justified |

The table distinguishes source repositories from installed applications. Repositories are cloned into a Pilot-managed bench; apps are then installed on a particular site. A repository present in a bench is not necessarily installed on that site.

## 4. Dependency direction

~~~mermaid
flowchart TD
  Pilot["Pilot"]
  Frappe["Frappe"]
  Helpdesk["Helpdesk"]
  Telephony["Telephony"]
  CBSUA["CBSUA extension"]
  Pilot --> Frappe
  Pilot --> Helpdesk
  Pilot --> Telephony
  Pilot --> CBSUA
  Helpdesk -->|"framework dependency"| Frappe
  Helpdesk -->|"declared app dependency"| Telephony
  CBSUA -->|"extends supported product APIs"| Helpdesk
  CBSUA -->|"framework services"| Frappe
~~~

Dependency direction must not be inverted: Frappe must not import CBSUA logic; Helpdesk must not contain CBSUA-only policy; Pilot must not encode ticket business rules.

## 5. Main flows

### User request flow
1. A requester opens the Helpdesk customer portal.
2. Helpdesk validates the request using Frappe services.
3. Helpdesk persists the ticket and associated records.
4. Native Helpdesk configuration routes the ticket to the enabled ICT team.
5. Authorized ICT agents process and resolve the ticket.
6. The requester receives permitted status updates and responses.

Precise fields, intake categories, visibility rules, notification channels and service targets remain subject to approved requirements and stakeholder decisions.

### App installation flow
1. A developer or administrator selects a repository/revision through Pilot's supported CLI or Admin UI.
2. Pilot stages and validates app metadata and dependencies.
3. The app is made available to the bench's shared Python environment.
4. An administrator installs the app on the intended site.
5. Site migrations/build operations run through Pilot's supported task/CLI workflow.
6. Smoke tests verify the combined site.

Adding app source to a bench and installing an app on a site are separate operations.

## 6. Runtime and state ownership

| State | Owner | Notes |
|---|---|---|
| Host configuration and bench inventory | Pilot | Host-level administration |
| App sources and shared Python environment | Pilot-managed bench | Apps share one interpreter |
| Site identity and site configuration | Frappe site, managed by Pilot | Site-scoped settings |
| Tickets, customers, teams and Helpdesk records | Helpdesk on Frappe | Product data/schema |
| CBSUA extension schema/configuration | CBSUA app on site | Migration-safe |
| Attachments and uploaded files | Site file storage | Back up with database |
| Jobs and queues | Frappe/Pilot runtime | Confirm worker/scheduler health |

## 7. Environment boundaries

- **Local development:** Pilot-managed local bench and non-production site; synthetic data only.
- **Integration/acceptance:** controlled environment for compatibility, workflow, authorization and recovery testing.
- **Production:** separately approved host/site configuration, hardened access, HTTPS/reverse proxy where applicable, monitoring, tested backup/restore and change-controlled releases.

Local Pilot hosting does not automatically provide production security, availability, backups, monitoring or institutional operational support.

## 8. Security boundaries

1. Pilot Admin UI/CLI administration is privileged.
2. Helpdesk requester, agent, manager and platform administrator roles are distinct trust levels.
3. Office/team membership is not proof of complete data isolation until tests cover lists, direct URLs, search, reports, attachments, comments, exports and assignment actions.
4. Secrets must remain in supported local/host/site secret configuration, never Git.
5. Use synthetic data until approved safeguards and access controls are in place.
6. Future office destinations remain disabled until onboarding approval and isolation tests pass.

## 9. Quality attributes

- Maintainability: minimize custom code; prefer native Helpdesk configuration.
- Compatibility: declare app dependencies and test the full set together.
- Recoverability: database and file backups are paired and restore-tested.
- Security: enforce authorization server-side with negative tests.
- Traceability: link every customization to an approved requirement and test.
- Portability: record exact Pilot revision, app commits, site settings and host prerequisites.

## 10. Out of scope

No separate physical walk-in token display/calling system, SIS, enrollment workflow, payment processing or general-purpose CRM is included absent separately approved scope and architecture.
