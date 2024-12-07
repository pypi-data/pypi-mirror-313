# Known issues and bugs

## Event bus connection limits

A single event bus server can only accepts as many concurrent connections as the `nofile` limit of the running process (4096 on interactive nodes of CC).
