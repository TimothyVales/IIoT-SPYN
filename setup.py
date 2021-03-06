#   Copyright (c) 2019, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from setuptools import setup, find_packages
from distutils.dir_util import copy_tree
import os
import shutil

__author__ = "KV Thanjavur Bhaaskar, Naveen Purushotham ,Timothy Vales"
__copyright__ = "Copyright 2019, Xilinx"
__email__ = "kvt@xilinx.com, npurusho@xilinx.com, timothyv@xilinx.com"

# global variables
board = os.environ['BOARD']
repo_board_folder = f'boards/{board}/'
board_notebooks_dir = os.environ['PYNQ_JUPYTER_NOTEBOOKS']
hw_data_files = []


# check whether board is supported
def check_env():
    if not os.path.isdir(repo_board_folder):
        raise ValueError("Board {} is not supported.".format(board))
    if not os.path.isdir(board_notebooks_dir):
        raise ValueError("Directory {} does not exist.".format(board_notebooks_dir))


# copy notebooks to jupyter home
def copy_notebooks():
    src_nb_dir = os.path.join(f'', 'notebooks') #grab from notebooks folder
    dst_nb_dir = os.path.join(board_notebooks_dir, 'spyn') #copy notebook to spyn directory inside of board folder 
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    copy_tree(src_nb_dir, dst_nb_dir)
    
# copy overlays to python package
def copy_overlays():
    src_ol_dir = os.path.join(repo_board_folder, '') #grab bit file from pynqz1 board folder
    dst_ol_dir = os.path.join('spyn', 'bitstream') #copy bit file to bitstream folder in spyn folder
    copy_tree(src_ol_dir, dst_ol_dir)
    hw_data_files.extend([os.path.join("..", dst_ol_dir, f) for f in os.listdir(dst_ol_dir)])

check_env()
copy_notebooks()
copy_overlays()

setup(
    name="spyn",
    version='1.1',
    install_requires=['pynq>=2.5'], #require 2.5 
    url='https://github.com/TimothyVales/IIoT-SPYN.git', #grab from personal github
    license='BSD 3-Clause License',
    author='Xilinx ISM + PYNQ',
    author_email='timothyv@xilinx.com',
    packages=find_packages(),
    package_data={
        '': hw_data_files,
    },
    description="PYNQ example designs supporting PYNQ-enabled boards"
)
