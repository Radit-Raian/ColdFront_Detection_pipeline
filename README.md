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
### CIAO Tool: `dmextract`, `deflare`, `dmcopy'

creates the lightcurve by dmextract, deflare used for deflaring and dmcopy to GTI to Event File

```bash
punlearn dmextract
dmextract "acisf16142_repro_evt2.fits[energy=500:7000][bin time=::259.28]" outfile=16142_lc.fits opt=ltc1 clobber=yes

punlearn deflare
deflare 16142_lc.fits 16142_gti.fits method=clean plot=no save=16142_lc.png
eog 16142_lc.png

punlearn dmcopy
dmcopy "acisf16142_repro_evt2.fits[@16142_gti.fits]" acisf16142_cleaned_evt2.fits clobber=yes
```
### CIAO Tool: `fluximage'

create temporary fluximage and exposure maps

```bash
punlearn fluximage
fluximage infile=./acisf16142_cleaned_evt2.fits outroot=./16142 binsize=1 bands=0.5:7:2.3 clobber=yes
```

