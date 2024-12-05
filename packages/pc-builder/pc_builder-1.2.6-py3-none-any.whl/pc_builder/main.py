import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pc_builder.cli import main

if __name__ == "__main__":
    main()
