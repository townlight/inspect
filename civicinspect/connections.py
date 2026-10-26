"""Resolve immutable, explicitly public Code evidence through trusted providers."""
import hashlib


class SourceUnavailable(RuntimeError):
    pass


def resolve(providers, link):
    try:
        rows = providers[link["provider"]](source_id=link["source_id"])
        if not isinstance(rows, (tuple, list)) or len(rows) != 1:
            raise ValueError("Source did not resolve exactly once")
        source = rows[0]
        digest = hashlib.sha256(source["text"].encode("utf-8")).hexdigest()
        if (source["visibility"] != "public" or source["source_id"] != link["source_id"]
                or digest != source["sha256"] or digest != link["expected_sha256"]):
            raise ValueError("Source changed or restricted")
        return {k: source[k] for k in ("source_id", "version", "title", "citation", "text", "sha256", "visibility")}
    except Exception:
        raise SourceUnavailable("Connected source unavailable, changed or restricted; saved work retained. Select current evidence before continuing.") from None


def search(providers, provider, query):
    if provider not in ("code",) or not 1 <= len(query.strip()) <= 500:
        raise ValueError("Choose Code and enter a search term.")
    try:
        rows = providers[provider](query=query)
        if not isinstance(rows, (tuple, list)):
            raise ValueError("Invalid results")
        result = []
        for row in rows[:50]:
            if row.get("visibility") != "public":
                continue
            item = resolve(providers, {"provider": provider, "source_id": row["source_id"], "expected_sha256": row["sha256"]})
            result.append({k: v for k, v in item.items() if k != "text"} | {"excerpt": item["text"][:500]})
        return {"results": result, "truncated": len(rows) > 50}
    except SourceUnavailable:
        raise
    except Exception:
        raise SourceUnavailable("Connected source search unavailable; no sample or cached substitute.") from None
