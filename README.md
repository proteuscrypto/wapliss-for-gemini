<p align="center">
  <img src="assets/logo.png" alt="Wapliss logo" width="120" />
</p>

<h1 align="center">Wapliss WhatsApp for Gemini</h1>

<p align="center">
  <strong>Connect your own WhatsApp to Gemini with the Wapliss MCP server.</strong><br />
  Read and summarize chats and groups, and send messages, files, locations and polls, always with your confirmation.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-25D366" alt="License: MIT" />
  <img src="https://img.shields.io/badge/MCP-2026--07--28%20%7C%202025--11--25-128C7E" alt="MCP" />
  <img src="https://img.shields.io/badge/Gemini-plugin-128C7E" alt="Gemini" />
  <img src="https://img.shields.io/badge/version-1.0.1-25D366" alt="Version" />
  <img src="https://img.shields.io/badge/Gemini%20CLI-extension-4285F4" alt="Gemini CLI" />
  <img src="https://img.shields.io/badge/Antigravity-plugin-4285F4" alt="Antigravity" />
</p>

<p align="center">
  <a href="https://wapliss.com/">Website</a> ·
  <a href="https://wapliss.com/integrations#gemini">Gemini guide</a> ·
  <a href="https://wapliss.com/integraciones#gemini">Guía en español</a> ·
  <a href="#example-prompts">Examples</a> ·
  <a href="#faq">FAQ</a> ·
  <a href="#wapliss-plugins">Other assistants</a>
</p>

---

## What is Wapliss?

