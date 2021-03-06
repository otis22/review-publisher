def parse_projects_channels(projects_channels):
    assert projects_channels != ""
    projects = projects_channels.split(",")
    result = []
    for project in projects:
        project = project.split("#")
        result.append(
            {"project_path": project[0], "slack_channel": "#" + project[1]}
        )
    return result


def parse_stop_words(stop_words):
    return [] if stop_words == "" else stop_words.split(",")


def projects_by_channel(projects_channels):
    result = dict()
    for project_channel in projects_channels:
        if project_channel['slack_channel'] not in result:
            result[project_channel['slack_channel']] \
                = {project_channel['project_path']}
        else:
            result[project_channel['slack_channel']]\
                .add(project_channel['project_path'])
    return result
