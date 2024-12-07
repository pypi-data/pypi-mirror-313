import os
import importlib.util

# Module provider.PlanqkQuantumProvider must be loaded dynamically to avoid partial initialization error
provider_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'provider.py'))
spec = importlib.util.spec_from_file_location('provider', provider_path)
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)

PlanqkQuantumProvider = provider.PlanqkQuantumProvider
