def format_link(link: str, allowed_domain: str) -> str:
    """
    Format the link to be used in the database.

    :param allowed_domain:
    :param link: The link to be formatted.
    :type link: str
    :return: The formatted link.
    :rtype: str
    """
    # if link starts with /, add the allowed domain
    if link.startswith('/'):
        return f"https://{allowed_domain}{link}"

    return link
