# RUN_REPORT – run_A1_hop_only_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Glue axes: **none** (pure hop-coherence / soft-rudder baseline)
- Config file: `configs/run_A1_hop_only.yml`
- Output directory (convention): `outputs_glue_axes/run_A1_hop_only`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [1, 2, 4, 8]
- Ensembles per (W_coh, N): 32
- Steps: 2000  (burn-in: 200)
- Hop coherence (soft-rudder telegraph): form=power_law, alpha=1.0, k_prefactor=2.0
- Shared-bias glue: enabled=False, lambda_bias=0.0
- Phase-lock axis: enabled=False, lambda_phase=0.0
- Domains axis: enabled=False, n_initial_domains=1, lambda_domain=0.0
- Diagnostics: store_states=True, compute_lockstep=True

## 3. Numerical outputs (lockstep metrics)

Summary table from `summary.json` (per (W_coh, N)):

| W_coh | N  | L_inst | ell_lock | Q_clock |
|------:|---:|-------:|---------:|--------:|
|    20 |  1 | 1.000 | 6.92 | 0.016 |
|    20 |  2 | 0.496 | 7.12 | 0.004 |
|    20 |  4 | 0.374 | 6.86 | 0.021 |
|    20 |  8 | 0.273 | 6.92 | 0.011 |
|    50 |  1 | 1.000 | 13.76 | 0.036 |
|    50 |  2 | 0.499 | 13.16 | 0.002 |
|    50 |  4 | 0.374 | 13.71 | 0.058 |
|    50 |  8 | 0.274 | 14.05 | 0.001 |
|   100 |  1 | 1.000 | 25.96 | 0.017 |
|   100 |  2 | 0.505 | 22.58 | 0.004 |
|   100 |  4 | 0.371 | 21.61 | 0.055 |
|   100 |  8 | 0.277 | 22.91 | 0.000 |

## 4. Interpretation

### 4.1 Single-thread baseline (N = 1)

- W_coh =  20: N = 1 gives L_inst = 1.000 (trivially fully aligned), ell_lock ≈ 6.92, Q_clock ≈ 0.016.
- W_coh =  50: N = 1 gives L_inst = 1.000 (trivially fully aligned), ell_lock ≈ 13.76, Q_clock ≈ 0.036.
- W_coh = 100: N = 1 gives L_inst = 1.000 (trivially fully aligned), ell_lock ≈ 25.96, Q_clock ≈ 0.017.

As expected for a single telegraph thread, the lockstep persistence time ell_lock grows monotonically with W_coh (≈6.9 → 13.8 → 26.0), while Q_clock remains very small: this is the pure diffusive baseline inherited from the IV_c soft-rudder law.

### 4.2 Multi-thread behaviour without glue (N > 1)

For N > 1, there is **no genuine bundle glue** in this run: the threads are independent copies of the same soft-rudder process, and any apparent coherence is just finite-N averaging.

- W_coh =  20:
  - L_inst vs N: N=2: L_inst=0.496, N=4: L_inst=0.374, N=8: L_inst=0.273
  - ell_lock vs N: N=2: ell_lock=7.12, N=4: ell_lock=6.86, N=8: ell_lock=6.92
- W_coh =  50:
  - L_inst vs N: N=2: L_inst=0.499, N=4: L_inst=0.374, N=8: L_inst=0.274
  - ell_lock vs N: N=2: ell_lock=13.16, N=4: ell_lock=13.71, N=8: ell_lock=14.05
- W_coh = 100:
  - L_inst vs N: N=2: L_inst=0.505, N=4: L_inst=0.371, N=8: L_inst=0.277
  - ell_lock vs N: N=2: ell_lock=22.58, N=4: ell_lock=21.61, N=8: ell_lock=22.91

Two key features show that bundles do **not** get any extra lockstep stiffness here:
- L_inst decreases roughly like 1/√N (≈0.50 → 0.37 → 0.27 as N goes 2 → 4 → 8), as expected for independent random telegraph processes averaged together.
- ell_lock is essentially **N-independent** at fixed W_coh; fluctuations in ell_lock are at the few-percent level and do not grow systematically with N.

Q_clock stays tiny across all (W_coh, N), which reinforces the picture that the COM performs a purely diffusive walk with no coherent drift.

## 5. Provisional conclusions

- This run provides the intended **diffusive ceiling**: with hop coherence only, bundles do not acquire extra temporal rigidity beyond the single-thread behaviour.

- Increasing N just improves the instantaneous averaging (L_inst falls like ≈1/√N) without extending the lockstep correlation time.

- Any β_COM > β_single or strong growth in ell_lock with N in later runs must therefore originate from genuine glue axes (shared bias, phase locking, domains), not from bundle size alone.

## 6. To-do / follow-ups

- [ ] Overlay these A1 ell_lock(W_coh, N) curves with the shared-bias run (A2) to make the glue effect visually explicit.
- [ ] Use stored timeseries to extract effective correlation times / diffusion constants and verify that they scale with W_coh in a way consistent with β ≈ 0.5.
- [ ] Decide whether any of these baselines should appear in BCQM V main text or be kept as lab-note material.
