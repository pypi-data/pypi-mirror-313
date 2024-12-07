version = '1.20.0'


def is_compatible(other):
    if other == version:
        return True
    if other.startswith('<'):
        return False
    if not (is_release(version) and is_release(other)):
        return False
    return version.split('.')[:2] == other.split('.')[:2]


def running_version_is_older(other):
    return get_comparison_tuple(version) < get_comparison_tuple(other)


def get_comparison_tuple(version_string):
    for release_stage, identifier in enumerate(['a', 'b', 'rc']):
        if identifier in version_string:
            numeric_part, candidate_number = version_string.split(identifier)
            break
    else:
        numeric_part = version_string
        candidate_number = 0
        release_stage = 3

    major, minor, micro = numeric_part.split('.')
    major = int(major)
    minor = int(minor)
    micro = int(micro)
    candidate_number = int(candidate_number)
    return (major, minor, micro, release_stage, candidate_number)


def is_release(version_string):
    return all(bit.isdigit() for bit in version_string.split('.'))


release = is_release(version)
title_version = f'Version {version}'
