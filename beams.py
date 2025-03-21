from dataclasses import dataclass
from math import pi
import sections_db as sect_db


@dataclass
class SteelBeam:
    """
    A data type to represent a doubly-symmetric beam made of steel.

    Units can be any units but should be internally consistent across the properties
    of the column.

    'beam_tag', section name
    'length', Unbraced length of the beam
    'd', depth of the beam
    'bf', Width of beam flange
    'tf', thickness of beam flange
    'tw', thickness of beam web
    'Ix', moment of inertia of section about XX direction
    'Iy', moment of inertia of section about YY direction
    'Sx', Section modulus of section about XX direction
    'Sy', Section modulus of section about YY direction
    'Zx', Plastic modulus of section about XX direction
    'Zy', Plastic modulus of section about YY direction
    'Cw', Warping constant
    'J', Torsional constant
    'omega_2', equivalent moment factor
    'E', Modulus of elasticity
    'G', shear modulus
    'fy', yield strength of steel

    """
    beam_tag: str
    length: float
    d: float
    bf: float
    tf: float
    tw: float
    Ix: float
    Iy: float
    Sx: float
    Sy: float
    Zx: float
    Zy: float
    Cw: float
    J: float
    fy: float
    omega_2: float = 1.0
    E: float = 200
    G: float = 77
    phi: float = 0.9

    def section_class(self) -> int:
        '''
        Returns the section class of a steel section based on the section geometry
        *Currently only valid for WF sections
        *No reduction in cross-sectional properties is currently applied when section is class 4
        '''
        # CSA S16:24 Table 2 Limits
        return section_class(self.bf, self.tf, self.d, self.tw, self.fy)
    

    def yield_moment(self) -> float:
        '''
        Returns the yield moment of a steel section (assuming class 3,2,or1)
        '''
        return yield_moment(self.Sx, self.Sy, self.fy)

    def plastic_moment(self) -> float:
        '''
        Returns the plastic moment of a steel section
        '''
        return plastic_moment(self.Zx, self.Zy, self.fy)

    def unbraced_moment(self) -> float:
        '''
        Caclulate the unbraced moment capacity of a steel doubly symmetric WF beam 
        '''
        return unbraced_moment(self.length, self.omega_2, self.Iy, self.J, self.Cw, self.E, self.G)

    def moment_capacity(self) -> float:
        '''
        Caclulate the moment capacity of a beam 
        '''
        return moment_capacity(self.length,
                                self.d,
                                self.bf,
                                self.tf,
                                self.tw,
                                self.Iy,
                                self.Sx,
                                self.Sy,
                                self.Zx,
                                self.Zy,
                                self.Cw,
                                self.J,
                                self.fy,
                                self.omega_2,
                                self.E,
                                self.G,
                                self.phi)

def section_class(bf: float, tf: float, d: float, tw: float, fy: float) -> int:
    '''
    Returns the section class of a steel section based on the section geometry
    *Currently only valid for WF sections
    *No reduction in cross-sectional properties is currently applied when section is class 4
    '''
    # CSA S16:24 Table 2 Limits
    flange_check = (bf / 2) / tf * (fy)**0.5

    if flange_check <= 145:
        flange_class = 1
    elif flange_check <= 170:
        flange_class = 2
    elif flange_check <= 200:
        flange_class = 3
    elif flange_check >200:
        flange_class = 4

    web_check_maj = (d - 2 * tf) / tw * (fy)**0.5 #add functionality of axial load in here to modify checks
    web_check_min = (d - 2 * tf) / tw * (fy)**0.5

    if web_check_maj > 83000:
        raise ValueError(f"Web is excessively slender: {web_check_maj} > 83000. Choose a different section")


    if web_check_maj <= 1100:
        web_class_maj = 1
    elif web_check_maj <= 1700:
        web_class_maj = 2
    elif web_check_maj <= 1900:
        web_class_maj = 3
    elif web_check_maj > 1900:
        web_class_maj = 4

    if web_check_min <= 525:
        web_class_min = 1
    elif web_check_min <= 525:
        web_class_min = 2
    elif web_check_min <= 1900:
        web_class_min = 3
    elif web_check_min >200:
        web_class_min = 4

    section_class_maj = max(web_class_maj, flange_class) #for bending about X-X axis or major axis
    section_class_min = max(web_class_min, flange_class) #for bending about Y-Y axis or minor axis

    return section_class_maj, section_class_min


