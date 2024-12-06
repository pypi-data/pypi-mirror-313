"""Wrapper for complex forward jacobian."""

__all__ = ["jacfwd"]

from functools import wraps

from typing import Callable, Optional
import torch


def jacfwd(argnums: tuple[int]) -> Callable:
    """
    Decorator to compute the Jacobian of a function with complex-valued outputs.

    Parameters
    ----------
    argnum : tuple[int]
        The argument indexes to compute the Jacobian with respect to.

    Returns
    -------
    Callable
        Decorated function that computes the Jacobian with appropriate handling of complex outputs.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> tuple[torch.Tensor, Optional[torch.Tensor]]:
            """
            Wrapper function for differentiation.

            Returns
            -------
            Tuple[torch.Tensor, Optional[torch.Tensor]]
                Original function output and its Jacobian.
            """

            # Define a wrapper function to evaluate real-imag split output
            def wrapped_fn(*wrapped_args):
                return _split_real_imag(fn(*wrapped_args, **kwargs))

            # Compute the Jacobian using jacfwd
            jacobian = torch.func.jacfwd(wrapped_fn, argnums=argnums)(*args)

            return _combine_real_imag(jacobian)

        return wrapper

    return decorator


# %% subroutines
def _split_real_imag(tensor: torch.Tensor) -> torch.Tensor:
    """Split complex tensor into real and imaginary components."""
    if torch.is_complex(tensor):
        return torch.stack([tensor.real, tensor.imag], dim=0)
    else:
        return torch.stack([tensor, torch.zeros_like(tensor)], dim=0)


def _combine_real_imag(split_tensor: torch.Tensor) -> torch.Tensor:
    """Combine split real and imaginary components into a complex tensor."""
    if isinstance(split_tensor, tuple):
        output = [tensor[..., 0, :] + 1j * tensor[..., 1, :] for tensor in split_tensor]
        output = torch.stack(output, dim=0)
    else:
        output = split_tensor[..., 0, :] + 1j * split_tensor[..., 1, :]
    return output
