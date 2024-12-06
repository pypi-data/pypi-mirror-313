# Extract data for Bifrost

This document describes how to extract data from specific CGE tools for implementation into the BiFrost summary fields.

**Warning:** Code in this document has not been tested.

## ResFinder

Standard CGE format has been almost fully implemented into ResFinder, and are therefore using the beone template described in details in [templates_json](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/) and [beone](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/beone/).

All results are stored in the json file ResFinder outputs. This description assumes the use of Python. It assumes the resfinder json file loaded into a dict named "resfinder" and that the results needed for BiFrost should be stored in the dictionary "bifrost". The keys in the bifrost dictionary matches the field names needed by bifrost.

```python

# ResFinder JSON file has been loaded into: resfinder.
# The dictionary "bifrost" stores all the summary data.
bifrost = {}

bifrost["software_name"] = resfinder["software_name"]
bifrost["ResfinderVersion"] = resfinder["software_version"]

# See issues
gene_names = set()
for key, gene in resfinder["genes"].items():
    gene_names.add(str(gene["name"]))
bifrost["Resistensgener"] = ";".join(gene_names)

# Phenotype conversion table
pheno_resfinder2bifrost = {
    "amikacin": "AMR_Ami",
    "ampicillin": "AMR_Amp",
    "azithromycin": "AMR_Azi",
    "cefepime": "AMR_Fep",
    "cefotaxime": "AMR_Fot",
    "cefotaxime+clavulanic acid": "AMR_F/C",
    "cefoxitin": "AMR_Fox",
    "ceftazidime": "AMR_Taz",
    "ceftazidime+clavulanic acid": "AMR_T/C",
    "chloramphenicol": "AMR_Chl",
    "ciprofloxacin": "AMR_Cip",
    "clindamycin": "AMR_Cli",
    "colistin": "AMR_Col",
    "daptomycin": "AMR_Dap",
    "ertapenem": "AMR_Etp",
    "erythromycin": "AMR_Ery",
    "fusidic acid": "AMR_Fus",
    "gentamicin": "AMR_Gen",
    "imipenem": "AMR_Imi",
    "kanamycin": "AMR_Kan",
    "linezolid": "AMR_Lzd",
    "meropenem": "AMR_Mero",
    "mupirocin": "AMR_Mup",
    "nalidixan": "AMR_Nal",
    "penicillin": "AMR_Pen",
    "quinupristin+dalfopristin": "AMR_Syn",
    "rifampin": "AMR_Rif",
    "streptomycin": "AMR_Str",
    "sulfamethoxazole": "AMR_Sul",
    "teicoplanin": "AMR_Tei",
    "temocillin": "AMR_Trm",
    "tetracycline": "AMR_Tet",
    "tiamulin": "AMR_Tia",
    "tigecycline": "AMR_Tgc",
    "trimethoprim": "AMR _Tmp",
    "vancomycin": "AMR_Van"
}

ab_profile = set()
for ab_rf, ab_bi in pheno_resfinder2bifrost.items():
    ab = resfinder["phenotypes"].get(ab_rf, None)
    if(ab is not None):
        is_resistant = resfinder["phenotypes"]["resistant"]
        if(is_resistant == "True" or is_resistant is True):
            bifrost[ab_bi] = "Resistent"
            ab_profile.add(ab_bi)
        elif(is_resistant.lower() == "unknown"):
            bifrost[ab_bi] = "Ukendt"
        else:
            bifrost[ab_bi] = "Sensitiv"
    else:
        bifrost[ab_bi] = "Ukendt"

bifrost["AMR_profil"] = ";".join(ab_profile)

```

## FVSTTyper or SalmonellaTypeFinder

The standard format has not been implemented for these tools. It is assumed the Serotype initially will be taken from FVSTTyper.

Results from FVSTTyper are stored in a tab sepparated text file. The format is the following:
```

Sample <TAB> Predicted Serotype <TAB> ST <TAB> ST mismatches <TAB> ST sero prediction <TAB> SeqSero prediction <TAB> O-type <TAB> H1-type <TAB> H2-type <TAB> MLST serotype <TAB> Enterobase annotations <TAB> Flagged

```

The fields in list form. Bold names are the ones that should be stored in the BiFrost summary. Following the bold name is a colon and then follows what the corresponding field in bifrost should be.

0. Sample
1. **Predicted Serotype:** Serotype_finder
2. **ST:** ST
3. ST mismatches
4. **ST sero prediction:** Sero_enterobase
5. **SeqSero prediction:** Sero_seqSero
6. **O-type:** Sero_Antigen_seqSero
7. **H1-type:** Sero_Antigen_seqSero
8. **H2-type:** Sero_Antigen_seqSero
9. MLST serotype details
10. Flagged

For the three fields O-type, H1-type, and H2-type, these needs to be concatenated with colons.

```python

antigen_list = [otype, h1, h2]
bifrost["Sero_Antigen_seqSero"] = ":".join(antigen_list)

```

**ToDo:**: implement standard format in SalmonellaTypeFinder and use this tool instead of FVSTTyper.


# Issues

- **ResFinder, Resistensgener**: This is a list of gene names. It is not clear if this should contain an entry for each single gene found or if it should be one entry per unique gene found. In this document the latter is assumed.
- **ResFinder, Resistensgener**: Separator not certain, needs decision from FVST-SSI. In this document ;
- **ResFinder, antibiotics + AMR_profil**: Not all antibiotics in ResFinder are defined in the list provided by SSI-FVST and vice versa. The antibiotics that exists only in ResFinder will not be translated.
- **FVSTTyper, Sero_D-tartrate**: This is not implemented yet.
