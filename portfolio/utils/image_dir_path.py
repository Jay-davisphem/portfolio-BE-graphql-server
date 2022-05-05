def project_dir_path(instance, filename):
    return f"projects/{instance.portfolio.owner.username}/{instance.portfolio.owner.password[-10:]}{instance.name}/{filename}"


def skill_dir_path(instance, filename):
    return f"skills/{instance.portfolio.owner.username}/{instance.portfolio.owner.password[-10:]}{instance.name}/{filename}"
