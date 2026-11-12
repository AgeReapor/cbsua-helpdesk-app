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
