import pytest

from prysm import PixelAperture, Pupil, PSF


@pytest.fixture
def sample_psf():
    p = Pupil()
    return PSF.from_pupil(p, 10)


@pytest.fixture
def sample_psf_bigger():
    p = Pupil()
    return PSF.from_pupil(p, 20)


@pytest.fixture
def sample_pixel():
    return PixelAperture(5)


@pytest.fixture
def sample_pixel_gridded():
    return PixelAperture(5, sample_spacing=0.1, samples_x=256)


def test_double_analyical_convolution_functions(sample_pixel, sample_pixel_gridded):
    assert sample_pixel.conv(sample_pixel_gridded)


def test_single_analytical_convolution_functions(sample_pixel, sample_psf):
    assert sample_pixel.conv(sample_psf)


def test_numerical_convolution_equal_functions(sample_psf):
    assert sample_psf.conv(sample_psf)


def test_numerical_convolution_unequal_functions(sample_psf, sample_psf_bigger):
    assert sample_psf.conv(sample_psf_bigger)
