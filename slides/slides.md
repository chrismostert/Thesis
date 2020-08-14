---
marp: true
footer: ![h:50px](img/TU-Delft-Logo.png)
paginate: true
---

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

# More than a feeling?
#### Reliability and robustness of high-level music classifiers
C. Mostert (4473353)

![bg right:33%](img/vinyl.jpg)

---

# High-level music classifiers can be great!
- Personalized music recommendations
- Searching for specific music
- ...or even *tell us something about the listener?*

---
# The first idea
Combining [The Music Listening Histories Dataset](https://ddmal.music.mcgill.ca/research/The_Music_Listening_Histories_Dataset_(MLHD)/#:~:text=The%20Music%20Listening%20Histories%20Dataset%20(MLHD)%20is%20a%20large%2D,logs%20extracted%20from%20Last.fm.&text=a%20set%20of%20user%20profiling,music%20listening%20behavior%20and%20activity) with [AcousticBrainz](http://mtg.upf.edu/node/3320)

But... Spotify recently had the same idea [(Park et al., 2019)](https://doi.org/10.1038/s41562-018-0508-z)

![bg right:60% fit](img/seasonalpattern.png)


---
# My assumption...

Multiple submissions should be redundant, *right?*

![bg right fit](img/multiplesubmissions.png)

---
![center](img/labelflips.png)

---
# *What* is the problem?

Sharing commercial music audio is illegal
Use *precomputed low-level features*
MFCCs and chroma features are sensitive to *representation* [(Urbano et al., 2014)](http://mtg.upf.edu/node/3015)

---
# *What* is the problem?

Labels can be ambiguous

<!-- Use for example pumped up kicks for emotion, or the label 'party', which can be culturally dependent -->

---
# *What* is the problem?

Modelling emotion requires knowledge from psychology

Which model to use?

Be careful with interpretation

![bg right fit](img/background/russellCircumplex.png)
<!-- _footer: ![h:50px](img/TU-Delft-Logo.png) $~~~$Image from [(Russell, 1980)](https://content.apa.org/doi/10.1037/h0077714)-->

---
# *What* is the problem?

Trained classifiers are not explainable
No good ways of validating

---
# *Why* should we care?
![center h:480px](img/motive/headlines.png)

<!-- For consistency, they only looked at the first submission for each MBID, and did note that the codec/bitrate could influence these values. However, journalism then likes to jump to conclusions-->

<!-- _footer: ![h:50px](img/TU-Delft-Logo.png) $~~~$Headlines all based on results by [(Interiano et al., 2018)](https://doi.org/10.1098/rsos.171274)-->

---
<!-- _class: invert -->
**Maybe add Hans here? Or not**

---
# <!-- fit --> Then *how* are we going to measure classifier performance?

---
# Stability analysis
![center h:350](img/stability/Dataset.png)
<!-- Mainly to see how the instability of low-level features cascades towards the high-level classifiers -->

---
# Stability analysis
![center h:400px](img/stability/dataframe_presentation.png)
Where the red box is indexed as $(MBID_1, danceability, danceable)$

---
# Stability analysis
Then $var((MBID_1, danceability, danceable))$ gives us information about the stability of this classifier **over one recording**

How do we use **all recordings**?

---
# Stability analysis
We calculate the **pooled variance**:
$$\overline{var}(c,l)=\frac{\Sigma_{i=1}^{k} (n_i \times var((MBID_i, c, l)))}{\Sigma_{i=1}^{k}n_i}$$
Where $n_i$ is the sample size of population $i$

---
# Stability analysis
But what about classifiers who almost always output the same label?
We need some measure of this 'biasedness'

---
# Stability analysis
Use **information entropy**
We assume that underlying data is uniformly distributed over labels

$$\hat{H}(c)_{all}=-\Sigma_{l \in L_c}P((c, l))log_{|L_c|}P((c, l))$$

Where $L_c$ is the set of labels for classifier $c$.

---
# Stability analysis
Now we can quantify classifiers based on their stability and 'biasedness':
![center](img/stability/labelstabilityplotv4.png)
<!-- 
Note that y-axis averaged pooled variance over all possible labels

Bottom right is best, lowest bias + highest stability. Many classifiers are either stable and biased or if they are less biased then they also become more stable. In essence, we can see the bias-variance tradeoff often discussed in machine learning. Only some classifiers, like mood_sad or genre_rosamerica seem to be relatively stable **and** unbiased.-->

---
# Can we use the stability metric to say something about how the representation of the audio influences high-level music classifiers? 

Due to the metric requiring multiple submissions, we cannot control the underlying data...

---
Still, data suggests an influence of bitrate on stability
![center](img/stability/bitrateeffectv3.png)

---
Of some codecs on stability
![center h:600](img/stability/320000-7405-v2.png)

---
And even of the low-level version extractor version used on the stability
![center h:600](img/stability/versionvariance-v2.png)

---
# Can we define another metric which does not require multiple submissions?

---
# Classifier agreement

Main idea: two classifiers implementing the same or similar tasks should **agree** with eachother

Quantified by calculating the **Pearson correlation** between confidence values
<!-- can also be related to construct validity in psychology, if unsure if the construct is correctly captured, do multiple measurements and see if they correspond -->

---
# Classifier agreement
There is **redundancy** in the AcousticBrainz classifiers

| Classifier, label A      | Classifier, label B      | Pearson r        |
|--------------------------|--------------------------|--------------|--------|
| genre_rosamerica, cla | genre_tzanetakis, cla | 0\.287475    | <.001 |
| genre_dortmund, blues | genre_tzanetakis, blu | 0\.00790441  | <.001 |
| genre_rosamerica, roc | genre_tzanetakis, roc | \-0\.074783  | <.001 |


---
# Classifier agreement
![center h:580](img/agreement/rosamerica_tzanetakis_rock-v2.png)

---
# Classifier agreement
What about related constructs?
| Classifier, label A            | Classifier, label B                   | Pearson r    |
|--------------------------------|---------------------------------------|-----------|--------|
| mood_aggressive, aggressive | mood_relaxed, not_relaxed       | 0.588771 | <.001 |
| danceability, danceable        | mood_party, party                  | 0.527954 | <.001 |
| mood_happy, happy           | mood_sad, not_sad               | 0.131705 | <.001 |

---
# Classifier agreement
![center h:580](img/agreement/happy_notsad-v2.png)

---
# Going down the rabbit hole: can we gain further insight into what causes these strange distributions?

---
# A closer look at the distributions
![center h:600](img/distribution.png)

---
# Are these peaks caused by differences in data representation?
Main idea: compare metadata value distributions of data in peak with 'baseline'
![bg right fit](img/distribution_isolated.png)

---
# Distance metric
The Jensen-Shannon distance is used as a measure of distributional difference
> The square root of the Jensen-Shannon Divergence [(Endres & Schindelin, 2003)]().
> Symmetric, finite value within [0, 1] [(Lin, 1991)](https://doi.org/10.1109/18.61115).

---
# Distributional differences in metadata
|                         | acoustic | relaxed | electronic | sad |
|---------------------------------|----------------------|---------------------|------------------------|-----------------|
| bit_rate                     | \.42                 | \.32                | \.39                   | \.17            |
| codec                           | \.34                 | \.26                | \.32                   | \.06            |
| length                          | \.15                 | \.15                | \.15                   | \.32            |
| lossless                        | \.28                 | \.21                | \.27                   | \.02            |
| essentia_low                 | \.61                 | \.52                | \.59                   | \.15            |
| essentia_git_sha_low   | \.67                 | \.58                | \.66                   | \.23            |
| essentia_build_sha_low | \.70                 | \.62                | \.69                   | \.24            |

---
# What about genre differences?
Using the [AcousticBrainz genre dataset](http://mtg.upf.edu/node/3960) we can check the distrubtional differences in genre in the peaks

|      | acoustic | relaxed | electronic | sad |
|----------|----------------------|---------------------|------------------------|-----------------|
| Discogs  | .12                 | .09                | .11                   | .11            |
| last.fm | .14                 | .12                | .13                   | .14            |
| tagtraum | .14                 | .11                | .13                   | .14            |

---
# Climbing back up: what have we learned?
- There are reasons to doubt high-level classifier performance from a theoretical point of view
- Stability, agreement and distributional anlyses highlight several classifiers that seem to perform poorly and show unexpected patterns
- Low-level extractor versions, codec or bitrate used seem to play a role in high-level classifier performance

---
# Maybe the observed influence  to the differences in the underlying data?

**TODO Ch6.1**

---
# Maybe all 
