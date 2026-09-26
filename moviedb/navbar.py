"""
Navbar definition.

Each entry is either a top-level link::

    {"type": "item", "text": "Home", "viewname": "Index"}

or a dropdown holding links::

    {"type": "dropdown", "text": "Browse", "items": [{"text": ..., "viewname": ...}]}

``viewname`` is a URL name resolved with ``reverse()``.
"""

NAVBAR = [
    {
        "type": "dropdown",
        "text": "Browse",
        "items": [
            {"text": "Browse Movies", "viewname": "BrowseMovie"},
            {"text": "Browse Actors", "viewname": "BrowseActor"},
            {"text": "Browse Directors", "viewname": "BrowseDirector"},
        ],
    },
    {
        "type": "dropdown",
        "text": "Add",
        "items": [
            {"text": "Add Movies", "viewname": "AddMovie"},
            {"text": "Add Actors/Directors", "viewname": "AddActorDirector"},
            {"text": "Add Actors to Movies", "viewname": "AddActorMovie"},
            {"text": "Add Directors to Movies", "viewname": "AddDirectorMovie"},
        ],
    },
    {
        "type": "dropdown",
        "text": "Reviews",
        "items": [
            {"text": "Browse Movie Reviews", "viewname": "BrowseReview"},
            {"text": "Write a Movie Review", "viewname": "WriteReview"},
        ],
    },
]
