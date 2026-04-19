---
name: telegram-send
description: Send text messages and files to a Telegram chat via the HTTP Bot API. Uses curl directly, without MCP server or external dependencies. Use this skill whenever you need to send a message or document to Telegram, even if the MCP channel is inactive.
---

# Telegram Send

Send messages and files to a Telegram chat using the HTTP Bot API directly via `curl`. It doesn't require the MCP plugin or persistent connections.

## Configuration

Credentials are in `.env` in this skill's directory (`<project>/.claude/skills/telegram-send/.env`).

**Before sending any message**, read the `.env` file with the Read tool and verify that it contains `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. If the file doesn't exist or variables are missing, ask the user to provide them and write the file with this format:

```
TELEGRAM_BOT_TOKEN=<bot_token>
TELEGRAM_CHAT_ID=<chat_id>
```

To find the chat ID, the user can send a message to the bot and call `getUpdates`, or use `@userinfobot`.

To verify that the token is valid before sending:
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
```

## Sending a text message

For simple single-line messages:
```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"<CHAT_ID>","text":"Your message here","parse_mode":"HTML"}'
```

For multiline messages or with special characters (quotes, apostrophes, slashes), build the JSON with `node -e` to avoid escaping issues in the shell:

```bash
node -e "
const token = '<TOKEN>';
const chatId = '<CHAT_ID>';
const text = \`Line 1
Line 2 with <b>bold</b>
Line 3\`;
const body = JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML' });
const { execSync } = require('child_process');
const result = execSync(\`curl -s -X POST 'https://api.telegram.org/bot\${token}/sendMessage' -H 'Content-Type: application/json' -d '\${body.replace(/'/g, \"'\\\\''\")}'\`);
console.log(result.toString());
"
```

### Supported HTML Formatting

Use `parse_mode: "HTML"` (default) to format the text:

| Tag | Effect |
|-----|---------|
| `<b>text</b>` | **bold** |
| `<i>text</i>` | *italic* |
| `<u>text</u>` | underlined |
| `<s>text</s>` | ~~strikethrough~~ |
| `<code>text</code>` | `inline code` |
| `<pre>text</pre>` | code block |
| `<a href="url">text</a>` | link |

Avoid MarkdownV2: it requires escaping 18 special characters and is highly fragile.

### Long messages

Telegram accepts a maximum of 4096 characters per message. If the text is longer, split it into chunks and send multiple sequential requests.

## Sending a file or document

Use `sendDocument` with a multipart request:

```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendDocument" \
  -F chat_id="<CHAT_ID>" \
  -F document=@"/absolute/path/to/file.pdf" \
  -F caption="<b>Optional description</b>" \
  -F parse_mode="HTML"
```

Notes:
- The path to the file must be absolute (not relative)
- `caption` is optional, supports the same HTML formatting
- For images, you can use `sendPhoto` instead of `sendDocument`

## Error Handling

After each call, check the JSON response:

- **Success**: `"ok": true` — the message was sent. You can extract `message_id` from the response.
- **Error**: `"ok": false` — read `error_code` and `description` to understand the problem:

| error_code | Cause | Solution |
|-----------|-------|-----------|
| 401 | Invalid token | Update `TELEGRAM_BOT_TOKEN` in `.env` |
| 400 "chat not found" | Invalid chat ID | Update `TELEGRAM_CHAT_ID` in `.env` |
| 400 "can't parse entities" | Malformed HTML | Check the HTML tags in the message |
| No JSON | Network error | Check internet connection |

In case of a network error (`curl` doesn't return JSON), report the raw curl message to the user.
