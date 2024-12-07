# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics


def test_import():
    import cosmic_toolbox
    import cosmic_toolbox.arraytools
    import cosmic_toolbox.colors
    import cosmic_toolbox.copy_guardian
    import cosmic_toolbox.file_utils
    import cosmic_toolbox.logger
    import cosmic_toolbox.MultiInterp
    import cosmic_toolbox.NearestWeightedNDInterpolator
    import cosmic_toolbox.TransformedGaussianMixture

    print(cosmic_toolbox.__version__)
    assert True


def test_dummy():
    assert True
