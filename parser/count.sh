#!/bin/sh

DIRS="alia auflia auflira aufnira bv lia lra nia nra qf_abv qf_alia qf_aufbv qf_auflia qf_ax qf_idl qf_lra qf_nia qf_nra qf_rdl qf_uf qf_ufbv qf_ufidl qf_uflia qf_uflra qf_ufnra uf ufbv uflia"

for i in $DIRS; do
    echo -n "$i : ";
    npickle=`ls $i/$i/*.pickle | wc -l`;
    echo $npickle;
done
