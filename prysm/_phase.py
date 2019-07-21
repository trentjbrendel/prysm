"""phase basics."""
import warnings

from .mathops import engine as e
from ._richdata import RichData
from .plotting import share_fig_ax
from .util import pv, rms, Sa, std


class OpticalPhase(RichData):
    """Phase of an optical field."""
    _data_attr = 'phase'
    _data_type = 'phase'

    def __init__(self, x, y, phase, units, labels):
        """Create a new instance of an OpticalPhase.

        Note that this class is not intended to be used directly, and is meant
        to allow shared functionality and interchange between the `Pupil` and
        `Interferogram` classes.

        Parameters
        ----------
        x : `numpy.ndarray`
            x unit axis
        y : `numpy.ndarray`
            y unit axis
        phase : `numpy.ndarray`
            phase data
        xlabel : `str`, optional
            x label used on plots
        ylabel : `str`, optional
            y label used on plots
        zlabel : `str`, optional
            z label used on plots
        xyunit : `str`, optional
            unit used for the XY axes
        zunit : `str`, optional
            unit used for the Z (data) axis
        wavelength : `float`, optional
            wavelength of light, in microns

        """
        super().__init__(x=x, y=y, data=phase, units=units, labels=labels)

    @property
    def phase_unit(self):
        """Unit used to describe the optical phase."""
        warnings.warn('phase_unit has been folded into zunit and will be removed in prysm v0.18')
        return self.zunit

    @phase_unit.setter
    def phase_unit(self, unit):
        unit = unit.lower()
        if unit == 'å':
            self._phase_unit = unit.upper()
        else:
            if unit not in self.units:
                raise ValueError(f'{unit} not a valid unit, must be in {set(self.units.keys())}')
            self._phase_unit = self.units[unit]

    @property
    def spatial_unit(self):
        """Unit used to describe the spatial phase."""
        warnings.warn('spatial_unit has been folded into xyunit and will be removed in prysm v0.18')
        return self.xyunit

    @spatial_unit.setter
    def spatial_unit(self, unit):
        unit = unit.lower()
        if unit not in self.units:
            raise ValueError(f'{unit} not a valid unit, must be in {set(self.units.keys())}')

        self._spatial_unit = self.units[unit]

    @property
    def pv(self):
        """Peak-to-Valley phase error.  DIN/ISO St."""
        return pv(self.phase)

    @property
    def rms(self):
        """RMS phase error.  DIN/ISO Sq."""
        return rms(self.phase)

    @property
    def Sa(self):
        """Sa phase error.  DIN/ISO Sa."""
        return Sa(self.phase)

    @property
    def std(self):
        """Standard deviation of phase error."""
        return std(self.phase)

    @property
    def diameter_x(self):
        """Diameter of the data in x."""
        return self.x[-1] - self.x[0]

    @property
    def diameter_y(self):
        """Diameter of the data in y."""
        return self.y[-1] - self.x[0]

    @property
    def diameter(self):
        """Greater of (self.diameter_x, self.diameter_y)."""
        return max((self.diameter_x, self.diameter_y))

    @property
    def semidiameter(self):
        """Half of self.diameter."""
        return self.diameter / 2

    def interferogram(self, visibility=1, passes=2, interp_method='lanczos', fig=None, ax=None):
        """Create an interferogram of the `Pupil`.

        Parameters
        ----------
        visibility : `float`
            Visibility of the interferogram
        passes : `float`
            Number of passes (double-pass, quadra-pass, etc.)
        interp_method : `str`, optional
            interpolation method, passed directly to matplotlib
        fig : `matplotlib.figure.Figure`, optional
            Figure to draw plot in
        ax : `matplotlib.axes.Axis`
            Axis to draw plot in

        Returns
        -------
        fig : `matplotlib.figure.Figure`, optional
            Figure containing the plot
        ax : `matplotlib.axes.Axis`, optional:
            Axis containing the plot

        """
        epd = self.diameter
        phase = self.change_zunit(to='waves', inplace=False)

        fig, ax = share_fig_ax(fig, ax)
        plotdata = visibility * e.sin(2 * e.pi * passes * phase)
        im = ax.imshow(plotdata,
                       extent=[-epd / 2, epd / 2, -epd / 2, epd / 2],
                       cmap='Greys_r',
                       interpolation=interp_method,
                       clim=(-1, 1),
                       origin='lower')
        fig.colorbar(im, label=r'Wrapped Phase [$\lambda$]', ax=ax, fraction=0.046)
        ax.set(xlabel=r'Pupil $\xi$ [mm]',
               ylabel=r'Pupil $\eta$ [mm]')
        return fig, ax
