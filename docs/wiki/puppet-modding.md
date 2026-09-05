# Puppet modding

Source: https://vic2.paradoxwikis.com/Puppet_modding

This page documents the formatting and creation of puppets.

### Creation of new puppet relationships

The files governing puppet relations are found within history\diplomacy. You are looking for the *"unions"* file and the *"puppetstates"* file. It does not matter which file you use, as long as it is within the correct folder.

Each relationship is made up of four informations:
- first =
- second =
- start_date =
- end_date =

You should note the overlord tag in *first =* and the puppet in *second =*.
The start date should be before the intented start date. Any date before 1836.1.1 is just for flavour. If you intend the relationship to only be present for the 'American Civil War' scenario, use the start date 1861.1.1 instead. The end date does not have an effect, so just use 1936.1.1.

```
Example: 

vassal = {
	
first = ENG
	
second = GWA
	
start_date = 1836.1.1
	
end_date = 1949.1.1
}
```

*This case creates the starting puppet relation between United Kingdom and Gwalior.*
