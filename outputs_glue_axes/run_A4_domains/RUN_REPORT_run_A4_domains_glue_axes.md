# RUN_REPORT – run_A4_domains_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Glue axes: **domains only** (no shared bias, no phase locking)
- Config file: `configs/run_A4_domains.yml`
- Output directory (convention): `outputs_glue_axes/run_A4_domains`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [4, 8, 16, 32]
- Ensembles per (W_coh, N): 32
- Steps: 2000  (burn-in: 200)
- Hop coherence (soft-rudder telegraph): form=power_law, alpha=1.0, k_prefactor=2.0
- Shared-bias glue: enabled=False, lambda_bias=0.0
- Phase-lock axis: enabled=False, lambda_phase=0.0, omega_0=0.1, noise_sigma=0.0
- Domains axis: **enabled=True**, n_initial_domains=4, lambda_domain=0.4, merge_threshold=0.8, split_threshold=0.3, min_domain_size=2
- Diagnostics: store_states=True, compute_lockstep=True

## 3. Numerical outputs (lockstep metrics)

Summary table from `summary.json` (per (W_coh, N)):

| W_coh | N  | L_inst | ell_lock | Q_clock |
|------:|---:|-------:|---------:|--------:|
|    20 |  4 | 0.418 | 7.62 | 0.025 |
|    20 |  8 | 0.333 | 8.38 | 0.002 |
|    20 | 16 | 0.278 | 9.66 | 0.012 |
|    20 | 32 | 0.246 | 12.60 | 0.001 |
|    50 |  4 | 0.412 | 16.06 | 0.022 |
|    50 |  8 | 0.376 | 20.83 | 0.015 |
|    50 | 16 | 0.343 | 31.05 | 0.054 |
|    50 | 32 | 0.348 | 64.76 | 0.146 |
|   100 |  4 | 0.413 | 24.15 | 0.002 |
|   100 |  8 | 0.402 | 42.27 | 0.105 |
|   100 | 16 | 0.390 | 81.18 | 0.015 |
|   100 | 32 | 0.306 | 105.04 | 0.185 |

## 4. Interpretation

### 4.1 General pattern

This run isolates the **domain glue axis**. Threads start in four domains and feel a local tendency to align with the magnetisation of their current domain, with lambda_domain = 0.4. There is no global shared bias and no explicit phase locking.

Across all W_coh slices, we see:
- L_inst decreasing moderately with N (≈0.42 → 0.25–0.35 as N goes 4 → 32),
- ell_lock growing substantially with N, especially at larger W_coh,
- Q_clock remaining modest for small N but becoming noticeable (≲0.19) at large N and large W_coh.

### 4.2 Behaviour by W_coh

- **W_coh = 20**:
  - N =  4: L_inst ≈ 0.418, ell_lock ≈ 7.62, Q_clock ≈ 0.025
  - N =  8: L_inst ≈ 0.333, ell_lock ≈ 8.38, Q_clock ≈ 0.002
  - N = 16: L_inst ≈ 0.278, ell_lock ≈ 9.66, Q_clock ≈ 0.012
  - N = 32: L_inst ≈ 0.246, ell_lock ≈ 12.60, Q_clock ≈ 0.001
- **W_coh = 50**:
  - N =  4: L_inst ≈ 0.412, ell_lock ≈ 16.06, Q_clock ≈ 0.022
  - N =  8: L_inst ≈ 0.376, ell_lock ≈ 20.83, Q_clock ≈ 0.015
  - N = 16: L_inst ≈ 0.343, ell_lock ≈ 31.05, Q_clock ≈ 0.054
  - N = 32: L_inst ≈ 0.348, ell_lock ≈ 64.76, Q_clock ≈ 0.146
- **W_coh = 100**:
  - N =  4: L_inst ≈ 0.413, ell_lock ≈ 24.15, Q_clock ≈ 0.002
  - N =  8: L_inst ≈ 0.402, ell_lock ≈ 42.27, Q_clock ≈ 0.105
  - N = 16: L_inst ≈ 0.390, ell_lock ≈ 81.18, Q_clock ≈ 0.015
  - N = 32: L_inst ≈ 0.306, ell_lock ≈ 105.04, Q_clock ≈ 0.185

The broad trend is that increasing W_coh boosts ell_lock at all N, just as in the hop-only baseline, but domains amplify the growth with N much more strongly.

### 4.3 Comparison to other glue axes

- Compared to **A1 hop-only**, ell_lock now grows strongly with N at fixed W_coh, so domains clearly provide genuine temporal lockstep rather than mere averaging.
- Compared to **A2 shared-bias**, the domain axis produces a slower rise in L_inst but can still reach very large ell_lock for big bundles (e.g. W_coh = 100, N = 32 gives ell_lock ≈ 105 with L_inst ≈ 0.306).
- Compared to **A3 phase-lock**, Q_clock values are generally smaller here for the same N and W_coh, indicating that domains favour **static rigidity** (long lockstep, modest drift) rather than the stronger clock-like drift seen with explicit phase coupling.

### 4.4 Qualitative picture

Intuitively, the domains axis behaves like a **patchy, localised glue**:
- Within each domain, threads are nudged toward local magnetisation, so local blocks stiffen.
- Because different domains can have different signs, global L_inst does not shoot to 1; instead we stabilise a mosaic of locally rigid regions whose net alignment remains moderate.
- As N increases, there are more threads per domain and the local averaging becomes stronger, which shows up as a steady increase in ell_lock with N and W_coh.

This is qualitatively distinct from both shared-bias (global mean-field glue) and phase-lock (internal clock glue) and will be useful in BCQM V as an analogue of local spacetime patches vs global inertial frames.

## 5. Provisional conclusions

- The domains axis on its own is **capable of generating long-lived lockstep**, especially at large W_coh and N, without forcing global alignment.

- The resulting bundles look like **locally stiff, globally mosaic** objects: good internal coherence, moderate overall magnetisation, and only modest COM drift except at the largest N.

- This makes domains a good candidate for modelling emergent **spacetime-like rigidity** in BCQM V, in contrast to the more particle-/clock-like behaviour of the phase-lock axis.

## 6. To-do / follow-ups

- [ ] Plot ell_lock vs N at fixed W_coh and compare directly with hop-only (A1) and shared-bias (A2) results.
- [ ] Inspect domain-level statistics (sizes, magnetisations) from the stored timeseries to see how the mosaic structure evolves.
- [ ] Decide whether any of the large-ell_lock slices (e.g. W_coh=100, N=32) should be promoted to BCQM V figures.
