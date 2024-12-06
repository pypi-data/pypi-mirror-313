from django.conf import settings


def get_settings():
    default = dict(
        run_gears_server_up_tasks=[],
        run_gears_server_down_tasks=[],
    )

    conf = getattr(settings, "GEARS", {})

    return {
        attr_name: conf.get(attr_name, default_value)
        for attr_name, default_value in default.items()
    }
