# Assumptions

*Bar_Barrier_Note = 24*
This note denotes the start and end of a bar.
Basically everything that exists between 2 Barrier_Notes is in the same bar.
So we calculate the notes per bar as the number of notes that exist between two 24s.

# Modelling Tenets

We want our recommender to be :

1. An honest and condorcet ranking pooler.
2. Sensitive to the note density.
3. Maximizing the recommended voicing coherence.
4. Aware of past recommendations

*Notes :* On (4) - we want to have a configurable recommender that can have a stationary/robust or chaotic behavior.
So it needs to be memory-aware in order to base future action also on past recommendation given the use configuration.

# References
https://tom.preston-werner.com/2010/08/23/readme-driven-development.html .
https://www.markdownguide.org/basic-syntax/ .