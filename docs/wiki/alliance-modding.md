# Alliance modding

Source: https://vic2.paradoxwikis.com/Alliance_modding

This page documents the formatting and creation of alliances.

### Creation of a new alliance

The file governing starting alliances are found within history\diplomacy. You are looking for the *"alliances"* file.

Each relationship contains four informations:
- first =
- second =
- start_date =
- end_date =

The two allies are described by tags in the lines * first =* and *second =*. It does not matter, which country tag you put in first and which you put in second.
The start date should be before the intented start date. Any date before 1836.1.1 is just for flavour. If you intend the alliance to only be present in the 'American Civil War' scenario, use the start date 1861.1.1 instead. The end date does not have an effect, so just use 1936.1.1.

```
Example: 

alliance = {
	
first = PEU
	
second = BOL
	
start_date = 1836.1.1
	
end_date = 1949.1.1
}
```

*This case creates the starting alliance between Peru and Bolivia.*
