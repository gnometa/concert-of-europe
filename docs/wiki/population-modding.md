# Population modding

Source: https://vic2.paradoxwikis.com/Population_modding

**Population modding** can be used to change the population of a country. The files needed are in *history/pops/*. In vanilla Victoria 2 there are two folders: *1836.1.1* and *1861.4.14*, they determine in what bookmarks the content of these folders are used.

In these folders there are files, based on modern borders. These files contain the information needed for the population in-game. For example, the file *Estonia.txt* contains:

```
#Estonia Region (436000) 
#under the rule of Russia in 1836  
#Tallinn/Reval (160000/40000 POPS)  
349 = {
	clergymen = {
		culture = estonian
		religion = protestant
		size = 325
	}
        etc...
}
#Narva (184000/46000 POPS)  
350 = {
	clergymen = {
		culture = estonian
		religion = protestant
		size = 425
	}
        etc...
}
etc...
```

### Setup

As shown, the population uses the following setup:

```
[Province ID] = {
	[Population type] = {
		culture = [culture]
		religion = [religion]
		size = [quantity]
	}
}
```

### Example

Editing existing population easy, since you only have to change some variables, or copy-paste a bit.

Let's say you made a new province with the code '3249', and you want to add the population.

A new file needs an unique name, like *Newprovinces.txt* and has to be a '.txt' file, which is nothing else than a normal text file, and most programs, like Notepad++, use this as standard format. I suggest making a new file, since it's easier to use when you have to upgrade it to the 1861 folder. It also needs to be in *history/pops/1836.1.1*.

This is what you need to fill in if you want the population to be to be mostly farmers, a large amount of soldiers, and a small amount of clergymen, aristocrats, labourers and artisans, the culture to be about 75% Dutch, 12.5% Flemish and 12.5% Wallonian, and the religion to be 75% Protestant and 25% Catholic, and have a total size of 20,000:

```
3249 = {
    farmers = {
        culture = dutch
        religion = protestant
        size = 8000
    }
    farmers = {
        culture = wallonian
        religion = catholic
        size = 1000
    }
    farmers = {
        culture = flemish
        religion = catholic
        size = 1000
    }
    soldiers = {
        culture = dutch
        religion = protestant
        size = 3700
    }
    soldiers = {
        culture = wallonian
        religion = catholic
        size = 650
    }
    soldiers = {
        culture = flemish
        religion = catholic
        size = 650
    }
    clergymen = {
        culture = dutch
        religion = protestant
        size = 100
    }
    artisans = {
        culture = dutch
        religion = protestant
        size = 1000
    }
    artisans = {
        culture = wallonian
        religion = catholic
        size = 500
    }
    artisans = {
        culture = flemish
        religion = catholic
        size = 500
    }
    aristocrats = {
        culture = dutch
        religion = protestant
        size = 150
    }
    labourers = {
        culture = dutch
        religion = protestant
        size = 2000
    }
    labourers = {
        culture = wallonian
        religion = catholic
        size = 450
    }
    labourers = {
        culture = flemish
        religion = catholic
        size = 300
    }
}
```

The total size of all the pops is now 20,000. The balance between Protestants and Catholics is 14,950/5,050 (74.75%/25.25%). The balance between Dutch, Wallonian and Flemish is 14,950/2,600/2,450 (74.75%/13%/12.25%).

### Upgrading to 1861

You also have to use a file for the *1861.4.14* folder. To do this simply copy-paste the file you used to the *1861.4.14* folder in the *history/pops/* folders, there is no need to change the name. You can then decide to keep it the same, but usually population grows. Most of the time population grows with about 3% between the 1836 and 1861 files. You can simply increase all the quantities by 3% in the 1861 file, sometimes this will end up giving you numbers with decimals, don't worry, you can either round it up or down, or fill in the number including the decimals, since the game will round it up or down itself. 

When everything is done, you will have a fully functional province population. 

### See also
