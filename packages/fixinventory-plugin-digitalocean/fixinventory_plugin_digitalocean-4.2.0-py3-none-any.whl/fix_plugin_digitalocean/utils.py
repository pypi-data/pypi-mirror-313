import logging
from datetime import datetime
from typing import Union, Callable, Any, Dict, Optional, Tuple, List

from fixlib.baseresources import DatabaseInstanceStatus


log = logging.getLogger("fix." + __name__)


def get_result_data(result: Dict[str, Any], value: Union[str, Callable[..., Any]]) -> Any:
    """Returns data from a DO API call result dict.

    Args:
        result: Dict containing the result
        value: Either directly the name of a key found in result or
            a callable like a lambda that finds the relevant data withing
            result.
    """
    data = None
    if callable(value):
        try:
            data = value(result)
        except Exception:
            log.exception(f"Exception while trying to fetch data calling {value}")
    elif value in result:
        data = result[value]
    return data


class RetryableHttpError(Exception):
    pass


def retry_on_error(e: Any) -> bool:
    if isinstance(e, RetryableHttpError):
        log.info(f"Got a retryable error {e}  - retrying")
        return True
    return False


def iso2datetime(ts: Optional[str]) -> Optional[datetime]:
    if ts is None:
        return None
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    if ts is not None:
        return datetime.fromisoformat(ts)


def region_id(slug: str) -> str:
    return f"do:region:{slug}"


def project_id(value: str) -> str:
    return f"do:project:{value}"


def droplet_id(value: int) -> str:
    return f"do:droplet:{value}"


def kubernetes_id(value: str) -> str:
    return f"do:kubernetes:{value}"


def volume_id(value: int) -> str:
    return f"do:volume:{value}"


def vpc_id(value: str) -> str:
    return f"do:vpc:{value}"


def snapshot_id(value: int) -> str:
    return f"do:snapshot:{value}"


def loadbalancer_id(value: int) -> str:
    return f"do:loadbalancer:{value}"


def floatingip_id(value: str) -> str:
    return f"do:floatingip:{value}"


def database_id(value: str) -> str:
    return f"do:dbaas:{value}"


def image_id(value: str) -> str:
    return f"do:image:{value}"


def size_id(value: str) -> str:
    return f"do:size:{value}"


def space_id(value: str) -> str:
    return f"do:space:{value}"


def app_id(value: str) -> str:
    return f"do:app:{value}"


def cdn_endpoint_id(value: str) -> str:
    return f"do:cdn_endpoint:{value}"


def certificate_id(value: str) -> str:
    return f"do:certificate:{value}"


def container_registry_id(value: str) -> str:
    return f"do:cr:{value}"


def container_registry_repository_id(registry_id: str, repository_id: str) -> str:
    return f"do:crr:{registry_id}/{repository_id}"


def container_registry_repository_tag_id(registry_id: str, repository_id: str, tag: str) -> str:
    return f"do:crrt:{registry_id}/{repository_id}:{tag}"


def ssh_key_id(value: str) -> str:
    return f"do:ssh_key:{value}"


def tag_id(value: str) -> str:
    return f"do:tag:{value}"


def domain_id(value: str) -> str:
    return f"do:domain:{value}"


def domain_record_id(value: str) -> str:
    return f"do:domain_record:{value}"


def firewall_id(value: str) -> str:
    return f"do:firewall:{value}"


def alert_policy_id(value: str) -> str:
    return f"do:alert:{value}"


def droplet_neighborhood_id(value: str) -> str:
    return f"do:neighborhood:{value}"


tag_value_sep: str = "--"


def parse_tag(tag: str) -> Optional[Tuple[str, Optional[str]]]:
    splitted = iter(tag.split(tag_value_sep, 1))
    key = next(splitted, None)
    if key is None:
        return None
    value = next(splitted, None)
    return (key, value)


def parse_tags(tags: List[str]) -> Dict[str, Optional[str]]:
    parsed_tags = {}
    for tag in tags:
        if parsed_tag := parse_tag(tag):
            key, value = parsed_tag
            parsed_tags[key] = value

    return parsed_tags


def dump_tag(key: str, value: Optional[str]) -> str:
    if value and len(value) > 0:
        return f"{key}{tag_value_sep}{value}"
    else:
        return f"{key}"


def get_db_status(db_status: str) -> DatabaseInstanceStatus:
    mapping = {
        "creating": DatabaseInstanceStatus.BUSY,
        "online": DatabaseInstanceStatus.AVAILABLE,
        "resizing": DatabaseInstanceStatus.BUSY,
        "migrating": DatabaseInstanceStatus.BUSY,
        "backing-up": DatabaseInstanceStatus.BUSY,
        "restoring": DatabaseInstanceStatus.BUSY,
        "maintenance": DatabaseInstanceStatus.BUSY,
        "failed": DatabaseInstanceStatus.FAILED,
        "offline": DatabaseInstanceStatus.STOPPED,
    }
    result = mapping.get(db_status, DatabaseInstanceStatus.UNKNOWN)
    return result
