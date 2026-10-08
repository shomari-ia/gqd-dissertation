%oldchk=archive/chk/cooh_gqd_class1_c1_pm6_opt_v03.chk
%chk=archive/chk/cooh_gqd_class1_c1_b3lyp_optfreq_v02.chk
%mem=32GB
%nprocshared=16
#p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

cooh_gqd Class-1/C1 B3LYP-D3(BJ)/6-31G(d,p) SMD-water opt+freq | from accepted PM6 v03 chk | v02

0 1

