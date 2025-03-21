import sections_db as sections


def test_aisc_w_sections():
    assert dict(sections.aisc_w_sections('si').loc['W150X13']) == {'Section': 'W150X13',
                                                                    'W': 13.0,
                                                                    'A': 1630,
                                                                    'd': 148,
                                                                    'bf': 100,
                                                                    'tw': 4.32,
                                                                    'tf': 4.95,
                                                                    'kdes': 11.3,
                                                                    'Ix': 6200000.0,
                                                                    'Zx': 93900.0,
                                                                    'Sx': 83600.0,
                                                                    'rx': 61.7,
                                                                    'Iy': 828000.0,
                                                                    'Zy': 25600.0,
                                                                    'Sy': 16600.0,
                                                                    'ry': 22.6,
                                                                    'J': 13900.0,
                                                                    'Cw': 4240000000.0}
    

