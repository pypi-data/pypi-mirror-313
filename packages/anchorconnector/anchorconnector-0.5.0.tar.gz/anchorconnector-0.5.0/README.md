# Anchor Connector

[![Docs](https://readthedocs.org/projects/anchor-connector/badge?version=latest)](https://anchor-connector.readthedocs.io)

[![OpenPodcast Banner](https://raw.githubusercontent.com/openpodcast/banner/main/openpodcast-banner.png)](https://openpodcast.app/)

This is a simple library for connecting to the unofficial Anchor API.  
It can be used to export data from your dashboard at
https://anchor.fm/dashboard.

## Supported Endpoints

- `total_plays`
- `plays_by_age_range`
- `plays_by_app`
- `plays_by_device`
- `plays_by_episode`
- `plays_by_gender`
- `plays_by_geo`
- `plays_by_geo_city`
- `episodes`

For each episode, the following endpoints are supported:

- `episode_plays`
- `episode_performance`
- `episode_aggregated_performance`
- `episode_all_time_video_data`

See `__main.py__` for all endpoints.

## Credentials

Before you can use the library, you must extract your Anchor credentials from the dashboard;
they are **not** exposed through your Anchor settings.

You can use our [web-extension](https://github.com/openpodcast/web-extension) for that
or [take a look at the code](https://github.com/openpodcast/web-extension/blob/47fd44723caf6e8a4660f244814f316cdcf19c4c/src/openpodcast.js) to see how to do it manually.

## Installation

```
pip install anchorconnector
```

## Usage as a library

```python
from anchorconnector import AnchorConnector

connector = AnchorConnector(
   base_url=BASE_URL,
   webstation_id=WEBSTATION_ID,
   anchorpw_s=ANCHOR_PW_S,
)

end = datetime.now()
start = end - timedelta(days=30)

total_plays = connector.total_plays(True)
logger.info("Podcast Total Plays = {}", json.dumps(total_plays, indent=4))

plays_by_age_range = connector.plays_by_age_range(start, end)
logger.info(
   "Plays by Age Range = {}",
   json.dumps(plays_by_age_range, indent=4),
)

# plays_by_app = connector.plays_by_app(start, end)
# plays_by_device = connector.plays_by_device(start, end)
# plays_by_episode = connector.plays_by_episode(start, end)
# plays_by_gender = connector.plays_by_gender(start, end)
# plays_by_geo = connector.plays_by_geo()
# plays_by_geo_city = connector.plays_by_geo_city("Germany")
# ...


for episode in connector.episodes():
   logger.info("Episode = {}", json.dumps(episode, indent=4))

   web_episode_id = episode["webEpisodeId"]

   episode_meta = connector.episode_plays(web_episode_id)
   logger.info("Episode Metadata = {}", json.dumps(episode_meta, indent=4))

   # ...
```

See `__main.py__` for all endpoints.

## Development

We use [Pipenv] for virtualenv and dev dependency management. With Pipenv
installed:

1. Install your locally checked out code in [development mode], including its
   dependencies, and all dev dependencies into a virtual environment:

```sh
pipenv sync --dev
```

2. Create an environment file and fill in the required values:

```sh
cp .env.sample .env
```

3. Run the script in the virtual environment, which will [automatically load
   your `.env`][env]:

```sh
pipenv run anchorconnector
```

To add a new dependency for use during the development of this library:

```sh
pipenv install --dev $package
```

To add a new dependency necessary for the correct operation of this library, add
the package to the `install_requires` section of `./setup.py`, then:

```sh
pipenv install
```

To publish the package:

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

or

```sh
make publish
```

[pipenv]: https://pipenv.pypa.io/en/latest/index.html#install-pipenv-today
[development mode]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[env]: https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env
