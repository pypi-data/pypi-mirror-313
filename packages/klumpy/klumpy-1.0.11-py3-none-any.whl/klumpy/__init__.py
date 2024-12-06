# Copyright 2024:
#        Giovanni Madrigal <gm33@illinois.edu>
#        Julian Catchen <jcatchen@illinois.edu>
#
# This file is part of Klumpy.
#
# Klumpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Klumpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Klumpy. If not, see <http://www.gnu.org/licenses/>.
#

from  .alignment_plot  import Alignment_Plot
from  .combine_klumps  import Combine_Klumps
from  .find_gaps       import Find_Gaps
from  .find_klumps     import Find_Klumps
from  .get_exons       import Get_Exons
from  .klump_plot      import Klump_Plot
from  .kmerize         import Kmerize
from  .klump_sizes     import Klump_Sizes
from  .scan_alignments import Scan_Alignments
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution('klumpy').version
except Exception:
    __version__ = "1.0.11"