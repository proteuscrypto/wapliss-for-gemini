# Wapliss WhatsApp

- The `wapliss` MCP server works with the user's own WhatsApp account. Use it only for requests about the user's WhatsApp chats, groups, messages or Wapliss account.
- Before any send tool, make sure the recipient and the content are what the user asked for; confirm both when either is ambiguous. Never send bulk or unsolicited messages.
- Sends are queued: report the queue id and status, never claim delivery.
- Summarize what you read; do not dump raw JSON or long histories unless asked.
- Never ask for passwords, API keys, tokens or QR data in the chat. Sign-in is OAuth; phone linking happens at https://wapliss.com/app/connect.
