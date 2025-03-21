from numpy import sqrt
from math import pi
from handcalcs.decorator import handcalc


##
@handcalc(override="long", precision=2)
def calc_M(S_x: float, Z_x: float, f_y: float, L:float, E:float, I_y:float, G:float, J:float, Cw:float, omega_2:float, section_class: int, phi: float):
    """
    Calculates the moment capacity of a WF steel section
    """
    M_yx = S_x * f_y #Yield Moment CL 13.5b) S16:24
    M_px = Z_x * f_y #Plastic Moment CL 13.5a) S16:24
    
    M_u = ((omega_2 * pi) / L) * sqrt((E * I_y * G * J + ((pi * E) / L)**2 * I_y * Cw)) #Unbraced Moment CL 13.6.1a)ii) S16:24

    if (section_class <= 2) & (M_u > (0.67 * M_px)): M_rxu = min(1.15 * phi * M_px * (1 - 0.28 * M_px / M_u), phi * M_px) #Unbraced Moment CL 13.6.1a)i) S16:24
    elif (section_class <= 2) & (M_u <= (0.67 * M_px)): M_rxu = phi * M_u #Unbraced Moment CL 13.6.1a)ii) S16:24
    elif (section_class > 2) & (M_u > (0.67 * M_yx)): M_rxu = min(1.15 * phi * M_yx * (1 - 0.28 * M_yx / M_u), phi * M_yx) #Unbraced Moment CL 13.6.1b)i) S16:24
    elif (section_class > 2) & (M_u <= (0.67 * M_yx)): M_rxu = phi * M_u #Unbraced Moment CL 13.6.1b)ii) S16:24

    return M_yx, M_px, M_u, M_rxu


@handcalc(precision=2)
def calc_section_class(b_f: float, t_f: float, d: float, t_w: float, f_y: float):
    """
    Calculates the section class from a WF steel beam
    """
    Check_flange = (b_f / 2) / t_f
    Flange_limit_1 = 145 / sqrt(f_y)
    Flange_limit_2 = 170 / sqrt(f_y)
    Flange_limit_3 = 200 / sqrt(f_y)
    Flange_limit = [Flange_limit_1, Flange_limit_2, Flange_limit_3] #Major bending flange limits

    Check_web = (d - 2 * t_f) / t_w
    Web_limit_maj1 = 1100 / sqrt(f_y)
    Web_limit_maj2 = 1700 / sqrt(f_y)
    Web_limit_maj3 = 1900 / sqrt(f_y)
    Web_limit_maj = [Web_limit_maj1, Web_limit_maj2, Web_limit_maj3] #Major bending web limits

    Web_limit_min1 = 525 / sqrt(f_y)
    Web_limit_min2 = 525 / sqrt(f_y)
    Web_limit_min3 = 1900 / sqrt(f_y)
    Web_limit_min = [Web_limit_min1, Web_limit_min2, Web_limit_min3] #Minor bending web limits

    if Check_flange <= Flange_limit[0]: Flange_class = 1
    elif Check_flange <= Flange_limit[1]: Flange_class = 2
    elif Check_flange <= Flange_limit[2]: Flange_class = 3
    elif Check_flange > Flange_limit[2]: Flange_class = 4

    if Check_web <= Web_limit_maj[0]: Web_class_maj = 1
    elif Check_web <= Web_limit_maj[1]: Web_class_maj = 2
    elif Check_web <= Web_limit_maj[2]: Web_class_maj = 3
    elif Check_web > Web_limit_maj[2]: Web_class_maj = 4

    if Check_web <= Web_limit_min[0]: Web_class_min = 1
    elif Check_web <= Web_limit_min[1]: Web_class_min = 2
    elif Check_web <= Web_limit_min[2]: Web_class_min = 3
    elif Check_web > Web_limit_min[2]: Web_class_min = 4

    class_section = max(Flange_class, Web_class_maj), max(Flange_class, Web_class_min) #Major bending, Minor bending

    return Check_flange, Flange_limit, Web_limit_maj, Web_limit_min, class_section