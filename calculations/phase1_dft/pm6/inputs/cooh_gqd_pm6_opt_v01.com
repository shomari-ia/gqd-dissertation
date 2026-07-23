%chk=archive/chk/cooh_gqd_pm6_opt_v01.chk
%mem=8GB
%nprocshared=8
#p PM6 opt

cooh_gqd PM6 pre-optimization | system=cooh_gqd charge=0 mult=1 | v01

0 1
 C   0.000000   0.000000   0.000000
 ... paste the Cartesian block written by Open Babel here ...

