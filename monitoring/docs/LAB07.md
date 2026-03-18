# Task 1

## Evidence

#### infoservice
![infoservice](/monitoring/docs/L7t1_infoservice.png)

#### grafana
![grafana](/monitoring/docs/L7t1_grafana.png)

#### loki
![loki](/monitoring/docs/L7t1_loki.png)

#### promtail
![promtail](/monitoring/docs/L7t1_promtail.png)

# Task 2

#### terminal output

![terminalout](/monitoring/docs/L7t2_terminalout.png)

#### grafana

![grafana](/monitoring/docs/L7t2_grafana.png)

# Task 3

#### panels

![panels](/monitoring/docs/L7t3_panels.png)

# Task 4

#### login page

![login page](/monitoring/docs/L7t4_login.png)

#### docker compose output

![docker compose output](/monitoring/docs/L7t4_compose.png)

# Task 5


## Architecture

```text
devops-infoservice
  ^
  |
  v
promtail -> loki <-> grafana
```

## Setup Guide

1. Run `docker compose up -d`.
2. Follow the detailed instructions on how to set up panels in the grafana webUI.

## Configuration

The configuration files are self-explanatory:
- promtail discovers docker containers, filters only the one that is the infoservice, labels the logs.
- loki stores the logs efficiently and indexes them once a day, vacuums once a week.

## Application Logging

I derived JSONFormatter class and used it.

## Dashboard

1. **Logs Table** (Logs visualization)
   - Shows recent logs from all apps
   - Query: `{app=~"devops-.*"}`

2. **Request Rate** (Time series graph)
   - Shows logs per second by app
   - Query: `sum by (app) (rate({app=~"devops-.*"} [1m]))`

3. **Error Logs** (Logs visualization)
   - Shows only ERROR level logs
   - Query: `{app=~"devops-.*"} | json | level="ERROR"`

4. **Log Level Distribution** (Stat or Pie chart)
   - Count logs by level (INFO, ERROR, etc.)
   - Query: `sum by (level) (count_over_time({app=~"devops-.*"} | json [5m]))`

## Production Config

The most important configuration is setting the security environment variables. Also, I allocated several GiB of memory
and several cores of CPU to the services in total.

## Testing

Run `docker compose ps` or check grafana.

## Challenges

Very difficult to configure. Luckily, the lecture provided a basic example.

