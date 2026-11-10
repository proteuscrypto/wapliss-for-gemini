---
name: wapliss-whatsapp
description: >
  Use when the user wants to read their WhatsApp chats, group messages or group
  members, see their latest received or sent WhatsApp messages, send a WhatsApp
  text, image, document, audio, video, location, contact card or poll, forward
  a WhatsApp message, or check their Wapliss account. Examples: "Show my latest
  WhatsApp messages", "What did they say in the family group?", "Send 'On my
  way' to Alex on WhatsApp", "Check my Wapliss account".
license: MIT
---

# Wapliss WhatsApp

Use the `wapliss` MCP server (`https://wapliss.com/mcp/v1`). Reply in the
user's language. Sign-in is OAuth in the browser; never ask for API keys,
WhatsApp credentials, QR data or tokens in the chat.

## Getting started

1. Authenticate the `wapliss` server when prompted and sign in to (or create)
   a Wapliss account at https://wapliss.com.
2. Link the phone once at https://wapliss.com/app/connect (WhatsApp > Linked
   devices > Link a device, then scan the QR code).
3. Ask, for example, "Show me my latest WhatsApp messages".

If a tool answers `account_awaiting_qr`, `account_disconnected` or
`instance_not_connected`, the phone is not linked: give the user the action URL
from the error.

## Tools

Read (only the authenticated user's own account):

| Tool | Use it to | Key arguments |
| --- | --- | --- |
| `get_chats` | List or find chats and groups | `query`, `type` (`all`, `individual`, `group`), `unread_only`, `limit` (1-50), `cursor` |
| `get_chat_history` | Read one chat or group | `chat_id` (from `get_chats`, a +number or the exact name), `limit`, `before` |
| `get_message` | Get one message | `chat_id`, `message_id` |
| `get_last_incoming_messages` | Latest received messages, all chats | `limit`, `since` (ISO 8601), `include_groups` |
| `get_last_outgoing_messages` | Latest sent messages, all chats | `limit`, `since` |
| `get_group` | Group name, description, admins, participants | `chat_id`, `refresh` |
| `get_account_status` | Plan, usage, quota, link status | none |

Send (state-changing, cannot be recalled):

| Tool | Arguments |
| --- | --- |
| `send_text_message` | `chat_id`, `text` |
| `send_image` | `chat_id`, `url`, optional `caption` |
| `send_document` | `chat_id`, `url`, `file_name`, optional `caption` |
| `send_audio` | `chat_id`, `url` |
| `send_video` | `chat_id`, `url`, optional `caption` |
| `send_location` | `chat_id`, `latitude`, `longitude`, optional `name`, `address` |
| `send_contact` | `chat_id`, `contact_phone`, `contact_name` |
| `send_poll` | `chat_id`, `question`, `options` (2-12) |
| `forward_messages` | `chat_id`, `message_ids` |

`chat_id` values come from `get_chats` (`pn:...` for people, `grp:...` for
groups) or are phone numbers with country code (`+5492995551234`). Media URLs
must be public HTTPS links.

## Sending safely

- Send only what the user asked for. If the recipient or the content is
  ambiguous, confirm the exact recipient and text first.
- To find a recipient by name, call `get_chats` with `query`. If several chats
  match, ask which one. Never invent numbers or chat IDs.
- Never send bulk or unsolicited messages, and never turn a one-to-one request
  into a broadcast.
- A successful send means the message was **queued**. Report the `queue_id`
  and status; do not claim delivery.

## Reading safely

- Read only the chats the user asked about. Start with a small `limit` and page
  with `before` only when more is needed.
- Summarize instead of copying long histories; quote exact text only when the
  user asks. Show group members' phone numbers only when needed.
- Never forward or send content you read unless the user asks and confirms the
  recipient.

## Errors

- Account errors carry an `action_url`: explain the message and give the link.
- `quota_exceeded`: report the message; do not promise a reset time.
- Rate limits (`-32300`) include a wait time; do not retry in a loop.
- `chat_not_found` or an empty history: say so plainly instead of guessing.
- Not available yet: contact book search, checking whether a number has
  WhatsApp, group management, editing or deleting messages, marking as read,
  archiving. Say so if asked; do not invent results.
