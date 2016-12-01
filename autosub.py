"""
Find all movie files in given directory and download subtitles if available (via QNapi).
If already downloaded, skip the task.

Example:
    python3 /home/piotr/Repo/autosub/autosub.py
    /run/user/1000/gvfs/smb-share:server=synergy.local,share=video/#TV

Dependencies:
    - QNapi: https://qnapi.github.io/
        sudo add-apt-repository ppa:krzemin/qnapi
        sudo apt-get update
        sudo apt-get install qnapi

        QNapi dependencies:
            - ffprobe: https://ffmpeg.org/
                sudo add-apt-repository ppa:mc3man/trusty-media
                sudo apt-get update
                sudo apt-get install ffmpeg

            - 7z
                sudo apt-get install p7zip-rar

            - libmediainfo: https://launchpad.net/ubuntu/+source/libmediainfo
                sudo apt-get install libmediainfo-dev

TODO:
- add cli support docopt
- improve docstring
- add more services for subs downloading
- pylint import

Based on: http://rexo.pl/files/scripts/subget.txt
"""
import sys
import os
import subprocess
from utilities.as_logging import MyLogger
from utilities.timing import TimingManager
from qnapiwrapper import QNapiWrapper

__author__ = "Piotr Skrzypiec"
__copyright__ = "Copyright 2016, Autosub Project"
__credits__ = ["QNapi team", "Rexo.pl"]
__license__ = "GPL"
__version__ = '0.1.1'
__maintainer__ = "Piotr Skrzypiec"
__email__ = "peterskrzypiec@gmail.com"
__status__ = "Development"
# metadata best practices: http://stackoverflow.com/a/1523456


class Autosub():
    """Autosub class"""

    process = None
    logger = MyLogger().logger

    def __init__(self):
        if len(sys.argv) == 1:
            self.logger.error('Directory to search movie file not specified')
            sys.exit(2)
        else:
            movie_list = self.get_files_list(sys.argv[1])
            self.download_sub(movie_list)

    def get_files_list(self, directory):
        """Get list of the files"""

        os.chdir(directory)
        movie_list = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for file in filenames:
                if os.path.splitext(file)[1] == '.avi' or \
                                os.path.splitext(file)[1] == '.mkv' or \
                                os.path.splitext(file)[1] == '.mp4':
                    movie_list.append(os.path.join(dirpath, file))

            self.logger.debug("dirpath %s", dirpath)
            self.logger.debug("dirnames %s", dirnames)
            self.logger.debug("filenames %s", filenames)

        self.logger.info("Found movie files: (%d)", len(movie_list))
        return movie_list

    def download_sub(self, movie_list, chosen_service=QNapiWrapper()):
        """Try to download subtitles for given files list"""

        with TimingManager() as time:
            for file in movie_list:
                self.logger.debug("(%s)", file)

                subname_srt = file.replace(".avi", ".srt").\
                    replace(".mkv", ".srt").\
                    replace(".mp4", ".srt")

                subname_txt = file.replace(".avi", ".txt").\
                    replace(".mkv", ".txt").\
                    replace(".mp4", ".txt")

                if len(sys.argv) > 2 and sys.argv[2] == "-f":  # force
                    self.logger.warning("Forcing download subtitle for (%s)", file)
                elif os.path.isfile(subname_srt) or os.path.isfile(subname_txt):
                    self.logger.info("Sub already exists for (%s)", file)
                    continue

                self.logger.info("Executing task for (%s)", file)
                process = subprocess.Popen(
                    chosen_service.build_console_cmd(file),
                    stdout=subprocess.PIPE)

                response = process.stdout.readlines()
                return_code, parsed_response = chosen_service.parse_response(response)

                if return_code:
                    self.logger.error(parsed_response)
                else:
                    self.logger.info(parsed_response)

            self.logger.info("Elapsed time %s", time.end_log())


if __name__ == '__main__':
    Autosub()
