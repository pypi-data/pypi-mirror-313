# Import all modules so that they can register themselvses to the registry.
from lisa.globalfit.framework.modules.stub import module

# Remove the imported modules once their code have run to prevent unused import
# warnings.
del module
