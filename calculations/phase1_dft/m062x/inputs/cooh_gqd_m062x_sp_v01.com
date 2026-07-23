%oldchk=archive/chk/cooh_gqd_b3lyp_optfreq_v01.chk
%chk=archive/chk/cooh_gqd_m062x_sp_v01.chk
%mem=32GB
%nprocshared=16
#p M06-2X/6-311+G(d,p) SCRF=(SMD,Solvent=Water) geom=check

cooh_gqd M06-2X/6-311+G(d,p) SMD-water single point | validation | v01

0 1

