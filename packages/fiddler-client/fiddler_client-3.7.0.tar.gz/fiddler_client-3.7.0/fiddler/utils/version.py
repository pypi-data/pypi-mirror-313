from fiddler.schemas.server_info import Version


def match_semver(version: Version, match_expr: str) -> bool:
    """
    Match the version with match_expr
    :param version: Server version
    :param match_expr: Version to match with. Read more at VersionInfo.match
    :return: True if server version matches, otherwise False
    """
    if not version:
        return False

    if version.prerelease:
        return Version(version.major, version.minor, version.patch).match(match_expr)

    return version.match(match_expr)
