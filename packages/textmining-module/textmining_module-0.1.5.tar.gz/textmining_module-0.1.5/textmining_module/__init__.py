# Import the main class from the miner module
from .miner import KEM as TextMiner
from .extractor import extract_keywords_to_dataframe as KeywordsExtractor

# Optionally define an __all__ for explicitness on what is exported
__all__ = ['TextMiner','KeywordsExtractor']