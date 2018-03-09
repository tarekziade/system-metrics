system-metrics
--------------

Generates system info metrics

- Runs in an asyncio loop
- Uses psutil to collect info
- Provides pluggable backends to send out the logs
- Built-in backends are stdout & gelf udp (for Graylog)

