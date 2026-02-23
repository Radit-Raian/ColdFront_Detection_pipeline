# ColdFront_Detection_pipeline

initial running for 16142, 16143, 16626, 16627 (reference)

→ deflare
→ fluximage
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
