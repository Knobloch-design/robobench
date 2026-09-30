# Task demonstrations

Every task needs two demonstrations before it can join the suite: one success and one failure.

```
demos/
  leap__cube_reorientation/      task name, with "/" replaced by "__"
    success.npz  success.json
    failure.npz  failure.json
```

Record them with `robobench.tasks.demonstrations.record_demonstration` (see
`examples/record_demonstrations.py`), then check them with:

```bash
robobench validate-task leap/cube_reorientation
```

No demonstrations have been recorded yet; the tasks in this library are still stubs.
