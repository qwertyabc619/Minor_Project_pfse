import hand_calculations as hc
import beams as bm
import forallpeople as si

si.environment("structural")

steel_beam_1 = bm.steel_beam_from_section_name_si('W150X22.5',2000,345)

def test_calc_section_class():
    bf = steel_beam_1.bf
    tf = steel_beam_1.tf
    d = steel_beam_1.d
    tw = steel_beam_1.tw
    fy = steel_beam_1.fy

    latex_out, result = hc.calc_section_class(bf, tf, d, tw, fy)
    assert result[4] == (4,4)


def test_calc_M():
    Sx = steel_beam_1.Sx * si.mm**3
    Zx = steel_beam_1.Zx * si.mm**3
    fy = steel_beam_1.fy * si.MPa
    L = steel_beam_1.length * si.mm
    E = steel_beam_1.E * si.GPa
    Iy = steel_beam_1.Iy * si.mm**4
    G = steel_beam_1.G * si.GPa
    J = steel_beam_1.J * si.mm**4
    Cw = steel_beam_1.Cw * si.mm**6
    omega_2 = steel_beam_1.omega_2
    section_class = steel_beam_1.section_class()[0]
    phi = steel_beam_1.phi

    result_1 = 54.855 * si.kN * si.m
    result_2 = 61.065 * si.kN * si.m
    result_3 = 159.881043513411 * si.kN * si.m
    result_4 = 49.3695 * si.kN * si.m

    latex_out, result = hc.calc_M(Sx, Zx, fy, L, E, Iy, G, J, Cw, omega_2, section_class, phi)
    assert result[0] == result_1
    assert result[1] == result_2
    assert result[2] == result_3
    assert result[3] == result_4