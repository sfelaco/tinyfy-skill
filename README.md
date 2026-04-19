# Skills Collection

A collection of useful skills for AI coding assistants. Each skill is designed to extend the capabilities of the assistant, providing specialized tools for various tasks.

## Available Skills

- **[tinyfy](skills/tinyfy/SKILL.md)**: A skill for compressing and resizing images using the TinyPNG API. It includes a Python CLI wrapper and handles automatic optimization within the assistant's workflow.
- **[telegram-send](skills/telegram-send/SKILL.md)**: A skill to send text messages and files to a Telegram chat directly via the HTTP Bot API using `curl`. It works without external dependencies or persistent connections.

## Installation

You can install skills from this collection using the following command:

```bash
npx skills add https://github.com/sfelaco/skills-collection --skill <skill-name>
```

Replace `<skill-name>` with the name of the skill you want to install (e.g., `tinyfy` or `telegram-send`).

## How to use

After installation, the skill is added to your local assistant configuration. Each skill folder contains a `SKILL.md` file with specific documentation, requirements, and configuration instructions.

## Contributing

Feel free to suggest new skills or improvements to existing ones by opening an issue or a pull request.

## License

Apache 2.0 — see [LICENSE](LICENSE).
