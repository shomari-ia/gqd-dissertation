%oldchk=archive/chk/cooh_gqd_class2_c3_pm6_opt_v03.chk
%chk=archive/chk/cooh_gqd_class2_c3_b3lyp_optfreq_v02.chk
%mem=32GB
%nprocshared=16
#p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

cooh_gqd Class-2/C3 B3LYP-D3(BJ)/6-31G(d,p) SMD-water opt+freq | from accepted PM6 v03 chk | v02

0 1

