# ColdFront_Detection_pipeline

initial running for 16142, 16143, 16626, 16627 (reference)

fluximage
→ mkpsfmap
→ wavdetect
→ reproject_aspect
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
# Processing each ID before Alignment

run from the repro/ files and ardlib is global and so need to change everytime switches different obsID

```bash
punlearn ardlib
acis_set_ardlib ./acisf16142_repro_bpix1.fits
```
### CIAO Tool: `dmextract`

creates the lightcurve

```bash
punlearn dmextract
dmextract "acisf16142_repro_evt2.fits[energy=500:7000][bin time=::259.28]" outfile=16142_lc.fits opt=ltc1 clobber=yes
```
### CIAO Tool: `deflare`

used for deflaring

```bash
punlearn deflare
deflare 16142_lc.fits 16142_gti.fits method=clean plot=no save=16142_lc.png
eog 16142_lc.png
```
### CIAO Tool: `dmcopy'

Here used to apply GTI to Event File

punlearn dmcopy
dmcopy "acisf16142_repro_evt2.fits[@16142_gti.fits]" acisf16142_cleaned_evt2.fits clobber=yes
```
