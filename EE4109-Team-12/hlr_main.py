import SLiCAP as sl
import importlib

_orig_eqn2html = sl.eqn2html


def _eqn2html_py314_compat(*args, **kwargs):
    try:
        return _orig_eqn2html(*args, **kwargs)
    except TypeError as exc:
        # Work around a Python 3.14 + pytexit incompatibility triggered by
        # SLiCAP's unit-string TeX conversion (e.g. "V^2/Hz").
        if "units" in kwargs and "not all arguments converted during string formatting" in str(exc):
            retry_kwargs = dict(kwargs)
            units = retry_kwargs.pop("units", None)
            print(f"Warning: SLiCAP unit formatting failed for units={units!r}; continuing without formatted units.")
            return _orig_eqn2html(*args, **retry_kwargs)
        raise


sl.eqn2html = _eqn2html_py314_compat


def _patch_units2tex_py314_compat():
    targets = []
    for module_name in (
        "SLiCAP.SLiCAPmath",
        "SLiCAP.SLiCAPhtml",
        "SLiCAP.SLiCAPdesignData",
    ):
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        if hasattr(module, "units2TeX"):
            targets.append(module)

    for module in targets:
        orig = getattr(module, "units2TeX")

        def _units2tex_wrapper(units, _orig=orig):
            try:
                return _orig(units)
            except TypeError as exc:
                if "not all arguments converted during string formatting" in str(exc):
                    print(f"Warning: SLiCAP units2TeX failed for units={units!r}; using plain text units.")
                    return str(units)
                raise

        setattr(module, "units2TeX", _units2tex_wrapper)


_patch_units2tex_py314_compat()

sl.initProject('Hearing Loop Receiver - EE4109')

import hlr_specs
import hlr_system
import hlr_a1_circuit
import hlr_source_noise
import hlr_fb_noise
import hlr_ideal_ctrl
import hlr_gm_opt
import hlr_mos_sizing
import hlr_controller
import hlr_biasing




