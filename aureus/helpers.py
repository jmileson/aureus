from urllib.parse import urljoin

URL_SEP = '/'


def format_url_tail(tail):
    if tail.startswith(URL_SEP):
        tail = tail[1:]

    if tail.endswith(URL_SEP):
        tail = tail[:-1]

    return tail


def format_resource_head(head):
    if head.startswith(URL_SEP):
        head = head[1:]

    if not head.endswith(URL_SEP):
        head += URL_SEP

    return head


def resource_join(*args):
    head, *tail = args

    if not tail:
        return format_url_tail(head)

    return urljoin(format_resource_head(head), resource_join(*tail))
