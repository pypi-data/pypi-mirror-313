"""Fast Spin Echo simulator."""

__all__ = ["fse_sim"]

import numpy.typing as npt
import torch

from ..models.fse import FSEModel


def fse_sim(
    flip: npt.ArrayLike,
    ESP: float,
    T1: float | npt.ArrayLike,
    T2: float | npt.ArrayLike,
    phases: float | npt.ArrayLike = 0.0,
    TR: float | npt.ArrayLike = 1e6,
    exc_flip: float = 90.0,
    exc_phase: float = 90.0,
    diff: str | tuple[str] = None,
    slice_prof: float | npt.ArrayLike = 1.0,
    B1: float | npt.ArrayLike = 1.0,
    M0: float | npt.ArrayLike = 1.0,
    nstates: int = 10,
    chunk_size: int = None,
    device: str | torch.device = None,
):
    """
    Fast Spin Echo simulator wrapper.

    Parameters
    ----------
    flip : float | npt.ArrayLike
        Refocusing flip angle train in degrees.
    ESP : float
        Echo spacing in milliseconds.
    phases : float | npt.ArrayLike, optional
        Refocusing flip angle phases in degrees.
        The default is ``90.0``.
    TR : float | npt.ArrayLike, optional
        Repetition time in milliseconds.
        The default is ``1e6``.
    exc_flip : float, optional
        Excitation flip angle train in degrees.
        The default is ``90.0``.
    exc_phase : float, optional
        Excitation flip angle phase in degrees.
        The default is ``0.0``.
    T1 : float | npt.ArrayLike
        Longitudinal relaxation time in milliseconds.
    T2 : float | npt.ArrayLike
        Transverse relaxation time in milliseconds.
    diff : str | tuple[str], optional
        Arguments to get the signal derivative with respect to.
        The default is ``None`` (no differentation).
    slice_prof : float | npt.ArrayLike, optional
        Flip angle scaling along slice profile.
        The default is ``1.0``.
    B1 : float | npt.ArrayLike, optional
        Flip angle scaling map, default is ``1.0``.
    inv_efficiency : float | npt.ArrayLike, optional
        Inversion efficiency map, default is ``1.0``.
    M0 : float or array-like, optional
        Proton density scaling factor, default is ``1.0``.
    TI : float | npt.ArrayLike, optional
        Inversion time in milliseconds.
        The default is ``0.0``.
    nstates : int, optional
        Number of EPG states to be retained.
        The default is ``10``.
    chunk_size : int, optional
        Number of atoms to be simulated in parallel.
        The default is ``None``.
    device : str | torch.device, optional
        Computational device for simulation.
        The default is ``None`` (infer from input).

    Returns
    -------
    sig : npt.ArrayLike
        Signal evolution of shape ``(..., len(flip))``.
    jac : npt.ArrayLike
        Derivatives of signal wrt ``diff`` parameters,
        of shape ``(..., len(diff), len(flip))``.
        Not returned if ``diff`` is ``None``.

    """
    model = FSEModel(diff, chunk_size, device)
    model.set_properties(T1, T2, M0, B1)
    model.set_sequence(flip, ESP, phases, TR, exc_flip, exc_phase, slice_prof, nstates)
    return model()
