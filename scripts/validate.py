#!/usr/bin/env python3
"""Validate the Wapliss Gemini package (Antigravity plugin, Gemini CLI extension, Connected Apps listing).

Usage:
  python3 scripts/validate.py          # offline checks
  python3 scripts/validate.py --live   # also checks the hosted MCP endpoint and OAuth metadata
Exit code 0 means no errors. For the official Antigravity check also run:
  agy plugin validate --strict .
"""
import json, re, struct, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(rel):
    try:
        return json.loads((ROOT / rel).read_text())
    except Exception as e:  # noqa: BLE001
        err(f"{rel}: invalid JSON ({e})")
        return {}


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


plugin = load("plugin.json")
mcp = load("mcp_config.json")
ext = load("gemini-extension.json")
listing = load("connected-apps/listing.json")

# Antigravity plugin.json
allowed = {"$schema", "name", "displayName", "description", "version", "logo", "suggestedPrompts", "skills",
           "disabled", "author", "homepage", "repository", "license", "keywords", "extensions"}
extra = set(plugin) - allowed
if extra:
    err(f"plugin.json: unknown fields {sorted(extra)} (schema has additionalProperties: false)")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", plugin.get("name", "")):
    err("plugin.json: name must be lowercase kebab-case")
for field in ("displayName", "description", "version", "logo"):
    if not plugin.get(field):
        err(f"plugin.json: {field} is required for the Marketplace")
d = plugin.get("description", "")
if not 120 <= len(d) <= 160:
    warn(f"plugin.json: description is {len(d)} characters (120-160 recommended)")
if len(plugin.get("suggestedPrompts", [])) > 3:
    err("plugin.json: suggestedPrompts allows at most 3 items")
if any(k != k.lower() for k in plugin.get("keywords", [])):
    warn("plugin.json: keywords should be lowercase")
if not re.fullmatch(r"\d+\.\d+\.\d+([-+].+)?", plugin.get("version", "")):
    err("plugin.json: version must be SemVer")

logo = ROOT / plugin.get("logo", "missing")
if logo.exists():
    size = png_size(logo)
    if not size:
        err("logo: must be a PNG")
    else:
        w, h = size
        if w != h or w < 128:
            err(f"logo: must be square and at least 128 px (is {w}x{h})")
        if w != 512:
            warn(f"logo: Connected Console asks for 512x512 (is {w}x{h})")
    if logo.stat().st_size > 1024 * 1024:
        err("logo: Connected Console limit is 1 MB")
else:
    err("logo: file not found")

# mcp_config.json (Antigravity)
servers = mcp.get("mcpServers", {})
if list(servers) != ["wapliss"]:
    err("mcp_config.json: expected exactly one server named 'wapliss'")
url = servers.get("wapliss", {}).get("serverUrl", "")
if url != "https://wapliss.com/mcp/v1":
    err("mcp_config.json: serverUrl must be https://wapliss.com/mcp/v1")

# gemini-extension.json (Gemini CLI)
if ext.get("name") != plugin.get("name"):
    err("gemini-extension.json: name must match plugin.json")
if ext.get("version") != plugin.get("version"):
    err("gemini-extension.json: version must match plugin.json")
gsrv = ext.get("mcpServers", {}).get("wapliss", {})
if gsrv.get("httpUrl") != url:
    err("gemini-extension.json: httpUrl must match mcp_config.json serverUrl")
if not gsrv.get("oauth", {}).get("enabled"):
    err("gemini-extension.json: oauth.enabled must be true")
ctx = ext.get("contextFileName")
if ctx and not (ROOT / ctx).exists():
    err(f"gemini-extension.json: contextFileName {ctx} not found")
if (ROOT / "GEMINI.md").read_text() != (ROOT / "rules/GEMINI.md").read_text():
    err("GEMINI.md and rules/GEMINI.md must be identical")

# Skills
for skill in (ROOT / "skills").glob("*/SKILL.md"):
    text = skill.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{skill}: missing YAML frontmatter")
        continue
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    if not name or name.group(1) != skill.parent.name:
        err(f"{skill}: frontmatter name must match the directory name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", skill.parent.name) or len(skill.parent.name) > 64:
        err(f"{skill}: skill name must be kebab-case, 1-64 characters")
    desc = re.search(r"^description:\s*>?\s*\n?((?:\s+.*\n?)+|.*)", fm, re.M)
    if not desc or not 1 <= len(" ".join(desc.group(1).split())) <= 1024:
        err(f"{skill}: description must be 1-1024 characters")

# Connected Apps listing
app = listing.get("app", {})
if len(app.get("description", "").split()) >= 30:
    err("listing: description must be under 30 words")
if len(app.get("capabilities", [])) < 3:
    err("listing: at least 3 capabilities")
if any(re.match(r"^\d", c) for c in app.get("capabilities", [])):
    err("listing: capabilities must not start with numbers")
prompts = app.get("example_prompts", [])
if len(prompts) < 3:
    err("listing: at least 3 example prompts")
if sum(p.startswith("@" + app.get("name", "")) for p in prompts) < 2:
    err("listing: at least 2 example prompts must start with @<AppName>")
if not any(app.get("name", "") in p and not p.startswith("@") for p in prompts):
    err("listing: at least 1 example prompt must mention the app name naturally")
if listing.get("endpoint", {}).get("mcp_url") != url:
    err("listing: mcp_url must match mcp_config.json")

# Live checks
if "--live" in sys.argv:
    def get(u, data=None, headers=None):
        r = urllib.request.Request(u, data=data, headers=headers or {})
        try:
            with urllib.request.urlopen(r, timeout=20) as resp:
                return resp.status, resp.read().decode(), dict(resp.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode(), dict(e.headers)

    s, body, _ = get("https://wapliss.com/.well-known/oauth-authorization-server")
    asm = json.loads(body) if s == 200 else {}
    if s != 200 or "code" not in asm.get("response_types_supported", []) or not asm.get("registration_endpoint"):
        err("live: authorization server metadata missing code/registration_endpoint")
    s, body, _ = get("https://wapliss.com/.well-known/oauth-protected-resource/mcp/v1")
    if s != 200 or not json.loads(body).get("resource", "").endswith("/mcp/v1"):
        err("live: /mcp/v1 protected resource metadata not deployed (CS-08)")
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                          "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "validate", "version": "1"}}}).encode()
    s, _, hdrs = get(url, payload, {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    www = hdrs.get("WWW-Authenticate") or hdrs.get("www-authenticate") or ""
    if s != 401 or "mcp/v1" not in www:
        err(f"live: POST {url} without token should be 401 with v1 resource_metadata (got {s})")
    s, _, _ = get("https://wapliss.com/.well-known/google-connected-apps")
    if s != 200:
        warn("live: /.well-known/google-connected-apps not configured yet (needs the Connected Console token)")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
