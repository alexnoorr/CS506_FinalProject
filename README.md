# An Analysis of 311 Reports in Boston
**CS506 Spark! Midterm Report**

**Presentation Link:** [https://youtu.be/g1BpLXyPG_Q](https://youtu.be/g1BpLXyPG_Q)

---

## Introduction
Boston’s 311 service connects city residents with trained representatives to mobilize city resources for non-emergency concerns. Available in 11 languages, 24/7, and updated daily, our project explores trends in 311 requests over the last 13 years (2011-2024) and aims to build a neural network to classify the Government department that will respond to a given call. Through data analysis, we answered various questions to uncover relationships between key factors.

---

## Preliminary Analysis of Data
Analyze Boston is an open data hub, housing all public data on Boston, including 311 reports. Before processing, we assessed the datasets to understand the overall picture.

### Key Columns:
- **open_dt:** Date the case was opened.
- **closed_dt:** Date the case was closed.
- **case_status:** Status of the case (e.g., "Closed").
- **on_time:** Whether the case was closed on time ("ONTIME" or "NOT_ONTIME").
- **queue:** Specific queue for the case.
- **subject:** Assigned department.
- **fire_district:** Fire district for the case.
- **pwd_district:** Public Works district for the case.
- **neighborhood:** Specified neighborhood by the caller.
- **type:** Detailed case type.
- **department:** Department handling the case.
- **source:** Method of submission (e.g., app, phone call).

We obtained the data using the CKAN Datastore API.

---

## Data Preprocessing/Cleaning
The 311 reports are continuously updated. To ensure consistency, we selected specific dates to stop data collection, making sure each question was based on data fetched in the same week.

| Question/Goal | Date Fetched | Data Count |
|---------------|--------------|------------|
| 1             | 30th October | 3,039,306  |
| 2             | 3rd November | 3,041,981  |
| 3             | 29th October | 3,038,355  |
| 4             | 3rd November | 3,041,981  |
| 5             | 30th October | 3,039,306  |
| 6             | 1st November | 3,039,306  |
| 7             | 1st November | 3,039,306  |
| 8             | 3rd November | 3,041,981  |

We included some records from surrounding years (e.g., late 2010 and early 2012 entries in the 2011 dataset) upon receiving approval from Spark. We then:
- Removed records outside the main year range.
- Combined data across years into a unified dataset for easier access.

---

## Data Processing + Visualizations
To begin modeling, we explored relationships between variables based on Spark's questions. Using an API call to fetch the data was time-consuming, so we utilized Pickle files to store data, processing it in batches for efficiency.

### Visualization of Submission Source Trends
![Image Description](https://raw.githubusercontent.com/alexnoorr/CS506_FinalProject/main/visualizations/q3.png)
Using Matplotlib, we visualized trends in 311 requests, showing a shift from traditional calls to app-based reporting over time. Constituent Calls were initially dominant, but the Citizens Connect App grew rapidly from 2014, peaking by 2023. Meanwhile, City Worker App and Employee Generated reports saw steady but limited use, reflecting specific applications. The slight decline in 2024 may suggest a plateau or the emergence of new platforms. Overall, the data indicates a shift toward digital reporting for civic issues.

### Volume of Requests over Time
![Request Volume](https://raw.githubusercontent.com/alexnoorr/CS506_FinalProject/main/visualizations/request-vol.png)
As shown in the graph above, the number of requests have overall increased over the years since 2012. This trend is also in line with the rising population of Boston since 2012.

### Top 5 Requests
![Top 5 Requests](https://raw.githubusercontent.com/alexnoorr/CS506_FinalProject/main/visualizations/top5-requests.png)
Among hundreds of unique requests, the top issues included vehicles and traffic, trash, and city maintenance.



---

## Data Modeling
The Boston 311 datasets contain various descriptors for each case. We used the **Type** column to predict the department. Due to time constraints, we used only 0.01% of the data (30,000 rows).

```python
tokenizer = Tokenizer()
tokenizer.fit_on_texts(subset_df['type'])
type_matrix = tokenizer.texts_to_matrix(subset_df['type'], mode='binary')

label_encoder = LabelEncoder()
department_labels = label_encoder.fit_transform(subset_df['department'])
department_one_hot = to_categorical(department_labels)

model = Sequential()
model.add(Dense(128, input_shape=(type_matrix.shape[1],), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(department_one_hot.shape[1], activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(type_matrix, department_one_hot, epochs=50, validation_split=0.2)

```


First, this code converts the text data in the "type" column into a binary matrix, where each row represents the presence or absence of specific words in the vocabulary. Next, it encodes the "department" labels into a format the model can interpret, assigning each department a unique integer and transforming it into a one-hot encoded vector for classification.
The neural network model is then created with three layers: an input layer, a hidden layer, and an output layer, using ReLU activation for the hidden layers and softmax activation for the output to produce probabilities for each department. Finally, the model is compiled and trained on the prepared data, using the Adam optimizer, which helps the model learn more efficiently. and categorical cross-entropy loss for multi-class classification of departments. The training process includes 50 cycles (epochs) and reserves 20% of the data for validation to monitor accuracy during training. There was no test train split this time, as we wanted to see how well the model was learning and stabilizing for now, with minimal overfitting. 
Here are the results:
Accuracy: The training accuracy starts at about 82% in the first epoch and quickly rises to around 94%, staying stable there. This means the model is learning to classify the data well and has reached a high level of accuracy quickly.
Loss: The training loss (a measure of model error) starts higher (around 0.8) and decreases to around 0.22, showing the model is reducing its error as it trains.
Validation Accuracy: The validation accuracy (on unseen data) is consistently around 94%, indicating that the model performs similarly on data it hasn’t seen before. This stable value suggests the model generalizes well without overfitting.
Validation Loss: The validation loss remains fairly constant (around 0.24) after a few epochs, showing no signs of overfitting.

Since the model doesn’t appear to learn anything new for most of the cycles, an extension of this could be implementing early stopping, to stop the model training when there are no improvements

## Next Steps
The next steps would be to obtain concrete visualizations for all of the questions posed by Spark. We want to take these visualizations and see how we can extend them, make them interactive, or simply better them for comprehension of the reader. Some of our visualizations have a lot of variables due to the nature of the departments of Boston being split up for specificity. As a result, we aim to work towards more interesting visualizations that can capture the scope of these variables and present more meaningful relationships. 

Further, our model does not use a testing data set, so utilizing train_test_split will hopefully give us a better understanding of its accuracy.

### Retained from Proposal
## **Goals**  
With this project we aim to answer the following questions:

- What is the total volume of requests per year, or how many 311 requests is the city receiving per year?  
- Which service requests are most common for the city overall AND by NEIGHBORHOOD and how is this changing year over year by SUBJECT (department), REASON,QUEUE?  
- How is the case volume changing by submission channel SOURCE?  
- What is the average \# of daily contacts by year?  
- Volume of top 5 request types (TYPE)    
- Average goal resolution time by QUEUE   
- Average goal resolution time by QUEUE and neighborhood  
- What % of service requests are closed (CLOSED\_DT or CASE\_STATUS) vs. no data (CASE\_STATUS \= null) vs. unresolved (CASE\_STATUS \= open)?

Our analysis and visualizations focus on improving how the City operates. This project will help the city understand trends that can be addressed at a strategic level.

**What to Plot**  
Total volume of requests per year, for all years 2011-2024. Use this to obtain values for how many requests the city is receiving each year.   
The most common service requests in Boston, AND *grouped by neighborhood*. We will need to plot this year by year to see changes in these values by the service department, the ‘umbrella’ term reason for calling and queue that the case is assigned to.  
We will also explore how the case volume is changing over time by the source the callers used. This change will be interesting to see due to the development of new mobile apps that could change the way people report requests.  
We can plot the 311 Call counts by service department  
Charts for specific ‘umbrella’ reasons for calling  
Average goal resolution time by neighbourhood and queue  
Percentage of service requests that are closed to unresolved

**Test Plan**

- We will use 70% of the data for training, and 30% for testing for each year from 2011-2024.  
- Train on data from earlier years, and test on later years (January to October from earlier years and October to December for more recent years)  
  - Goal of classifying which government services respond to each call

**Rough Time Plan for the semester**

| Project Milestones    | Data review \+ initial questions Data preprocessing, infrastructure, engineering/ visualization checklist \*Data Analysis \*Early Insights presentation Answer all base questions Challenges/limitations encountered, assumptions made \*Final Report  Cover pages, Intros (goal/overview/ethics/misconceptions/ big picture), answer key questions Visualizations are properly created, and described Started extension mini-chapters \*End of Semester Showcase (Final Presentation)  |
| :---- | :---- |

### Month of October:

- Week 1 (30th Sep-6th)  
  - **Proposal Due 10/1**  
  - **Come up with a timeline**  
- Week 2 (7th to 13th)  
- Week 3 (14th to 20th)  
- Week 4 (21st to 27th)

Month of November:

- Week 1 (28th Oct to 3rd)  
- Week 2 (4th to 10th)  
  - **Midterm Report and Presentation Due 11/5**  
  - ​​The midterm report and 5-minute presentation should include the following.  
    - Preliminary visualizations of data.  
    - Detailed description of data processing done so far.  
    - Detailed description of data modeling methods used so far.  
    - Preliminary results. (e.g. we fit a linear model to the data and we achieve promising results, or we did some clustering and we notice a clear pattern in the data)  
- Week 3 (11th to 17th)  
- Week 4 (18th to 24th)  
- Week 5 (25th to 1st December)

Month of December:

- Week 1 \- 2nd December to 8th  
- **10th \- Final report due**  
  - You must include the following:  
    - How to build and run the code (Include this first so we know how to reproduce your results). There should be a makefile that installs all dependencies and builds the code. This is the most important part.  
    - Include test code and a GitHub workflow that runs the test code. Just test a few things you think are important \- no need to overdo it on the testing front, since that’s not the focus of the project.  
    - Visualizations of data (interactive visualizations are highly encouraged).  
    - Description of data processing and modeling (what the code does).  
    - Results showing that you achieved your goal.  
- **End of Semester Spark\! Showcase (Final Presentation)**
