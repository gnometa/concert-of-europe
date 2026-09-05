# Event

Source: https://vic2.paradoxwikis.com/Event

An **event** is a pop-up during the game, that has an effect on anything from a single province, a nation to world politics.
It is very similar to a [decision](decision.md) and the only difference is that the player (or the AI) has control over decisions while events are somewhat random.

There are essentially two ways an event can be provoked:
- Some Events have a set of parameters that need to be fulfilled in order for the event to happen. It can be anything e.g. a certain nation existing, a certain date passed, a certain invention or anything else. If these requirements are fulfilled, there is a mean time to happen (short: MTTH), which tells the average time for the event to fire in months.
- as an effect of another nation taking a decision e.g. An Elephant for America? (decision).

*Here you can find a list of events.*

#### Mean Time to Happen

Mean time to happen (MTTH) is a concept used by the game's engine to determine how often events should occur. This is more useful than a probability, because a probability depends on how frequently an event is checked: if an event has the potential to fire every month, its probability must be a lot lower than if it can only fire every year, lest it fire much more often. An MTTH remains constant, however.

The probability of an event with a certain MTTH happening at a given moment is 1/MTTH. An event with an MTTH of 50 years has 1/50 = 0.02 chance of happening each year, for example, while an event with an MTTH of 200 days has a 1/200 = 0.005 chance of happening each day, assuming it has the potential to fire on any day.

##### See also

- Wikipedia:Geometric distribution

#### Event chains

Some events come in clusters, where the first one will eventually lead to more events related to the same issue. These clusters are often called event chains. As an example The Sioux Wars will eventually lead the End of the Sioux Wars.

#### How to mod an event

For a guide on how to mod in an event look at [How to make an event](how-to-make-an-event.md).

*
