import sys, gc, traceback
import math
import base64
import os
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display, HTML

def ju_init():
    display(HTML("<style>.container {width:95% !important;}</style>"))
    display(HTML("<style>div.output pre {font-family:Sans-Serif;font-size:10pt;color:black;font-weight:400;letter-spacing:1px;}</style>"))
    display(HTML("""<style>div.output_stderr {background: #FF7F50;}</style>"""))
    InteractiveShell.ast_node_interactivity = "all"
    pd.options.display.max_rows = 1000
    pd.options.display.max_columns = 1000
    pd.options.display.float_format = '{:,.2f}'.format

def in_ipynb():
    try:
        ret = get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
    except: return False
    return True

jupyter_stdout = sys.stdout
def disablePrint(): sys.stdout = open(os.devnull, 'w')
def enablePrint(): sys.stdout = jupyter_stdout
    
def force_print(*args):
    _stdout = sys.stdout
    enablePrint()
    print(*args)
    sys.stdout = _stdout

def imshow(im, title):
    if type(im)==np.ndarray and im.shape[0]==1: im = im[0]
    plt.imshow(im)
    plt.title(title)
    plt.show()
    plt.pause(0.001)
    
def imgrid(x, y):
    if len(x.shape) not in [3,4]: Exception('x dims must be 3 ou 4')
    if len(x.shape)==3: x = x[None,:,:,:]
    n = x.shape[0]
    nr = math.floor(math.sqrt(n))
    nc = n // nr
    fig, axs = plt.subplots(nr, nc, figsize=(15,8))
    if type(axs)!=np.ndarray: axs = [[axs]]
    elif len(axs.shape)==1: axs = [axs]
    for i in range(n):
        r,c = i//nc,i%nc
        ax = axs[r][c]
        ax.imshow(x[i])
        ax.set_title(y[i])
    fig.tight_layout()
    plt.show()
    plt.pause(0.001)

def plot_signal(x, ch=0, title=None):
    plt.plot(x[ch])
    if title: plt.title(title)
    plt.show()
    plt.pause(0.001)
    
def plot_signal_grid(x):
    n = x.shape[0]
    nr = math.floor(math.sqrt(n))
    nc = n // nr
    fig, axs = plt.subplots(nr, nc, figsize=(15,8))
    for i in range(n):
        r,c = i//nc,i%nc
        axs[r][c].plot(x[i])
        axs[r][c].set_title(f'Channel {i}')
    fig.tight_layout()
    plt.show()
    plt.pause(0.001)

# ####################################################################################################
# clean_mem
# https://github.com/fastai/course22p2/blob/df9323235bc395b5c2f58a3d08b83761947b9b93/miniai/init.py#L58
# ####################################################################################################

def clean_ipython_hist():
    # Code in this function mainly copied from IPython source
    if not 'get_ipython' in globals(): return
    ip = get_ipython()
    user_ns = ip.user_ns
    ip.displayhook.flush()
    pc = ip.displayhook.prompt_count + 1
    for n in range(1, pc): user_ns.pop('_i'+repr(n),None)
    user_ns.update(dict(_i='',_ii='',_iii=''))
    hm = ip.history_manager
    hm.input_hist_parsed[:] = [''] * pc
    hm.input_hist_raw[:] = [''] * pc
    hm._i = hm._ii = hm._iii = hm._i00 =  ''

def clean_tb():
    # h/t Piotr Czapla
    if hasattr(sys, 'last_traceback'):
        traceback.clear_frames(sys.last_traceback)
        delattr(sys, 'last_traceback')
    if hasattr(sys, 'last_type'): delattr(sys, 'last_type')
    if hasattr(sys, 'last_value'): delattr(sys, 'last_value')

def clean_mem():
    clean_tb()
    clean_ipython_hist()
    gc.collect()
    torch.cuda.empty_cache()

# ####################################################################################################
# DisplayPDF
# ####################################################################################################

class DisplayPDF(object):
    """
    Displays PDF data direclty from response.content on Jupyter
    """
    def __init__(self, pdf_bytes, width=200, height=None):
        # Assuming pdf_bytes is response.content or any binary data
        self.pdf = pdf_bytes
        height = height or width*1.41
        self.width,self.height = f'{width}px',f'{height}px'
    def _repr_html_(self):
        # Convert the binary PDF content to a base64-encoded string
        pdf_base64 = base64.b64encode(self.pdf).decode('utf-8')
        # HTML iframe with base64-encoded PDF and dynamic height adjustment
        html = f'''
        <iframe src="data:application/pdf;base64,{pdf_base64}" 
                style="width:{self.width}; height:{self.height}; border:none;" 
                onload="this.style.height = this.contentWindow.document.body.scrollHeight + 'px';">
        </iframe>
        '''
        return html
    def _repr_latex_(self):
        # LaTeX representation (still assumes the pdf is saved to a file)
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)