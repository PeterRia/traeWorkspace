import os
import sys


def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def is_frozen():
    return bool(getattr(sys, "frozen", False))


def resource_root():
    if is_frozen() and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return project_root()


def writable_root():
    if is_frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    return project_root()


def bundled_asset_root():
    return os.path.join(resource_root(), "assets")


def generated_asset_root():
    if is_frozen():
        return os.path.join(writable_root(), "assets")
    return os.path.join(project_root(), "assets")


def generated_asset_path(*parts):
    return os.path.join(generated_asset_root(), *parts)


def resolve_asset(*parts):
    generated = generated_asset_path(*parts)
    if os.path.exists(generated):
        return generated
    bundled = os.path.join(bundled_asset_root(), *parts)
    if os.path.exists(bundled):
        return bundled
    return generated


def save_dir():
    return os.path.join(writable_root(), "saves")


def save_file():
    return os.path.join(save_dir(), "save_data.json")


def screenshots_dir():
    return os.path.join(writable_root(), "screenshots")


def ensure_runtime_dirs():
    for path in [
        save_dir(),
        screenshots_dir(),
        generated_asset_path("images"),
        generated_asset_path("sounds"),
    ]:
        os.makedirs(path, exist_ok=True)
