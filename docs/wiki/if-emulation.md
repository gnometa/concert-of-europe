# IF Emulation

Source: https://vic2.paradoxwikis.com/IF_Emulation

In modern Paradox games (CK2 and later) and in any actual programming language, a mod developer can use if statements to enact effects if and only if a certain condition is met. In other words: `if [condition] then [effect]`. Victoria 2 and all older Paradox games do not have a dedicated `if` keyword, but the impact of an if statement can still be emulated.

### Goal

Modern Paradox games have `if` scopes that look like this:

```
if = {
    limit = {
        # conditions
    }
    # effects
}

else_if = {
    limit = {
        # conditions
    }
    # effects
}

else = {
    # effects
}
```

The above code does not work in Victoria 2 because `if`, `else_if`, and `else` are not valid. Instead, Victoria 2 modders must get creative with the options available in the game to emulate such logical behaviour.

### Workaround

The workaround for emulating `if` statements in Victoria 2 involves using scopes with a `limit` clause to ensure that only certain effects are applied if certain conditions are met.

Let's suppose you want an event that has two different possible effects, one if the country is free trade, the other if the country is protectionist. Without if emulation, you would have to write two different events, one for protectionist nations and the other for free trade nations, but with if emulation you need only write a single event. The option for the event would look something like this:

```
option = {
    name = "If free trade, lose prestige, if protectionist, gain prestige"
    random_owned = {
        limit = {
            owner = {
                trade_policy = free_trade
            }
        }
        owner = {
            prestige = -10
        }
    }
    random_owned = {
        limit = {
            owner = {
                trade_policy = protectionism
            }
        }
        owner = {
            prestige = 10
        }
    }
}
```

Note that the code above contains two `if` statements, not an `if else` statement.

### See Also

See https://eu3.paradoxwikis.com/IF_Emulation for further examples of code emulating `if`, though note the differences between EU3 and Victoria 2 code.