def yield_moment(Sx: float, Sy: float, fy: float) -> float:
    '''
    Returns the yield moment of a steel section (assuming class 3,2,or1)
    '''
    Myx = Sx * fy / 1000 #to convert to Nm (from mm3 * MPa = Nmm)
    Myy = Sy * fy / 1000 #to convert to Nm (from mm3 * MPa = Nmm)
    return Myx, Myy

def plastic_moment(Zx: float, Zy: float, fy: float) -> float:
    '''
    Returns the plastic moment of a steel section
    '''
    Mpx =  Zx * fy / 1000 #to convert to Nm (from mm3 * MPa = Nmm)
    Mpy =  Zy * fy / 1000 #to convert to Nm (from mm3 * MPa = Nmm)
    return Mpx, Mpy

def unbraced_moment(
        L_unbr: float,
        omega_2: float,
        Iy: float,
        J: float,
        Cw: float,
        E: float,
        G: float
        ) -> float:
    '''
    Caclulate the unbraced moment capacity of a steel doubly symmetric WF beam 
    '''
    Mu = (omega_2 * pi / L_unbr) * ((E * Iy * G * J) + (pi * E / L_unbr)**2 * Iy * Cw) ** 0.5
    return Mu

def moment_capacity(
    L_unbr: float,
    d: float,
    bf: float,
    tf: float,
    tw: float,
    Iy: float,
    Sx: float,
    Sy: float,
    Zx: float,
    Zy: float,
    Cw: float,
    J: float,
    fy: float,
    omega_2: float = 1.0,
    E: float = 200, #GPa
    G: float = 77, # GPa
    phi: float = 0.9) -> float:
    '''
    Caclulate the moment capacity of a beam 
    '''
    section_class_maj = section_class(bf, tf, d, tw, fy)[0]
    Mu = unbraced_moment(L_unbr, omega_2, Iy, J, Cw, E, G)
    Mpx = plastic_moment(Zx, Zy, fy)[0]
    Myx = yield_moment(Sx, Sy, fy)[0]

    # CSA S16:24 CL 13.6.1
    if (section_class_maj <= 2) and (Mu > (0.67 * Mpx)):
        Mrxu = min(1.15 * phi * Mpx * (1 - 0.28 * Mpx / Mu), phi * Mpx)
    elif (section_class_maj <= 2) and (Mu <= (0.67 * Mpx)):
        Mrxu = phi * Mu
    elif (section_class_maj > 2) and (Mu > (0.67 * Myx)):
        Mrxu = min(1.15 * phi * Myx * (1 - 0.28 * Myx / Mu), phi * Myx)
    else:
        Mrxu = phi * Mu
    return Mrxu


def steel_beam_from_section_name_si(
        section_name: str,
        length: float,
        fy: float,
        omega_2: float = 1.0,
        E: float = 200,
        G: float = 77,
        phi: float = 0.9
        ) -> SteelBeam:
    '''
    Returns a SteelBeam dataclass instance based on a section name form the AISC section database
    '''
    steel_beams = sect_db.aisc_w_sections('si')
    steel_beam = SteelBeam(beam_tag = section_name,
        length = length,
        d = steel_beams.loc[section_name]['d'],
        bf = steel_beams.loc[section_name]['bf'],
        tf = steel_beams.loc[section_name]['tf'],
        tw = steel_beams.loc[section_name]['tw'],
        Ix = steel_beams.loc[section_name]['Ix'],
        Iy = steel_beams.loc[section_name]['Iy'],
        Sx = steel_beams.loc[section_name]['Sx'],
        Sy = steel_beams.loc[section_name]['Sy'],
        Zx = steel_beams.loc[section_name]['Zx'],
        Zy = steel_beams.loc[section_name]['Zy'],
        Cw = steel_beams.loc[section_name]['Cw'],
        J = steel_beams.loc[section_name]['J'],
        omega_2 = omega_2,
        fy = fy,
        E = E,
        G = G,
        phi = phi)
    return steel_beam