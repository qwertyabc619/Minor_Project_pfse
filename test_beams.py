import beams as bm
import math


steel_beam_1 = bm.steel_beam_from_section_name_si('W150X22.5',12000,345)
steel_beam_2 = bm.steel_beam_from_section_name_si('W150X22.5',4000,345)
steel_beam_3 = bm.steel_beam_from_section_name_si('W150X22.5',1200,345)
steel_beam_4 = bm.steel_beam_from_section_name_si('W130X23.8',12000,345)
steel_beam_5 = bm.steel_beam_from_section_name_si('W130X23.8',4000,345)
steel_beam_6 = bm.steel_beam_from_section_name_si('W130X23.8',1200,345)


def test_section_class():
    assert steel_beam_1.section_class() == (4, 4)
    assert steel_beam_4.section_class() == (1, 1)


def test_yield_moment():
    assert math.isclose(steel_beam_1.yield_moment()[0],54855.0)
    assert math.isclose(steel_beam_1.yield_moment()[1],17595.0)


def test_plastic_moment():
    assert math.isclose(steel_beam_1.plastic_moment()[0],61065.0)
    assert math.isclose(steel_beam_1.plastic_moment()[1],26841.0)


def test_unbraced_moment():
    assert math.isclose(steel_beam_1.unbraced_moment(),13672.966292392553)


def test_moment_capacity():
    assert math.isclose(steel_beam_1.moment_capacity(),12305.669663153298)
    assert math.isclose(steel_beam_2.moment_capacity(),40172.079638835596)
    assert math.isclose(steel_beam_3.moment_capacity(),49369.5)
    assert math.isclose(steel_beam_4.moment_capacity(),14798.840052909407)
    assert math.isclose(steel_beam_5.moment_capacity(),40413.83430560689)
    assert math.isclose(steel_beam_6.moment_capacity(),49059.0)

def test_steel_beam_from_section_name_si():
    assert bm.steel_beam_from_section_name_si('W150X22.5',12000,345).beam_tag == 'W150X22.5'
    assert bm.steel_beam_from_section_name_si('W150X22.5',12000,345).length == 12000
    assert bm.steel_beam_from_section_name_si('W150X22.5',12000,345).fy == 345
    assert bm.steel_beam_from_section_name_si('W150X22.5',12000,345).Ix == 12100000.0
    assert bm.steel_beam_from_section_name_si('W150X22.5',12000,345).Cw == 20500000000.0