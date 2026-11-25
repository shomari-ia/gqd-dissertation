# Scientific formula library

Working reference for design, teaching, dissertation slides and oral defense. Symbols and units must be defined in final captions. These are method equations, not new results.

## F-001 — Orbital normalization (VE-001)

$$\int_{\mathbb R^3}|\psi_i(\mathbf r)|^2\,d^3r=1$$

Grid estimate: $I_i\approx |\det A|\sum_j|\psi_i(\mathbf r_j)|^2$, where the three cube-grid step vectors form $A$. Deviation (%): $100|I_i-1|$. The integral tests numerical representation, not localization.

## F-002 — Fragment spatial localization proxy (VE-002)

$$P_{\mathrm{GQD}}=100\frac{\int_{\Omega_{\mathrm{GQD}}}|\psi_i(\mathbf r)|^2dV}{\int_{\Omega_{\mathrm{total}}}|\psi_i(\mathbf r)|^2dV}$$

Assign each grid point to the fragment containing its nearest nucleus (split exact ties equally). Repeat with heavy atoms only as a sensitivity check. This is a geometric partition of squared orbital amplitude, not an AO population, Hirshfeld charge, or QTAIM basin.

## F-003 — Adsorption electronic energy

$$E_{\mathrm{bind,raw,SMD}}=E_{AB}^{\mathrm{SMD}}-E_A^{\mathrm{SMD}}-E_B^{\mathrm{SMD}}$$

Negative binding energy favors adsorption under the stated reference convention. The accepted mixed correction uses gas-phase counterpoise on the frozen SMD geometries:

$$E_{\mathrm{bind,SMD+BSSE}}=E_{\mathrm{bind,raw,SMD}}+\mathrm{BSSE}_{\mathrm{gas}}$$

Do not describe this as a direct solvent counterpoise calculation or as Gibbs free energy. See SE-ERL-007 and SE-ERL-008.

## F-004 — Reduced density gradient

$$s(\mathbf r)=\frac{|\nabla\rho|}{2(3\pi^2)^{1/3}\rho^{4/3}}$$

NCI uses $s$ and $\mathrm{sign}(\lambda_2)\rho$, where $\lambda_2$ is the intermediate eigenvalue of the density Hessian. Negative signed density indicates attractive character; near-zero weak interactions; positive steric/repulsive character. This is not an energy decomposition. Grid counts are sampling descriptors; full-box fractions depend on bounding box.

## F-005 — QTAIM

Bond critical point: $\nabla\rho=0$ with Hessian signature $(3,-1)$, two negative and one positive eigenvalues. Laplacian $\nabla^2\rho=\lambda_1+\lambda_2+\lambda_3$. The accepted Edge CP 275 connects H75 and N81. Positive Laplacian supports closed-shell character but does not alone settle covalency or interaction strength.

## F-006 — Frontier orbital energy gap

$$E_g=E_{\mathrm{LUMO}}-E_{\mathrm{HOMO}}$$

Report as a method-dependent orbital-energy gap, not an experimental optical gap or excitation energy.
