%oldchk=archive/chk/cooh_gqd_pm6_opt_v01.chk
%chk=archive/chk/cooh_gqd_b3lyp_optfreq_v01.chk
%mem=32GB
%nprocshared=16
#p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

cooh_gqd B3LYP-D3(BJ)/6-31G(d,p) SMD-water opt+freq | from PM6 chk | v01

0 1

