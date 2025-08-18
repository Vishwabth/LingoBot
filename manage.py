#!/usr/bin/env python
import os
import sys

# --- Silence TensorFlow noisy logs (safe to keep here) ---
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lingobot.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
