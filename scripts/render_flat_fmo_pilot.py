#!/usr/bin/env python3
"""Flat orbital rendering pilot from accepted Gaussian MO cubes, no new SCF."""
import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import skimage
from skimage.measure import marching_cubes
from ase.data import covalent_radii
from ase.units import Bohr
from analyze_orbital_cubes import read_cube

BASE = Path("calculations/phase1_dft/descriptors/orbitals/results")
AID = "CUBEGEN-ERLOTINIB-FLAT-FMO-PILOT-001"
ISO = 0.020
PHASE = {"positive": "#D65E36", "negative": "#347DA6"}

def sha(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def frame(atoms):
    xyz = atoms[:, 2:5] * Bohr
    z = atoms[:, 0].astype(int)
    # Carboxyl C72 excluded; remaining 54 carrier carbons define basal plane.
    mask = (z[:75] == 6)
    mask[71] = False
    if z[71] != 6 or mask.sum() != 54:
        raise ValueError("Unexpected carrier atom order")
    ring = xyz[:75][mask]
    center = ring.mean(axis=0)
    _, _, vh = np.linalg.svd(ring-center, full_matrices=False)
    normal = vh[-1]
    if np.dot(normal, xyz[75:].mean(axis=0)-center) < 0:
        normal = -normal
    anchor = ring[np.argmax(np.linalg.norm(ring-center,axis=1))]-center
    x = anchor-np.dot(anchor,normal)*normal
    x /= np.linalg.norm(x)
    y = np.cross(normal,x)
    return xyz, z, center, np.column_stack((x,y,normal))

def extract(data, sign, center, rot):
    field = data["values"].reshape(data["dims"], order="C")
    # Check all six boundary planes: no isosurface clipped at cube boundary.
    boundary = max(np.max(np.abs(np.take(field,i,axis=a))) for a in range(3) for i in (0,-1))
    if boundary >= ISO:
        raise ValueError(f"Cube boundary amplitude {boundary} reaches isovalue")
    if not field.min() < sign*ISO < field.max():
        raise ValueError("Requested signed isovalue absent")
    v, f, _, _ = marching_cubes(field, level=sign*ISO, allow_degenerate=False)
    raw = (data["origin"] + v @ np.asarray(data["vecs"])) * Bohr
    aligned = (raw-center) @ rot
    if not len(f) or not np.isfinite(aligned).all():
        raise ValueError("Invalid extracted surface")
    return aligned, f, float(boundary)

def bonds(xyz,z):
    result=[]
    for i in range(len(z)):
        for k in range(i+1,len(z)):
            if (i<75)!=(k<75): continue
            if z[i]==1 and z[k]==1: continue
            dist=np.linalg.norm(xyz[i]-xyz[k])
            if 0.5 < dist <= 1.20*(covalent_radii[z[i]]+covalent_radii[z[k]]):
                result.append((i,k))
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", type=Path, required=True)
    args=ap.parse_args()
    if args.outdir.exists():
        raise SystemExit(f"Refusing existing output directory: {args.outdir}")
    with (BASE/"erlotinib_fmo_cube_qc_comparison.tsv").open() as f:
        qc={r["orbital"]:r for r in csv.DictReader(f,delimiter="\t") if r["pose"]=="flat"}
    pair={}
    source={}
    for orb,idx in (("HOMO",286),("LUMO",287)):
        path=BASE/AID/f"erlotinib_flat_m062x_{orb.lower()}.cube"
        digest=sha(path)
        if digest!=qc[orb]["cube_sha256"] or qc[orb]["qc_status"]!="PASS":
            raise ValueError(f"{orb}: canonical QC hash mismatch")
        d=read_cube(path)
        if d["nat"]!=127 or d["mo_index"]!=idx or abs(d["norm2"]-1)>0.01:
            raise ValueError(f"{orb}: grid QC failed")
        pair[orb]=d
        source[orb]={"path":str(path),"sha256":digest,"mo_index":idx,"grid":d["dims"],"norm":d["norm2"]}
    h,l=pair.values()
    if h["dims"]!=l["dims"] or any(not np.allclose(h[k],l[k],rtol=0,atol=1e-10) for k in ("atoms","origin","vecs")):
        raise ValueError("HOMO/LUMO geometry/grid mismatch")
    xyz,z,center,rot=frame(h["atoms"])
    if Counter(z[:75])!=Counter({6:55,1:18,8:2}) or Counter(z[75:])!=Counter({6:22,1:23,7:3,8:4}):
        raise ValueError("Fragment formula check failed")
    aligned=(xyz-center)@rot
    edges=bonds(xyz,z)
    meshes={}
    for orb,d in pair.items():
        for name,sign in (("positive",1),("negative",-1)):
            meshes[(orb,name)]=extract(d,sign,center,rot)
    coords=np.concatenate([aligned]+[v for v,f,b in meshes.values()])
    lo=coords.min(axis=0)-0.65
    hi=coords.max(axis=0)+0.65
    # A single common box for the two orbitals and both views in this pilot.
    args.outdir.mkdir(parents=True,exist_ok=False)
    metadata={"analysis_id":args.outdir.name,"source":source,"isovalue_au":ISO,
              "bohr_to_angstrom":Bohr,"center_angstrom":center.tolist(),"rotation_columns":rot.tolist(),
              "bounds_angstrom":[lo.tolist(),hi.tolist()],"bond_rule":"Within-fragment distances <=1.20 times sum of ASE covalent radii; display only",
              "python":platform.python_version(),"numpy":np.__version__,"matplotlib":matplotlib.__version__,
              "skimage":skimage.__version__,"git_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
              "slurm_job_id":os.getenv("SLURM_JOB_ID","NA"),"mesh":{}}
    for (orb,name),(v,f,b) in meshes.items():
        key=f"{orb.lower()}_{name}"
        np.savez_compressed(args.outdir/f"{key}.npz",vertices_angstrom_aligned=v,faces=f)
        metadata["mesh"][key]={"vertices":len(v),"faces":len(f),"boundary_abs_max":b}
        print(f"PASS {key}: vertices={len(v)} faces={len(f)} boundary_abs_max={b:.6g}",flush=True)
    np.savez_compressed(args.outdir/"geometry_and_frame.npz",atomic_numbers=z,xyz_angstrom=xyz,xyz_aligned_angstrom=aligned,
                        center_angstrom=center,rotation_columns=rot,bonds_display=np.asarray(edges))
    fig=plt.figure(figsize=(12,10),facecolor="white")
    colors={1:"#C8CDD0",6:"#525A60",7:"#3164A0",8:"#C23B39"}
    for row,orb in enumerate(("HOMO","LUMO")):
        for col,(elev,azim,label) in enumerate(((75,-90,"Near face-on"),(12,-75,"Side-oblique"))):
            ax=fig.add_subplot(2,2,row*2+col+1,projection="3d",computed_zorder=False)
            for name in ("positive","negative"):
                v,f,_=meshes[(orb,name)]
                ax.add_collection3d(Poly3DCollection(v[f],facecolor=PHASE[name],edgecolor="none",alpha=.46,zorder=2))
            ax.add_collection3d(Line3DCollection([[aligned[a],aligned[b]] for a,b in edges],colors="#596167",linewidths=.85,zorder=1))
            ax.scatter(*aligned.T,s=[9 if a==1 else 22 for a in z],c=[colors[a] for a in z],depthshade=False,zorder=3)
            ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]))
            ax.set_box_aspect(hi-lo)
            ax.set_proj_type("ortho")
            ax.view_init(elev=elev,azim=azim)
            ax.set_axis_off()
            ax.set_title(f"{orb} {source[orb]['mo_index']} | {label}",fontsize=13)
    fig.suptitle("Erlotinib / COOH-GQD — Flat frontier orbitals",fontsize=20,y=.97)
    fig.legend(handles=[Patch(color=PHASE["positive"],label="+0.020 a.u."),Patch(color=PHASE["negative"],label="-0.020 a.u."),
                        Line2D([0],[0],marker="o",color="none",markerfacecolor="#525A60",label="C"),
                        Line2D([0],[0],marker="o",color="none",markerfacecolor="#3164A0",label="N"),
                        Line2D([0],[0],marker="o",color="none",markerfacecolor="#C23B39",label="O"),
                        Line2D([0],[0],marker="o",color="none",markerfacecolor="#C8CDD0",label="H")],
               loc="lower center",ncol=6,bbox_to_anchor=(.5,.065),frameon=False)
    fig.text(.5,.035,"M06-2X/6-311+G(d,p), SMD water | Frozen accepted geometry | Phase colors denote orbital sign, not charge.",ha="center",fontsize=10)
    fig.subplots_adjust(left=.02,right=.98,bottom=.11,top=.92,wspace=.01,hspace=.1)
    fig.savefig(args.outdir/"flat_fmo_pilot.png",dpi=220)
    plt.close(fig)
    metadata["outputs"]={p.name:sha(p) for p in sorted(args.outdir.iterdir()) if p.is_file()}
    (args.outdir/"manifest.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print("FLAT_FMO_RENDER_EXECUTION=PASS")
    print(f"Output: {args.outdir}")
    print("VISUAL_REVIEW=PENDING")

if __name__=="__main__":
    main()
