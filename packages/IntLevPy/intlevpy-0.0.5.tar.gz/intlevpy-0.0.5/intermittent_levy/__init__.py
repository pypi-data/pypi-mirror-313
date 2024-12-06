# __init__.py

from .processes import intermittent3, levy_flight_2D_Simplified
from .moments import mom2_serg_log, mom4_serg_log, theor_levy_moment, levy_moments_log
from .optimization import (
    to_optimize_mom4_and_2_serg_log,
    to_optimize_mom4_serg_log_vl,
    to_optimize_second_ll,
    # Include other optimization functions if needed
)
from .classification import (
    frequency_matrix_2D,
    form_groups,
    real_k_and_fisher,
    parse_trials,
)
from .utils import (
    r_square,
    adjusted_r_square,
    adjusted_r_square_array,
    powerl_fit,
    funcPairs,
)

