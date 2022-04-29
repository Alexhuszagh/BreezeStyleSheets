---
name: Custom pull request template
about: Pull request template for miscellaneous changes.
title: "[OTHER]"
labels: ''
assignees: Alexhuszagh

---

**NOTE:**
- If you have made any changes to the light or dark themes without extensions, please ensure to build the distribution files as part of your commit.

```bash
python configure.py --clean --pyqt6 \
    --compiled-resource breeze_resources.py
```

## Description
Please include a clear and concise description of the changes.
