# Metrics

## Statsd

Statsd allows us to send internal metrics for certain operations we want to monitor in Grafana.

### Sending events

There are currently four types of events we can send:

- `timer`
- `incr`
- `gauge`
- `set`

In order to send events, we must decide in advance the prefix we're going to use, which is what we'll be setting in Grafana. Prefixes have the following format, where each 'source' is separated by a dot `'.'`:

- "source_a.source_b.source_c"

> Note: We don't have yet a convention on prefixes.

**Example:**

We want to log the amount of successful and failed jobs, and also monitorize how much time jobs take to finish. From the `job.py` file:

```python
def job_finished(self, job):
    database_server = job.database_server
    executors = self._get_executors(job)

    if database_server in executors:
        executors[database_server].job_finished(job.id)
        statsd_prefix = f'tinybird.{statsd_client.region_machine}.jobs.{sanitize_database_server(database_server)}.{job.database}.{job.kind}'
        job_status = 'ok' if job.status != JobStatus.ERROR else 'error'
        statsd_client.incr(f'{statsd_prefix}.{job_status}')
        if job.updated_at is not None:
            statsd_client.timing(f'{statsd_prefix}.total', (job.updated_at - job.created_at).seconds)
        if job.started_at is not None:
            statsd_client.timing(f'{statsd_prefix}.working', (job.updated_at - job.started_at).seconds)
```

### Visualizing events

In Grafana, create a new panel and choose the following settings in the query:

```
Series > statsite > event_type (timers, gauges...) > source_a > ...
```

You can explore other pannels (for example, in the Jobs dashboard) to see different examples

### Testing it locally

Events are sent to the following server: `ops-metrics-1`. You can debug the server by entering via SSH and check the logs:

```
ssh ops-metrics-1
journalctl -u statsite
```

It's possible to test events locally by doing the following:

1. Forward startsd events from localhost:8125 to ops-metrics-1:8125:

```
ssh -L 8125:ops-metrics-1:8125 ops-metrics-1 -N -v
```

2. Add the `statsd_server` config in `default_secrets.py`:

```
statsd_server={
    'host': 'localhost',
    'type': 'tcp',
},
```

3. Run your analytics code locally and check directly in a testing panel in Grafana the events are being sent
