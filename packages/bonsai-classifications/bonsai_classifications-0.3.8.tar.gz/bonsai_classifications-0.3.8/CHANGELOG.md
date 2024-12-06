# Changelog

## Version 0.3.8
- revise structure of `conc_` table (incl. a revision of utilities)
- use `skos:broadMatch` (one-to-many) and `skos:narrowMatch` (many-to-one) instead `skos:closeMatch`
- update documentation (readme.md + sphinx)

## Version 0.3.7

- first version of tree table for USGS
- first version of concordance table between USGS and BONSAI
- Updated BONSAI tree table to add a new sub-product (code: "fi_41118", "pig iron and direct-reduced iron")
- small adjustment to `get_bonsai_classification()`
- fix mapping types in "bonsai to undata_energy_stats"
- fix of column structure  `conc_bonsai_hexio_v_3_3_18_va.csv`
- revise `get_concordance()` to return `concpair_` table type
- revise structure of `concpair_` table

## Version 0.3.6

- new structure - category `flow` includes `activitytype` and `flowobject`
- new `concpair_` table type to allow pairwise concordances
- fixes for `iea_energy_balance` tree structure in `activitytype`
- add method `classifications.<category>.get_classification_names()`
- fix `classifications.get_concordance()`

## Version 0.3.5

- bug fixes
- deploy on pypi

## Version 0.3.4

- add `disaggregate_bonsai()` method, also executable via terminal (yaml file)
- addded Hybrid-Exiobase4 codes for `units`, `emissions`, `chemical_compound`, `compartment` as Bonsai codes
- include CAS numbers for `chemical_compound`
- add concordance `conc_bonsai_ecoinvent`
- make final codes in SUT tables explicit
- minor bug fixes

## Version 0.3.3

- clarify the mapping type in the `conc_` tables (only mapping for most detailed codes allowed)
- provide classifications tables as excel sheets in the documentation website
- add method `disaggregate_bonsai` to disaggregate existing bonsai codes and revise all relevent dataframes

## Version 0.3.2

- add `tree_exio_v_3_3_18` for EXIOBASE v3
- add the `conc_bonsai_exio_v_3_3_18` concordance table between EXIOBASE v3 and BONSAI
- `resources.csv` being accordingly updated

## Version 0.3.1

- revise `tree_bonsai` for activitytype and flowobject based on `ISIC rev2` and `CPC 2.1`
- add `skos uri` in correspondence tables to specify type of mapping (e.g. "many to one")
- remove dependency to `dataio` (only for testing)
- use BONSAI colors for docs
- add `create_conc()` to generate concordance table

## Version 0.3.0

- based on new dataio version (pydantic schemes)
- bug fixes

## Version 0.2.1

- new classifications for prodcom, un data, unido
- revision, bug fixes

## Version 0.2.0

- classifications as importable python package (util)
- based on dataio.datapackage
- uuid as additional column (uuid4)
- adding sub-types for `activitytype`: such as `industry_activity`, `treatment_activity` etc
- adding sub-types for `flowobject`: such as `industry_product`, `material_for_treatment` etc
- special naming convention that is based on [Weidema et al. 2013](https://ecoinvent.org/app/uploads/2024/02/dataqualityguideline_ecoinvent_3_20130506_.pdf)
- helper functions to find keywords in and filter the tables (pd.DataFrames)
