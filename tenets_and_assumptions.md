# Assumptions

*Bar_Barrier_Note = 24*.
This note denotes the start and end of a bar.
Basically everything that exists between 2 Barrier_Notes is in the same bar.
So we calculate the notes per bar as the number of notes that exist between two 24s.

# Modelling Tenets

We want our recommender to be :

1. An honest and condorcet ranking pooler.
2. Sensitive to the note density.
3. Maximizing the recommended voicing coherence.
4. Aware of past recommendations
5. 

*Notes :*
On (4) - we want to have a configurable recommender that can have a stationary/robust or chaotic behavior.
So it needs to be memory-aware in order to base future action also on past recommendation given the use configuration.

On (3) - our coherence metric is inverse similarity. We aim to recommend voicing combination that contain additive voicings.
We'll try to avoid similar voicings as this would be considered duplicating and it would not have any musical value.

# Corresponding Model Architecture

0a. Software architecture
	a. Input Gathering
	b. Rank Pooling
	c. Recommender
	d. Regularization from past recommendations
	e. send cc to ableton

0b. Input Gathering
	a. get the notes and split them into bars - a recommendation is made every 2 bars
--> underlying architecture (read 2 bars, recommend, read 2 bars, recommend regularized)


1. Rank Pooling system
	a. Applied fast in dataframes
	b. Condorcet & median voter theorem consistent
	c. Applied at the beginning of the process.

2. Rank based recommendation
	a. Given note density - decide on the upper and lower bound number of components
	b. Given your rank quality threshold - decide on the final number of components
	c. Given the ranking and coherence - pick the number of items that minimize the median rank of the selection and maximize the inverse similarity

3. Memory Component


# References
https://tom.preston-werner.com/2010/08/23/readme-driven-development.html .
https://www.markdownguide.org/basic-syntax/ .