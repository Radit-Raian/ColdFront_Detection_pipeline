# ColdFront_Detection_pipeline

initial running for 16142, 16143, 16626, 16627 (reference)

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
## Pre-processing each ID before Alignment

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
## Correcting Absolute Astrometry


Further analysis needs the RA-Dec coordinate system in the decimal system. 
```bash
python regCoord_change.py
```
Here we will apply both `reproject_events` and `wcs_update`. Because-

<ul>
  <li><code>wcs_update</code>:
    <ul>
      <li>Fixes absolute astrometry</li>
      <li>Applies small shift/rotation correction</li>
      <li>Does NOT change pixel grid</li>
      <li>Does NOT put files on identical tangent plane</li>
    </ul>
  </li>
</ul>

<ul>
  <li><code>reproject_events</code>:
    <ul>
      <li>Forces all event files onto the exact same sky grid</li>
      <li>Makes them compatible for merging</li>
      <li>Required before <code>merge_obs</code></li>
    </ul>
  </li>
</ul>


### CIAO Tool: `wcs_match`

Align the images

```bash
punlearn wcs_match

pset wcs_match infile=16142_src.fits
pset wcs_match refsrcfile=../../16627/repro/16627_src.fits
pset wcs_match outfile=16142.xform
pset wcs_match wcsfile=16142_0.5-7_thresh.img
pset wcs_match method=trans
pset wcs_match radius=2.0
pset wcs_match clobber=yes
wcs_match

dmlist 16142.xform"[cols a11,a12,a21,a22,t1,t2]" data,clean
```

### CIAO Tool: `wcs_update`

updating the aspect solutions and event files accordingly

```bash
punlearn wcs_update

pset wcs_update infile=pcadf16142_000N001_asol1.fits
pset wcs_update outfile=pcadf16142_000N001_corrected_asol1.fits
pset wcs_update transformfile=16142.xform
pset wcs_update wcsfile=16142_0.5-7_thresh.img
wcs_update
```

```bash
punlearn wcs_update

dmcopy acisf16142_cleaned_evt2.fits acisf16142_corrected_evt2.fits
pset wcs_update infile=acisf16142_corrected_evt2.fits
pset wcs_update outfile=acisf16142_wcs_corrected_evt2.fits
pset wcs_update transformfile=16142.xform
pset wcs_update wcsfile=16142_0.5-7_thresh.img
wcs_update

dmhedit acisf16142_corrected_evt2.fits file= op=add key=ASOLFILE value=pcadf16142_000N001_corrected_asol1.fits
```
### CIAO Tool: `reproject_events`

```bash
punlearn reproject_events

pset reproject_events infile=acisf16142_corrected_evt2.fits
pset reproject_events outfile=acisf16142_reproj_evt2.fits
pset reproject_events match=../../16627/repro/acisf16627_corrected_evt2.fits
pset reproject_events aspect=none
pset reproject_events clobber=yes
verbose=1

reproject_events
```
