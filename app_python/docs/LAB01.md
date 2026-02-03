## Framework selection

For this project, I chose the Flask web framework because:
1. I am most familiar with it;
2. its simplicity will help me to complete labs quickly in the future :)

| Framework | Asynchronous | Complex Features                                                                     | Learning Curve | Verdict                            |
| ---       | ---          | ---                                                                                  | ---            | ---                                |
| Flask     | NO           | ORM, authentication, caching                                                         | Easy to learn  | Fit for our purposes               |
| FastAPI   | YES          | Strongly typed models, automatic API documentation, WebSocket support                | Steep          | Too much setup for unused features |
| Django    | YES          | Robust ORM, extensive libraries (e.g., authentication, admin), scalable architecture | Steep          | Overkill for small projects        |

## Best Practices Applied
- Typed functions:
    ```python
    def get_system_info() -> dict[str, str | int | None]:
    def get_uptime() -> dict[str, int | str | None]:
    def word_plural(number: int) -> str:
    def get_request_info() -> dict[str, str | None]:
    ```
    This helps not forget what the functions expect as arguments and what output they return. Also, some LSPs (like my
    favorite, `pyright`) offer type checking when this is done.
- Docstrings:
    ```python
    def word_plural(number: int) -> str:
        """Used for grammar when composing human-readable uptime (uptime_human)"""
    ```
    Increases maintainability. Also, my IDE shows docstrings in tooltips, which is helpful.

## API Documentation
### Request/response examples
See next subsection (**Testing commands**).

### Testing commands

Index:
```sh
curl http://localhost:5000/ 2>/dev/null | jq
```
Response:
```json
{
  "endpoints": [
    {
      "description": "Service information",
      "method": "GET",
      "path": "/"
    },
    {
      "description": "Health check",
      "method": "GET",
      "path": "/health"
    }
  ],
  "request": {
    "client_ip": "127.0.0.1",
    "method": "GET",
    "path": "/",
    "user_agent": "curl/8.18.0"
  },
  "runtime": {
    "current_time": "2026-01-26T15:56:22.043+03:00",
    "timezone": "MSK",
    "uptime_human": "0 hours, 2 minutes",
    "uptime_seconds": 160
  },
  "service": {
    "description": "DevOps course info service",
    "framework": "Flask",
    "name": "devops-info-service",
    "version": "1.0.0"
  },
  "system": {
    "architecture": "x86_64",
    "cpu_count": 16,
    "hostname": "timur-ficus",
    "platform": "Linux",
    "platform_version": "#1 SMP PREEMPT_DYNAMIC Sun, 18 Jan 2026 00:34:07 +0000",
    "python_version": "3.14.2"
  }
}
```

Health:
```sh
curl http:///localhost:5000/health 2>/dev/null | jq
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-26T12:57:30.745116+00:00",
  "uptime_seconds": 229
}
```

## Testing Evidence

### Screenshots showing endpoints work

Main endpoint:

![Main endpoint](/app_python/docs/screenshots/01-main-endpoint.png)

Health check:

![Health check](/app_python/docs/screenshots/02-health-check.png)

Formatted output:

![Formatted output](/app_python/docs/screenshots/03-formatted-output.png)

### Terminal output
See section **API Documentation**, subsection **Testing commands**.

## Challenges & Solutions

When programming the endpoints, I encountered the problem of formatting `datetime` objects and converting between
timezones. But it was easy to find a solution on Stack Overflow:
[Stack Overflow](https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone).

I am familiar with writing small apps on Flask, so this framework did not present any challenges.

## GitHub Community

### Why Stars Matter

**Discovery & Bookmarking:**
- Stars help you bookmark interesting projects for later reference
- Star count indicates project popularity and community trust
- Starred repos appear in your GitHub profile, showing your interests

**Open Source Signal:**
- Stars encourage maintainers (shows appreciation)
- High star count attracts more contributors
- Helps projects gain visibility in GitHub search and recommendations

**Professional Context:**
- Shows you follow best practices and quality projects
- Indicates awareness of industry tools and trends

### Why Following Matters

**Networking:**
- See what other developers are working on
- Discover new projects through their activity
- Build professional connections beyond the classroom

**Learning:**
- Learn from others' code and commits
- See how experienced developers solve problems
- Get inspiration for your own projects

**Collaboration:**
- Stay updated on classmates' work
- Easier to find team members for future projects
- Build a supportive learning community

**Career Growth:**
- Follow thought leaders in your technology stack
- See trending projects in real-time
- Build visibility in the developer community

**GitHub Best Practices:**
- Star repos you find useful (not spam)
- Follow developers whose work interests you
- Engage meaningfully with the community
- Your GitHub activity shows employers your interests and involvement