[Wapliss](https://wapliss.com/), by [NetDigitalTech](https://github.com/netdigitaltech), is a WhatsApp gateway for AI assistants. You
link your WhatsApp number once with a QR code, authorize your assistant, and
the assistant can read your chats and groups and send WhatsApp messages for
you through a standard [Model Context Protocol](https://modelcontextprotocol.io/)
(MCP) server. A free plan is available, with no credit card required.

This repository is the official **Gemini package** of Wapliss
(Antigravity plugin, Gemini CLI extension and Google Connected Apps listing). It only points Gemini to the hosted Wapliss MCP
server; it stores no account data, messages or credentials.

## Compatibility

| Surface | How | Status |
| --- | --- | --- |
| Gemini app (web, Android, iOS) | **Settings → Connected Apps → Add a custom app** with `https://wapliss.com/mcp/v1`; published app: type `@Wapliss` | Custom app works; Connected Apps listing pending Google access |
| Gemini CLI | `gemini extensions install https://github.com/proteuscrypto/wapliss-for-gemini` | Works |
| Antigravity (App, IDE, `agy`) | `agy plugin install ./wapliss-for-gemini` | Works; Marketplace listing pending |

## Quick start

1. Create a free account at [wapliss.com](https://wapliss.com/) and link your
   phone once at [wapliss.com/app/connect](https://wapliss.com/app/connect).
2. Pick your surface:

   ```bash
   # Gemini CLI
   gemini extensions install https://github.com/proteuscrypto/wapliss-for-gemini
   # then, inside Gemini CLI:
   /mcp auth wapliss

   # Antigravity
   git clone https://github.com/proteuscrypto/wapliss-for-gemini
   agy plugin install ./wapliss-for-gemini
   ```

   Gemini app: **Settings → Connected Apps → Connectors → + Custom**, MCP
   server URL `https://wapliss.com/mcp/v1`, then **Next** and sign in.
3. Sign in to Wapliss and approve access.
4. Ask: *"@Wapliss show me my latest WhatsApp messages"*.

## Example prompts

| Goal | Ask (type `@Wapliss` first) |
| --- | --- |
| Catch up | "@Wapliss Show me my latest WhatsApp messages" |
| Summarize a group | "@Wapliss Summarize what was said today in my family group" |
| Read a chat | "@Wapliss Read my last 20 messages with Ana and tell me what she needs" |
| Group info | "@Wapliss Who are the admins of the work group?" |
| Send a message | "@Wapliss Send 'On my way, 10 minutes' to +1 555 010 2030" |
| Send a file | "@Wapliss Send this PDF to Laura: https://example.com/quote.pdf" |
| Share a location | "@Wapliss Send the office location to the project group" |
| Run a poll | "@Wapliss Create a poll in the team group: Friday or Monday?" |
| Check the account | "@Wapliss Check my Wapliss account and today's usage" |

Tips: name the chat or group as it appears in WhatsApp, or use the number with
country code. The assistant shows you the recipient and the text before
sending when anything is ambiguous.

## What it can do (16 tools)

| Area | Tools | What they do |
| --- | --- | --- |
| Chats and groups | `get_chats`, `get_chat_history`, `get_message` | List and search your conversations, read a chat or group in order, get one message |
| Latest activity | `get_last_incoming_messages`, `get_last_outgoing_messages` | What you received or sent recently, across all chats |
| Groups | `get_group` | Name, description, admins and participants |
| Send | `send_text_message`, `send_image`, `send_document`, `send_audio`, `send_video`, `send_location`, `send_contact`, `send_poll`, `forward_messages` | Text, files by public URL, locations, contact cards, polls and forwards |
| Account | `get_account_status` | Plan, linked number, daily usage and quota |

Every tool declares MCP annotations (`readOnlyHint`, `destructiveHint`,
`idempotentHint`, `openWorldHint`). Send tools are marked destructive, so the
assistant asks for confirmation. A successful send means the message was
**queued** (with a `queue_id`), not yet delivered.

## How it works

```text
Gemini app / Gemini CLI / Antigravity
        |  OAuth 2.1: discovery, dynamic client registration, PKCE S256
        v
https://wapliss.com/mcp/v1   (Streamable HTTP, MCP 2025-11-25 and earlier)
        |
Wapliss WhatsApp engine  --->  WhatsApp
```

- Protected resource metadata: `https://wapliss.com/.well-known/oauth-protected-resource/mcp/v1`
- Authorization server metadata: `https://wapliss.com/.well-known/oauth-authorization-server`
- Scopes: `wapliss:mcp`, `whatsapp:read`, `whatsapp:write`
- Refresh tokens are not rotated for Google redirect URIs (Persistent Linking);
  unlinking in Gemini revokes the whole grant.
- `/mcp/v1` keeps fixed English tool definitions; breaking changes ship on
  `/mcp/v2` while `v1` stays live.

## Security and privacy

- **Your own account only.** The assistant can reach only the WhatsApp account
  linked to your Wapliss account, and only when you ask.
- **No credentials in the chat.** Never paste passwords, API keys, QR data or
  session data into a conversation; this package contains none either.
- **Confirmation before sending.** Ambiguous recipients or texts are confirmed
  first; bulk or unsolicited messaging is not allowed.
- **Revocable at any time** from the Wapliss dashboard.
- **Limits:** daily plan quota and 60 MCP calls per minute per user.
- [Privacy policy](https://wapliss.com/privacy-policy) ·
  [Terms of service](https://wapliss.com/terms-of-service)

## FAQ

**Is it free?** Yes, there is a free plan to start, with no credit card.

**Does it use the official WhatsApp Business Platform?** No. Wapliss links
your number as a WhatsApp linked device, like WhatsApp Web, so it works with
your personal or business number without a Meta Business account. Use it for
your own conversations and follow WhatsApp's terms.

**Can the assistant send messages on its own?** No. It only acts when you ask,
confirms ambiguous sends and refuses bulk or unsolicited messages.

**Where are my messages stored?** In your private Wapliss account, so the
assistant can read them when you ask. What the assistant reads is processed by
its AI provider. See the [privacy policy](https://wapliss.com/privacy-policy).

**Can I use several assistants at once?** Yes. Each one is authorized
separately and can be revoked separately.

**Why `/mcp/v1`?** Google Connected Apps snapshots tool definitions per
version, so Wapliss serves a stable, versioned endpoint for Gemini.

**Custom apps in the Gemini app** need a personal Google account, the app in
English and a supported country.

## Troubleshooting

| Message from Wapliss | What it means | What to do |
| --- | --- | --- |
| `account_awaiting_qr` / `instance_not_connected` | No phone is linked to this Wapliss account | Link it at [wapliss.com/app/connect](https://wapliss.com/app/connect) |
| `account_disconnected` | WhatsApp closed the linked session | Scan the QR code again |
| `quota_exceeded` | Daily message quota reached | Wait for the reset or upgrade the plan |
| Rate limit (`-32300` / HTTP 429) | More than 60 calls in a minute | Wait the seconds indicated |
| `chat_not_found` | No chat matches the name or number | Search with another name or the full number with country code |

## Package layout

```text
plugin.json                       Antigravity plugin manifest
mcp_config.json                   Antigravity MCP server (serverUrl)
gemini-extension.json             Gemini CLI extension manifest (httpUrl + OAuth)
GEMINI.md / rules/GEMINI.md       Context and always-on rule (same text)
skills/wapliss-whatsapp/SKILL.md  Usage rules for the agent
assets/logo.png                   512 × 512 logo
connected-apps/listing.json       Values for the Google Connected Console
connected-apps/SUBMISSION.md      Submission checklist
scripts/validate.py               Package checks (--live also checks the endpoint)
```

## Development

```bash
python3 scripts/validate.py          # offline checks
python3 scripts/validate.py --live   # plus endpoint and OAuth metadata
gemini extensions validate .         # Gemini CLI
agy plugin validate --strict .       # Antigravity
```

Bump `version` in `plugin.json` and `gemini-extension.json`. Do not change tool
names or schemas inside `/mcp/v1`.

## Wapliss plugins

Wapliss works the same way in every assistant: one account, one linked phone,
the same 16 tools.

| Assistant | Where it works | Format | Get it |
| --- | --- | --- | --- |
| Claude | Claude.ai, Claude Desktop, Claude Code | Custom connector / Claude plugin | [github.com/proteuscrypto/wapliss-whatsapp-for-claude](https://github.com/proteuscrypto/wapliss-whatsapp-for-claude) |
| ChatGPT | ChatGPT web and desktop | ChatGPT plugin (Agent Plugins) / custom MCP connector | [github.com/proteuscrypto/wapliss-for-chatgpt](https://github.com/proteuscrypto/wapliss-for-chatgpt) |
| **Gemini** | Gemini app, Gemini CLI, Antigravity | Connected app, Gemini CLI extension, Antigravity plugin | this repository |
| DeepSeek | DeepSeek Harness (dsh) | dsh bundle | [github.com/proteuscrypto/wapliss-for-deepseek](https://github.com/proteuscrypto/wapliss-for-deepseek) |
| GitHub Copilot | VS Code, Copilot CLI, Copilot app | Agent Plugins 1.0 | [github.com/proteuscrypto/wapliss-for-copilot](https://github.com/proteuscrypto/wapliss-for-copilot) |
| Grok | Grok Build, grok.com connectors, xAI API | Grok Build plugin / custom MCP connector | [github.com/proteuscrypto/wapliss-for-grok](https://github.com/proteuscrypto/wapliss-for-grok) |
| Any MCP client | Clients with remote MCP (Streamable HTTP) | OAuth 2.1, or a personal API key | [wapliss.com/integrations#mcp](https://wapliss.com/integrations#mcp) |

## Credits and support

- **Created and maintained by [NetDigitalTech](https://github.com/netdigitaltech)**, the company that
  created and owns [Wapliss](https://wapliss.com/).
- Support: [open an issue](https://github.com/proteuscrypto/wapliss-for-gemini/issues) in this repository.
- Integration guides: [English](https://wapliss.com/integrations#gemini) ·
  [Español](https://wapliss.com/integraciones#gemini)

## Español

**Wapliss WhatsApp para Gemini**: conecta tu propio WhatsApp a
Gemini con el servidor MCP de Wapliss. Lee y resume chats y grupos y
envía mensajes, archivos, ubicaciones y encuestas, siempre con tu confirmación.

Cómo empezar: crea tu cuenta gratis en wapliss.com y vincula tu teléfono. En
la app de Gemini agrega una app personalizada con `https://wapliss.com/mcp/v1`;
en Gemini CLI ejecuta `gemini extensions install https://github.com/proteuscrypto/wapliss-for-gemini`
y `/mcp auth wapliss`; en Antigravity, `agy plugin install ./wapliss-for-gemini`.

Ejemplos: *"Muéstrame mis últimos mensajes de WhatsApp"*, *"Resume lo que se
habló hoy en el grupo de la familia"*, *"Envía 'Llego en 10 minutos' a
+54 9 11 5555 0100"*. Creado y mantenido por **[NetDigitalTech](https://github.com/netdigitaltech)**,
la empresa creadora y dueña de [Wapliss](https://wapliss.com/). Guía completa:
[wapliss.com/integraciones#gemini](https://wapliss.com/integraciones#gemini).

## Trademarks and license

Gemini, Google and Antigravity are trademarks of Google LLC. WhatsApp is a trademark of Meta Platforms, Inc. Wapliss is
an independent service and is not affiliated with, sponsored or endorsed by
Meta, WhatsApp or Google.

Released under the [MIT License](LICENSE). © 2026 NetDigitalTech, creator and owner of Wapliss.
