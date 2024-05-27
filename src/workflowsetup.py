
import urllib.request
import os
import shutil
import os


def download_data(url, path):
    urllib.request.urlretrieve(url, path)

base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')
# downloading block design data
block_url = 'https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip'

block_path = os.path.join(base_dir, 'MoAEpilot.bids.zip')

face_rep_url = 'https://www.fil.ion.ucl.ac.uk/spm/download/data/face_rep/face_rep.zip'
face_rep_path = os.path.join(base_dir, 'face_rep.zip')

download_data(block_url, block_path)

shutil.unpack_archive(block_path, base_dir)
# downloading event related design dataset

download_data(face_rep_url, face_rep_path)

shutil.unpack_archive(face_rep_path, base_dir)

# Copying block design data to the output directory

block_source = os.path.join(base_dir, 'MoAEpilot')
os.makedirs(os.path.join(base_dir, 'output'))
output_dir = os.path.join(base_dir, 'output')
_, blockname = os.path.split(block_source)
block_gui = blockname + '_gui'
batchname = blockname + '_batch'
scriptname = blockname + '_script'
os.makedirs(os.path.join(output_dir, batchname))
os.makedirs(os.path.join(output_dir, scriptname))
os.makedirs(os.path.join(output_dir, block_gui))

block_dest0 = os.path.join(output_dir, block_gui)
block_dest1 = os.path.join(output_dir, batchname)
block_dest2 = os.path.join(output_dir, scriptname)

def copytree2(source, dest):
  shutil.copytree(source, dest, symlinks=False, ignore=None, copy_function=shutil.copy2,  dirs_exist_ok=True)

copytree2(block_source, block_dest1)
copytree2(block_source, block_dest2)
copytree2(block_source, block_dest0)

# Copying event related design data to the output directory

event_source = os.path.join(base_dir, 'face_rep')
_, eventname = os.path.split(event_source)
event_gui = eventname + '_gui'
event_batch = eventname + '_batch'
event_script = eventname + '_script'
os.makedirs(os.path.join(output_dir, event_batch))
os.makedirs(os.path.join(output_dir, event_script))
os.makedirs(os.path.join(output_dir, event_gui))

event_dest0 = os.path.join(output_dir, event_gui)
event_dest1 = os.path.join(output_dir, event_batch)
event_dest2 = os.path.join(output_dir, event_script)

copytree2(event_source, event_dest1)
copytree2(event_source, event_dest2)
copytree2(event_source, event_dest0)

