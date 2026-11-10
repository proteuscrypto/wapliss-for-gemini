<p align="center">
  <img src="assets/logo.png" alt="Wapliss logo" width="120" />
</p>

# Wapliss WhatsApp for Gemini

Use your own WhatsApp from Google's Gemini surfaces through
[Wapliss](https://wapliss.com/). This repository contains only the Gemini
packages. They all connect to the hosted Wapliss MCP service at
`https://wapliss.com/mcp/v1` with OAuth 2.1; no account data or WhatsApp
credentials are stored here.

| Surface | What this repo provides | How users get it |
| --- | --- | --- |
| **Gemini app** (gemini.google.com, Android, iOS) | Listing for Google **Connected Apps** (`connected-apps/`) | Published app: type `@Wapliss` in Gemini. Before publication: *Settings > Connected Apps > Add a custom app* with `https://wapliss.com/mcp/v1` |
| **Antigravity** (App, IDE, CLI `agy`) | Antigravity plugin: `plugin.json`, `mcp_config.json`, `skills/`, `rules/` | `agy plugin install <path to this repo>`, or the Antigravity Marketplace once listed |
| **Gemini CLI** (enterprise and API-key users) | Gemini CLI extension: `gemini-extension.json`, `GEMINI.md` | `gemini extensions install https://github.com/proteuscrypto/wapliss-for-gemini` |

## Setup (users)

1. Add Wapliss on your surface (table above) and choose **Connect** /
   **Authenticate** when asked.
2. Sign in to (or create) your account at [wapliss.com](https://wapliss.com/)
   and approve access.
3. Link your phone once at
   [wapliss.com/app/connect](https://wapliss.com/app/connect): WhatsApp >
   Linked devices > Link a device, then scan the QR code.
4. Ask, for example: "@Wapliss show me my latest WhatsApp messages".

Never paste Wapliss API keys, WhatsApp credentials or session data into a chat.
If authorization expires, authenticate again.

## What it can do (16 tools)

| Area | Tools |
| --- | --- |
| Read chats and groups | `get_chats`, `get_chat_history`, `get_message` |
| Latest activity | `get_last_incoming_messages`, `get_last_outgoing_messages` |
| Groups | `get_group` (name, description, admins, participants) |
| Send | `send_text_message`, `send_image`, `send_document`, `send_audio`, `send_video`, `send_location`, `send_contact`, `send_poll`, `forward_messages` |
| Account | `get_account_status` (plan, usage, quota) |

Every tool declares `readOnlyHint`, `destructiveHint`, `idempotentHint` and
`openWorldHint`; send tools are destructive, so Gemini asks for confirmation.
Sends are queued: a successful call returns a `queue_id`, not a delivery
receipt. Bulk or unsolicited messaging is not allowed.

## How it works

```text
Gemini / Antigravity / Gemini CLI
        |  OAuth 2.1: discovery, Dynamic Client Registration, PKCE S256
        v
https://wapliss.com/mcp/v1   (Streamable HTTP, MCP 2025-11-25 and earlier)
        |
Wapliss WhatsApp engine  --->  WhatsApp
```

- Protected resource metadata:
  `https://wapliss.com/.well-known/oauth-protected-resource/mcp/v1`
- Authorization server metadata:
  `https://wapliss.com/.well-known/oauth-authorization-server`
- Scopes: `wapliss:mcp`, `whatsapp:read`, `whatsapp:write`
- Refresh tokens: not rotated for Google redirect URIs (Persistent Linking);
  revoking a refresh token ends the whole grant.
- `/mcp/v1` keeps fixed English tool definitions. Breaking changes ship on a new
  path (`/mcp/v2`) while `v1` stays live, as Google snapshots tools per version.

## Package layout

```text
plugin.json                       Antigravity plugin manifest
mcp_config.json                   Antigravity MCP server (serverUrl)
gemini-extension.json             Gemini CLI extension manifest (httpUrl + OAuth)
GEMINI.md                         Gemini CLI context (same text as rules/GEMINI.md)
rules/GEMINI.md                   Antigravity always-on rule
skills/wapliss-whatsapp/SKILL.md  Usage rules for the agent
assets/logo.png                   512x512 logo (Connected Console and Marketplace)
connected-apps/listing.json       Values for Google Connected Console
connected-apps/SUBMISSION.md      Step-by-step submission checklist
scripts/validate.py               Package checks (--live also checks the endpoint)
```

## Development

```bash
python3 scripts/validate.py          # offline checks
python3 scripts/validate.py --live   # plus endpoint and OAuth metadata
gemini extensions validate .         # Gemini CLI
agy plugin validate --strict .       # Antigravity (0 errors, 0 warnings for the Marketplace)
```

Bump `version` in both `plugin.json` and `gemini-extension.json`. Do not change
tool names or schemas inside `/mcp/v1`.

## Support and legal

- Support: [GitHub issues](https://github.com/proteuscrypto/wapliss-for-gemini/issues)
- [Privacy policy](https://wapliss.com/privacy-policy) ·
  [Terms of service](https://wapliss.com/terms-of-service)

Wapliss is an independent service and is not affiliated with or endorsed by
Meta, WhatsApp or Google.

## License

MIT
