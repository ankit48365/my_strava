![pylint](https://img.shields.io/badge/pylint-8.46-yellow)
![CurrentLocal](https://img.shields.io/badge/machine-Latitude-brightgreen)

<h2>My Strava Stats Dashboard</h2>
Tech Stack used in this Project
<div style="text-align: center;">
  <table>
    <tr>
      <td align="center"><img src="./image/dlthub.png" width="50"/></td>
      <td align="center"><img src="./image/bigquery2.png" width="50"/></td>
      <td align="center"><img src="./image/github-svgrepo-com (1).png" width="50"/></td>
      <td align="center"><img src="./image/looker.png" width="50"/></td>
      <td align="center"><img src="./image/strava-logo-png-4.png" width="50"/></td>
    </tr>
  </table>
</div>

<a href="https://lookerstudio.google.com/reporting/f472dda8-c0e5-45c6-a52f-95eee12d3e1a">My Strava Stats Dashboard Link</a>

### High Level Conceptual Data Flow Diagram:

![The Idea!!](image/strava_pipeline.png "System Designn Overview")

### Initial Setup steps

```
uv init
uv add dlt[bigquery]
dlt init rest_api bigquery
uv run dlt_strava_bigquery_extn.py

``` 

### Day today 

Run ~strava_authorize.py to refresh access code for strava api
Access Code, Client ID, Secret etc shared here ~ .dlt/secrets.toml
Pylint will only run when commit message has this string "CheckCodeQuality"

### Looker Studio Portal

<a href="https://lookerstudio.google.com/u/0/navigation/reporting">Looker Studio Editor Link</a>

### for initial load 

![alt text](image/initial_load.png)
