# RUN_REPORT – run_S_symmetry_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Purpose: **symmetry / sanity check** with hop coherence only
- Config file: `configs/run_S_symmetry.yml`
- Output directory: `outputs_glue_axes/run_S_symmetry`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh = 50, N ∈ [1, 16]
- Ensembles per (W_coh, N): 64
- Steps: 4000  (burn-in: 400)
- Hop coherence: form=power_law, alpha=1.0, k_prefactor=2.0, memory_depth=1
- Shared bias: enabled=False, lambda_bias=0.0
- Phase lock: enabled=False, lambda_phase=0.0
- Domains: enabled=False, lambda_domain=0.0
- Diagnostics: store_states=True, compute_lockstep=True, compute_psd=False

## 3. Numerical outputs

| W_coh |  N  | L_inst | ell_lock | Q_clock |
|------:|----:|-------:|---------:|--------:|
|    50 |   1 | 1.000 | 15.09 | 0.020 |
|    50 |  16 | 0.197 | 14.78 | 0.013 |

## 4. Interpretation

### 4.1 Hop-only baseline behaviour

- For N = 1 we recover the expected telegraph baseline: L_inst = 1.000, ell_lock ≈ 15.1, Q_clock ≈ 0.020 (essentially zero drift).
- For N = 16 the bundle behaves like an average of independent threads: L_inst drops to 0.197 (≈ 1/√N), while ell_lock remains almost unchanged at 14.8.
- Q_clock stays very small for both N values, confirming that the centre-of-mass performs a nearly pure diffusive walk with no hidden bias.

### 4.2 Symmetry conclusions

- With all glue axes disabled, the statistics are invariant in the sense we expect:
  - increasing N reduces instantaneous magnetisation roughly like 1/√N,
  - the lockstep persistence time is set by W_coh alone and does not grow with N,
  - there is no evidence of spontaneous drift or asymmetry in the hop law.
- This run therefore supports the assumption that the **only** source of bundle-level stiffness and clock-like behaviour in later runs is the explicit glue axes, not some hidden asymmetry in the hop-coherence implementation.

## 5. Status

- Symmetry / hop-only sanity check: **passed**.
- No further action required unless we later change the hop kernel implementation.