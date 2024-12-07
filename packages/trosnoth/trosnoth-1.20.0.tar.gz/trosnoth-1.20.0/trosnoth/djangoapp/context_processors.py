from trosnoth import version


def version_processor(request):
    return {
        'version': version.version,
        'release': version.release,
        'title_version': version.title_version,
    }
