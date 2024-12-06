# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from .types import InputData
from .utils import format_as_json, safe_first_element

image_examples = [
    {
        "content": "Format png",
        "attachment": {
            "type": "Document",
            "url": "http://pasture-one-actor/images/001.png",
        },
    },
    {
        "content": "Format png",
        "attachment": {
            "type": "Document",
            "url": "http://pasture-one-actor/images/001b.png",
            "mediaType": "image/png",
        },
    },
    {
        "content": "Format jpg",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/002.jpg",
        },
    },
    {
        "content": "Format jpg",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/002b.jpg",
            "mediaType": "image/jpeg",
        },
    },
    {
        "content": "Format svg",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/assets/FediverseLogo.svg",
        },
    },
    {
        "content": "Format eps",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/003.eps",
        },
    },
    {
        "content": "Format gif",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/003b.gif",
        },
    },
    {
        "content": "Format tiff",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/003c.tiff",
        },
    },
    {
        "content": "Format webp",
        "attachment": {
            "type": "Image",
            "url": "http://pasture-one-actor/images/003d.webp",
        },
    },
    {
        "content": "url does not exit",
        "attachment": {
            "type": "Document",
            "url": "http://pasture-one-actor/assets/does_not_exist.png",
        },
    },
    {
        "content": "Wrong height / width",
        "attachment": {
            "type": "Document",
            "width": 13,
            "height": 17,
            "url": "http://pasture-one-actor/images/004.png",
        },
    },
    {
        "content": "No type",
        "attachment": {
            "url": "http://pasture-one-actor/images/005.png",
        },
    },
    {
        "content": "url is Link object",
        "attachment": {
            "type": "Image",
            "url": {
                "type": "Link",
                "href": "http://pasture-one-actor/images/006.png",
            },
        },
    },
    {
        "content": "url is Link object with media type",
        "attachment": {
            "type": "Image",
            "url": {
                "type": "Link",
                "href": "http://pasture-one-actor/images/006b.png",
                "mediaType": "image/png",
            },
        },
    },
    {
        "content": "url is Link object in an array",
        "attachment": {
            "type": "Image",
            "url": [
                {
                    "type": "Link",
                    "href": "http://pasture-one-actor/images/006c.png",
                }
            ],
        },
    },
    {
        "content": "url is array of two Link objects",
        "attachment": {
            "type": "Image",
            "url": [
                {
                    "type": "Link",
                    "href": "http://pasture-one-actor/images/007.png",
                    "mediaType": "image/png",
                },
                {
                    "type": "Link",
                    "href": "http://pasture-one-actor/images/008.jpg",
                    "mediaType": "image/jpeg",
                },
            ],
        },
    },
]


def mastodon_support(x):
    if not x:
        return "❌"
    media = x.get("media_attachments")
    if not media or len(media) == 0:
        return "-"
    comment = media[0].get("type", "-")
    if comment is None:
        return "-"
    return comment


def firefish_support(x):
    if not x:
        return "❌"
    media = x.get("files")
    if not media or len(media) == 0:
        return "-"
    comment = media[0].get("type", "-")
    if comment is None:
        return "-"
    return comment


data = InputData(
    title="Image Attachments",
    frontmatter="""The Image type is defined in
[ActivityStreams Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image).

In the following, we test how various configurations of it are rendered.

A ❌ in the support table means that the entire message has failed to parse. A "-" means that the message was parsed, but
no attachment was generated. The text, e.g. `image` or
`unknown` is the the media type the Fediverse application
determined for the attachment.

We furthermore wish to point out that having several links
in the `url` property is useful to both offer the attachment
in different formats and say dimensions, e.g. one high resolution
and one low resolution one.
""",
    filename="image_attachments.md",
    examples=image_examples,
    detail_table=True,
    detail_extractor={
        "activity": lambda x: format_as_json(x.get("object", {}.get("attachment"))),
        "mastodon": lambda x: format_as_json(
            safe_first_element(x.get("media_attachments"))
        ),
        "firefish": lambda x: format_as_json(x.get("files"))
        + format_as_json(x.get("fileIds")),
    },
    detail_title={
        "mastodon": "| attachment | media_attachments | Example |",
        "firefish": "| attachment | files | fileIds | Example |",
    },
    support_table=True,
    support_title="attachment",
    support_result={
        "activity": lambda x: format_as_json(x["object"]["attachment"], small=True)[0],
        "mastodon": mastodon_support,
        "firefish": firefish_support,
    },
)
