# Proposal

## Title Page

- Short, descriptive title.
- Information about author, instution etc.

Visualizing Meaning: Image Representations for Predicting Multi-Word Expression Compositionality

## Abstract

- Outline the key tasks of the thesis.

The goal of this thesis is to understand whether image representations contain valuable information for predicting the compositionality rating of multi-word expressions. To understand the effect of using image representations and what value they provide, first, the compositionality ratings are predicted with purely image-based approaches (for various forms of image representations) and secondly, the ratings are predicted by combining state-of-the-art text-based approaches and information from image representations. Results from both approaches will be compared to state-of-the-art approaches. Additionaly, the framework created during the thesis, aims to be highly automated and easy to use. Ideally, it can find its use for both research and practical applications.

## Table of Contents

## Introduction

- Explain the background of the project.

A compound is a word that is formed by combining two or more words (called constituents). Based on the principle of compositionality we assume that the meaning of a compound can be derived from its constituents and how they are combined. Linguists and NLP researchers are interested in the degree of compositionality (i.e. how much the constituents contribute to the understanding of the compound) and how it can be derived quickly. A compositionality rating specifies the degree of compositionality (in other words, how true this assumption is) for a given compound. This rating can be done manually, by people, which is very time consuming, or ideally automated, by computers. The second approach is largely done using text-based approaches (typically Vector Space Models). There is some research, using images, but not a lot. The goal of this thesis is to find out whether images are valuable for predicting the degree of compositionality.

## Goal(s)

- State what you want to accomplish.
- Scientific research question.
- Capture essence of the project and also set boundaries.


The research question for this thesis is: *What is the value that image representations provide for predicting the compositionality rating of multi-word expressions?*. This thesis will try to find out how valuable the information captured in image representations is, and how the usage of this information affects the prediction of compositionality ratings for multi-word expressions. 


**Research Question**: What is the value that image representations provide for predicting the compositionality rating of multi-word expressions?


- Understand what effect the usage of image representations have for predicting the compositionality rating of multi-word expressions.
- Primary focus is on the value that they provide for this task. But analyzing the overall effects of using image representations for this task will also be researched.
- More concrete, the goal is to understand the following:
1. How valuable is the information captured by image representations for this task.
2. How does the usage of image representations affect the prediction of compsitionality ratings.
- These are solved by solving following subgoals:
1. Find out whether image-based approaches can compete with state-of-the-art text-based approaches.
2. Find out whether text-based approaches can be enhanced by using information from image representations.





## Data and Methods

- How will data be collected and analyzed.
- Which methods will be used.

- Existing datasets will be used.
- Data from the internet (e.g. bing) will be used.
- Data generated from models will be used (local generation, e.g. stable diffusion).

## Expected Results and Discussion

- What do you expect to find?

- Whether image representations alone are sufficient to predict high quality predictions.
- Wheher image representations can be used to enhance text-based approaches.
- Ultimately, whether image representations provide valuable information for predicting the compositionality rating of multi-word expressions.

## Potential Conclusion

- What new knowledge will the proposed project produce?
- Why is it work knowing, what are the major implications?



## Misc (Place into other Sections later)

### Procedure

#### Dataset Acquisition

- Use existing image datasets.
- Gather images from the internet (e.g. via bing).
- Generate images with AI models (e.g. stable diffusion).

#### Creating Image Representations

- Use images from the datasets to extract representations via different methods (e.g. color distribution, fine-tuning existing models)

#### Creating Text-based Representations

- Create word vectors (e.g. via word2vec or co-occurence matrix)

#### Combine Representations

- Enhance Text-based representations with the image-based representations (e.g. average vector).

#### Predicting Compositionality Ratings

- Use representations (image, text, combined) to predict compositionality ratings (e.g. via cosine distance)

#### Measure Performance

- Compute spearman correlation against gold standard.
