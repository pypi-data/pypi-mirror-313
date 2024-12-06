def add_version_to_metadata(model, **kwargs):
    schema = model.schema["record"]["properties"]
    if "metadata" not in schema:
        return
    schema["metadata"].setdefault("properties", {}).setdefault(
        "version",
        {
            "type": "keyword",
            "sample": ["1.0", "1.1", "2.0", "2.1", "2.2"],
            "label.cs": "Verze zdroje",
            "label.en": "Resource version",
            "hint.cs": "Zapište verzi (první, druhá…).",
            "hint.en": "Write down the version (first, second…).",
        },
    )
