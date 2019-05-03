

# Data Science Ethics Checklist

## A. Data Collection
 - [x] **A.1 Informed consent**: If there are human subjects, have they given informed consent, where subjects affirmatively opt-in and have a clear understanding of the data uses to which they consent? - It’s our understanding the Jigsaw web service “Civil Comments” made people aware of its goals and how their data maybe used.
 - [x] **A.2 Collection bias**: Have we considered sources of bias that could be introduced during data collection and survey design and taken steps to mitigate those? - We have thought about the potential intrinsic bias that surveyors employed by Berkeley’s “Online Hate Index” may carry, but no clear approach to address such concerns came to mind.
 - [x] **A.3 Limit PII exposure**: Have we considered ways to minimize exposure of personally identifiable information (PII) for example through anonymization or not collecting information that isn't relevant for analysis? - We do not post any of the survey data.

## B. Data Storage
 - [x] **B.1 Data security**: Do we have a plan to protect and secure data (e.g., encryption at rest and in transit, access controls on internal users and third parties, access logs, and up-to-date software)? - Our project does not carry any data; they must find it through another source.
 - [x] **B.2 Right to be forgotten**: Do we have a mechanism through which an individual can request their personal information be removed? - Not applicable.
 - [x] **B.3 Data retention plan**: Is there a schedule or plan to delete the data after it is no longer needed? - Not applicable.

## C. Analysis
 - [ ] **C.1 Missing perspectives**: Have we sought to address blindspots in the analysis through engagement with relevant stakeholders (e.g., checking assumptions and discussing implications with affected communities and subject matter experts)? - No, the only communications with Kaggle and Jigsaw came through submissions to the contest; no direct conversations.
 - [ ] **C.2 Dataset bias**: Have we examined the data for possible sources of bias and taken steps to mitigate or address these biases (e.g., stereotype perpetuation, confirmation bias, imbalanced classes, or omitted confounding variables)? - No, we have not attempted to alter the Kaggle competition data.
 - [x] **C.3 Honest representation**: Are our visualizations, summary statistics, and reports designed to honestly represent the underlying data? - Our results came from the evaluation approved by Jigsaw; thereby, honestly reflecting the perspective of the data’s owner.
 - [x] **C.4 Privacy in analysis**: Have we ensured that data with PII are not used or displayed unless necessary for the analysis? - Yes, other than the comment “No”, we have not shown any data from the Jigsaw data set.
 - [x] **C.5 Auditability**: Is the process of generating the analysis well documented and reproducible if we discover issues in the future? - True, but only if Jigsaw continues to provide the data; we don’t carry that data.

## D. Modeling
 - [x] **D.1 Proxy discrimination**: Have we ensured that the model does not rely on variables or proxies for variables that are unfairly discriminatory? - We are abiding to the identity groups defined by Jigsaw and the word2vec large scale data sets. We have not modified any of the data personally.
 - [ ] **D.2 Fairness across groups**: Have we tested model results for fairness with respect to different affected groups (e.g., tested for disparate error rates)? - No. We restricted our testing to Kaggle, so we never used another approach to determine results.
 - [x] **D.3 Metric selection**: Have we considered the effects of optimizing for our defined metrics and considered additional metrics? - Yes, we used word2vec data to extend the values considered for analysis
 - [ ] **D.4 Explainability**: Can we explain in understandable terms a decision the model made in cases where a justification is needed? - Not fully because we do not have access to the data Kaggle requires for scoring, so we cannot fully explain what caused our scores.
 - [x] **D.5 Communicate bias**: Have we communicated the shortcomings, limitations, and biases of the model to relevant stakeholders in ways that can be generally understood? - Although we have not talked directly to the stakeholders, they have our data and their results, so they should be able to understand, better than we’re allowed, what caused the scores and what are the reasons for limitations.

## E. Deployment
 - [ ] **E.1 Redress**: Have we discussed with our organization a plan for response if users are harmed by the results (e.g., how does the data science team evaluate these cases and update analysis and models to prevent future harm)? - No. We do not know the users and we have not tried to find out who they were.
 - [x] **E.2 Roll back**: Is there a way to turn off or roll back the model in production if necessary? - Yes. The training set and/or word2vec data may change in the future. In such a case, our processes should generate a new set of results without having to change the source code.
 - [ ] **E.3 Concept drift**: Do we test and monitor for concept drift to ensure the model remains fair over time? - No. We do not have a way to regulate how other people may use our software.
 - [ ] **E.4 Unintended use**: Have we taken steps to identify and prevent unintended uses and abuse of the model and do we have a plan to monitor these once the model is deployed? - No. We have not made plans for monitoring this software or being notified of its use.

*Data Science Ethics Checklist generated with [deon](http://deon.drivendata.org).*
