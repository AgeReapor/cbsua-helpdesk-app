# Agent Skills Review

**Reviewed:** 2026-11-12  
**Source:** [`lubusIN/frappe-skills`](https://github.com/lubusIN/frappe-skills)  
**Installer:** [`skills` CLI](https://www.skills.sh/docs/cli)

## Installed set

The project installed 14 skills from `lubusIN/frappe-skills` with:

```sh
npx skills add lubusIN/frappe-skills
```

The CLI placed the skill content in the local `.agents/skills/` directory and wrote `skills-lock.json` with each skill's source, path, and content hash. `.agents/` remains ignored by the project workflow; the lock file can be committed to record the intended skill set without vendoring the skill content. A content hash helps identify changes, but it does not certify the skill as safe or correct.

The installed collection contains: `api-development`, `app-development`, `desk-customization`, `doctype-development`, `enterprise-patterns`, `frappe-manager`, `frontend-development`, `printing-templates`, `project-triage`, `reports`, `router`, `testing`, `ui-patterns`, and `web-forms`.

## Review findings

The CLI's installation scan classified `printing-templates` as **Critical Risk**, and `frappe-manager`, `frontend-development`, and `web-forms` as **Medium Risk**. The remaining installed skills were classified as Low Risk by that scan. These labels are a screening signal, not a security guarantee; the Skills directory itself says it cannot guarantee each listed skill's quality or security.

Review found examples that should not be copied into CBSUA production code without correction:

- Some report and permission examples use `frappe.get_all`. Frappe documents that `get_all` does not apply user permissions. Use permission-aware queries or establish and document a trusted server-side authorization boundary before retrieving restricted records.
- Some snippets interpolate values into SQL or mark template values `|safe`. Use parameterized query APIs or escaped values, and only mark content safe after context-appropriate sanitization.
- `frappe-manager` includes insecure sample administrator credentials. Never use those defaults; provision credentials through the environment's secret-management process.
- `frontend-development` includes advice that may not match this app's pinned Frappe/Helpdesk versions, including CSRF-related examples. Verify current framework behavior and the installed source before adopting it.
- `doctype-development` presents developer mode as more universally required than it is. It is needed for particular UI export workflows; app-bundled DocType JSON can also be maintained and migrated through the normal app workflow.
- Generic enterprise examples propose custom ticket, SLA, and activity models. CBSUA should use native Helpdesk records where they already cover the requirement and add a custom DocType only for a distinct CBSUA concept.

## CBSUA usage rules

1. Treat third-party skill content as untrusted reference material. Review the relevant file and its supporting references before following instructions or copying code.
2. Check all Frappe APIs and behavior against the pinned framework/Helpdesk release and installed source. Skill examples may target another version.
3. Keep Helpdesk's native ticket, team, agent, customer, priority, and SLA models as the baseline. Extend these only when the SRS identifies a CBSUA-specific data concept or behavior.
4. For office authorization, verify list queries, direct document access, RPC/REST methods, search, reports and exports, comments, attachments, assignment paths, and administrator exceptions. A list-query hook is not a complete access boundary: Frappe documents that `permission_query_conditions` affects `get_list`, not `get_all`; document `has_permission` is separate.
5. Do not use insecure sample credentials, bypass CSRF protections, interpolate untrusted SQL, or emit unsanitized HTML based solely on a skill example.

These rules complement the authorization design in [Architecture](architecture.md) and the security requirements in the [SRS](SRS.md). For Frappe's documented query and document-permission hook behavior, see [Frappe Hooks](https://docs.frappe.io/framework/user/en/python-api/hooks) and [Database API](https://docs.frappe.io/framework/user/en/api/database).

## Frappe Helpdesk upstream review

**Reviewed:** 2026-11-12 against the public `frappe/helpdesk` `develop` branch and its `AGENTS.md`.

The upstream instructions reinforce reading the target Site before assuming its data state, avoiding unapproved Site writes, updating the spec in the same session as implementation, and keeping test factories in a shared utility. Its repository layout separates Python backend code (`helpdesk/`), the Vue agent UI (`desk/`), and shared frontend code. Its current `develop` README states that the branch requires Frappe `develop` and uses a Studio-based customer portal at `/help`. That differs from CBSUA's pinned Framework 16 / Helpdesk 16.1.0 baseline, whose customer and agent routes share the `/helpdesk/` Vue app. Therefore `develop` code, Studio JSON, routes, and API examples are references only until checked against the installed `version-16` source.

The Helpdesk repository also contains `skills/frappe-helpdesk/SKILL.md`, an operational `frappectl` guide for managing real tickets and customer data. It is not the coding skill referenced by `AGENTS.md` and is not installed as a development skill. A CBSUA-specific development skill is available at `.agents/skills/cbsua-helpdesk-development/SKILL.md`; the local skill router points M1 work to it. The upstream repository's test-helper rule applies to its own `helpdesk/test_utils.py`; CBSUA tests must keep helpers within the CBSUA app and must not edit vendor files.

The reviewed upstream `HD Ticket` create endpoint stamps the caller's identity, derives its portal-origin flag from the session, validates uploaded attachments, and rate-limits ticket creation. This supports using the native Helpdesk submission path for integration testing, but the exact method and validation behavior must be verified against Helpdesk `version-16` before use. M1 portal submission must remain behind the approved requester identity policy; SRS open question OQ-01 is still unresolved.
