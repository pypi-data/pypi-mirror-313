# coding = utf-8

"""see documentation @ ../../docs/reader.md"""

from time import time

from ..reader.gsd_reader_helper import read_gsd_dcd_wrapper, read_gsd_wrapper
from ..reader.lammps_reader_helper import (read_lammps_centertype_wrapper,
                                           read_lammps_vector_wrapper,
                                           read_lammps_wrapper)
from ..reader.reader_utils import DumpFileType, Snapshots
from ..utils.logging import get_logger_handle

logger = get_logger_handle(__name__)

# pylint: disable=too-few-public-methods

FILE_TYPE_MAP_READER = {
    DumpFileType.LAMMPS: read_lammps_wrapper,
    DumpFileType.LAMMPSCENTER: read_lammps_centertype_wrapper,
    DumpFileType.GSD: read_gsd_wrapper,
    DumpFileType.GSD_DCD: read_gsd_dcd_wrapper,
    DumpFileType.LAMMPSVECTOR: read_lammps_vector_wrapper,
}


class DumpReader:
    """
    Reading snapshots generated by various simulators for materials science,
    chemistry, and physics, and so on,
    such as LAMMPS and Hoomd-blue engines.

    By specifying the filetype argument when initializing DumpReader class,
    so far the module can read:
    1. filetype=DumpFileType.LAMMPS
        atomistic system in LAMMPS, by calling
        reader.lammps_reader_helper.read_lammps_wrapper

    2. filetype=DumpFileType.LAMMPSCENTER
        molecular system in LAMMPS, by calling
        reader.lammps_reader_helper.read_lammps_centertype_wrapper

    3. filetype=DumpFileType.GSD
        static properties in Hoomd-blue, gsd file, by calling
        reader.gsd_reader_helper.read_gsd_wrapper

    4. filetype=DumpFileType.GSD_DCD
        dyanmic properties in Hoomd-blue, both gsd and dcd files, by calling
        reader.gsd_reader_helper.read_gsd_dcd_wrapper

    5. filetype=DumpFileType.LAMMPSVECTOR
        additional column(s) information from lammps configuration
        reader.lammps_reader_helper.read_lammps_vector_wrapper

    Example:
        from ..reader.dump_reader import DumpReader
        from ..reader.reader_utils import DumpFileType
        readdump=DumpReader(filename, ndim=3, filetype=DumpFileType.LAMMPS)
        readdump.read_onefile()

        you can also directly call wrapper function, such as,
        from ..reader.lammps_reader_helper import read_lammps_wrapper
        snapshots = read_lammps_wrapper(filename, ndim=3)

    Important Notes:
        1. In LAMMPS, x, xs, and xu format coordinates are acceptable,
            such as with format "id type x y z".
            The reduced xs will be rescaled to the absolute coordinates x.

        2. Supports both orthogonal and triclinic boxes.
            For a triclinic box, convert the bounding box back into the trilinic box parameters:
                xlo = xlo_bound - MIN(0.0,xy,xz,xy+xz)
                xhi = xhi_bound - MAX(0.0,xy,xz,xy+xz)
                ylo = ylo_bound - MIN(0.0,yz)
                yhi = yhi_bound - MAX(0.0,yz)
                zlo = zlo_bound
                zhi = zhi_bound
            See 'https://docs.lammps.org/Howto_triclinic.html'

        3. For the xs and x types in orthogonal cells with periodic boundary conditions,
            particle coordinates are warp to the inside of the box by default,
            which could be changed by hand when necessary.
            In non-periodic boundary conditions,
            there should be no particles at the outside of the cell.

        4. All snapshots should be in one file at this stage.

        5. To read the Hoomd-blue outputs, two new modules should be installed first:
            i) gsd; ii) mdtraj. These modules are available by conda.
            Currently, the dump files from Hoomd-blue only support orthogonal box.
    """

    def __init__(
        self,
        filename: str,
        ndim: int,
        filetype: DumpFileType = DumpFileType.LAMMPS,
        moltypes: dict = None,
        columnsids: list = None,
    ) -> None:
        """
        Inputs:
            1. filename (str): the name of dump file

            2. ndim (int): dimensionality

            3. filetype (DumpFileType): input dump format,
                defined in reader.reader_utils;
                can have the following format:
                    1. DumpFileType.LAMMPS (default)
                    2. DumpFileType.LAMMPSCENTER
                    3. DumpFileType.GSD
                    4. DumpFileType.GSD_DCD
                    5. DumpFileType.LAMMPSVECTOR

            4. moltypes (dict, optional): only used for molecular system in LAMMPS, default is None.
               To specify, for example, if the system has 5 types of atoms in which 1-3 is
               one type of molecules and 4-5 is the other, and type 3 and 5 are the center of mass.
               Then moltypes should be {3:1, 5:2}. The keys ([3, 5]) of the dict (moltypes)
               are used to select specific atoms to present the corresponding molecules.
               The values ([1, 2]) is used to record the type of molecules.

            5. columnsids (list of int, optional): column id for additional information,
                for example, [5, 6] for "vx vy" from "id type x y vx vy"

        Return:
            list of snapshot that has all of the configuration information
            see self.read_onefile()
        """

        self.filename = filename
        self.ndim = ndim
        self.filetype = filetype
        self.moltypes = moltypes
        self.columnsids = columnsids
        self.snapshots: Snapshots = None

    def read_onefile(self):
        """
        read single or multiple snapshots in one trajectory

        Return:
            reader.snapshots: stores a list of snapshot, which consisits:
                snapshot.timestep:         simulation timestep at each snapshot
                snapshot.nparticle:        particle number from each snapshot
                snapshot.particle_type:    particle type in array in each snapshot
                snapshot.positions:        particle coordinates in array in each snapshot
                                           can be additional column information when
                                           self.columnids is activated
                snapshot.boxlength:        box length in array in each snapshot
                snapshot.boxbounds:        box boundaries in array in each snapshot
                snapshot.realbounds:       real box bounds of a triclinic box
                snapshot.hmatrix:          h-matrix of the cells in each snapshot

        The information is stored in a list of which the elements are mainly numpy arrays.
        Particle-level information is referred by particle ID.
        """

        logger.info(f"Start reading file {self.filename} of type {self.filetype}")

        reader_inputs = {"file_name": self.filename, "ndim": self.ndim}

        if self.filetype == DumpFileType.LAMMPSCENTER:
            reader_inputs["moltypes"] = self.moltypes

        if self.filetype == DumpFileType.LAMMPSVECTOR:
            reader_inputs["columnsids"] = self.columnsids

        t0 = time()
        self.snapshots = FILE_TYPE_MAP_READER[self.filetype](**reader_inputs)

        logger.info(f"Finish reading file {self.filename} in {time() - t0} seconds")
