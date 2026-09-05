# War modding

Source: https://vic2.paradoxwikis.com/War_modding

This page documents the formatting and creation of wars which are currently ongoing on the start date.

### Creation of a new wars

This part details how you create a new war at the start of the game.
The file governing starting alliances are found within history\wars. You can use any of the files present or create a new txt-file.

Wars are declared like so:

```
name =
[date] = {
  add_attacker = 
  add_defender = 
  war_goal = { 
    casus_belli = 
    actor = 
    receiver = 
    state_province_id =
    country = 
  }
}
```

Under `add_attacker` and `add_defender`, you add all tags you wish to be on the offensive side and defensive of the war respectively. If you want more countries on each side, you can add multiple tags.

The start date should be before the intented starting scenario. The format is year.month.day. Any date before 1836.1.1 is just for flavour, but if you intend the war to only be present for the American Civil War scenario, use 1861.1.1 instead. 

The actor defines who has added the war goal, and in case of province transfers, who will receive it. The receiver defines who will be the victim of the CB. The state province id field is only required if the casus belli specifically targets a specific state - for example, an acquire state casus belli. The country field is only required if the casus belli targets another country tag - for example, a free peoples casus belli.

The name is purely for flavour.

```
name = "Ottoman Restoration of Tripoli"
1835.10.2 = {
	add_attacker = TUR
	add_defender = TRI

	war_goal = {
		casus_belli = conquest
		actor = TUR
		receiver = TRI 
	}
}
```

*This case creates the starting conquest war between Ottoman Empire and Tripoli.*

For wars that start in an earlier start date but are ended in a later start date, or wars that only happened prior to the game start, you must ensure that the war end is specified in the file as well.

```
1836.4.21 = {
	rem_attacker = MEX
	rem_defender = TEX
}
```

*This case ends a war between Mexico and Texas.*
