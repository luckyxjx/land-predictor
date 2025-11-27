#!/usr/bin/env python3
"""
Big Data Land Price Analytics Platform
Simple entry point for the consolidated dashboard
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main dashboard
if __name__ == "__main__":
    from ui.big_data_dashboard import *