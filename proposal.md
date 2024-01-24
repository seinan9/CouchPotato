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

## Goal(s) / Research Question

- State what you want to accomplish.
- Scientific research question.
- Capture essence of the project and also set boundaries.


The research question for this thesis is: *What is the value that image representations provide for predicting the compositionality rating of multi-word expressions?*. This thesis will try to find out how valuable the information captured in image representations is, and how the usage of this information affects the prediction of compositionality ratings for multi-word expressions. 


- Understand what effect the usage of image representations have for predicting the compositionality rating of multi-word expressions.
- Primary focus is on the value that they provide for this task. But analyzing the overall effects of using image representations for this task will also be researched.
- More concrete, the goal is to understand the following:
1. How valuable is the information captured by image representations for this task.
2. How does the usage of image representations affect the prediction of compsitionality ratings.
- These are solved by solving following subgoals:
1. Find out whether image-based approaches can compete with state-of-the-art text-based approaches.
2. Find out whether text-based approaches can be enhanced by using information from image representations.

## Approach

- State how the goals will be achieved

- Implement and reproduce the state-of-the-art text-based approach which will act as a baseline for comparison.
- Acquire image datasets: (1) By image generation via AI (e.g. stable diffusion), (2) by downloading existing datasets, (3) by crawling images from the internet (e.g. bing). Image generation via AI might be very interesting and could be the main focus if it works well.
- Create image representations out of the image datasets. For this, there are a lot of possible options. From very simple ones (e.g. simply using color information) to more sophisiticated ones (e.g. fine tuning visual models). Various methods will be researched, implemented and analyzed.
- Use image representations to predict compositionality ratings.
- Combine image representations with text-based information and also predict compositionality ratings. Again, various methods will be researched and analyzed.
- Analyze the overall findings.

## Limitations (optional)

- There are endless possibilities for most of the steps, especially creating image representations. During this work I will not be able to cover all of them (obviously). Therefore, in the first month, a set of methods should be decided on wich will be the main focus during the rest of the work. This allows to thoroughly investigate them, in order to gain meaningful insights. Naturally, the selection can be modified during the work if the circumstances require/allow it (e.g. when a new promising approach is found).
- Drawing proper conclusions in the end might be difficult based on the outcome. If the results show that using image representations is valuable and can either compete or even outperform state-of-the-art text-based approaches, the conclusion is easy. However, in the other case, the only certain conclusion that can be drawn is that the way it was done in this work was not valuable. 


## Contributions to Knowledge / Potential Conclusion

- What new knowledge will the proposed project produce?
- Why is it worth knowing, what are the major implications?

- Hopefully, we will understand if images contain information that is valuable for predicting the compostitionality rating of multi-word expressions.
- Currently, text-based apporaches dominate the field. This makes sense because acquiring and working with images is quite cumbersome. However, there are large advancements in image processing, especially in the field of AI. They could prove very valuable.
- Ideally, image representations will be valuable, and generating datasets via visual ai models will work well. In this case the task can be largely if not fully automated. 


## Überblick

1. Abstract
2. Introduction
3. Research Question / Goal(s)
- Was ist das Ziel?
- Was sind die Unterziele?
- Wie lautet die research question?
4. Approach
- Wie werden die Ziele erreicht?
- Wie wird die research question beantwortet?
5. Limitations 
- Was sind die Limitierungen, und warum gibt es sie?
6. Contributions to Knowledge / Potential Conclusion
- Was bringt die Thesis?
- Was bringt es die research question zu beantworten?
- Wie kann das Feld davon profitieren?
