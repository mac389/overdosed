# overdosed 0.1
What linguistic features are unique to discussions of nonmedical substance use?

### Background

 Social media (Twitter, Facebook, websites like CrazyMeds) can provide us with information on how the general population uses substances for nonmedical purposes. Social media may, in fact, provide a more accurate picture of usage than data from surveys or emergency rooms. Surveys ask a small sample of the population to remember (sometimes) illicit activities and report them to a federal authority under the promise of anonymynity. Emergency rooms only see the part of the story when substance use goes wrong. 

### Methodology

  _overdosed 0.1_ uses <a href="http://en.wikipedia.org/wiki/Latent_semantic_analysis">latent semantic analysis</a> to identify the words or phrases that distinguish tweets discussing the use of substances from other substances. There are two phases:

   <b>Phase 1</b>

1. **Sample** two streams from Twitter gardenhose (1% sampler). 
   <br>Stream 1: Unfiltered. 
   <br>Stream 2: Filtered for keywords describing substance of interest. 

1. **Develop** the classifier. 
    <br> Sensitive (rule-in) component: Identify words present in both streams. 
    <br> Specific (rule-out) component: Identify words present in filtered stream but not unfiltered stream. (Filtered stream - unfiltered stream)

1. **Analyze** the classifier.
    <br> Identify groups of semantically related words in the rule-in component. 
    <br> Same for rule-out component. (_i.e._ Taxonomize)

1. **Test** the classifier.
	<br> Curate new samples from the two streams
	<br> Adjust the words needed to be present or absent in a tweet to achieve an acceptable sensitivity and specificity

<b>Phase 2</b> 

1. **Sample** the unfiltered Twitter gardenhose (1% sampler)
   <br> Cannot calculate valid sample statistics if you combine streams

2. **Partition** the unfiltered Twitter stream into 
	<br> All tweets discussing use of the substance
	<br> All other tweets

3. **Calculate** the relative abundance of each component of the metadata, _e.g._
	<br> Are the geographic distributions the same?
	<br> What latent attributes differ?
	
### Quickstart

     git clone https://github.com/mac389/overdosed.git
     cd overdosed

### Dependencies
1. Tweepy (3.3.0)