# RUN_REPORT – run_V1_all_axes_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Glue axes: **all enabled** (shared bias + phase lock + domains)
- Config file: `configs/run_V1_all_axes.yml`
- Output directory (convention): `outputs_glue_axes/run_V1_all_axes`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [2, 4, 8, 16, 32]
- Ensembles per (W_coh, N): 64
- Steps: 4000  (burn-in: 400)
- Hop coherence (soft-rudder telegraph): form=power_law, alpha=1.0, k_prefactor=2.0, memory_depth=1
- Shared-bias glue: enabled=True, lambda_bias=0.3
- Phase-lock axis: enabled=True, lambda_phase=0.3, theta_join=0.3, theta_break=1.5, omega_0=0.1, noise_sigma=0.05
- Domains axis: enabled=True, n_initial_domains=4, lambda_domain=0.3, merge_threshold=0.8, split_threshold=0.3, min_domain_size=2
- Diagnostics: store_states=True, compute_lockstep=True, compute_psd=False

## 3. Numerical outputs (lockstep metrics)

Summary table from `summary.json` (per (W_coh, N)):

| W_coh | N  | L_inst | ell_lock | Q_clock |
|------:|---:|-------:|---------:|--------:|
|    20 |  2 | 0.615 | 7.11 | 0.280 |
|    20 |  4 | 0.687 | 10.75 | 0.274 |
|    20 |  8 | 0.748 | 24.86 | 0.288 |
|    20 | 16 | 0.794 | 130.42 | 0.305 |
|    20 | 32 | 0.818 | 19.16 | 0.219 |
|    50 |  2 | 0.711 | 12.99 | 0.552 |
|    50 |  4 | 0.840 | 33.72 | 0.520 |
|    50 |  8 | 0.892 | 192.94 | 0.477 |
|    50 | 16 | 0.912 | 20.74 | 0.129 |
|    50 | 32 | 0.924 | 3.78 | 0.126 |
|   100 |  2 | 0.793 | 20.58 | 0.869 |
|   100 |  4 | 0.920 | 86.34 | 0.948 |
|   100 |  8 | 0.945 | 87.27 | 0.374 |
|   100 | 16 | 0.955 | 9.47 | 0.011 |
|   100 | 32 | 0.962 | 3.83 | 0.094 |

## 4. Interpretation

### 4.1 Overall pattern

With all three glue axes active, the bundles show **strong instantaneous alignment**, **very long lockstep** at intermediate N, and **substantial clock-like drift** for the stiffer, higher-$W_{\mathrm{coh}}$ cases:

- W_coh =  20: peak ell_lock ≈ 130.4 at N = 16 (L_inst ≈ 0.794, Q_clock ≈ 0.305).
- W_coh =  50: peak ell_lock ≈ 192.9 at N = 8 (L_inst ≈ 0.892, Q_clock ≈ 0.477).
- W_coh = 100: peak ell_lock ≈ 87.3 at N = 8 (L_inst ≈ 0.945, Q_clock ≈ 0.374).

For example, $\ell_{\mathrm{lock}}$ reaches ~130 at $W_{\mathrm{coh}}=20$, $N=16$, ~193 at $W_{\mathrm{coh}}=50$, $N=8$, and ≈86--87 at $W_{\mathrm{coh}}=100$, $N=4$--8. These are significantly larger than the hop-only baseline and comparable to, or above, the strongest A2--A4 cases.

### 4.2 Alignment and clock behaviour

- $L_{\mathrm{inst}}$ is high across the board (typically 0.6--0.96), indicating that bundles spend most of their time in strongly aligned states.
- $Q_{\mathrm{clock}}$ becomes very large in the high-$W_{\mathrm{coh}}$, moderate-$N$ regime: at $W_{\mathrm{coh}}=100$ we see $Q_{\mathrm{clock}} \approx 0.87$ for $N=2$ and $\approx 0.95$ for $N=4$, signalling a pronounced net drift of the COM.

