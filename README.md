## This is a small script written in Python that makes use of the [Genderize.io API](https://genderize.io/) to determine genders based on names.

The script scrapes names from a list of computer science students located on my University's Moodle platform. It will feed the API with these names to try to guess their genders.

I ended up creating this script because one day, I was curious about the percentage of female students that were currently enrolled on my undergraduate course at the time. Since I had no access to anything that would give me the information about the genders of each student, I made this.

I remember having a lot of work waiting to be done at the time, both for my college classes and for my internship job, but anyways I was still kind of bored and wanted to practice a little bit more my almost non-existant Python skills, so I ended up making this thing.
Enjoy it :D


### The results generated by this script are the following files:

- 'females' -> filters the names guessed as female
- 'males' -> filters the names guessed as male
- 'undefined' -> names that were inconclusive

- 'sample_output' contains an overview of the results as well as the counts and percentages

### NOTE: I have removed all last names, so hopefully the names will be kept annonymous and will not be able to be traced back to people
