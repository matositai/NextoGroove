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

0a. Software architecture.
	a. Input Gathering
	b. Rank Pooling
	c. Recommender
	d. Regularization from past recommendations
	e. send cc to ableton

0b. Input Gathering.
	a. get the notes and split them into bars - a recommendation is made every 2 bars
--> underlying architecture (read 1 bars, recommend, read 2 bars, recommend regularized)

Type A Model : Rank Based Recommendation

1. Rank Pooling system - expecting ranked items from 1 to 5 in the choice ranks.
	a. Applied fast in dataframes
	b. Condorcet & median voter theorem consistent
	c. Applied at the beginning of the process.

2. Rank based recommendation.
	a. for each bar, get the model note
	a. Given note density - decide on the upper and lower bound number of components
	b. Given your rank quality threshold - decide on the final number of components
	c. Given the ranking and coherence - pick the number of items that minimize the median rank of the selection and maximize the inverse similarity

Type B Model : Score Based Recommendation.

1. Score Pooling - expecting scored items (1 to 5) with 0 being an exclusion indicator in the choice ranks
	a. Average the scores and add a zero rule (how to deal with zeros)

2. Score based recommendation.
	a. for each bar get the mode note {future : add a recommendation for each note and combine recommendations or pool the recommendations}
	b. given the note density in the bar pick a random number in the accepted components range (that number is k) {future : add memory component here}
	c. pick the topk items based on their scoring - exclude zeros
	d. that's the final recommendation

3. Regularization / Memory Structure.
	a. keep the last given recommendation
	b. pool the current & last recommendation - keep the components from the last recommendation that maximize coherence
	c. Calculate the local difference between 2 bars (calculate number of difference components) - as a percentage 0,1
	d. Calculate the global difference between 2 bars (binary difference between keynote & duration)
	e. Calculate Pooled difference between two bars which is the average between local & global
	f. if pooled difference is 
		a. [80, 100] : dont keep anything from the previous rec
		b. [60, 80] : keep 1/3 of the previous rec
		c. [30, 60] : keep 2/3 of the previous rec
		d. [0, 30] : keep everything from the previous rec and discard the next rec
	
	*need to figure out a way to make this selection procedure coherence aware*

# References
https://tom.preston-werner.com/2010/08/23/readme-driven-development.html .
https://www.markdownguide.org/basic-syntax/ .