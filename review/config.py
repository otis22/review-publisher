def parse_projects_channels(projects_channels):
    projects = projects_channels.split(",")
    result = []
    for project in projects:
        project = project.split("#")
        result.append(
            {"project_path": project[0], "slack_channel": "#" + project[1]}
        )
    return result
