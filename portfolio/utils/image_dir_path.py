def project_dir_path(instance, filename):
    return f"projects/{instance.portfolio.owner.username}/{instance.name}/{filename}"


def skill_dir_path(instance, filename):
    return f"skills/{instance.portfolio.owner.username}/{instance.name}/{filename}"
