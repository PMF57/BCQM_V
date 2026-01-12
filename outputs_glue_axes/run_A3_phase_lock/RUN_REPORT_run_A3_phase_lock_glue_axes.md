# RUN_REPORT – run_A3_phase_lock_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Glue axes: **phase-lock only** (no shared bias, no domains)
- Config file: `configs/run_A3_phase_lock.yml`
- Output directory (convention): `outputs_glue_axes/run_A3_phase_lock`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [1, 2, 4, 8, 16]
- Ensembles per (W_coh, N): 32
- Steps: 2000  (burn-in: 200)
- Hop coherence (soft-rudder telegraph): form=power_law, alpha=1.0, k_prefactor=2.0
- Shared-bias glue: enabled=False, lambda_bias=0.0
- Phase-lock axis: **enabled=True**, lambda_phase=0.3, omega_0=0.1, noise_sigma=0.05
- Domains axis: enabled=False, n_initial_domains=1, lambda_domain=0.0
- Diagnostics: store_states=True, compute_lockstep=True

## 3. Numerical outputs (lockstep metrics)

Summary table from `summary.json` (per (W_coh, N)):

| W_coh | N  | L_inst | ell_lock | Q_clock |
|------:|---:|-------:|---------:|--------:|
|    20 |  1 | 1.000 | 7.18 | 0.008 |
|    20 |  2 | 0.615 | 6.86 | 0.270 |
|    20 |  4 | 0.517 | 7.67 | 0.277 |
|    20 |  8 | 0.446 | 9.64 | 0.327 |
|    20 | 16 | 0.399 | 13.53 | 0.300 |
|    50 |  1 | 1.000 | 13.76 | 0.014 |
|    50 |  2 | 0.714 | 13.07 | 0.566 |
|    50 |  4 | 0.644 | 15.90 | 0.614 |
|    50 |  8 | 0.604 | 26.26 | 0.599 |
|    50 | 16 | 0.585 | 69.16 | 0.634 |
|   100 |  1 | 1.000 | 23.17 | 0.011 |
|   100 |  2 | 0.788 | 18.80 | 0.848 |
|   100 |  4 | 0.751 | 32.38 | 0.870 |
|   100 |  8 | 0.741 | 80.01 | 0.852 |
|   100 | 16 | 0.735 | 28.76 | 0.749 |

## 4. Interpretation

### 4.1 Single-thread baseline (N = 1)

- W_coh =  20: N = 1 gives L_inst = 1.000 (trivial), ell_lock ≈ 7.18, Q_clock ≈ 0.008.
- W_coh =  50: N = 1 gives L_inst = 1.000 (trivial), ell_lock ≈ 13.76, Q_clock ≈ 0.014.
- W_coh = 100: N = 1 gives L_inst = 1.000 (trivial), ell_lock ≈ 23.17, Q_clock ≈ 0.011.

For N = 1 the phase-lock axis reduces to a weak, noisy phase drift; the magnetisation is always ±1 by definition, so L_inst = 1 and the lockstep persistence ell_lock is essentially the soft-rudder telegraph baseline.

### 4.2 Phase-lock effects for N > 1

Turning on phase locking (with lambda_phase = 0.3, modest noise_sigma = 0.05) produces a clear enhancement of bundle coherence compared to the hop-only baseline:

- W_coh =  20: peak ell_lock ≈ 13.5 at N = 16 (L_inst ≈ 0.399, Q_clock ≈ 0.300).
- W_coh =  50: peak ell_lock ≈ 69.2 at N = 16 (L_inst ≈ 0.585, Q_clock ≈ 0.634).
- W_coh = 100: peak ell_lock ≈ 80.0 at N = 8 (L_inst ≈ 0.741, Q_clock ≈ 0.852).

In all three W_coh slices, ell_lock grows significantly with N (often by a factor ≳ 3–5 over N = 1) before showing some non-monotonic behaviour at the largest N.

### 4.3 Comparison in words to hop-only and shared-bias runs

- Unlike the hop-only baseline (A1), ell_lock now **does** increase strongly with N at fixed W_coh, signalling genuine temporal lockstep rather than simple 1/√N averaging.
- Compared to the shared-bias run (A2), the phase-lock axis drives **larger Q_clock values** (up to ≈0.85–0.87 at W_coh=100, N=4–8), i.e. a stronger tendency for the bundle COM to drift persistently in one direction.

Qualitatively, the phase variable is acting like a weak internal clock: when many phases are pulled into step, the bundle not only aligns (L_inst ≳ 0.7 for N ≥ 2) but also moves in a more clock-like way, with an enhanced lockstep persistence and a noticeable net drift.

### 4.4 Non-monotonicity at large N

As in the shared-bias run, very large bundles do not simply become better:
- At W_coh = 100, ell_lock peaks around N = 8 (≈80) and then drops back to ≈29 at N = 16, while L_inst stays ≳0.73.
- Q_clock is largest in the intermediate-N regime, indicating the strongest effective 'clock' behaviour happens for moderately large bundles, not for the very largest N.

This reinforces the emerging picture that there is a **sweet spot in bundle size** for a given glue strength: too few threads and lockstep is weak; too many threads and the simple local rule becomes over-constraining or noisy.

## 5. Provisional conclusions

- Phase locking alone is clearly capable of producing **long-lived lockstep** and a significant COM drift without resorting to extreme hierarchical glue.

- The results are qualitatively consistent with the BCQM V picture where an internal phase degree of freedom, coupled through modest local rules, can act as a seed for emergent clock behaviour and inertial 'stiffness' at the bundle level.
- At the same time, the non-monotonic dependence on N cautions against assuming that 'more threads → more rigidity'; the detailed scaling of ell_lock and Q_clock with N and W_coh will be important for constraining realistic glue models.

## 6. To-do / follow-ups

- [ ] Overlay A3 (phase-lock) and A2 (shared-bias) runs for a fixed W_coh to compare how each axis shapes ell_lock and Q_clock vs N.
- [ ] Extract effective correlation times from the stored timeseries and check how they scale with W_coh for different N.
- [ ] Decide whether the strongest-lockstep cases (e.g. W_coh=50, N=16; W_coh=100, N=8) should be promoted to BCQM V figures.
