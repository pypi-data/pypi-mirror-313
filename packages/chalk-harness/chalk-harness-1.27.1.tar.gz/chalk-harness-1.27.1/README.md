# Chalk Harness

---
This package wraps [Chalk's CLI](https://github.com/chalk-ai/cli)
with Python to aid with testing.
---

Chalk enables innovative machine learning teams to focus on building
the unique products and models that make their business stand out.
Behind the scenes Chalk seamlessly handles data infrastructure with
a best-in-class developer experience.

---

## Example Usage

```python
harness = CLIHarness()
harness.apply_await(force=True)
version = harness.version()
assert version.version == "v0.4.5" == harness.version_tag_only()
print(harness.whoami().user)
print(harness.token().token)
```
