# Belly Button Biodiversity

![Bacteria by filterforge.com](Images/bacteria_by_filterforgedotcom.jpg)

Interactive dashboard to explore the [Belly Button Biodiversity DataSet](http://robdunnlab.com/projects/belly-button-biodiversity/).

## Plotly.js

Use Plotly.js to build interactive charts for your dashboard.

* Create a PIE chart that uses data from your samples route (`/samples/<sample>`) to display the top 10 samples.

  * Use `sample_values` as the values for the PIE chart

  * Use `otu_ids` as the labels for the pie chart

  * Use `otu_labels` as the hovertext for the chart

  ![PIE Chart](Images/pie_chart.png)

* Create a Bubble Chart that uses data from your samples route (`/samples/<sample>`) to display each sample.

  * Use `otu_ids` for the x values

  * Use `sample_values` for the y values

  * Use `sample_values` for the marker size

  * Use `otu_ids` for the marker colors

  * Use `otu_labels` for the text values

  ![Bubble Chart](Images/bubble_chart.png)

* Display the sample metadata from the route `/metadata/<sample>`

  * Display each key/value pair from the metadata JSON object somewhere on the page

* Update all of the plots any time that a new sample is selected.

* An example dashboard page might look something like the following.

![Example Dashboard Page](Images/dashboard_part1.png)
![Example Dashboard Page](Images/dashboard_part2.png)

- - -

## Gauge Chart

The following task is completely optional and is very advanced.

* Adapt the Gauge Chart from <https://plot.ly/javascript/gauge-charts/> to plot the Weekly Washing Frequency obtained from the route `/wfreq/<sample>`
* You will need to modify the example gauge code to account for values ranging from 0 - 9.
* Update the chart whenever a new sample is selected

![Weekly Washing Frequency Gauge](Images/gauge.png)

## Deployment (Heroku)

Prepare the application with additional configuration files.

**Virtual Environment**

* If not already, create a new conda environment for this app.

```sh
conda create -n virtual_environment_name python=3.7
```

* Activate this environment. 

```sh
source activate virtual_environment_name
```

**Requirements.txt**

* Install gunicorn web server along with any 

```sh
pip install gunicorn
pip install flask
pip install flask-sqlalchemy
pip install numpy
pip install pandas
```

* Test run the app locally.

```sh
FLASK_APP=app_folder_name/app.py flask run
```

* Create the requirements.txt file

```sh
pip freeze > requirements.txt
```

**Procfile**

* Create a Procfile that Heroku will use as commands to execute on app startup.

```sh
touch Procfile
```

* Within any text editor add:

```sh
web: gunicorn app_folder_name.app:app
```

**Heroku**

Create a new application on [Heroku](https://dashboard.heroku.com/apps).

Deploy using Heroku Git.

* Download and install the Heroku CLI.
* Create a new Git repository in the existing directory.
* Deploy the Flask application.