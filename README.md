# ColdFront_Detection_pipeline

initial running for 16142, 16143, 16626, 16627 (reference)

 reproject_aspect
→ reproject_events
→ blanksky
→ fluximage
→ mkpsfmap
→ wavdetect
→ dmfilth
→ merge_obs

### CIAO Tool: `chandra_repro`

run from parent directory at the location of four ObsID, for my analysis- data/

```bash
chandra_repro indir=16142,16143,16626,16627 verbose=1 outdir="" clobber=yes check_vf_pha=yes
```
# Pre-processing each ID before Alignment

run from the repro/ files and ardlib is global and so need to change everytime switches different obsID

```bash
punlearn ardlib
acis_set_ardlib ./acisf16142_repro_bpix1.fits
```
### CIAO Tool: `dmextract`, `deflare`, `dmcopy`

creates the lightcurve by `dmextract`, `deflare` used for deflaring and `dmcopy` to GTI to Event File

```bash
punlearn dmextract
dmextract "acisf16142_repro_evt2.fits[energy=500:7000][bin time=::259.28]" outfile=16142_lc.fits opt=ltc1 clobber=yes

punlearn deflare
deflare 16142_lc.fits 16142_gti.fits method=clean plot=no save=16142_lc.png
eog 16142_lc.png

punlearn dmcopy
dmcopy "acisf16142_repro_evt2.fits[@16142_gti.fits]" acisf16142_cleaned_evt2.fits clobber=yes
```
### CIAO Tool: `fluximage`

create temporary fluximage and exposure maps

```bash
punlearn fluximage
fluximage infile=./acisf16142_cleaned_evt2.fits outroot=./16142 binsize=1 bands=0.5:7:2.3 clobber=yes
```

### CIAO Tool: `mkpsfmap`

create psfmaps for wavedetect to identify sources

```bash
punlearn mkpsfmap
mkpsfmap infile=./16142_0.5-7_thresh.img \
         outfile=./16142_0.5-7.psf \
         energy=2.3 ecf=0.9 clobber=yes
```
### CIAO Tool: `wavdetect`

make source lists in region files

```bash
punlearn wavdetect
wavdetect infile=./16142_0.5-7_thresh.img \
         psffile=./16142_0.5-7.psf \
         expfile=./16142_0.5-7_thresh.expmap \
         outfile=./16142_src_0.5-7.fits \
         scellfile=./16142_scell_0.5-7.fits \
         imagefile=./16142_imgfile_0.5-7.img \
         defnbkgfile=./16142_defnbkg_0.5-7.fits \
         regfile=./16142_src_0.5-7-noem.reg \
         scales="1 2 4 8 16 32" \
         maxiter=3 sigthresh=5e-6 ellsigma=5.0 \
         clobber=yes
```
# Correcting Absolute Astrometry

Further analysis needs the RA-Dec coordinate system in the decimal system.

```bash
python regCoord_change.py
```

### CIAO Tool: `wcs_match`

Align the images

```bash
punlearn wcs_match

pset wcs_match infile=16142_src.asc
pset wcs_match refsrcfile="../../16627/repro/16627_src.asc"
pset wcs_match outfile=16142.xform
pset wcs_match wcsfile=16142_0.5-7_thresh.img
pset wcs_match method=trans
pset wcs_match radius=2.0
pset wcs_match verbose=1

wcs_match
clobber=yes
```
