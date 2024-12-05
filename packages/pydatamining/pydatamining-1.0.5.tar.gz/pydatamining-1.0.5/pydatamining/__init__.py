# Импортируйте основные модули и подпакеты
from .controller import *  # Импорты из controller.py
from .logger import *      # Импорты из logger.py

# Если вы хотите явно объявить отсутствующие подпакеты:
# from .manager import *
# from .proxy import *

# Укажите метаинформацию
__version__ = "1.0.5"
__all__ = ["controller", "logger"] 