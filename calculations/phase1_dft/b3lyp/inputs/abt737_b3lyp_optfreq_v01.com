%oldchk=archive/chk/abt737_pm6_opt_v01.run002.chk
%chk=archive/chk/abt737_b3lyp_optfreq_v01.chk
%mem=32GB
%nprocshared=16
#p opt freq B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Water) geom=check

abt737 B3LYP-D3(BJ)/6-31G(d,p) SMD-water opt+freq | from PM6 chk | v01

0 1

