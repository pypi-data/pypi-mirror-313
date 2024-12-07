import sys
sys.modules['haplostat'] = sys.modules[__name__]
from .main import run_convert_hla  
__all__ = ["run_convert_hla"] 