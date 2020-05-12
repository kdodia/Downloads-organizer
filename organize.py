""" Title: Downloads Organizer
Original Author: Jan B.
Second Author: Karan Dodia
Date: May 2020
Version: 1.1
Python-version: 3.8

This program is designed to organize the contents of a folder by assigning
files with specific extensions to specific folders.
This program is made with the purpose of organizing the user download folder
(i.e. `~/Downloads`), but can be easily be extended to similar use cases. The
only 3rd-party dependency is the `toolz` package—if you're not already using
it, now you have an excuse to install it and look around. =]

Modified by Karan D. for cross-platform compatability, Python 3.8, pathlib.

MIT License

Copyright (c) [2020] [Jan B.]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#                                <   Imports   >
from pathlib import Path
from typing import Dict, Sequence, Union

from operator import methodcaller
from toolz.dicttoolz import valmap

#                           <   Utility Functions   >
space_splitter = methodcaller('split', ' ')


#===========================^                       ^============================
#==========================<   Directory Organizer   >===========================
#===========================v                       v============================
class DirectoryOrganizer(object):
  """Thin class wrapper to create and organize configured directories.

  Initialize an instance with the target directory and organization
  directories and extensions, then call `organize()` to execute
  the common organization steps.
  """

  #-----------------------------<   Defaults   >---------------------------------
  TARGET_DIR = '~/Downloads'

  _ORG_DIRECTORIES = dict(
      Documents=(".oxps .epub .pages .docx .doc .fdf .ods .odt "
                 ".pwi .xsn .xps .dotx .docm .dox .rvg .rtf "
                 ".rtfd .wpd .csv .xls .xlsx .ppt pptx"),
      Plaintext=".txt .in .out",
      PDFs=".pdf",
      Images=(".jpeg .jpg .tif .tiff .gif .bmp "
              ".png .bpg svg .heif .psd"),
      Audio=(".aac .aa .aac .dvf .m4a .m4b .m4p "
             ".mp3 .msv .ogg .oga .raw .vox .wav .wma"),
      Videos=(".avi .flv .wmv .mov .mp4 .webm .vob "
              ".mng .qt .mpg .mpeg .3gp .mkv"),
      Archives=(".a .ar .cpio .iso .tar .gz "
                ".rz .7z .dmg .rar .xar .zip"),
      Scripts=".sh .zsh .py")
  ORG_DIRECTORIES = valmap(space_splitter, _ORG_DIRECTORIES)

  #------------------------------<   __init__   >--------------------------------
  def __init__(self,
               target_dir: Union[Path, str] = None,
               org_directories: Dict[str, Sequence[str]] = None):
    """Initialize with the target directory and organization directories.

    Attributes:
      target_dir: a str or Path to the directory that is to be sorted.
      org_directories: a dictionary containing the names of the sorted
      folders mapped to a list of extensions that corresponds to those folders.
    """

    if target_dir is None:
      target_dir = self.TARGET_DIR
    self.target_dir = Path(target_dir).expanduser()

    if org_directories is None:
      org_directories = self.ORG_DIRECTORIES
    self.org_directories = org_directories

  #--------------------------<   Instance Methods   >----------------------------
  def create_folders(self) -> None:
    """Creates directories for organization in the target folder."""

    for x in self.org_directories:
      Path(self.target_dir, x).mkdir(exist_ok=True)

  def organize_files(self) -> None:
    """Organizes the files into the specified directories."""

    for path in self.target_dir.iterdir():
      if path.is_file() and path.suffix:
        for org_dir in self.org_directories:
          if path.suffix.lower() in self.org_directories[org_dir]:
            path.rename(self.target_dir / org_dir / path.name)

  def organize_remaining_files(self) -> None:
    """Assigns remaining files to the the `target_dir/Other` directory."""
    for path in self.target_dir.iterdir():
      if path.is_file() and path.suffix:
        path.rename(self.target_dir / 'Other' / path.name)

  def organize_remaining_folders(self) -> None:
    """Assigns remaining folders to the the `target_dir/FOLDERS` directory."""

    for path in self.target_dir.iterdir():
      if all((path.is_dir(), path.name not in self.org_directories,
              path.name != 'FOLDERS')):
        path.rename(self.target_dir / 'FOLDERS' / path.name)

  def organize(self) -> None:
    """Performs the common organization routine.

    Steps:
      1. Creates the folders for organization in the target_dir
      2. Organizes files with recognized extensions
      3. Organizes remaining files into the "Other" directory
      4. Organizes remaining folders into the "Folders" directory
    """

    self.create_folders()
    self.organize_files()
    self.organize_remaining_files()
    self.organize_remaining_folders()


#==========================<   __name__ == __main__   >==========================
if __name__ == '__main__':

  organizer = DirectoryOrganizer()
  organizer.organize()
