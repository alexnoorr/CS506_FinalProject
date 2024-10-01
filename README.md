  
**Project Proposal \- 311 Reports**  
**Spark Project Link:** [https://docs.google.com/document/d/14a1OMTLvDSXaO1UOsfY3aME3oEkhH9RgcbPRol194EI/edit](https://docs.google.com/document/d/14a1OMTLvDSXaO1UOsfY3aME3oEkhH9RgcbPRol194EI/edit)

**NYC 311 Example:**  
[https://towardsdatascience.com/analyzing-and-modelling-nyc-311-service-requests-eb6a9c9adc7c](https://towardsdatascience.com/analyzing-and-modelling-nyc-311-service-requests-eb6a9c9adc7c)

**Description**  
Boston’s 311 service is intended to connect city residents with highly trained service representatives that can mobilize city resources in order to address pressing non-emergency concerns around the city. The service is available in 11 languages, 24 hours a day, 365 days a year. To make sure this service is as efficient and equitable as possible, the city of Boston has partnered with BU Spark\! to analyze how (and which) communities are using it. 

**Goals**  
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

**Data Collection**  
We will be collecting data from the 311 Service Requests csv files: [https://data.boston.gov/dataset/311-service-requests](https://data.boston.gov/dataset/311-service-requests)  
We will also be using the 311 Data Dictionary to define certain services and their code words, linked here: [https://data.boston.gov/dataset/311-service-requests/resource/b237f352-49d1-4423-804f-b478e4f24e61](https://data.boston.gov/dataset/311-service-requests/resource/b237f352-49d1-4423-804f-b478e4f24e61)  
Based on the project goals, we will obtain the daily calls from the data.

**Modeling Data**  
Keras for Neural Networks- used to model which government services respond to which calls with increased accuracy

**Visualizing Data**  
Heatmap showing which areas of Boston generate the most requests (plotly) including the type of service request as well as government service. We will aim to potentially make this interactive.  
A graph/chart representing total volume of requests received from 2011-2024, shows trends over time.  
Bar chart showing volume of different types of requests.  
A t-SNE plot for clustering similar groups (interactive). 

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
