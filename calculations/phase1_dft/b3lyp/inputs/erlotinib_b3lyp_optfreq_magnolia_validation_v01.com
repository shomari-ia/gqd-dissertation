%oldchk=archive/chk/erlotinib_pm6_opt_v01_magnolia_seed.chk
%chk=archive/chk/erlotinib_b3lyp_optfreq_magnolia_validation_v01.chk
%mem=32GB
%nprocshared=16
#p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

erlotinib B3LYP-D3(BJ)/6-31G(d,p) SMD-water opt+freq | Magnolia cross-platform validation | v01

0 1
