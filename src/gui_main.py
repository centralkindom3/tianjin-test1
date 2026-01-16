# Source Generated with Decompyle++
# File: gui_main.pyc (Python 3.11)

# WARNING: This file could not be fully decompiled.
# The original logic of this file is missing.

__doc__ = '\n文件搜索工具 - 图形界面版\n使用tkinter实现标签页区分文件搜索和近义词界面\n'
import os
import json
import zipfile
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from search_engine import FileSearchEngine
from thesaurus import Thesaurus
import subprocess
import re
import jieba
from pypinyin import lazy_pinyin, Style
try:
    from pycorrector import Corrector
    PYCORRECTOR_AVAILABLE = True
except ImportError:
    PYCORRECTOR_AVAILABLE = False
