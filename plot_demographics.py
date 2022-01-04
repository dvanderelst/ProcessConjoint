import numpy
import pandas
from matplotlib import pyplot
from library import PlotSettings

within = pandas.read_csv('demographic_data/within.csv')
between = pandas.read_csv('demographic_data/between.csv')
simple = pandas.read_csv('demographic_data/simple.csv')
simple_amazon = pandas.read_csv('demographic_data/simple_amazon.csv')
jurgen = pandas.read_csv('demographic_data/jurgen.csv')
student = pandas.read_csv('demographic_data/student.csv')
simple_replication = pandas.read_csv('demographic_data/simple_replication.csv')


within['Age'] = 2021 - within.BirthYear
between['Age'] = 2021 - between.BirthYear
simple_amazon['Age'] = 2021 - simple_amazon.BirthYear
simple['Age'] = 2021 - simple.BirthYear
jurgen['Age'] = 2021 - jurgen.BirthYear
student['Age'] = 2021 - student.BirthYear
simple_replication['Age'] = 2021 - simple_replication.BirthYear

gender_within = within.Gender.value_counts()
gender_within.index = ['Female', 'Male','Non-Conf.','Not Say']

gender_between = between.Gender.value_counts()
gender_between.index = ['Female','Male', 'Trans.']

gender_simple = simple.Gender.value_counts()

gender_simple_amazon = simple_amazon.Gender.value_counts()
gender_simple_amazon.index = ['Male', 'Female', 'Other']

gender_simple_replication = simple_replication.Gender.value_counts()
gender_simple_replication.index = ['Male', 'Female']

gender_jurgen = jurgen.Gender.value_counts()
gender_jurgen.index = ['Male', 'Female']

gender_student = student.Gender.value_counts()

bins = numpy.linspace(18, 75, 20)
density = False

pyplot.figure(figsize=(10,10))
# ------------------------------------
pyplot.subplot(6, 2, 5)
pyplot.title('Study 3')
pyplot.hist(within.Age, density=density, alpha=0.25, bins=bins)
pyplot.subplot(6, 2, 6)
pyplot.bar(gender_within.index, gender_within)
pyplot.title('Study 3')
# ------------------------------------
pyplot.subplot(6, 2, 3)
pyplot.hist(between.Age, density=density, alpha=0.25, bins=bins)
pyplot.title('Study 2')
pyplot.subplot(6, 2, 4)
pyplot.bar(gender_between.index, gender_between)
pyplot.title('Study 2')
# ------------------------------------
# pyplot.subplot(6, 2, 5)
# pyplot.hist(simple.Age, density=density, alpha=0.25, bins=bins)
# pyplot.title('Study 1c')
# pyplot.subplot(6, 2, 6)
# pyplot.bar(gender_simple.index, gender_simple)
# pyplot.title('Study 1c')
# ------------------------------------
pyplot.subplot(6, 2, 1)
pyplot.hist(simple_amazon.Age, density=density, alpha=0.25, bins=bins)
pyplot.title('Study 1')
pyplot.subplot(6, 2, 2)
pyplot.bar(gender_simple_amazon.index, gender_simple_amazon)
pyplot.title('Study 1')
# ------------------------------------
pyplot.subplot(6, 2, 9)
pyplot.hist(jurgen.Age, density=density, alpha=0.25, bins=bins)
pyplot.title('Study 5')
pyplot.subplot(6, 2, 10)
pyplot.bar(gender_jurgen.index, gender_jurgen)
pyplot.title('Study 5')
# ------------------------------------
pyplot.subplot(6, 2, 7)
pyplot.hist(student.Age, density=density, alpha=0.25, bins=bins)
pyplot.title('Study 4')
pyplot.subplot(6, 2, 8)
pyplot.bar(gender_student.index, gender_student)
pyplot.title('Study 4')
# ------------------------------------
pyplot.subplot(6, 2, 11)
pyplot.hist(simple_replication.Age, density=density, alpha=0.25, bins=bins)
pyplot.title('Study 6')
pyplot.xlabel('Reported Age')

pyplot.subplot(6, 2, 12)
pyplot.bar(gender_simple_replication.index, gender_simple_replication)
pyplot.title('Study 6')
pyplot.xlabel('Reported Gender')
pyplot.tight_layout()
pyplot.savefig(PlotSettings.output_file('demographics.pdf'))
pyplot.show()

PlotSettings.copy_output()
