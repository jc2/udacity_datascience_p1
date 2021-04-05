- [UDACITY DATA SCIENCE PROJECT 1: A noob approach for CRISP DM](#udacity-data-science-project-1-a-noob-approach-for-crisp-dm)
- [Installation](#installation)
- [File Description](#file-description)
- [How to interact](#how-to-interact)
- [Acknowledgement](#acknowledgement)
- [Results Summary](#results-summary)
- [License](#license)

# UDACITY DATA SCIENCE PROJECT 1: A noob approach for CRISP DM

This project was created as part of a project evaluation for Udacity.

It aims to provide answers to certain questions for a given data set following the CRIPS DM approach. In this case the data set is a StackOverflow survey.

The questions were:
- What are the benefits that people who have been coding for the longest time enjoy the most? and, Does them change over the time?
- What are the skills a Developer think influence more the Salary, or in other words, the better paid?
- Apart of the Career satisfaction, what are other factors (implicit or explicit company factors) that influence Job Satisfaction?

You can check more about the motivation of the project here:
https://juancamiloceron.medium.com/a-noob-approach-for-crisp-dm-that-probably-will-make-you-cry-d938bdb6f951

# Installation

This project was implemented and tested with **Python 3.8**. You will need to install the dependencies: you can use either **Conda** (with the environment.yml file) or **PIP** (with the requirements.txt file)

After you will need to start a Jupyter service: **$ jupyter notebook** 

# File Description

- **data**: A folder with the data set
- **enviroment.yml**: A export file with the dependencies in Conda format
- **requirements.txt**: A export file with the dependencies in PIP format
- **utils.py**: A python module with some helper funtions
- **takeaway_.ipynb**: Jupyter notebook with  the solution of each questions above

# How to interact

Execute each of the takeaway notebooks

# Acknowledgement

You can find the data used here in: https://insights.stackoverflow.com/survey/2017

The data set used is a Stackoverflow survey for developers.
The questions are about developers behaviour,their industry, and their peers

# Results Summary

The initial approach was kind of satisfactory.
- It seems that when it comes about benefits there are not to much difference between the different year of experience.
**Professional development sponsorship**, **Education sponsorship** and **Meals** are things that cease to matter
In the other hand, things like **Retirement**, **Private office** and **Remote Options**, are things that seems to be more important for people with more experience
- It seems that effectiveness (gettings thing done), communication and Technical Experience are the most relevant. And there is a little trend to make it even more relevant according to the Salary. In the other hand, it seems (dont tell my PM) that the PM experience is something that is not longer as much relevent the more you are paid
- It was interesting to see that for instance, more **hours or weeks** have a negative impact on **job satisfaction**, as well as the feeling of **being underpaid**. And also that makes sense that if you are satisfied with your job *you don’t want to change it*. Or that if you feel satisfied with the **equipment your company has provided you**, you are also more motivated to work.


# License
MIT License