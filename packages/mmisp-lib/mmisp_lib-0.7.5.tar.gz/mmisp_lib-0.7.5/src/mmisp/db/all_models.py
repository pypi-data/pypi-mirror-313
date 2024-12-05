import importlib
import importlib.resources
import itertools

model_pkg = "mmisp.db.models"
all_models = (
    resource.name[:-3]
    for resource in importlib.resources.files(model_pkg).iterdir()
    if resource.is_file() and resource.name != "__init__.py"
)

model_module_names = map(".".join, zip(itertools.repeat(model_pkg), all_models))

for m in model_module_names:
    importlib.import_module(m)

importlib.import_module("mmisp.db.additional_properties")
