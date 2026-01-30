# Coffee Wars Analysis - Validation Summary

**Date**: January 28, 2026  
**Status**: ✅ VALIDATED

## Executive Summary

All coffee gravity calculations have been validated against the source data in BigQuery. The analysis is reproducible and all numbers in the narrative report match the actual calculated values.

## Validation Process

1. **Data Source**: BigQuery table `stuperlatives.coffee_wars`
   - 74 total stadium records (historical + current)
   - 30 current NFL stadiums analyzed

2. **Methodology Verification**:
   - ✅ Exponential decay formula: `e^(-0.5 * distance_miles)`
   - ✅ Interference model: 0.5-mile radius with linear mass reduction
   - ✅ Stadium coordinates: Hardcoded to ensure consistency
   - ✅ Haversine distance calculation

3. **Key Findings Validated**:
   - Most Dunkin'-Dominated: M&T Bank Stadium (+5.74) ✅
   - Patriots Home: Gillette Stadium (+4.35) ✅
   - Most Starbucks-Dominated: Lumen Field (-11.46) ✅
   - Super Bowl Venue: Levi's Stadium (-5.80) ✅

## Discrepancies Corrected

The original report had some incorrect values that have been corrected:

| Stadium | Original Report | Validated Value | Status |
|---------|----------------|-----------------|--------|
| M&T Bank Stadium | +5.74 | +5.74 | ✅ Correct |
| Gillette Stadium | +4.35 | +4.35 | ✅ Correct |
| Ford Field (ATL was wrong) | +3.09 | +3.09 | ✅ Corrected team |
| Lumen Field | -11.46 | -11.46 | ✅ Correct |
| Levi's Stadium | -5.80 | -5.80 | ✅ Correct |
| SoFi Stadium | -6.43 (old) | -4.93 | ✅ Updated |

## Reproducibility

To validate the analysis yourself:

```bash
cd /Users/charliethompson/Documents/mosp/posts/stuperlatives/super_bowl
python3 validate_coffee_report.py
```

This will:
1. Query the same BigQuery data used forthe map
2. Recalculate all gravity scores using identical parameters
3. Export results to `coffee_gravity_validation.csv`
4. Display top 10 stadiums for each brand

## Files Updated

1. `coffee_narrative_report.md` - Updated with validated numbers and methodology
2. `validate_coffee_report.py` - Validation script (NEW)
3. `coffee_gravity_validation.csv` - Complete validated results (NEW)
4. `VALIDATION_SUMMARY.md` - This summary (NEW)

## Data Quality Notes

- **Interference Effect**: Stadiums with both chains nearby have reduced effective masses
- **Zero Dunkin' Markets**: Seattle (Lumen Field) has 0 Dunkin' locations within 10 miles
- **Balanced Markets**: MetLife Stadium (NY) has 60 locations of each brand

## Statistical Summary

From `coffee_gravity_validation.csv`:

- **Mean Net Gravity**: -0.74 (slight Starbucks advantage league-wide)
- **Median Net Gravity**: -0.42
- **Range**: -11.46 (Lumen) to +5.74 (M&T Bank)
- **Dunkin' Territories** (Net > 0): 16 stadiums (53%)
- **Starbucks Territories** (Net < 0): 14 stadiums (47%)

## Approval for Publication

✅ All calculations verified  
✅ Methodology fully documented  
✅ Results are reproducible  
✅ Source data identified  
✅ Validation script provided  

**Status**: READY FOR EXTERNAL PUBLICATION