This is stronger ``clock behaviour'' than in the shared-bias and domains-only runs and is comparable to, or slightly more extreme than, the phase-lock-only A3 run.  It fits the intuition that combining phase coupling with mean-field and domain glue yields a very stiff, clock-like bundle at intermediate sizes.

### 4.3 Non-monotonicity in $N$

As in the A-series, increasing $N$ does **not** simply make everything stiffer. Instead, for fixed $W_{\mathrm{coh}}$ we see a clear sweet spot in $N$ where $\ell_{\mathrm{lock}}$ is maximal, followed by a drop:

- W_coh =  20: ell_lock vs N → N=2: 7.1, N=4: 10.8, N=8: 24.9, N=16: 130.4, N=32: 19.2
- W_coh =  50: ell_lock vs N → N=2: 13.0, N=4: 33.7, N=8: 192.9, N=16: 20.7, N=32: 3.8
- W_coh = 100: ell_lock vs N → N=2: 20.6, N=4: 86.3, N=8: 87.3, N=16: 9.5, N=32: 3.8

For instance, at $W_{\mathrm{coh}}=50$ $\ell_{\mathrm{lock}}$ climbs from ≈13 (N=2) to ≈193 (N=8) and then falls to ≈21 (N=16) and ≈3.8 (N=32).  A similar pattern holds at $W_{\mathrm{coh}}=100$.  This mirrors the A2--A4 behaviour: for a fixed glue strength, there is an optimal bundle size beyond which extra threads actually reduce the effective lockstep.

### 4.4 Comparison to A1--A4

- Relative to **A1 hop-only**, V1 shows the expected transition from diffusive bundles to stiff, clock-like bundles: $\ell_{\mathrm{lock}}$ and $Q_{\mathrm{clock}}$ are both dramatically enhanced.
- Compared to **A2 shared-bias**, $\ell_{\mathrm{lock}}$ peaks are larger and $Q_{\mathrm{clock}}$ is significantly higher at large $W_{\mathrm{coh}}$, reflecting the added effect of phase coupling and domains.
- Compared to **A3 phase-lock**, the all-axes run keeps similarly high $Q_{\mathrm{clock}}$ in the stiff regime but also benefits from domain glue, which can support high lockstep even at moderate global magnetisation.
- Compared to **A4 domains**, V1 tends to have higher $L_{\mathrm{inst}}$ and stronger drift; domains in combination with shared-bias and phase-lock appear to play more of a ``background rigidity'' role rather than limiting global alignment.

## 5. Provisional conclusions

- The V1 all-axes run behaves like a **hybrid of the strongest features** of the A-series: it can sustain long-lived lockstep and strong COM drift at intermediate $N$ and large $W_{\mathrm{coh}}$, without locking completely into the pathological 2×2 hierarchical regime explored in IV\_d lab runs.

- The persistence of a sweet spot in $N$, and the collapse of $\ell_{\mathrm{lock}}$ for the largest bundles, is a robust feature: realistic glue models in BCQM~V will need to respect this constraint rather than assuming indefinitely increasing rigidity with bundle size.

- From a BCQM perspective, V1 provides a first concrete example of a bundle that looks simultaneously ``spacetime-like'' (domains providing local rigidity) and ``mass/clock-like'' (phase + shared bias providing coherent drift and inertia).

## 6. To-do / follow-ups

- [ ] Produce comparison plots of A1--A4 vs V1 at fixed $W_{\mathrm{coh}}$ ($\ell_{\mathrm{lock}}$ and $Q_{\mathrm{clock}}$ vs $N$).
- [ ] Inspect a few V1 trajectories in detail to see how domains, phase, and bias co-evolve during long lockstep episodes.
- [ ] Decide which V1 slices (e.g. $W_{\mathrm{coh}}=50$, $N=8$ or $W_{\mathrm{coh}}=100$, $N=4$) are the best candidates to illustrate ``near-ballistic'' bundle behaviour in BCQM~V.
