# overdosed 0.1
What linguistic features are unique to discussions of nonmedical substance use?

### Background

 Social media (Twitter, Facebook, websites like CrazyMeds) can provide us with information on how the general population uses substances for nonmedical purposes. Social media may, in fact, provide a more accurate picture of usage than data from surveys or emergency rooms. Surveys ask a small sample of the population to remember (sometimes) illicit activities and report them to a federal authority under the promise of anonymynity. Emergency rooms only see the part of the story when substance use goes wrong. 

### Methodology

  _overdosed 0.1_ uses <a href="http://en.wikipedia.org/wiki/Latent_semantic_analysis">latent semantic analysis</a> to identify the words or phrases that distinguish tweets discussing the use of substances from other substances. There are two phases:

   <b>Phase 1</b>

1. Sample two streams from Twitter gardenhose (1% sampler). 
   <br>Stream 1: Unfiltered. 
   <br>Stream 2: Filtered for keywords describing substance of interest. 

2. Develop a classifier. 
    <br> Sensitive (rule-in) component: Identify words present in both streams
    <br> Specific (rule-out) component: Identify words 

<b>Phase 2</b> 

### Quickstart

     git clone https://github.com/mac389/overdosed.git
     cd overdosed

### Dependencies
1. Tweepy (3.3.0)