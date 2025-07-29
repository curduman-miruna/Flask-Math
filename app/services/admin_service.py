from prometheus_client import REGISTRY


def get_admin_metrics():
    data = []
    for metric in REGISTRY.collect():
        metric_entry = {
            "name": metric.name,
            "type": metric.type,
            "documentation": metric.documentation,
            "samples": [],
        }
        for sample in metric.samples:
            metric_entry["samples"].append(
                {
                    "name": sample.name,
                    "labels": sample.labels,
                    "value": sample.value,
                    "timestamp": getattr(sample, "timestamp", None),
                }
            )
        data.append(metric_entry)
    return data
