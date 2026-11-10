# Submitting Wapliss to Google Connected Apps (Gemini app)

Source: Google Connected Apps Platform docs (developers.google.com/connected-apps),
checked 10 November 2026. Values to paste are in `listing.json`.

## 0. Before you start

- [ ] Access to the **Connected Apps Platform** preview (interest form). The
      preview opens in phases; reports say it starts with US developers.
- [ ] CS-08 deployed: `python3 scripts/validate.py --live` passes, except the
      domain-verification warning until step 3.
- [ ] Demo account (email + password, **no 2FA**) with a permanently linked demo
      WhatsApp, the chat "Demo Contact" and the group "Demo Group".

## 1. Create the app

Connected Console > **Create app**. Accept the Connected Apps Terms (account
admin only). Name **Wapliss**, category **Communication**, connection type
**MCP server**. Category and connection type cannot be changed later.

## 2. App details

Icon `assets/logo.png` (512 x 512 PNG, under 1 MB). Description (under 30 words),
at least 3 capabilities, at least 3 example prompts (2 start with `@Wapliss`, 1
mentions Wapliss naturally), Spanish translation, Terms URL, Privacy URL and
website: all in `listing.json` > `app`.

## 3. Endpoint and domain

- MCP endpoint: `https://wapliss.com/mcp/v1`
- Download the verification file and publish its content at
  `https://wapliss.com/.well-known/google-connected-apps` (HTTP 200, no
  redirects). The server reads it from the `GOOGLE_CONNECTED_APPS_VERIFICATION`
  environment variable (Cloud Run) or from the constant of the same name in
  `server.ts`.

## 4. Access credentials

**User-delegated (Authorization Code)** with **Dynamic Client Registration**.
Google's redirect URIs are accepted by the Wapliss DCR (HTTPS, exact match per
registered client).

## 5. Test account

Paste the demo credentials (owner only) and the instructions in
`listing.json` > `test_account`. Google may reject the app if it cannot test
everything.

## 6. Sync tools

**Sync tools** must list 16 tools with no "Must fix" items. The snapshot is
frozen for this version: any change needs a new version and endpoint.

## 7. Availability and tool settings

Countries, languages (en, es), product **Gemini app**. Require user
confirmation for the 9 send tools (`listing.json` > `tool_settings`). No
context signals.

## 8. Testers

Add Gmail testers, wait up to 10 minutes, then test with `@Wapliss` and natural
language: sign-in, each read tool, one send to Demo Contact with confirmation,
and a refused bulk send.

## 9. Review and publish

Releases > **Send for review**. Fix and resubmit if needed. When approved,
**Publish**.

## Testing before access (Developer Mode)

gemini.google.com > Settings > **Gemini Apps Developer Mode** (or
gemini.google.com/devmode) > **+ Create new** > `https://wapliss.com/mcp/v1`.
Inspect the Event Log, Tool Schemas (safety badges) and Authentication tabs.
Custom apps currently require a personal Google account, 18+, English, Keep
Activity on, and a supported country.
