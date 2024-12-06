# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from .types import InputData
from .utils import format_as_json

hashtag_examples = [
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#test"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "nohash"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#with-dash_under"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#with white space"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#with(subtag)"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#with123"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#1234"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#CamelCase"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#ümläütß"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#🐄"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#❤️"},
    },
    {
        "content": "text",
        "tag": {"type": "Hashtag", "name": "#牛"},
    },
    {
        "content": "text",
        "tag": {
            "type": "Hashtag",
            "name": "#test",
            "url": "https://ignore.example",
        },
    },
    {
        "content": "text",
        "tag": {"type": "as:Hashtag", "name": "#test"},
    },
    {
        "content": "text",
        "tag": {"name": "#test"},
    },
]


def mastodon_hashtag(x):
    if not x:
        return ""
    tags = x.get("tags", [])
    if len(tags) == 0:
        return ""
    return tags[0]["name"]


def firefish_hashtag(x):
    if not x:
        return ""
    tags = x.get("tags", [])
    if len(tags) == 0:
        return ""
    return tags[0]


data = InputData(
    title="Hashtags",
    frontmatter="""The following mostly illustrates how the
name of a hashtag gets transformed by the applications. The input has the form

```json
"tag": {"type": "Hashtag", "name": "${tag}"}
```

The last two examples illustrate more technical behavior.
""",
    filename="hashtags.md",
    examples=hashtag_examples,
    detail_table=True,
    detail_extractor={
        "activity": lambda x: format_as_json(x.get("object", {}).get("tag")),
        "mastodon": lambda x: format_as_json(x.get("tags")),
        "firefish": lambda x: format_as_json(x.get("tags")),
    },
    detail_title={
        "mastodon": "| tag | tags | Example |",
        "firefish": "| tag | tags | Example |",
    },
    support_table=True,
    support_title="tag",
    support_result={
        "activity": lambda x: x["object"]["tag"].get("name", ""),
        "mastodon": mastodon_hashtag,
        "firefish": firefish_hashtag,
    },
)
